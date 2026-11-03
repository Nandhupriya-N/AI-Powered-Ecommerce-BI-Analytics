import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
from src.data_processor import clean_and_prepare
from src.clv_engine import CustomerLifetimeValueEngine
from src.inventory_optimizer import InventoryIntelligenceEngine
from src.recommender import compute_association_rules, analyze_aspect_based_sentiment

cust_df = clean_and_prepare(pd.read_csv("data/historical_customer_profiles.csv"))
trans_df = clean_and_prepare(pd.read_csv("data/historical_ecommerce_data.csv"))

print("1. Testing CLV Engine...")
clv_engine = CustomerLifetimeValueEngine()
clv_res = clv_engine.compute_clv(cust_df, trans_df)
print("CLV Summary:", clv_res['summary'])
print("Top 3 CLV Accounts:")
print(clv_res['scored_clv_df'][['Customer_ID', 'Monetary_Spend', 'Probability_Alive', 'Predicted_CLV_12M', 'CLV_Tier', 'Retention_Priority']].head(3))

print("\n2. Testing Marketing Campaign Evaluator...")
mktg_res = clv_engine.evaluate_marketing_campaigns(clv_res['scored_clv_df'], trans_df)
print("Campaign Comparison:")
print(mktg_res['campaign_comparison'][['Campaign Name', 'Target Audience', 'Expected Gross ROI', 'Net Benefit ($)']])

print("\n3. Testing Inventory Intelligence Engine...")
inv_engine = InventoryIntelligenceEngine()
inv_res = inv_engine.compute_inventory_plan(trans_df)
print("Inventory Plan:")
print(inv_res['inventory_plan_df'][['Product Category', 'Avg Daily Demand (Units)', 'Recommended Safety Stock', 'Reorder Point (ROP)', 'Economic Order Qty (EOQ)', 'Stockout Risk Assessment']])

print("\n4. Testing Association Rules & Product Bundles...")
assoc_res = compute_association_rules(trans_df)
print(f"Generated {len(assoc_res['rules_df'])} association rules and {len(assoc_res['bundles'])} product bundles.")
if not assoc_res['rules_df'].empty:
    print(assoc_res['rules_df'].head(3)[['Antecedent (If Bought)', 'Consequent (Then Also)', 'Support (%)', 'Confidence (%)', 'Lift Ratio', 'Affinity Strength']])

print("\n5. Testing Aspect-Based Sentiment...")
aspect_res = analyze_aspect_based_sentiment(trans_df)
print("Aspect Breakdown:")
print(aspect_res['aspect_breakdown'])

print("\n>>> PHASE 6 ENGINES VERIFIED WITH ZERO ERRORS! <<<")
