import pandas as pd
import numpy as np

df = pd.read_csv('data/historical_ecommerce_data.csv')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

print(f"Date Range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
print(f"Total Rows: {len(df)}")
print(f"Unique Dates: {df['Order_Date'].nunique()}")

daily = df.groupby('Order_Date')['Total_Amount'].sum()
print("\nDaily Sales Distribution:")
print(daily.describe())

print("\nProduct Categories Breakdown:")
print(df.groupby('Product_Category').agg(
    Revenue=('Total_Amount', 'sum'),
    Orders=('Order_ID', 'count'),
    Avg_Price=('Unit_Price', 'mean'),
    Avg_Qty=('Quantity', 'mean')
))

# Weekly aggregation
weekly = df.set_index('Order_Date').resample('W-MON')['Total_Amount'].sum()
print(f"\nWeekly Time Points: {len(weekly)}")
print("Weekly Sales Distribution:")
print(weekly.describe())

# Monthly aggregation
monthly = df.set_index('Order_Date').resample('ME')['Total_Amount'].sum()
print(f"\nMonthly Time Points: {len(monthly)}")
print(monthly)
