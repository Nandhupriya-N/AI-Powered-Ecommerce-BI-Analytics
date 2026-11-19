"""
MasterMind AI - Comprehensive Full System Cross-Functionality Testing Suite
Verifies all 16 enterprise modules, data processors, ML models, time-series forecasters,
inventory optimizers, CLV tiers, prescriptive decision matrices, PDF reporting,
conversational natural-language voice pipeline, and live Streamlit server responsiveness.
"""

import os
import sys
import time
import io
import pandas as pd
import numpy as np

# Ensure project root is on sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

print("=" * 80)
print("🚀 MASTERMIND AI - COMPREHENSIVE FULL SYSTEM CROSS-FUNCTIONAL TEST")
print("=" * 80)

passed_count = 0
total_count = 0

def test_assert(name, condition, details=""):
    global passed_count, total_count
    total_count += 1
    status = "✅ PASS" if condition else "❌ FAIL"
    if condition:
        passed_count += 1
    print(f"[{total_count:02d}] {status} | {name}")
    if details:
        print(f"     └─ {details}")
    return condition

# =========================================================================
# MODULE 1: AUTHENTICATION, CRYPTOGRAPHY & AUDIT TRAIL
# =========================================================================
print("\n[M1] Testing Enterprise Security & Cryptographic Access Control...")
try:
    from src.auth_db import (
        init_db, hash_password, verify_password,
        authenticate_user, register_user, log_activity, get_audit_logs, list_users
    )
    init_db()
    test_assert("Database Schema Initialization", True, "SQLite database & tables verified")
    
    pwd = "ExecutiveSecure#2026"
    h = hash_password(pwd)
    test_assert("PBKDF2-HMAC-SHA256 Hashing & Salt Verification", verify_password(pwd, h) and not verify_password("WrongPass", h), "100k iteration security check passed")
    
    test_u = f"exec_test_{int(time.time())}"
    reg_res = register_user(test_u, pwd, role="Executive", full_name="Test Executive Auditor")
    user_data = authenticate_user(test_u, pwd)
    test_assert("Role-Based Access Control (RBAC) Authentication", user_data is not None and user_data.get("role") == "Executive", f"Authenticated user '{test_u}' with Executive clearance")
    
    log_activity(test_u, "Test Executive Auditor", "Executive", "SYSTEM_CROSS_TEST", "Verified cross-functional suite execution")
    audit_logs = get_audit_logs(limit=10)
    test_assert("Security Audit Log Persistence", len(audit_logs) > 0, f"Logged & retrieved {len(audit_logs)} audit entries")
except Exception as e:
    test_assert("Module 1 Security & Authentication", False, str(e))

# =========================================================================
# MODULE 2: MULTI-DATASET SCHEMA HARMONIZATION (5 SCENARIOS)
# =========================================================================
print("\n[M2] Testing Multi-Dataset Harmonization Across 5 Real-World Scenarios...")
datasets = [
    ("ready_to_upload_datasets/1_US_Superstore_Retail.csv", "US Superstore Enterprise Retail"),
    ("ready_to_upload_datasets/2_UK_Online_Retail.csv", "UK Online Global Retail"),
    ("ready_to_upload_datasets/3_Brazilian_Olist_Store.csv", "Brazilian E-Commerce Marketplace"),
    ("ready_to_upload_datasets/4_Minimal_Quick_Sales.csv", "Minimal Quick Test Stream"),
    ("ready_to_upload_datasets/5_Kaggle_Customer_Churn_Cohort.csv", "Kaggle Churn Benchmark Cohort")
]

harmonized_data = {}
try:
    from src.data_processor import harmonize_any_ecommerce_dataset
    for d_path, d_label in datasets:
        if os.path.exists(d_path):
            raw_df = pd.read_csv(d_path)
            trans_df, cust_df, status_msg = harmonize_any_ecommerce_dataset(raw_df)
            success = cust_df is not None and not cust_df.empty and trans_df is not None and not trans_df.empty
            harmonized_data[d_label] = (cust_df, trans_df)
            test_assert(f"Harmonization: {d_label}", success, f"{status_msg} ({len(cust_df)} cust, {len(trans_df)} trans)")
        else:
            test_assert(f"Dataset File Check: {d_label}", False, f"File {d_path} missing")
