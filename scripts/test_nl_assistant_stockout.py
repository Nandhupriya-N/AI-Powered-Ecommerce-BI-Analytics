import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.nl_assistant import NaturalLanguageBusinessAssistant
from src.inventory_optimizer import InventoryIntelligenceEngine
from src.clv_engine import CustomerLifetimeValueEngine

inv_engine = InventoryIntelligenceEngine()
clv_engine = CustomerLifetimeValueEngine()
assistant = NaturalLanguageBusinessAssistant(inv_engine=inv_engine, clv_engine=clv_engine)

trans_df = pd.read_csv('ready_to_upload_datasets/1_US_Superstore_Retail.csv')
inv_df, inv_sum = inv_engine.optimize_inventory(trans_df)

print("--- TEST 1: Stockout Risks Query (Explicit inventory_df) ---")
res1 = assistant.answer_query('Which items are at risk of stockout?', scored_trans=trans_df, inventory_df=inv_df)
print("Answer:", res1['answer'])
assert 'Data Dependency Missing' not in res1['answer'], "Test 1 failed!"
print("Status: 100% PASS ✅")

print("\n--- TEST 2: Stockout Risks Query (Auto-heal fallback from trans_df) ---")
res2 = assistant.answer_query('Which items are at risk of stockout?', scored_trans=trans_df)
print("Answer:", res2['answer'])
assert 'Data Dependency Missing' not in res2['answer'], "Test 2 failed!"
print("Status: 100% PASS ✅")

print("\n--- TEST 3: Top Customers by CLV Query ---")
cust_df = pd.DataFrame({
    'Customer_ID': [f'CUST-{i}' for i in range(10)],
    'Monetary_Spend': [1000 + i*200 for i in range(10)],
    'Frequency_Orders': [3 + i for i in range(10)],
    'Recency_Days': [10 + i*5 for i in range(10)],
    'Predicted_Churn': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
})
res3 = assistant.answer_query('Show me top customers by CLV', scored_cust=cust_df, scored_trans=trans_df)
print("Answer:", res3['answer'])
assert 'Data Dependency Missing' not in res3['answer'], "Test 3 failed!"
print("Status: 100% PASS ✅")

print("\nALL NL ASSISTANT DATA DEPENDENCY TESTS PASSED SUCCESSFULLY!")
