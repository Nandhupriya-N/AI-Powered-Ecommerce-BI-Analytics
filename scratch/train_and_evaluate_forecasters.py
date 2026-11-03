import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

# Ensure root is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

models_dir = os.path.join(BASE_DIR, 'models')
data_dir = os.path.join(BASE_DIR, 'data')

# Load historical transactions
trans_path = os.path.join(data_dir, 'historical_ecommerce_data.csv')
df = pd.read_csv(trans_path)
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

print(f"Loaded {len(df):,} transactions from {trans_path}")

# Daily aggregation
daily = df.groupby('Order_Date').agg(
    Daily_Revenue=('Total_Amount', 'sum'),
    Total_Orders=('Order_ID', 'count'),
    Total_Quantity=('Quantity', 'sum'),
    Avg_Discount=('Discount_Percent', 'mean'),
    Daily_Profit=('Profit', 'sum')
).reset_index().sort_values('Order_Date')

# Category daily shares
cat_daily = df.pivot_table(index='Order_Date', columns='Product_Category', values='Total_Amount', aggfunc='sum', fill_value=0)
cat_daily.columns = [f"Rev_{c.replace(' ', '_').replace('&', 'and')}" for c in cat_daily.columns]
daily = daily.merge(cat_daily, on='Order_Date', how='left')

# Calendar and temporal features
daily['Day_of_Week'] = daily['Order_Date'].dt.dayofweek
daily['Day_of_Month'] = daily['Order_Date'].dt.day
daily['Month'] = daily['Order_Date'].dt.month
daily['Is_Weekend'] = (daily['Day_of_Week'] >= 5).astype(int)

# Lag features (strictly known at prediction time)
daily['Lag_1_Revenue'] = daily['Daily_Revenue'].shift(1).bfill()
daily['Lag_2_Revenue'] = daily['Daily_Revenue'].shift(2).bfill()
daily['Lag_7_Revenue'] = daily['Daily_Revenue'].shift(7).bfill()
daily['Lag_14_Revenue'] = daily['Daily_Revenue'].shift(14).bfill()

# Rolling features (strictly shifted by 1 to prevent target leakage)
daily['Rolling_7_Avg'] = daily['Daily_Revenue'].shift(1).rolling(window=7, min_periods=1).mean().bfill()
daily['Rolling_7_Std'] = daily['Daily_Revenue'].shift(1).rolling(window=7, min_periods=1).std().fillna(0).bfill()
daily['Rolling_14_Avg'] = daily['Daily_Revenue'].shift(1).rolling(window=14, min_periods=1).mean().bfill()
daily['Rolling_7_Orders'] = daily['Total_Orders'].shift(1).rolling(window=7, min_periods=1).mean().bfill()
daily['Rolling_7_Discount'] = daily['Avg_Discount'].shift(1).rolling(window=7, min_periods=1).mean().bfill()

# Features for enhanced Random Forest
rf_features = [
    'Day_of_Week', 'Day_of_Month', 'Month', 'Is_Weekend',
    'Lag_1_Revenue', 'Lag_2_Revenue', 'Lag_7_Revenue', 'Lag_14_Revenue',
    'Rolling_7_Avg', 'Rolling_7_Std', 'Rolling_14_Avg',
    'Rolling_7_Orders', 'Rolling_7_Discount'
]

# Baseline features for Ridge
ridge_features = [
    'Day_of_Week', 'Day_of_Month', 'Month',
    'Lag_1_Revenue', 'Lag_7_Revenue', 'Rolling_7_Avg', 'Rolling_7_Discount'
]

# Time-based split (80% train, 20% test strictly chronological)
split_idx = int(len(daily) * 0.8)
train_df = daily.iloc[:split_idx]
test_df = daily.iloc[split_idx:]

y_train = train_df['Daily_Revenue'].values
y_test = test_df['Daily_Revenue'].values

# 1. Train Baseline Ridge Regressor
X_train_ridge = train_df[ridge_features].values
X_test_ridge = test_df[ridge_features].values

ridge = Ridge(alpha=10.0)
ridge.fit(X_train_ridge, y_train)
ridge_preds = ridge.predict(X_test_ridge)

ridge_mae = mean_absolute_error(y_test, ridge_preds)
ridge_rmse = root_mean_squared_error(y_test, ridge_preds)
ridge_r2 = r2_score(y_test, ridge_preds)
ridge_mape = float(np.mean(np.abs((y_test - ridge_preds) / np.maximum(y_test, 1))) * 100)

