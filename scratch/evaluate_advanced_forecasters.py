import os
import sys
sys.path.insert(0, os.path.abspath('.'))
import torch
import numpy as np
import pandas as pd
from chronos import ChronosBoltPipeline
import joblib

# Load datasets
trans_df = pd.read_csv('data/historical_ecommerce_data.csv')
trans_df['Order_Date'] = pd.to_datetime(trans_df['Order_Date'])

# Aggregate daily
daily = trans_df.groupby('Order_Date').agg(
    Daily_Revenue=('Total_Amount', 'sum'),
    Total_Orders=('Order_ID', 'count'),
    Total_Quantity=('Quantity', 'sum'),
    Avg_Discount=('Discount_Percent', 'mean'),
    Daily_Profit=('Profit', 'sum')
).reset_index().sort_values('Order_Date')

# Chronological 80/20 split
split_idx = int(len(daily) * 0.80)
train_df = daily.iloc[:split_idx].copy()
test_df = daily.iloc[split_idx:].copy()

print(f"Total days: {len(daily)}")
print(f"Train period: {train_df['Order_Date'].min().strftime('%Y-%m-%d')} to {train_df['Order_Date'].max().strftime('%Y-%m-%d')} ({len(train_df)} days)")
print(f"Test period:  {test_df['Order_Date'].min().strftime('%Y-%m-%d')} to {test_df['Order_Date'].max().strftime('%Y-%m-%d')} ({len(test_df)} days)")

y_test = test_df['Daily_Revenue'].values

# -------------------------------------------------------------
# 1. Baseline Ridge Forecaster
# -------------------------------------------------------------
ridge_model = joblib.load('models/sales_forecaster.joblib')
ridge_features = joblib.load('models/forecaster_features.joblib')

# Build feature matrix for test set
test_features_ridge = pd.DataFrame()
test_features_ridge['Day_of_Week'] = test_df['Order_Date'].dt.dayofweek
test_features_ridge['Day_of_Month'] = test_df['Order_Date'].dt.day
test_features_ridge['Month'] = test_df['Order_Date'].dt.month
test_features_ridge['Lag_1_Revenue'] = daily['Daily_Revenue'].shift(1).iloc[split_idx:].values
test_features_ridge['Lag_7_Revenue'] = daily['Daily_Revenue'].shift(7).iloc[split_idx:].values
test_features_ridge['Rolling_7_Avg'] = daily['Daily_Revenue'].shift(1).rolling(7, min_periods=1).mean().iloc[split_idx:].values
test_features_ridge['Avg_Discount'] = test_df['Avg_Discount'].values

ridge_preds = ridge_model.predict(test_features_ridge[ridge_features].values)

# -------------------------------------------------------------
# 2. Enhanced Random Forest Forecaster (IEEE Papers 7 & 8)
# -------------------------------------------------------------
rf_model = joblib.load('models/rf_sales_forecaster.joblib')
rf_features = joblib.load('models/rf_forecaster_features.joblib')

test_features_rf = pd.DataFrame()
test_features_rf['Day_of_Week'] = test_df['Order_Date'].dt.dayofweek
test_features_rf['Day_of_Month'] = test_df['Order_Date'].dt.day
test_features_rf['Month'] = test_df['Order_Date'].dt.month
test_features_rf['Is_Weekend'] = (test_features_rf['Day_of_Week'] >= 5).astype(int)
test_features_rf['Lag_1_Revenue'] = daily['Daily_Revenue'].shift(1).iloc[split_idx:].values
test_features_rf['Lag_2_Revenue'] = daily['Daily_Revenue'].shift(2).iloc[split_idx:].values
test_features_rf['Lag_7_Revenue'] = daily['Daily_Revenue'].shift(7).iloc[split_idx:].values
test_features_rf['Lag_14_Revenue'] = daily['Daily_Revenue'].shift(14).iloc[split_idx:].values
test_features_rf['Rolling_7_Avg'] = daily['Daily_Revenue'].shift(1).rolling(7, min_periods=1).mean().iloc[split_idx:].values
test_features_rf['Rolling_7_Std'] = daily['Daily_Revenue'].shift(1).rolling(7, min_periods=1).std().fillna(0).iloc[split_idx:].values
test_features_rf['Rolling_14_Avg'] = daily['Daily_Revenue'].shift(1).rolling(14, min_periods=1).mean().iloc[split_idx:].values
test_features_rf['Rolling_7_Orders'] = daily['Total_Orders'].shift(1).rolling(7, min_periods=1).mean().iloc[split_idx:].values
test_features_rf['Rolling_7_Discount'] = daily['Avg_Discount'].shift(1).rolling(7, min_periods=1).mean().iloc[split_idx:].values