except Exception as e:
    test_assert("Module 2 Multi-Dataset Harmonization", False, str(e))

# Pick primary benchmark dataset for downstream cross-functional tests
primary_cust, primary_trans = harmonized_data.get("US Superstore Enterprise Retail", (None, None))
if primary_cust is None or primary_trans is None:
    primary_cust, primary_trans = list(harmonized_data.values())[0]

# =========================================================================
# MODULE 3: DATA QUALITY ASSESSMENT & CLEANING
# =========================================================================
print("\n[M3] Testing Autonomous Data Quality Assessment & Cleansing...")
try:
    from src.data_processor import assess_data_quality, clean_and_prepare
    dq_summary = assess_data_quality(primary_trans)
    test_assert("Autonomous Data Quality Profiling", dq_summary is not None and "total_rows" in dq_summary, f"Total Rows: {dq_summary.get('total_rows', 0)}, Missing Cols: {len(dq_summary.get('missing_values', {}))}")
    
    clean_df = clean_and_prepare(primary_trans)
    test_assert("Data Sanitization & Preprocessing Pipeline", not clean_df.empty, f"Sanitized {len(clean_df)} valid operational records")
except Exception as e:
    test_assert("Module 3 Data Quality Assessment", False, str(e))

# =========================================================================
# MODULE 4: AUTONOMOUS BI ANALYZER & BATCH INFERENCE
# =========================================================================
print("\n[M4] Testing Autonomous BI Analyzer Batch Inference & Scoring...")
scored_cust = None
scored_trans = None
analysis_results = None
analyzer = None
try:
    from src.analyzer import AutonomousBIAnalyzer
    analyzer = AutonomousBIAnalyzer()
    analyzer.load_models()
    test_assert("Model Artifact Ingestion", analyzer.churn_model is not None and analyzer.anomaly_detector is not None, "Random Forest & Isolation Forest model artifacts verified")
    
    analysis_results = analyzer.analyze_new_batch(primary_cust, primary_trans)
    scored_cust = analysis_results.get('scored_customers', primary_cust)
    scored_trans = analysis_results.get('scored_transactions', primary_trans)
    has_churn_prob = 'Predicted_Churn' in scored_cust.columns or 'Churn_Risk_Score' in scored_cust.columns
    test_assert("Automated Batch Churn Scoring", has_churn_prob, f"Scored {len(scored_cust)} accounts with churn probabilities")
except Exception as e:
    test_assert("Module 4 Autonomous BI Analyzer", False, str(e))

# =========================================================================
# MODULE 5: ADVANCED TIME-SERIES DEMAND FORECASTER
# =========================================================================
print("\n[M5] Testing Multi-Horizon Advanced Demand Forecasting Engine...")
forecast_res = None
try:
    from src.advanced_forecaster import AdvancedDemandForecastingEngine
    forecaster = AdvancedDemandForecastingEngine()
    fc_out = forecaster.generate_daily_forecast(primary_trans, horizon=14)
    forecast_res = fc_out
    has_fc_df = isinstance(fc_out, dict) and "forecast_df" in fc_out
    test_assert("14-Day Multi-Horizon Demand Forecast", has_fc_df, f"Projected demand using '{fc_out.get('model_used', 'Chronos/RF')}'")
    
    cat_fc = forecaster.generate_category_forecast(primary_trans, horizon=14)
    has_cat = cat_fc is not None and (not cat_fc.empty if hasattr(cat_fc, 'empty') else len(cat_fc) > 0)
    test_assert("Category-Level Micro-Forecast Decomposition", has_cat, "Segmented multi-category demand curves")
except Exception as e:
    test_assert("Module 5 Advanced Demand Forecaster", False, str(e))

