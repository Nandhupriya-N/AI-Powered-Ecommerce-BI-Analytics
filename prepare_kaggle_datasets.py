"""
Kaggle Dataset Importer and Preprocessor
Extracts, cleans, and structures real Kaggle datasets downloaded via kagglehub:
1. ankitverma2010/ecommerce-customer-churn-analysis-and-prediction (5,630 customers)
2. carrie1/ecommerce-data (541,909 transactions -> cleaned sample for BI)
"""

import os
import shutil
import pandas as pd
import numpy as np

def prepare_kaggle_data():
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Process E-Commerce Churn Dataset
    churn_cache = r'C:\Users\Nandhupriya\.cache\kagglehub\datasets\ankitverma2010\ecommerce-customer-churn-analysis-and-prediction\versions\1\E Commerce Dataset.xlsx'
    if os.path.exists(churn_cache):
        print("[1/2] Loading Real Kaggle E-Commerce Churn Dataset...")
        df_churn = pd.read_excel(churn_cache, sheet_name='E Comm')
        
        # Clean column names & handle nulls
        df_churn['Tenure'] = df_churn['Tenure'].fillna(df_churn['Tenure'].median())
        df_churn['WarehouseToHome'] = df_churn['WarehouseToHome'].fillna(df_churn['WarehouseToHome'].median())
        df_churn['HourSpendOnApp'] = df_churn['HourSpendOnApp'].fillna(df_churn['HourSpendOnApp'].median())
        df_churn['OrderAmountHikeFromlastYear'] = df_churn['OrderAmountHikeFromlastYear'].fillna(df_churn['OrderAmountHikeFromlastYear'].median())
        df_churn['CouponUsed'] = df_churn['CouponUsed'].fillna(df_churn['CouponUsed'].median())
        df_churn['OrderCount'] = df_churn['OrderCount'].fillna(df_churn['OrderCount'].median())
        df_churn['DaySinceLastOrder'] = df_churn['DaySinceLastOrder'].fillna(df_churn['DaySinceLastOrder'].median())
        
        # Standardize category typos in original dataset
        df_churn['PreferedOrderCat'] = df_churn['PreferedOrderCat'].replace({'Mobile': 'Mobile Phone'})
        df_churn['PreferredPaymentMode'] = df_churn['PreferredPaymentMode'].replace({'CC': 'Credit Card', 'COD': 'Cash on Delivery'})
        
        # Save complete cleaned dataset
        full_churn_path = os.path.join(output_dir, 'kaggle_ecommerce_churn.csv')
        df_churn.to_csv(full_churn_path, index=False)
        print(f"Saved complete Kaggle churn dataset: {len(df_churn)} rows to {full_churn_path}")
        
        # Split into Baseline Historical Training (75%) and New Incoming Evaluation Batch (25%)
        # To simulate a realistic business change in the new batch, we sample by date/tier
        df_churn_shuffled = df_churn.sample(frac=1.0, random_state=42).reset_index(drop=True)
        split_idx = int(len(df_churn_shuffled) * 0.75)
        
        train_split = df_churn_shuffled.iloc[:split_idx]
        test_split = df_churn_shuffled.iloc[split_idx:]
        
        train_split.to_csv(os.path.join(output_dir, 'kaggle_baseline_churn_train.csv'), index=False)
        test_split.to_csv(os.path.join(output_dir, 'kaggle_new_batch_churn_test.csv'), index=False)
        print(f"Split created: Baseline Train ({len(train_split)} rows) & New Batch Test ({len(test_split)} rows).")

    # 2. Process Online Retail Transactions Dataset
    retail_cache = r'C:\Users\Nandhupriya\.cache\kagglehub\datasets\carrie1\ecommerce-data\versions\1\data.csv'
    if os.path.exists(retail_cache):
        print("\n[2/2] Loading Real Kaggle Online Retail Transaction Dataset...")
        df_retail = pd.read_csv(retail_cache, encoding='latin1')
        print(f"Total raw transactions: {len(df_retail):,}")
        
        # Filter valid records (positive quantity & price, non-null customerID)
        df_clean = df_retail.dropna(subset=['CustomerID']).copy()
        df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]
        df_clean['Total_Amount'] = np.round(df_clean['Quantity'] * df_clean['UnitPrice'], 2)
        df_clean['CustomerID'] = df_clean['CustomerID'].astype(int)
        
        # Save a high-quality sample for fast dashboard rendering
        sample_size = min(15000, len(df_clean))
        df_sample = df_clean.sample(n=sample_size, random_state=42).sort_values('InvoiceDate')
        sample_path = os.path.join(output_dir, 'kaggle_transactions_sample.csv')
        df_sample.to_csv(sample_path, index=False)
        print(f"Saved Kaggle retail transaction sample: {len(df_sample)} rows to {sample_path}")

    print("\nAll Kaggle datasets prepared and saved to 'data/' folder successfully!")

if __name__ == '__main__':
    prepare_kaggle_data()
