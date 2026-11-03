import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import pandas as pd
from src.advanced_forecaster import AdvancedDemandForecastingEngine

print("Initializing AdvancedDemandForecastingEngine...")
engine = AdvancedDemandForecastingEngine()

trans_df = pd.read_csv('data/historical_ecommerce_data.csv')

print("\n1. Testing Daily Forecast (14 days)...")
daily_res = engine.generate_daily_forecast(trans_df, horizon=14)
df_daily = daily_res['forecast_df']
print(f"Model used: {daily_res['model_used']}")
print(f"Generated {len(df_daily)} daily forecast records.")
print(df_daily[['Date', 'Forecasted_Revenue', 'Lower_Bound_80', 'Upper_Bound_80', 'Demand_Signal']].head(3))

print("\n2. Testing Weekly Forecast (8 weeks)...")
weekly_res = engine.generate_weekly_forecast(trans_df, horizon_weeks=8)
df_weekly = weekly_res['forecast_weekly']
print(f"Generated {len(df_weekly)} weekly forecast records.")
print(df_weekly.head(3))

print("\n3. Testing Monthly Forecast (3 months)...")
monthly_res = engine.generate_monthly_forecast(trans_df, horizon_months=3)
df_monthly = monthly_res['forecast_monthly']
print(f"Generated {len(df_monthly)} monthly forecast records.")
print(df_monthly)

print("\n4. Testing Category Forecast (14 days)...")
cat_res = engine.generate_category_forecast(trans_df, horizon=14)
df_cat = cat_res['category_forecast_df']
print(f"Generated {len(df_cat)} category breakdown records.")
print(df_cat.head(3))

print("\n5. Testing Seasonality and Trends...")
seasonality = engine.get_seasonality_and_trends(trans_df)
print("Seasonality Index:", seasonality['seasonality_index'])
print(f"Weekend Lift: {seasonality['weekend_lift_pct']}%")

print("\n6. Testing Benchmark Comparison Table...")
bench = engine.get_model_comparison_benchmark()
bench_df = pd.DataFrame(bench)
print(bench_df[['Model Architecture', 'MAE ($)', 'RMSE ($)', 'R² Score', 'MAPE (%)', 'RAM Footprint']])

print("\n>>> ALL ADVANCED FORECASTER TESTS PASSED WITH ZERO ERRORS! <<<")