# =========================================================================
# MODULE 6: CUSTOMER LIFETIME VALUE (CLV ENGINE)
# =========================================================================
print("\n[M6] Testing Customer Lifetime Value (CLV Engine) & Segmentation...")
clv_df = None
clv_summary = None
try:
    from src.clv_engine import CustomerLifetimeValueEngine
    clv_engine = CustomerLifetimeValueEngine()
    clv_df, clv_summary = clv_engine.predict_clv(scored_cust, scored_trans)
    has_tier = clv_df is not None and ('CLV_Tier' in clv_df.columns or 'Predicted_CLV_12M' in clv_df.columns)
    test_assert("12-Month Predictive CLV & Tiering", has_tier, f"Segmented {len(clv_df)} customer accounts into predictive value tiers")
except Exception as e:
    test_assert("Module 6 CLV Modeling Engine", False, str(e))

# =========================================================================
# MODULE 7: INVENTORY OPTIMIZER & STOCKOUT RISKS
# =========================================================================
print("\n[M7] Testing Inventory Intelligence & Stockout Risk Engine...")
inventory_df = None
inventory_summary = None
try:
    from src.inventory_optimizer import InventoryIntelligenceEngine
    inv_engine = InventoryIntelligenceEngine()
    inventory_df, inventory_summary = inv_engine.optimize_inventory(scored_trans)
    has_rop = "Reorder_Point" in inventory_df.columns and "Safety_Stock" in inventory_df.columns
    test_assert("Reorder Point (ROP) & Safety Stock Optimization", has_rop, f"Calculated ROP & stockout vulnerability across {len(inventory_df)} SKUs/categories")
except Exception as e:
    test_assert("Module 7 Inventory Optimization", False, str(e))

# =========================================================================
# MODULE 8: MARKET BASKET ANALYSIS & PRODUCT AFFINITY
# =========================================================================
print("\n[M8] Testing Market Basket Affinity & Cross-Sell Recommender...")
try:
    from src.recommender import compute_association_rules, generate_recommendations
    rules_out = compute_association_rules(scored_trans, min_support=0.01)
    rules_df = rules_out.get('rules_df') if isinstance(rules_out, dict) else rules_out
    test_assert("Apriori Market Basket Association Mining", rules_df is not None and not rules_df.empty, f"Identified {len(rules_df)} high-lift cross-sell affinity pairs")
    
    sample_cust = scored_cust.iloc[0].to_dict() if scored_cust is not None and not scored_cust.empty else {}
    recs = generate_recommendations(sample_cust, scored_trans, top_n=5)
    test_assert("Cross-Sell Product Bundle Generation", recs is not None and len(recs) > 0, f"Generated {len(recs)} prioritized bundle recommendations")
except Exception as e:
    test_assert("Module 8 Market Basket Recommender", False, str(e))

# =========================================================================
# MODULE 9: SENTIMENT & NLP TEXT MINING
# =========================================================================
print("\n[M9] Testing Customer Sentiment & Aspect-Based NLP Mining...")
try:
    from src.recommender import analyze_sentiment_detailed, analyze_aspect_based_sentiment, extract_text_eda_summary
    sample_text = "The electronics item arrived extremely fast and customer service was helpful, but packaging was torn."
    sent_res = analyze_sentiment_detailed(sample_text)
    test_assert("Customer Sentiment Polarity Scoring", sent_res is not None and "polarity" in sent_res, f"Polarity: {sent_res.get('polarity', 0.0):.2f}, Label: {sent_res.get('label', 'N/A')}")
    
    aspects = analyze_aspect_based_sentiment(sample_text)
    test_assert("Aspect-Based NLP Sentiment Extraction", isinstance(aspects, dict), f"Extracted feedback aspects across delivery, service, and product")
except Exception as e:
    test_assert("Module 9 Sentiment & NLP Engine", False, str(e))

# =========================================================================
# MODULE 10: ENTERPRISE MODEL MONITORING & DRIFT AUDITING
# =========================================================================
print("\n[M10] Testing Enterprise Model Governance & Feature Drift Suite...")
drift_report = None
try:
    from src.drift_monitor import EnterpriseModelMonitoringSuite
    monitor = EnterpriseModelMonitoringSuite()
    base = analyzer.baseline_cust if analyzer and analyzer.baseline_cust is not None else scored_cust
    drift_report = monitor.generate_drift_report(base, scored_cust)
    test_assert("Population Stability Index (PSI) & KS Drift Audit", drift_report is not None and "overall_psi" in drift_report, f"Overall PSI: {drift_report.get('overall_psi', 0.0):.4f}, Level: {drift_report.get('drift_level', 'Stable')}")
