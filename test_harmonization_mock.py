import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta

def derive_trans_from_cust(cust_df):
    """Generates realistic transaction history synchronized with customer profiles."""
    df = cust_df.copy()
    ref_date = pd.Timestamp.now()
    
    trans_rows = []
    default_cats = ['Laptop & Electronics', 'Mobile Phone & Accessories', 'Fashion & Apparel', 'Home & Kitchen', 'Grocery & Health']
    
    for idx, row in df.iterrows():
        cust_id = str(row.get('Customer_ID', f"CUST_{1000+idx}"))
        freq = int(row.get('Frequency_Orders', row.get('OrderCount', np.random.randint(1, 5))))
        freq = max(1, min(15, freq))
        total_spend = float(row.get('Monetary_Spend', row.get('CashbackAmount', 200.0) * 5.0))
        if total_spend <= 0:
            total_spend = 150.0
        avg_item_price = round(total_spend / freq, 2)
        
        pref_cat = str(row.get('PreferedOrderCat', row.get('Product_Category', 'General')))
        if pref_cat in ['nan', 'None', '', 'General']:
            pref_cat = default_cats[idx % len(default_cats)]
            
        region = str(row.get('Region', 'North'))
        pref_pay = str(row.get('PreferredPaymentMode', row.get('Payment_Method', 'Credit Card')))
        
        sat = int(row.get('SatisfactionScore', row.get('Rating', 4)))
        sat = max(1, min(5, sat))
        complain = int(row.get('Complain', 0))
        
        recency = int(row.get('Recency_Days', row.get('DaySinceLastOrder', 15)))
        last_order_dt = ref_date - pd.Timedelta(days=recency)
        
        for o_idx in range(freq):
            order_id = f"ORD_{hash(cust_id)%100000:05d}_{o_idx+1}"
            # Stagger orders backward
            dt = last_order_dt - pd.Timedelta(days=o_idx * np.random.randint(15, 45))
            cat = pref_cat if (o_idx == 0 or np.random.rand() > 0.4) else default_cats[(idx + o_idx) % len(default_cats)]
            qty = int(np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1]))
            item_spend = max(15.0, round(avg_item_price * (0.8 + 0.4 * np.random.rand()), 2))
            unit_price = round(item_spend / qty, 2)
            profit = round(item_spend * 0.22, 2)
            disc = float(np.random.choice([0.0, 5.0, 10.0, 15.0, 20.0], p=[0.3, 0.25, 0.25, 0.15, 0.05]))
            
            is_ret = 1 if (complain and o_idx == 0) else 0
            
            templates = {
                5: "Excellent quality and fast delivery. Very satisfied!",
                4: "Good product, arrived on time as described.",
                3: "Average item, delivery was slightly delayed.",
                2: "Poor packaging and delayed courier service.",
                1: "Defective item received, customer support was unhelpful."
            }
            rev = templates.get(sat, "Good purchase overall.")
            
            trans_rows.append({
                'Order_ID': order_id,
                'Order_Date': dt.strftime('%Y-%m-%d'),
                'Customer_ID': cust_id,
                'Product_Category': cat,
                'Description': f"{cat} Item #{o_idx+1}",
                'Quantity': qty,
                'Unit_Price': unit_price,
                'Total_Amount': item_spend,
                'Discount_Percent': disc,
                'Profit': profit,
                'Payment_Method': pref_pay,
                'Rating': sat,
                'Review_Text': rev,
                'Is_Returned': is_ret,
                'Region': region
            })
            
    return pd.DataFrame(trans_rows)

# Test with Kaggle Churn
raw_k = pd.read_csv('data/kaggle_export/kaggle_ecommerce_churn_sample_500.csv')
print("Kaggle raw shape:", raw_k.shape)

from src.data_processor import map_kaggle_to_standard
mapped_k = map_kaggle_to_standard(raw_k)
print("Mapped Kaggle shape:", mapped_k.shape)

gen_trans = derive_trans_from_cust(mapped_k)
print("Synthesized transactions shape:", gen_trans.shape)
print("Unique customers in trans:", gen_trans['Customer_ID'].nunique())
print("Categories:", gen_trans['Product_Category'].unique().tolist())
