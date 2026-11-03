import os
import sys
sys.path.insert(0, os.path.abspath('.'))
import torch
import numpy as np
import pandas as pd
from datetime import timedelta
import joblib

# Load transactions
trans_df = pd.read_csv('data/historical_ecommerce_data.csv')
trans_df['Order_Date'] = pd.to_datetime(trans_df['Order_Date'])

daily = trans_df.groupby('Order_Date').agg(
    Daily_Revenue=('Total_Amount', 'sum'),
    Total_Orders=('Order_ID', 'count'),
    Total_Quantity=('Quantity', 'sum'),
    Avg_Discount=('Discount_Percent', 'mean'),
    Daily_Profit=('Profit', 'sum')
).reset_index().sort_values('Order_Date')

# Try loading Chronos-Bolt
from chronos import ChronosBoltPipeline
pipeline = ChronosBoltPipeline.from_pretrained(
    "amazon/chronos-bolt-tiny",
    device_map="cpu",
    torch_dtype=torch.float32,
)

# 1. 14-Day Daily Forecast with Chronos-Bolt
horizon = 14
context = torch.tensor(daily['Daily_Revenue'].values, dtype=torch.float32)
fc = pipeline.predict(context, prediction_length=horizon)
# fc shape: [1, 9, 14]
# quantiles: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

last_date = daily['Order_Date'].max()
future_dates = [last_date + timedelta(days=i) for i in range(1, horizon + 1)]
avg_aov = daily['Daily_Revenue'].sum() / max(1, daily['Total_Orders'].sum())

daily_fc_df = pd.DataFrame({
    'Date': [d.strftime('%Y-%m-%d') for d in future_dates],
    'Day_of_Week': [d.strftime('%A') for d in future_dates],
    'Forecasted_Revenue': np.round(fc[0, 4, :].numpy(), 2),
    'Lower_Bound_80': np.round(fc[0, 0, :].numpy(), 2), # 10th percentile
    'Upper_Bound_80': np.round(fc[0, 8, :].numpy(), 2), # 90th percentile
    'Lower_Bound_95': np.round(np.maximum(100.0, fc[0, 0, :].numpy() * 0.92), 2),
    'Upper_Bound_95': np.round(fc[0, 8, :].numpy() * 1.08, 2),
    'Projected_Demand_Orders': [int(round(r / avg_aov)) for r in fc[0, 4, :].numpy()]
})

# Detect spikes & declines vs trailing 14-day baseline
trail_mean = daily['Daily_Revenue'].tail(14).mean()
trail_std = daily['Daily_Revenue'].tail(14).std()
daily_fc_df['Demand_Signal'] = 'Normal Demand'
daily_fc_df.loc[daily_fc_df['Forecasted_Revenue'] > (trail_mean + 1.25 * trail_std), 'Demand_Signal'] = 'Surge Spike ⚠️'
daily_fc_df.loc[daily_fc_df['Forecasted_Revenue'] < (trail_mean - 1.25 * trail_std), 'Demand_Signal'] = 'Demand Drop 🔻'

print("--- Daily 14-Day Forecast with Chronos-Bolt ---")
print(daily_fc_df[['Date', 'Day_of_Week', 'Forecasted_Revenue', 'Lower_Bound_80', 'Upper_Bound_80', 'Demand_Signal']].head(7))

# 2. Category-Level Demand Breakdown
cat_shares = trans_df.groupby('Product_Category')['Total_Amount'].sum() / trans_df['Total_Amount'].sum()
cat_forecasts = {}
for cat, share in cat_shares.items():
    cat_forecasts[cat] = np.round(daily_fc_df['Forecasted_Revenue'] * share, 2)

cat_fc_df = pd.DataFrame(cat_forecasts)
cat_fc_df.insert(0, 'Date', daily_fc_df['Date'])
print("\n--- Category-Level Forecast Breakdown (First 3 Days) ---")
print(cat_fc_df.head(3))

# 3. Weekly Aggregation
weekly = daily.set_index('Order_Date').resample('W-MON')['Daily_Revenue'].sum().reset_index()
print(f"\nHistorical Weeks: {len(weekly)}, Recent Mean Weekly: ${weekly['Daily_Revenue'].tail(4).mean():,.2f}")

# 4. Seasonality Index
daily['DOW'] = daily['Order_Date'].dt.day_name()
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_rev = daily.groupby('DOW')['Daily_Revenue'].mean().reindex(dow_order)
overall_mean = daily['Daily_Revenue'].mean()
seasonality_index = (dow_rev / overall_mean).round(3)
print("\n--- Day-of-Week Seasonality Index ---")
print(seasonality_index)
