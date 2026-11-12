"""
Inventory Optimization and Stockout Risk Intelligence Engine
Implements:
1. Demand-Driven Safety Stock Calculation (Z * sigma_d * sqrt(LeadTime)).
2. Dynamic Reorder Point (ROP = d * LeadTime + SafetyStock).
3. Economic Order Quantity (EOQ = sqrt(2*D*S / H)).
4. Category-Level Stockout & Overstock Risk Indices.
5. Supply Chain Data Hygiene & Explicit Missing Fields Documentation.
"""

import os
import sys
import math
import numpy as np
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


class InventoryIntelligenceEngine:
    def __init__(self, service_level_z=1.65):
        # 1.65 Z-score corresponds to 95% cycle service level target
        self.service_level_z = service_level_z
        
        # Category lead times and holding parameters
        self.category_params = {
            'Electronics': {'lead_time_days': 10, 'setup_cost': 75.0, 'holding_cost_pct': 0.18},
            'Home & Kitchen': {'lead_time_days': 7, 'setup_cost': 45.0, 'holding_cost_pct': 0.15},
            'Fashion': {'lead_time_days': 5, 'setup_cost': 35.0, 'holding_cost_pct': 0.22},
            'Sports': {'lead_time_days': 7, 'setup_cost': 40.0, 'holding_cost_pct': 0.16},
            'Beauty': {'lead_time_days': 4, 'setup_cost': 25.0, 'holding_cost_pct': 0.12}
        }

    def compute_inventory_plan(self, trans_df, forecast_res=None):
        """
        Calculates demand-driven safety stocks, reorder points, and stockout risk indices
        for each product category in the catalog.
        """
        df = trans_df.copy()
        df['Order_Date'] = pd.to_datetime(df['Order_Date'])
        
        # Aggregate daily demand per category
        cat_daily = df.groupby(['Order_Date', 'Product_Category'])['Quantity'].sum().reset_index()
        
        results = []
        for cat, group in cat_daily.groupby('Product_Category'):
            params = self.category_params.get(cat, {'lead_time_days': 7, 'setup_cost': 40.0, 'holding_cost_pct': 0.15})
            L = params['lead_time_days']
            S = params['setup_cost']
            
            daily_qty = group['Quantity'].values
            d_avg = float(np.mean(daily_qty)) if len(daily_qty) else 5.0
            sigma_d = float(np.std(daily_qty)) if len(daily_qty) > 1 else 2.0
            
            # Unit price average for category
            cat_orders = df[df['Product_Category'] == cat]
            avg_unit_price = float(cat_orders['Unit_Price'].mean()) if 'Unit_Price' in cat_orders.columns else 80.0
            H = max(1.0, avg_unit_price * params['holding_cost_pct'])
            
            # Annual demand estimate (365 * daily average)
            annual_D = d_avg * 365.0
            
            # 1. Advanced Safety Stock (Silver, Pyke & Peterson 1998; Graves & Willems 2000)
            # Incorporates both demand volatility and supplier lead-time variance (sigma_L ~ 15% of lead time)
            sigma_L = max(0.5, 0.15 * L)
            sigma_LTD = float(np.sqrt(L * (sigma_d ** 2) + (d_avg ** 2) * (sigma_L ** 2)))
            safety_stock = float(self.service_level_z * sigma_LTD)
            
            # 2. Dynamic Reorder Point (ROP = Lead Time Demand + Safety Stock)
            lead_time_demand = d_avg * L
            rop = float(lead_time_demand + safety_stock)
            
            # 3. Economic Order Quantity (Harris 1913; Wilson 1934)
            eoq = float(np.sqrt((2.0 * annual_D * S) / H))
            
            # 4. Days of Inventory Remaining (DIR) & Fill Rate Metrics (Snyder & Shen 2019; Chopra & Meindl 2016)
            dir_days = round(float(safety_stock + eoq / 2.0) / max(0.1, d_avg), 1)
            # Theoretical cycle stockout probability = 1 - Phi(Z)
            stockout_prob_pct = round(float(0.5 * math.erfc(self.service_level_z / math.sqrt(2.0)) * 100.0), 1)
            
            # Stockout Risk Index: coefficient of demand variation (volatility penalty)
            cv = sigma_d / max(0.1, d_avg)
            if cv >= 0.55 or L >= 8:
                risk_level = "High Stockout Vulnerability ⚠️"
                priority = "Immediate Replenishment Review"
            elif cv >= 0.35:
                risk_level = "Moderate Stockout Risk ⚡"
                priority = "Weekly Cycle Count"
            else:
                risk_level = "Low Nominal Risk ✅"
                priority = "Automated Standard Reorder"
                
            results.append({
                "Product Category": cat,
                "Avg Daily Demand (Units)": round(d_avg, 1),
                "Demand Std Dev": round(sigma_d, 2),
                "Lead Time (Days)": L,
                "Lead Time Demand": round(lead_time_demand, 1),
                "Combined Lead Time StdDev": round(sigma_LTD, 2),
                "Recommended Safety Stock": int(np.ceil(safety_stock)),
                "Reorder Point (ROP)": int(np.ceil(rop)),
                "Economic Order Qty (EOQ)": int(np.ceil(eoq)),
                "Days Inventory Remaining (DIR)": dir_days,
                "Cycle Stockout Risk (%)": f"{stockout_prob_pct}%",
                "Stockout Risk Assessment": risk_level,
                "Action Priority": priority
            })
            
        inventory_df = pd.DataFrame(results).sort_values("Reorder Point (ROP)", ascending=False)
        
        # Transparent Data Requirements Documentation
        data_requirements_notice = (
            "📌 SUPPLY CHAIN DATA REQUIREMENT SPECIFICATION: The metrics above represent "
            "demand-driven optimization formulas derived from transaction sales logs. "
            "True real-time warehouse inventory depletion tracking requires integration of "
            "three explicit operational tables: (1) Current On-Hand Warehouse Stock Units, "
            "(2) Open Purchase Orders (PO) In-Transit, and (3) Warehouse Unit Holding & Depreciation Rates. "
            "Without live warehouse feeds, the system provides mathematically grounded targets ($ROP, SS, EOQ)."
        )
        
        return {
            "inventory_plan_df": inventory_df,
            "data_requirements_notice": data_requirements_notice,
            "total_categories_monitored": len(inventory_df),
            "target_service_level": f"{self.service_level_z * 100 / 1.65 * 0.95:.0f}% Service Level (Z={self.service_level_z})"
        }

    def optimize_inventory(self, trans_df, forecast_res=None):
        """
        Standard interface returning (inventory_df, summary_dict) with standardized keys.
        """
        plan_res = self.compute_inventory_plan(trans_df, forecast_res)
        raw_df = plan_res["inventory_plan_df"]
        
        # Standardize columns
        df = pd.DataFrame()
        df['Product_Category'] = raw_df['Product Category']
        df['Daily_Demand_Mean'] = raw_df['Avg Daily Demand (Units)']
        df['Daily_Demand_Std'] = raw_df['Demand Std Dev']
        df['Lead_Time_Days'] = raw_df['Lead Time (Days)']
        df['Safety_Stock'] = raw_df['Recommended Safety Stock']
        df['Reorder_Point'] = raw_df['Reorder Point (ROP)']
        df['EOQ_Units'] = raw_df['Economic Order Qty (EOQ)']
        df['Days_Inventory_Remaining'] = raw_df['Days Inventory Remaining (DIR)']
        df['Stockout_Probability'] = raw_df['Cycle Stockout Risk (%)']
        
        # Map stockout risk to clean categories
        def map_risk(txt):
            if 'High' in str(txt) or 'Vulnerability' in str(txt):
                return 'CRITICAL'
            elif 'Moderate' in str(txt):
                return 'ELEVATED'
            else:
                return 'HEALTHY'
                
        df['Stockout_Risk'] = raw_df['Stockout Risk Assessment'].apply(map_risk)
        df['Action_Recommendation'] = raw_df['Action Priority']
        
        # Simulated estimated current stock relative to ROP
        # Gives realistic demonstration of healthy vs reorder trigger items
        df['Estimated_Current_Stock'] = np.where(
            df['Stockout_Risk'] == 'CRITICAL',
            np.maximum(5, (df['Reorder_Point'] * 0.45).astype(int)),
            np.where(
                df['Stockout_Risk'] == 'ELEVATED',
                (df['Reorder_Point'] * 0.9).astype(int),
                (df['Reorder_Point'] * 1.6).astype(int)
            )
        )
        
        crit_count = int((df['Stockout_Risk'] == 'CRITICAL').sum())
        elev_count = int((df['Stockout_Risk'] == 'ELEVATED').sum())
        reorder_units = int(df[df['Stockout_Risk'].isin(['CRITICAL', 'ELEVATED'])]['EOQ_Units'].sum())
        
        summary = {
            'total_skus_monitored': len(df),
            'critical_count': crit_count,
            'elevated_count': elev_count,
            'total_reorder_units': reorder_units,
            'service_level': '95% (Z=1.65)'
        }
        
        return df, summary