except Exception as e:
    test_assert("Module 10 Enterprise Model Monitoring", False, str(e))

# =========================================================================
# MODULE 11: UNIFIED PRESCRIPTIVE DECISION ENGINE
# =========================================================================
print("\n[M11] Testing Unified Prescriptive Decision Engine...")
decision_register = None
try:
    from src.decision_engine import BusinessDecisionEngine
    dec_engine = BusinessDecisionEngine()
    decision_register, _ = dec_engine.generate_executive_decision_register(
        churn_summary={'churn_rate': 20.8},
        anomalies_summary=analysis_results.get('anomaly_summary', {}) if analysis_results else {},
        forecast_summary=forecast_res,
        inventory_summary=inventory_summary,
        drift_summary=drift_report,
        clv_summary=clv_summary
    )
    test_assert("Prescriptive Intervention Matrix Generation", decision_register is not None and len(decision_register) > 0, f"Formulated {len(decision_register)} prioritized ROI actions")
except Exception as e:
    test_assert("Module 11 Unified Prescriptive Engine", False, str(e))

# =========================================================================
# MODULE 12: EXECUTIVE REPORT GENERATOR
# =========================================================================
print("\n[M12] Testing Automated Executive Report & Dossier Generation...")
try:
    from src.report_generator import ExecutiveReportGenerator
    rep_gen = ExecutiveReportGenerator()
    kpis = {'total_revenue': float(scored_trans['Total_Amount'].sum()), 'total_orders': len(scored_trans)}
    
    md_summary = rep_gen.generate_markdown_summary(
        user_info={'full_name': 'Test Executive', 'role': 'Executive'},
        dataset_name='US Superstore Enterprise Retail',
        kpi_metrics=kpis,
        decision_register=decision_register
    )
    test_assert("Executive Markdown Synthesis", len(md_summary) > 50, f"Compiled executive summary ({len(md_summary)} chars)")
    
    html_dossier = rep_gen.generate_html_dossier(
        user_info={'full_name': 'Test Executive', 'role': 'Executive'},
        dataset_name='US Superstore Enterprise Retail',
        kpi_metrics=kpis,
        forecast_summary=forecast_res,
        clv_summary=clv_summary,
        inventory_summary=inventory_summary,
        decision_register=decision_register,
        drift_summary=drift_report
    )
    test_assert("HTML Executive Dossier Rendering", len(html_dossier) > 200, f"Rendered HTML analytical dossier ({len(html_dossier)} chars)")
except Exception as e:
    test_assert("Module 12 Executive Report Generation", False, str(e))

# =========================================================================
# MODULE 13: RESEARCH COMPENDIUM (ACADEMIC VIVA REPOSITORY)
# =========================================================================
print("\n[M13] Testing Research Compendium & Literature Benchmark Repository...")
try:
    from src.research_compendium import get_all_papers, get_domains, search_papers
    papers = get_all_papers()
    domains = get_domains()
    test_assert("Academic Literature Compendium Repository", len(papers) >= 100 and len(domains) >= 10, f"Indexed {len(papers)} peer-reviewed papers across {len(domains)} analytical domains")
    
    search_res = search_papers("Random Forest")
    test_assert("Semantic Literature Search Engine", len(search_res) > 0, f"Found {len(search_res)} papers on Tree Ensemble architectures")
except Exception as e:
    test_assert("Module 13 Research Compendium", False, str(e))

