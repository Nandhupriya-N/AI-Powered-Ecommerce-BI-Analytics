import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
from src.data_processor import clean_and_prepare, compute_customer_journey_metrics
from src.clv_engine import CustomerLifetimeValueEngine
from src.inventory_optimizer import InventoryIntelligenceEngine
from src.recommender import compute_association_rules, analyze_aspect_based_sentiment
from src.nl_assistant import NaturalLanguageBusinessAssistant

# Load data
t = clean_and_prepare(pd.read_csv("data/historical_ecommerce_data.csv"))
c = clean_and_prepare(pd.read_csv("data/historical_customer_profiles.csv"))

clv_engine = CustomerLifetimeValueEngine()
clv_res = clv_engine.compute_clv(c, t)
inv_engine = InventoryIntelligenceEngine()
inv_res = inv_engine.compute_inventory_plan(t)
assoc_res = compute_association_rules(t)
aspect_res = analyze_aspect_based_sentiment(t)
journey = compute_customer_journey_metrics(t)

ctx = {
    'transactions': t,
    'customers': c,
    'clv_data': clv_res['scored_clv_df'],
    'inventory_plan': inv_res['inventory_plan_df'],
    'rules_df': assoc_res['rules_df'],
    'bundles': assoc_res['bundles'],
    'aspect_sentiment': aspect_res['aspect_breakdown'],
    'customer_journey': journey,
    'anomalies_count': 12
}

assistant = NaturalLanguageBusinessAssistant()

test_questions = [
    "Which categories generated the highest revenue?",
    "Which customer segments have high churn risk?",
    "Which customer segments have the highest predicted CLV?",
    "What are the major business risks?",
    "What are the stockout risks in inventory?",
    "Tell me about repeat purchase behavior in the customer journey."
]

print(">>> TESTING NATURAL-LANGUAGE BUSINESS ASSISTANT <<<")
for q in test_questions:
    print(f"\nQ: {q}")
    res = assistant.query(q, ctx)
    print(f"Intent Matched: {res['intent']}")
    print(f"Answer: {res['answer'][:120]}...")
    print(f"Methodology: {res['calculation_methodology']}")
    print(f"Data rows: {len(res['supporting_data'])}")

print("\n>>> ALL NL ASSISTANT QUERIES PROCESSED SUCCESSFULLY! <<<")
