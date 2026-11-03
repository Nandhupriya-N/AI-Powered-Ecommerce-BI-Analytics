"""
Creates several distinct, realistic testing datasets for interactive evaluation.
"""

import os
import shutil
import pandas as pd
import numpy as np

def create_all_test_datasets():
    test_dir = 'data/test_datasets'
    os.makedirs(test_dir, exist_ok=True)
    
    # 1. Festive Surge Batch
    print("[1/5] Generating Batch 1: Festive Surge (High Growth, Low Churn)...")
    base_trans = pd.read_csv('data/historical_ecommerce_data.csv')
    festive = base_trans.sample(n=1500, random_state=101).copy()
    festive['Total_Amount'] = (festive['Total_Amount'] * 1.25).round(2)
    festive['Profit'] = (festive['Profit'] * 1.30).round(2)
    festive['Discount_Percent'] = (festive['Discount_Percent'] * 0.85).round(1)
    festive.to_csv(os.path.join(test_dir, 'test_batch_1_festive_surge.csv'), index=False)
    
    # 2. Regional Friction Batch (South Service Calls Escalation)
    print("[2/5] Generating Batch 2: Regional Friction (Customer Support Spike)...")
    friction = base_trans.sample(n=1800, random_state=202).copy()
    friction.loc[friction['Region'] == 'South', 'Rating'] = np.random.choice([1, 2, 3], size=len(friction[friction['Region'] == 'South']))
    friction.to_csv(os.path.join(test_dir, 'test_batch_2_regional_friction.csv'), index=False)
    
    # 3. Discount Leakage / Anomaly Heavy Batch
    print("[3/5] Generating Batch 3: Discount Leakage & Margin Risk (Anomalies)...")
    anom_batch = base_trans.sample(n=1200, random_state=303).copy()
    # Inject 5% severe discount leakage anomalies
    leak_idx = anom_batch.sample(frac=0.05, random_state=42).index
    anom_batch.loc[leak_idx, 'Discount_Percent'] = 75.0
    anom_batch.loc[leak_idx, 'Profit'] = -85.50
    anom_batch.loc[leak_idx, 'Is_Anomaly'] = 1
    anom_batch.to_csv(os.path.join(test_dir, 'test_batch_3_discount_leakage.csv'), index=False)
    
    # 4. Real Kaggle Customer Evaluation Cohort
    print("[4/5] Copying Batch 4: Real Kaggle Test Cohort (1,408 records)...")
    if os.path.exists('data/kaggle_new_batch_churn_test.csv'):
        shutil.copy('data/kaggle_new_batch_churn_test.csv', os.path.join(test_dir, 'test_batch_4_kaggle_test_cohort.csv'))
        
    # 5. New Customer Profiles Cohort
    print("[5/5] Generating Batch 5: Fresh Customer Profiles Cohort...")
    cust_base = pd.read_csv('data/new_batch_customer_profiles.csv')
    cust_sample = cust_base.sample(n=min(500, len(cust_base)), random_state=505).copy()
    cust_sample.to_csv(os.path.join(test_dir, 'test_batch_5_customer_profiles.csv'), index=False)
    
    print(f"All 5 test datasets generated in '{test_dir}/' successfully!")

if __name__ == '__main__':
    create_all_test_datasets()
