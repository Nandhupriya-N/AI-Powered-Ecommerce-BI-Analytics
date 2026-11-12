import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from scripts.universal_query_prototype import resolve_universal_query

ctx = {
    'transactions': pd.DataFrame({'Total_Amount': [100, 200, 300], 'Region': ['East', 'West', 'East'], 'Profit': [20, 40, 60]}),
    'customers': pd.DataFrame({'Customer_ID': ['C1', 'C2', 'C3'], 'Tenure': [5, 10, 15], 'Predicted_Churn': [0, 1, 0]})
}

test_queries = [
    'How many customers do we have?',
    'What is our total profit?',
    'Which region has the most sales?',
    'What is Random Forest and why did you use it?',
    'How can we increase our profit?'
]

for q in test_queries:
    res = resolve_universal_query(q, ctx)
    print(f"Q: {q}")
    print(f"Intent: {res.get('intent')}")
    print(f"Answer: {res.get('answer')[:120]}...\n")