rf_preds = rf_model.predict(test_features_rf[rf_features].values)

# -------------------------------------------------------------
# 3. Amazon Chronos-Bolt Foundation Model
# -------------------------------------------------------------
print("Loading Chronos-Bolt for holdout evaluation...")
pipeline = ChronosBoltPipeline.from_pretrained(
    "amazon/chronos-bolt-tiny",
    device_map="cpu",
    torch_dtype=torch.float32,
)

# Rolling 14-day window inference across the test horizon (simulating multi-step forecast)
context_full = torch.tensor(train_df['Daily_Revenue'].values, dtype=torch.float32)

# Predict full test length (61 days) directly or via rolling chunks
chronos_preds_list = []
chronos_lower_list = []
chronos_upper_list = []

# In Chronos-Bolt, predict over the 61 holdout days
fc_bolt = pipeline.predict(context_full, prediction_length=len(test_df))
# Shape: [1, 9, 61]
# Quantiles: 0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4, 4: 0.5 (median), 5: 0.6, 6: 0.7, 7: 0.8, 8: 0.9
chronos_p10 = fc_bolt[0, 0, :].numpy()
chronos_p50 = fc_bolt[0, 4, :].numpy() # Median forecast
chronos_p90 = fc_bolt[0, 8, :].numpy()

# Also rolling 7-day autoregressive update evaluation
chronos_rolling_preds = []
context_rolling = list(train_df['Daily_Revenue'].values)
step = 7
for start in range(0, len(test_df), step):
    chunk_len = min(step, len(test_df) - start)
    ctx_tensor = torch.tensor(context_rolling, dtype=torch.float32)
    fc = pipeline.predict(ctx_tensor, prediction_length=chunk_len)
    p50_chunk = fc[0, 4, :chunk_len].numpy().tolist()
    chronos_rolling_preds.extend(p50_chunk)
    # Add actual historical values as time advances
    context_rolling.extend(list(y_test[start:start+chunk_len]))

chronos_rolling_preds = np.array(chronos_rolling_preds)

# -------------------------------------------------------------
# Metrics Calculation
# -------------------------------------------------------------
def get_metrics(y_true, y_pred, quant_low=None, quant_high=None):
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred)**2)))
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    ss_res = np.sum((y_true - y_pred)**2)
    r2 = float(1.0 - (ss_res / ss_tot))
    mape = float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)
    
    cov = None
    if quant_low is not None and quant_high is not None:
        inside = (y_true >= quant_low) & (y_true <= quant_high)
        cov = float(np.mean(inside) * 100)
    return {'MAE': round(mae, 2), 'RMSE': round(rmse, 2), 'R2': round(r2, 4), 'MAPE': round(mape, 2), 'Coverage': cov}

m_ridge = get_metrics(y_test, ridge_preds)
m_rf = get_metrics(y_test, rf_preds)
m_chronos_direct = get_metrics(y_test, chronos_p50, chronos_p10, chronos_p90)
m_chronos_rolling = get_metrics(y_test, chronos_rolling_preds)

print("\n=======================================================")
print("EMPIRICAL HOLDOUT EVALUATION (61 UNSEEN TEST DAYS)")
print("=======================================================")
print(f"1. Baseline AutoRegressive Ridge:     MAE: ${m_ridge['MAE']:,.2f} | RMSE: ${m_ridge['RMSE']:,.2f} | R2: {m_ridge['R2']} | MAPE: {m_ridge['MAPE']}%")
print(f"2. Enhanced Random Forest (IEEE 7&8): MAE: ${m_rf['MAE']:,.2f} | RMSE: ${m_rf['RMSE']:,.2f} | R2: {m_rf['R2']} | MAPE: {m_rf['MAPE']}%")
print(f"3. Chronos-Bolt (Direct 61-Day Zero-Shot): MAE: ${m_chronos_direct['MAE']:,.2f} | RMSE: ${m_chronos_direct['RMSE']:,.2f} | R2: {m_chronos_direct['R2']} | MAPE: {m_chronos_direct['MAPE']}% | 80% CI Coverage: {m_chronos_direct['Coverage']}%")
print(f"4. Chronos-Bolt (Rolling Weekly Re-anchored): MAE: ${m_chronos_rolling['MAE']:,.2f} | RMSE: ${m_chronos_rolling['RMSE']:,.2f} | R2: {m_chronos_rolling['R2']} | MAPE: {m_chronos_rolling['MAPE']}%")
print("=======================================================")