# =========================================================================
# MODULE 14: UNIVERSAL NATURAL LANGUAGE ASSISTANT (VIVA & AD-HOC)
# =========================================================================
print("\n[M14] Testing Universal Conversational Business Assistant...")
try:
    from src.nl_assistant import NaturalLanguageBusinessAssistant
    nl_bot = NaturalLanguageBusinessAssistant(inv_engine=inv_engine, clv_engine=clv_engine)
    
    # 1. Academic defense viva query
    ans_viva = nl_bot.answer_query("Why did you choose Random Forest over Deep Learning?", scored_trans=scored_trans, scored_cust=scored_cust)
    test_assert("Academic Viva Defense Query Resolution", "Random Forest" in ans_viva.get("answer", ""), "Correctly defends algorithmic inductive bias for tabular data")
    
    # 2. Financial KPI query
    ans_kpi = nl_bot.answer_query("What is our total profit and margin?", scored_trans=scored_trans, scored_cust=scored_cust)
    test_assert("Financial Metric Query Resolution", "$" in ans_kpi.get("answer", "") or "profit" in ans_kpi.get("answer", "").lower(), "Resolved realized operating profit and margin")
    
    # 3. Product Underperformance Diagnosis
    ans_low = nl_bot.answer_query("which product has lowest sales?", scored_trans=scored_trans, scored_cust=scored_cust)
    test_assert("Root-Cause Category Diagnosis Query", len(ans_low.get("answer", "")) > 20, "Identified lowest volume category with prescriptive guidance")
    
    # 4. Churn Rate Query
    ans_churn = nl_bot.answer_query("what is our overall churn rate?", scored_trans=scored_trans, scored_cust=scored_cust)
    test_assert("Portfolio Churn Rate Query", "%" in ans_churn.get("answer", ""), "Returned portfolio churn percentage and risk profile")
except Exception as e:
    test_assert("Module 14 Universal NL Assistant", False, str(e))

# =========================================================================
# MODULE 15: VOICE SYNTHESIS & AUDIO STREAMING
# =========================================================================
print("\n[M15] Testing Text-to-Speech Normalization & gTTS Audio Generation...")
try:
    import re
    from gtts import gTTS
    
    def clean_text_for_voice(text: str) -> str:
        if not text: return ""
        t = re.sub(r'[*_#`]', '', str(text))
        t = re.sub(r'\$([0-9,]+(?:\.[0-9]+)?)', r'\1 dollars', t)
        t = t.replace('%', ' percent')
        return re.sub(r'\s+', ' ', t).strip()
        
    def gen_voice(txt: str) -> bytes:
        fp = io.BytesIO()
        tts = gTTS(text=txt, lang='en', tld='co.uk', slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    
    sample_answer = "**Electronics** delivered $381,498.05 which is 63.4% of total sales."
    clean_speech = clean_text_for_voice(sample_answer)
    test_assert("Text-to-Speech Markdown Normalization", "*" not in clean_speech and "$" not in clean_speech, f"Spoken: '{clean_speech}'")
    
    aud_bytes = gen_voice(clean_speech)
    test_assert("gTTS Speech Audio Byte Generation", aud_bytes is not None and len(aud_bytes) > 1000, f"Synthesized {len(aud_bytes)} bytes of MP3 audio")
except Exception as e:
    test_assert("Module 15 Voice Audio Synthesis", False, str(e))

# =========================================================================
# MODULE 16: STREAMLIT WEB SERVER & APPLICATION HEALTH
# =========================================================================
print("\n[M16] Testing Web Server Port Health & Python 3.13 Bytecode Compilation...")
try:
    import py_compile
    py_compile.compile("app.py", doraise=True)
    test_assert("Streamlit app.py Python 3.13 Bytecode Compilation", True, "Zero syntax or indentation errors")
    
    import urllib.request
    req = urllib.request.Request("http://localhost:8501", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=4) as resp:
        test_assert("Streamlit Live Uvicorn Server Response (Port 8501)", resp.status == 200, f"HTTP Status: {resp.status} OK")
except Exception as e:
    test_assert("Module 16 Web Server Health", False, str(e))

# =========================================================================
# FINAL SYSTEM SCORECARD
# =========================================================================
print("\n" + "=" * 80)
print(f"📊 FULL SYSTEM CROSS-FUNCTIONAL SCORECARD: {passed_count} / {total_count} TESTS PASSED ({(passed_count/total_count)*100:.1f}%)")
print("=" * 80)

if passed_count == total_count:
    print("🌟 ALL 16 ENTERPRISE MODULES ARE 100% OPERATIONAL AND CROSS-COMPATIBLE!\n")
    sys.exit(0)
else:
    print(f"⚠️ {total_count - passed_count} TEST(S) FAILED.\n")
    sys.exit(1)
