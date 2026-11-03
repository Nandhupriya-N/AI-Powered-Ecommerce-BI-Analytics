"""
End-to-end headless verification test for enterprise AI BI platform.
Tests all intelligence engines and checks memory footprint.
"""

import os
import sys
import psutil
import time
import pandas as pd
import numpy as np

# Ensure root directory is on sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.analyzer import AutonomousBIAnalyzer
from src.clv_engine import CustomerLifetimeValueEngine
from src.inventory_optimizer import InventoryIntelligenceEngine
from src.drift_monitor import EnterpriseModelMonitoringSuite
from src.nl_assistant import NaturalLanguageBusinessAssistant
from src.decision_engine import BusinessDecisionEngine
from src.report_generator import ExecutiveReportGenerator
from src.recommender import compute_association_rules, analyze_aspect_based_sentiment
from src.data_processor import clean_and_prepare, map_kaggle_to_standard

def test_full_pipeline():
    sys.stdout.reconfigure(encoding='utf-8')
    process = psutil.Process()
    ram_initial = process.memory_info().rss / (1024 * 1024)
    print(f"[1] Initial RAM Usage: {ram_initial:.2f} MB")

    # 1. Initialize Analyzer
    analyzer = AutonomousBIAnalyzer(models_dir='models', data_dir='data')
    print("[OK] Analyzer initialized successfully.")

    # 2. Load dataset
    k_test = pd.read_csv('data/kaggle_export/kaggle_ecommerce_churn_test_unseen_1408.csv')
    cust_df = map_kaggle_to_standard(k_test)
    trans_df = pd.read_csv('data/kaggle_export/kaggle_transactions_orders_2000.csv')
    cust_df = clean_and_prepare(cust_df)
    trans_df = clean_and_prepare(trans_df)
    print(f"[OK] Data loaded & cleaned: {len(cust_df):,} customers, {len(trans_df):,} transactions.")

    # 3. Run Analyzer Batch
    t0 = time.time()
    results = analyzer.analyze_new_batch(trans_df, cust_df)
    scored_cust = results['scored_customers']
    scored_trans = results['scored_transactions']
    print(f"[OK] Analyzer batch processed in {time.time() - t0:.2f}s.")

    # 4. Run CLV Engine
    clv_engine = CustomerLifetimeValueEngine()
    clv_df, clv_summary = clv_engine.predict_clv(scored_cust, scored_trans)
    print(f"[OK] CLV Engine complete. 12M Portfolio CLV: ${clv_summary['total_clv_12m']:,.2f}, Top-Tier: {clv_summary['top_tier_count']} accounts.")

    # 5. Run Inventory Engine
    inv_engine = InventoryIntelligenceEngine()
    inventory_df, inventory_summary = inv_engine.optimize_inventory(scored_trans)
    print(f"[OK] Inventory Engine complete. SKUs: {inventory_summary['total_skus_monitored']}, Critical: {inventory_summary['critical_count']}, Reorder: {inventory_summary['total_reorder_units']:,} units.")

    # 6. Run Drift Suite
    drift_suite = EnterpriseModelMonitoringSuite()
    drift_report = drift_suite.generate_drift_report(analyzer.baseline_cust, scored_cust)
    print(f"[OK] Drift Suite complete. Status: {drift_report['drift_level']}, Max KS: {drift_report['max_ks_statistic']:.4f}, PSI: {drift_report['overall_psi']:.4f}.")

    # 7. Run Decision Engine
    decision_engine = BusinessDecisionEngine()
    decision_reg, what_if = decision_engine.generate_executive_decision_register(
        churn_summary=results['changes'].get('churn_rate', {}),
        anomalies_summary=results.get('anomaly_summary', {}),
        forecast_summary=results.get('forecast', {}),
        inventory_summary=inventory_summary,
        drift_summary=drift_report,
        clv_summary=clv_summary
    )
    print(f"[OK] Decision Engine complete. Generated {len(decision_reg)} strategic action items.")

    # 8. Test NL Assistant
    nl_assistant = NaturalLanguageBusinessAssistant(
        analyzer=analyzer,
        clv_engine=clv_engine,
        inv_engine=inv_engine,
        drift_suite=drift_suite
    )
    q_ans = nl_assistant.answer_query(
        query="What is our overall churn rate?",
        scored_trans=scored_trans,
        scored_cust=scored_cust,
        clv_df=clv_df,
        inventory_df=inventory_df,
        forecast_res=results.get('forecast', {})
    )
    print(f"[OK] NL Assistant test answered: '{q_ans['answer'][:80]}...'")

    # 8b. Test Association Rules and Aspect Sentiment
    ar_res = compute_association_rules(scored_trans)
    assoc_rules = ar_res.get('rules_df', pd.DataFrame()) if isinstance(ar_res, dict) else ar_res
    print(f"[OK] Association rules mined: {len(assoc_rules)} rules found.")
    aspect_res = analyze_aspect_based_sentiment(scored_trans)
    asp_df = aspect_res.get('aspect_breakdown', pd.DataFrame()) if isinstance(aspect_res, dict) else pd.DataFrame(aspect_res)
    print(f"[OK] Aspect sentiment extracted: {len(asp_df)} operational dimensions.")

    # 9. Test Report Generator
    report_gen = ExecutiveReportGenerator()
    kpi_m = {
        'total_revenue': float(scored_trans['Total_Amount'].sum()),
        'total_profit': float(scored_trans['Profit'].sum()),
        'profit_margin': float((scored_trans['Profit'].sum() / scored_trans['Total_Amount'].sum() * 100)),
        'order_count': int(len(scored_trans)),
        'aov': float(scored_trans['Total_Amount'].sum() / len(scored_trans)),
        'churn_rate': float(scored_cust['Predicted_Churn'].mean() * 100)
    }
    fc_m = {
        'daily_run_rate': 25000.0,
        'cumulative_14d': 350000.0,
        'top_category': 'Multi-Category'
    }
    html_dossier = report_gen.generate_html_dossier(
        user_info={'full_name': 'Chief BI Architect', 'role': 'Administrator'},
        dataset_name='Kaggle Test Cohort',
        kpi_metrics=kpi_m,
        forecast_summary=fc_m,
        clv_summary=clv_summary,
        inventory_summary=inventory_summary,
        drift_summary=drift_report,
        decision_register=decision_reg
    )
    print(f"[OK] Report Generator created HTML dossier ({len(html_dossier):,} bytes).")

    ram_final = process.memory_info().rss / (1024 * 1024)
    print(f"[OK] End-to-End Pipeline Successful! Final RAM: {ram_final:.2f} MB (Delta: +{ram_final - ram_initial:.2f} MB)")

if __name__ == '__main__':
    test_full_pipeline()
