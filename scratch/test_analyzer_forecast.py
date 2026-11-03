import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import pandas as pd
from src.data_processor import clean_and_prepare
from src.analyzer import AutonomousBIAnalyzer

print("Loading data and initializing analyzer...")
t = clean_and_prepare(pd.read_csv("data/historical_ecommerce_data.csv"))
c = clean_and_prepare(pd.read_csv("data/historical_customer_profiles.csv"))
a = AutonomousBIAnalyzer()

print("Running analyze_new_batch...")
res = a.analyze_new_batch(t, c)
fc = res["forecast"]
print("Active forecaster:", fc["model_used"])
print("\nDaily FC head:")
print(fc["future_14_day_forecast"].head(2))
print("\nWeekly FC head:")
print(fc["weekly_forecast"].head(2))
print("\nCategory FC head:")
print(fc["category_forecast"].head(2))
print("\nBenchmark Comparison count:", len(fc.get("benchmark_comparison", [])))
print("\n>>> FULL ANALYZER INTEGRATION SUCCESS! <<<")
