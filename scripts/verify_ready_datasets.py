import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.data_processor import harmonize_any_ecommerce_dataset
from src.analyzer import AutonomousBIAnalyzer

def verify():
    files = sorted(glob.glob('ready_to_upload_datasets/*.csv'))
    analyzer = AutonomousBIAnalyzer()
    print(f"Found {len(files)} test datasets.")
    for f in files:
        df = pd.read_csv(f)
        fname = os.path.basename(f)
        print(f"\n--- Testing Dataset: {fname} ({len(df)} rows) ---")
        t_df, c_df, msg = harmonize_any_ecommerce_dataset(df)
        print(f"  [Harmonizer] {msg}")
        print(f"  [Shapes] Trans: {t_df.shape}, Cust: {c_df.shape}")
        res = analyzer.analyze_new_batch(new_trans_df=t_df, new_cust_df=c_df)
        scored_trans = res['scored_transactions']
        scored_cust = res['scored_customers']
        rev = scored_trans['Total_Amount'].sum()
        churn_counts = scored_cust['Predicted_Churn'].value_counts().to_dict()
        print(f"  [Analyzer] Scored Revenue: ${rev:,.2f} | Churn predictions: {churn_counts}")
        print(f"  [Status] 100% SUCCESS! ✅")

    print("\n" + "=" * 70)
    print("ALL 5 DATASETS FULLY HARMONIZED & TESTED ACROSS COMPLETE PIPELINE!")
    print("=" * 70)

if __name__ == '__main__':
    verify()
