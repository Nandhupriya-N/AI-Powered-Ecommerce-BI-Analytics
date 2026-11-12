import pandas as pd
import numpy as np
import os
import sys

from src.data_processor import (
    clean_and_prepare,
    harmonize_any_ecommerce_dataset,
    assess_data_quality,
    compute_rfm_segments
)
from src.analyzer import AutonomousBIAnalyzer
from src.clv_engine import CustomerLifetimeValueEngine
from src.inventory_optimizer import InventoryIntelligenceEngine
from src.decision_engine import BusinessDecisionEngine
from src.recommender import compute_association_rules, analyze_aspect_based_sentiment

def test_all_custom_datasets():
    print("=" * 70)
    print("TESTING UNIVERSAL E-COMMERCE DATASET INGESTION ACROSS ALL MODULES")
    print("=" * 70)
    
    analyzer = AutonomousBIAnalyzer()
    clv_engine = CustomerLifetimeValueEngine()
    inv_engine = InventoryIntelligenceEngine()
    dec_engine = BusinessDecisionEngine()

    test_cases = [
        (
            "1. US Superstore Retail Dataset",
            pd.DataFrame({
                'Order ID': [f'CA-2021-{100000+i}' for i in range(30)],
                'Order Date': [f'2021-{(i%12)+1:02d}-{(i%28)+1:02d}' for i in range(30)],
                'Customer ID': [f'CUST-{100+(i%6)}' for i in range(30)],
                'Customer Name': [f'Customer {i%6}' for i in range(30)],
                'Category': ['Furniture', 'Office Supplies', 'Technology', 'Furniture', 'Technology', 'Office Supplies'] * 5,
                'Sub-Category': ['Bookcases', 'Labels', 'Phones', 'Chairs', 'Accessories', 'Paper'] * 5,
                'Sales': [f"${100.0 + i*15:.2f}" for i in range(30)],
                'Quantity': [1 + (i%4) for i in range(30)],
                'Discount': [f"{(i%4)*5}%" for i in range(30)],
                'Profit': [f"${20.0 + i*3:.2f}" for i in range(30)],
                'Region': ['South', 'West', 'East', 'North', 'West', 'East'] * 5
            })
        ),
        (
            "2. UK Online Retail Dataset (Cancellations, NaNs, Raw Currency)",
            pd.DataFrame({
                'InvoiceNo': [f'5363{65+i}' if i != 3 else 'C536379' for i in range(25)],
                'StockCode': [f'8512{i}' for i in range(25)],
                'Description': [
                    'WHITE HANGING HEART T-LIGHT HOLDER', 'WHITE METAL LANTERN', 'ALARM CLOCK BAKELIKE RED',
                    'DISCOUNT VOUCHER', 'RED RETROSPOT MINI BACKPACK'
                ] * 5,
                'Quantity': [6, 4, 2, -1, 10] * 5,
                'InvoiceDate': ['12/1/2010 8:26', '12/2/2010 9:15', '12/3/2010 14:00', '12/4/2010 16:30', '12/5/2010 18:00'] * 5,
                'UnitPrice': ['$2.55', '$3.39', '$3.75', '$27.50', '$1.25'] * 5,
                'CustomerID': [17850.0, 17850.0, 17851.0, None, 17852.0] * 5,
                'Country': ['United Kingdom', 'United Kingdom', 'France', 'Germany', 'United Kingdom'] * 5
            })
        ),
        (
            "3. Brazilian Olist E-Commerce Schema",
            pd.DataFrame({
                'order_id': [f'ord_br_{i}' for i in range(20)],
                'customer_id': [f'cust_br_{i%5}' for i in range(20)],
                'order_purchase_timestamp': [f'2022-0{(i%9)+1:02d}-15 12:00:00' for i in range(20)],
                'price': [49.90 + i*5 for i in range(20)],
                'freight_value': [15.20 for _ in range(20)],
                'product_category_name': ['beleza_saude', 'informatica_acessorios', 'cama_mesa_banho', 'relogios_presentes'] * 5,
                'review_score': [5, 4, 3, 1] * 5
            })
        ),
        (
            "4. Minimal 2-Column E-Commerce Export",
            pd.DataFrame({
                'sales': [45.0, 120.5, 300.0, 89.9, 1500.0, 220.0, 60.0, 450.0],
                'date': ['2023-01-10', '2023-01-11', '2023-01-12', '2023-01-13', '2023-01-14', '2023-01-15', '2023-01-16', '2023-01-17']
            })
        ),
        (
            "5. Kaggle Customer Churn Cohort",
            pd.read_csv('data/kaggle_export/kaggle_ecommerce_churn_sample_500.csv')
        )
    ]

    for title, raw_df in test_cases:
        print(f"\n---> Testing Scenario: {title}")
        print(f"     Raw records: {len(raw_df):,}, columns: {list(raw_df.columns)[:5]}...")
        
        # Ingestion via Universal Harmonizer
        active_trans, active_cust, msg = harmonize_any_ecommerce_dataset(raw_df)
        print(f"     [Harmonizer] {msg}")
        print(f"     [Harmonizer] Active Trans: {len(active_trans):,}, Active Cust: {len(active_cust):,}")
        
        # Clean and prepare verification
        active_trans = clean_and_prepare(active_trans)
        active_cust = clean_and_prepare(active_cust)
        
        # Pipeline Execution
        res = analyzer.analyze_new_batch(new_trans_df=active_trans, new_cust_df=active_cust)
        scored_cust = res['scored_customers']
        scored_trans = res['scored_transactions']
        print(f"     [Analyzer] Churn predictions: {scored_cust['Predicted_Churn'].value_counts().to_dict()}")
        print(f"     [Analyzer] Revenue: ${scored_trans['Total_Amount'].sum():,.2f}")
        
        # CLV Engine
        clv_df, clv_sum = clv_engine.predict_clv(scored_cust, scored_trans)
        print(f"     [CLV] 12M Portfolio CLV: ${clv_sum.get('total_portfolio_clv_12m', 0):,}")
        
        # Inventory Optimizer
        inv_df, inv_sum = inv_engine.optimize_inventory(scored_trans)
        print(f"     [Inventory] Monitored SKUs: {inv_sum.get('total_skus_monitored')}, Critical: {inv_sum.get('critical_count')}")
        
        # Recommender (Association Rules & Sentiment)
        ar_res = compute_association_rules(scored_trans)
        rules_cnt = len(ar_res.get('rules_df', []))
        sentiment_res = analyze_aspect_based_sentiment(scored_trans)
        asp_cnt = len(sentiment_res.get('aspect_breakdown', []))
        print(f"     [Recommender] Association rules: {rules_cnt}, Aspect sentiments: {asp_cnt}")
        
        # Decision Engine
        reg, _ = dec_engine.generate_executive_decision_register(
            churn_summary=res['changes'].get('churn_rate', {}),
            anomalies_summary=res.get('anomaly_summary', {}),
            forecast_summary=res.get('forecast', {}),
            inventory_summary=inv_sum,
            clv_summary=clv_sum
        )
        print(f"     [Decision Engine] Generated {len(reg)} executive initiatives.")
        print(f"     [STATUS] PASSED WITH ZERO ERRORS! ✅")

    print("\n" + "=" * 70)
    print("ALL 5 CUSTOM DATASET TEST SCENARIOS PASSED 100%!")
    print("=" * 70)

if __name__ == '__main__':
    test_all_custom_datasets()
