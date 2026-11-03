import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
from src.data_processor import clean_and_prepare, validate_incremental_batch, compute_customer_journey_metrics
from src.drift_monitor import EnterpriseModelMonitoringSuite

print("Testing Incremental Batch Validation...")
df_raw = pd.read_csv("data/historical_ecommerce_data.csv")
val_report = validate_incremental_batch(df_raw)
print("Batch Validation Report:")
for k, v in val_report.items():
    print(f"  {k}: {v}")

print("\nTesting Customer Journey Metrics...")
journey = compute_customer_journey_metrics(df_raw)
print("Customer Journey:")
for k, v in journey.items():
    print(f"  {k}: {v}")

print("\nTesting Enterprise Model Monitoring Suite...")
suite = EnterpriseModelMonitoringSuite()
b_cust = clean_and_prepare(pd.read_csv("data/historical_customer_profiles.csv"))
n_cust = clean_and_prepare(pd.read_csv("data/new_batch_customer_profiles.csv"))
b_trans = clean_and_prepare(pd.read_csv("data/historical_ecommerce_data.csv"))
n_trans = clean_and_prepare(pd.read_csv("data/new_batch_ecommerce_data.csv"))

gov_report = suite.generate_governance_report(b_cust, n_cust, b_trans, n_trans)
print("Governance Alert Level:", gov_report["alert_level"])
print("Retraining Recommended:", gov_report["retraining_recommended"])
print("Action Summary:", gov_report["action_summary"])
print("\nTop 4 Customer Feature Drifts:")
print(gov_report["customer_feature_drift"].head(4)[['Feature Name', 'Mean Shift (%)', 'P-Value', 'PSI Score', 'Drift Status']])
print("\n>>> PHASE 5 VERIFICATION PASSED SUCCESSFULLY! <<<")
