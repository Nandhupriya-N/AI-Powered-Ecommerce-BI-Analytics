"""
Power BI Data Model Exporter
Transforms e-commerce analytics, predictions, and customer segments into
a normalized Star Schema ready for instant import into Microsoft Power BI Desktop.
"""

import os
import pandas as pd
import numpy as np

def export_powerbi_star_schema(trans_df, cust_df, output_dir='data/powerbi'):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Dim_Customer
    dim_cust_cols = [c for c in ['Customer_ID', 'Age', 'Gender', 'Region', 'Membership_Type', 'Customer_Segment', 'Segment_Name', 'Cluster_ID'] if c in cust_df.columns]
    dim_customer = cust_df[dim_cust_cols].drop_duplicates().copy()
    dim_customer.to_csv(os.path.join(output_dir, 'Dim_Customer.csv'), index=False)
    
    # 2. Dim_Product_Category
    categories = trans_df['Product_Category'].unique()
    category_summary = trans_df.groupby('Product_Category').agg(
        Avg_Price=('Unit_Price', 'mean'),
        Total_Orders=('Order_ID', 'count'),
        Category_Revenue=('Total_Amount', 'sum'),
        Category_Profit=('Profit', 'sum')
    ).reset_index()
    category_summary['Margin_Pct'] = (category_summary['Category_Profit'] / category_summary['Category_Revenue'] * 100).round(2)
    category_summary.to_csv(os.path.join(output_dir, 'Dim_Product_Category.csv'), index=False)
    
    # 3. Dim_Date
    dates = pd.to_datetime(trans_df['Order_Date'].unique()).sort_values()
    dim_date = pd.DataFrame({'Date': dates})
    dim_date['Date_Key'] = dim_date['Date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['Year'] = dim_date['Date'].dt.year
    dim_date['Quarter'] = 'Q' + dim_date['Date'].dt.quarter.astype(str)
    dim_date['Month_Num'] = dim_date['Date'].dt.month
    dim_date['Month_Name'] = dim_date['Date'].dt.strftime('%B')
    dim_date['Day_of_Week'] = dim_date['Date'].dt.day_name()
    dim_date['Is_Weekend'] = dim_date['Date'].dt.dayofweek.isin([5, 6]).astype(int)
    dim_date.to_csv(os.path.join(output_dir, 'Dim_Date.csv'), index=False)
    
    # 4. Fact_Orders
    fact_cols = ['Order_ID', 'Customer_ID', 'Order_Date', 'Product_Category', 'Quantity', 'Unit_Price', 'Discount_Percent', 'Total_Amount', 'Profit', 'Payment_Method', 'Rating', 'Is_Returned']
    if 'Is_Anomaly_Predicted' in trans_df.columns:
        fact_cols.append('Is_Anomaly_Predicted')
    elif 'Is_Anomaly' in trans_df.columns:
        fact_cols.append('Is_Anomaly')
        
    fact_orders = trans_df[[c for c in fact_cols if c in trans_df.columns]].copy()
    fact_orders.to_csv(os.path.join(output_dir, 'Fact_Orders.csv'), index=False)
    
    # 5. Fact_Predictions_and_Risk
    pred_cols = ['Customer_ID', 'Predicted_Churn', 'Churn_Risk_Score', 'Risk_Level', 'Recency_Days', 'Frequency_Orders', 'Monetary_Spend', 'Customer_Service_Calls', 'Return_Rate']
    available_pred_cols = [c for c in pred_cols if c in cust_df.columns]
    if available_pred_cols:
        fact_preds = cust_df[available_pred_cols].copy()
        fact_preds.to_csv(os.path.join(output_dir, 'Fact_Customer_Predictions.csv'), index=False)
        
    print(f"Power BI Star Schema tables successfully exported to '{output_dir}/'!")
    return {
        'Dim_Customer': len(dim_customer),
        'Dim_Product_Category': len(category_summary),
        'Dim_Date': len(dim_date),
        'Fact_Orders': len(fact_orders),
        'Fact_Customer_Predictions': len(cust_df) if available_pred_cols else 0
    }

if __name__ == '__main__':
    t_df = pd.read_csv('data/historical_ecommerce_data.csv')
    c_df = pd.read_csv('data/historical_customer_profiles.csv')
    export_powerbi_star_schema(t_df, c_df)