ridge_metrics = {
    'Model_Name': 'Baseline AutoRegressive Ridge',
    'MAE': round(float(ridge_mae), 2),
    'RMSE': round(float(ridge_rmse), 2),
    'R2': round(float(ridge_r2), 4),
    'MAPE': round(float(ridge_mape), 2),
    'Features_Count': len(ridge_features)
}

# 2. Train Enhanced Random Forest Regressor (IEEE Papers 7 & 8)
X_train_rf = train_df[rf_features].values
X_test_rf = test_df[rf_features].values

rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    min_samples_split=5,
    min_samples_leaf=3,
    max_features=0.8,
    random_state=42
)
rf.fit(X_train_rf, y_train)
rf_preds = rf.predict(X_test_rf)

rf_mae = mean_absolute_error(y_test, rf_preds)
rf_rmse = root_mean_squared_error(y_test, rf_preds)
rf_r2 = r2_score(y_test, rf_preds)
rf_mape = float(np.mean(np.abs((y_test - rf_preds) / np.maximum(y_test, 1))) * 100)

# Calculate empirical 95% confidence interval coverage
tree_preds = np.array([tree.predict(X_test_rf) for tree in rf.estimators_])
pred_std = np.std(tree_preds, axis=0)
lower_95 = rf_preds - 1.96 * pred_std
upper_95 = rf_preds + 1.96 * pred_std
coverage_pct = float(np.mean((y_test >= lower_95) & (y_test <= upper_95)) * 100)

# Feature importances
rf_importances = {feat: round(float(imp), 4) for feat, imp in zip(rf_features, rf.feature_importances_)}
sorted_rf_imp = dict(sorted(rf_importances.items(), key=lambda x: x[1], reverse=True))

rf_metrics = {
    'Model_Name': 'Enhanced Random Forest Demand Forecaster',
    'MAE': round(float(rf_mae), 2),
    'RMSE': round(float(rf_rmse), 2),
    'R2': round(float(rf_r2), 4),
    'MAPE': round(float(rf_mape), 2),
    'Coverage_95_CI': round(coverage_pct, 1),
    'Features_Count': len(rf_features),
    'Top_Features': list(sorted_rf_imp.keys())[:5]
}

print("\n=== TIME-SERIES EVALUATION RESULTS (80/20 Time Split) ===")
print(f"Train Period: {train_df['Order_Date'].min().strftime('%Y-%m-%d')} to {train_df['Order_Date'].max().strftime('%Y-%m-%d')} ({len(train_df)} days)")
print(f"Test Period:  {test_df['Order_Date'].min().strftime('%Y-%m-%d')} to {test_df['Order_Date'].max().strftime('%Y-%m-%d')} ({len(test_df)} days)")
print("-" * 60)
print(f"{'Metric':<18} | {'Baseline Ridge':<20} | {'Enhanced Random Forest':<20}")
print("-" * 60)
print(f"{'MAE ($)':<18} | ${ridge_metrics['MAE']:<19} | ${rf_metrics['MAE']:<19}")
print(f"{'RMSE ($)':<18} | ${ridge_metrics['RMSE']:<19} | ${rf_metrics['RMSE']:<19}")
print(f"{'R-Squared (R2)':<18} | {ridge_metrics['R2']:<20} | {rf_metrics['R2']:<20}")
print(f"{'MAPE (%)':<18} | {ridge_metrics['MAPE']:<19}% | {rf_metrics['MAPE']:<19}%")
print(f"{'95% CI Coverage':<18} | {'N/A (Point Only)':<20} | {rf_metrics['Coverage_95_CI']}%")
print("-" * 60)

# Save artifacts
joblib.dump(rf, os.path.join(models_dir, 'rf_sales_forecaster.joblib'))
joblib.dump(rf_features, os.path.join(models_dir, 'rf_forecaster_features.joblib'))
print(f"\nSaved enhanced model to {os.path.join(models_dir, 'rf_sales_forecaster.joblib')}")
print(f"Saved feature list to {os.path.join(models_dir, 'rf_forecaster_features.joblib')}")

# Update models/model_metadata.json
meta_path = os.path.join(models_dir, 'model_metadata.json')
with open(meta_path, 'r') as f:
    metadata = json.load(f)

metadata['forecasting_models'] = {
    'comparison': {
        'Baseline Ridge': ridge_metrics,
        'Random Forest (IEEE 7&8)': rf_metrics
    },
    'best_model': 'Random Forest (IEEE 7&8)',
    'rf_feature_importance': sorted_rf_imp,
    'training_split': {
        'train_days': len(train_df),
        'test_days': len(test_df),
        'split_ratio': '80/20 Chronological'
    }
}

with open(meta_path, 'w') as f:
    json.dump(metadata, f, indent=4)

print(f"Updated metadata successfully in {meta_path}")
