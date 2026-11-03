"""
Synthetic E-Commerce Data Generator
Generates realistic baseline historical data and new batch data with explainable shifts
for the AI-Powered Business Intelligence and Predictive Analytics platform.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

REGIONS = ['North', 'South', 'East', 'West']
CATEGORIES = ['Electronics', 'Fashion', 'Home & Kitchen', 'Beauty', 'Sports']
PAYMENT_METHODS = ['Credit Card', 'UPI', 'Debit Card', 'Net Banking', 'Cash on Delivery']
MEMBERSHIPS = ['Bronze', 'Silver', 'Gold', 'Platinum']

CATEGORY_PRICES = {
    'Electronics': (50, 800),
    'Fashion': (15, 150),
    'Home & Kitchen': (20, 300),
    'Beauty': (10, 90),
    'Sports': (15, 200)
}

CATEGORY_MARGINS = {
    'Electronics': 0.18,
    'Fashion': 0.40,
    'Home & Kitchen': 0.28,
    'Beauty': 0.45,
    'Sports': 0.32
}

SAMPLE_REVIEWS = {
    5: ["Excellent product, exceeded expectations!", "Super fast delivery and top quality.", "Loved it! Will definitely buy again."],
    4: ["Good quality product, meets expectations.", "Nice value for money, arrived on time.", "Pretty good, minor packaging damage."],
    3: ["Average quality, does the job.", "Decent product but delivery was slightly slow.", "Acceptable for the price point."],
    2: ["Disappointed with the quality.", "Item arrived late and not as pictured.", "Customer support was unhelpful."],
    1: ["Terrible experience, requested refund.", "Broken on arrival, poor customer support.", "Worst purchase ever, do not recommend."]
}

def generate_customers(num_customers=1200, id_offset=1000, high_support_south=False):
    customers = []
    for i in range(num_customers):
        cid = f"CUST_{id_offset + i}"
        age = int(np.random.normal(36, 11))
        age = max(18, min(75, age))
        gender = random.choice(['Male', 'Female', 'Non-Binary'])
        region = random.choice(REGIONS)
        membership = np.random.choice(MEMBERSHIPS, p=[0.45, 0.30, 0.18, 0.07])
        
        # Support calls: if high_support_south, escalate South region calls
        if high_support_south and region == 'South':
            support_calls = int(np.random.poisson(3.8))
        else:
            support_calls = int(np.random.poisson(1.2))
            
        website_visits = int(max(1, np.random.normal(12, 5)))
        
        customers.append({
            'Customer_ID': cid,
            'Age': age,
            'Gender': gender,
            'Region': region,
            'Membership_Type': membership,
            'Customer_Service_Calls': support_calls,
            'Website_Visits_Per_Month': website_visits
        })
    return pd.DataFrame(customers)

def generate_transactions(customer_df, num_transactions=5000, start_date='2025-01-01', end_date='2025-10-31', shift_mode=None):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    days_range = max(1, (end - start).days)

    cust_ids = customer_df['Customer_ID'].values
    records = []

    for i in range(num_transactions):
        order_id = f"ORD_{100000 + i}"
        cust_id = random.choice(cust_ids)
        cust_info = customer_df[customer_df['Customer_ID'] == cust_id].iloc[0]

        # Shift effects for "new batch"
        if shift_mode == 'new_batch':
            if cust_info['Region'] == 'South':
                prob_discount = 0.06
            else:
                prob_discount = 0.14
            category_p = [0.14, 0.24, 0.36, 0.16, 0.10] # Electronics dropped, Home & Kitchen increased
        else:
            prob_discount = 0.12
            category_p = [0.28, 0.25, 0.20, 0.15, 0.12]

        category = np.random.choice(CATEGORIES, p=category_p)
        min_p, max_p = CATEGORY_PRICES[category]
        unit_price = round(np.random.uniform(min_p, max_p), 2)
        quantity = int(np.random.choice([1, 2, 3, 4, 5], p=[0.55, 0.25, 0.12, 0.05, 0.03]))
        
        discount_rate = round(max(0.0, min(0.40, np.random.normal(prob_discount, 0.05))), 2)
        gross_amount = round(unit_price * quantity, 2)
        discount_amount = round(gross_amount * discount_rate, 2)
        total_amount = round(gross_amount - discount_amount, 2)
        
        margin = CATEGORY_MARGINS[category]
        profit = round((total_amount * margin) - (discount_amount * 0.3), 2)
        
        rand_days = random.randint(0, days_range)
        order_date = start + timedelta(days=rand_days)
        payment = random.choice(PAYMENT_METHODS)
        
        # Rating & sentiment
        if shift_mode == 'new_batch' and cust_info['Region'] == 'South':
            rating = int(np.random.choice([1, 2, 3, 4, 5], p=[0.32, 0.28, 0.22, 0.12, 0.06]))
        else:
            rating = int(np.random.choice([1, 2, 3, 4, 5], p=[0.06, 0.11, 0.20, 0.35, 0.28]))
            
        review_text = random.choice(SAMPLE_REVIEWS[rating])
        return_prob = 0.20 if rating <= 2 else 0.04
        is_returned = 1 if np.random.rand() < return_prob else 0

        # Anomaly inject: 1% outlier discounts or transactions
        is_anomaly = 0
        if np.random.rand() < 0.012:
            is_anomaly = 1
            if np.random.rand() > 0.5:
                total_amount = round(total_amount * 4.5, 2)
                profit = round(profit * 3.5, 2)
            else:
                discount_rate = 0.70
                total_amount = round(gross_amount * 0.30, 2)
                profit = round(-1 * gross_amount * 0.25, 2)

        records.append({
            'Order_ID': order_id,
            'Customer_ID': cust_id,
            'Order_Date': order_date.strftime('%Y-%m-%d'),
            'Product_Category': category,
            'Unit_Price': unit_price,
            'Quantity': quantity,
            'Discount_Percent': round(discount_rate * 100, 1),
            'Total_Amount': total_amount,
            'Profit': profit,
            'Payment_Method': payment,
            'Rating': rating,
            'Review_Text': review_text,
            'Is_Returned': is_returned,
            'Is_Anomaly': is_anomaly
        })

    return pd.DataFrame(records)

def create_integrated_dataset(cust_df, trans_df, reference_date):
    """
    Computes Customer-level RFM and churn attributes merged with customer profiles
    """
    ref_dt = datetime.strptime(reference_date, '%Y-%m-%d')
    trans_df['Order_Date_dt'] = pd.to_datetime(trans_df['Order_Date'])
    
    agg = trans_df.groupby('Customer_ID').agg(
        Recency_Days=('Order_Date_dt', lambda dates: (ref_dt - dates.max()).days),
        Frequency_Orders=('Order_ID', 'count'),
        Monetary_Spend=('Total_Amount', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Discount=('Discount_Percent', 'mean'),
        Avg_Rating=('Rating', 'mean'),
        Total_Returns=('Is_Returned', 'sum')
    ).reset_index()

    agg['Recency_Days'] = agg['Recency_Days'].apply(lambda x: max(1, x))
    agg['Avg_Order_Value'] = round(agg['Monetary_Spend'] / agg['Frequency_Orders'], 2)
    agg['Return_Rate'] = round((agg['Total_Returns'] / agg['Frequency_Orders']) * 100, 2)
    agg['Avg_Discount'] = round(agg['Avg_Discount'], 2)
    agg['Avg_Rating'] = round(agg['Avg_Rating'], 2)

    merged = pd.merge(cust_df, agg, on='Customer_ID', how='inner')
    
    # Realistic Churn Function: multi-factor behavioral
    def calculate_churn_prob(row):
        score = 0.08
        if row['Customer_Service_Calls'] >= 4:
            score += 0.45
        elif row['Customer_Service_Calls'] >= 2:
            score += 0.20
            
        if row['Recency_Days'] > 90:
            score += 0.35
        elif row['Recency_Days'] > 45:
            score += 0.15
            
        if row['Avg_Rating'] < 2.5:
            score += 0.25
        elif row['Avg_Rating'] < 3.2:
            score += 0.10
            
        if row['Return_Rate'] > 20:
            score += 0.15
            
        if row['Membership_Type'] in ['Gold', 'Platinum']:
            score -= 0.15
            
        return max(0.02, min(0.95, score))

    merged['Churn_Probability'] = merged.apply(calculate_churn_prob, axis=1)
    merged['Churn'] = (merged['Churn_Probability'] >= 0.45).astype(int)

    full_dataset = pd.merge(
        trans_df.drop(columns=['Order_Date_dt']),
        merged[['Customer_ID', 'Age', 'Gender', 'Region', 'Membership_Type', 'Customer_Service_Calls', 'Website_Visits_Per_Month', 'Recency_Days', 'Frequency_Orders', 'Avg_Order_Value', 'Return_Rate', 'Churn']],
        on='Customer_ID',
        how='left'
    )
    
    return merged, full_dataset

def generate_and_save_data(output_dir='data'):
    os.makedirs(output_dir, exist_ok=True)
    
    print("[1/3] Generating Baseline Historical Data (10-Month Timeline)...")
    base_customers = generate_customers(num_customers=1200, id_offset=1000, high_support_south=False)
    base_trans = generate_transactions(base_customers, num_transactions=6000, start_date='2025-01-01', end_date='2025-10-31', shift_mode='baseline')
    base_cust_agg, base_full = create_integrated_dataset(base_customers, base_trans, reference_date='2025-11-01')
    
    base_full.to_csv(os.path.join(output_dir, 'historical_ecommerce_data.csv'), index=False)
    base_cust_agg.to_csv(os.path.join(output_dir, 'historical_customer_profiles.csv'), index=False)
    print(f"Historical Baseline Data saved: {len(base_full)} transactions, {len(base_cust_agg)} customers.")
    
    print("[2/3] Generating New Incoming Batch with Market Shifts (Timeline through Dec 2025)...")
    # For new batch, customers are evaluated as of end of year 2025-12-31 with support escalation in South
    new_customers = generate_customers(num_customers=700, id_offset=2000, high_support_south=True)
    new_trans = generate_transactions(new_customers, num_transactions=3000, start_date='2025-06-01', end_date='2025-12-31', shift_mode='new_batch')
    new_cust_agg, new_full = create_integrated_dataset(new_customers, new_trans, reference_date='2026-01-01')
    
    new_full.to_csv(os.path.join(output_dir, 'new_batch_ecommerce_data.csv'), index=False)
    new_cust_agg.to_csv(os.path.join(output_dir, 'new_batch_customer_profiles.csv'), index=False)
    print(f"New Batch Data saved: {len(new_full)} transactions, {len(new_cust_agg)} customers.")
    
    print("[3/3] Saving Demo Single Record Payload for Interactive What-If Tool...")
    demo_record = {
        "Customer_ID": "CUST_TEST_999",
        "Age": 38,
        "Gender": "Female",
        "Region": "South",
        "Membership_Type": "Silver",
        "Customer_Service_Calls": 4,
        "Website_Visits_Per_Month": 8,
        "Recency_Days": 75,
        "Frequency_Orders": 3,
        "Avg_Order_Value": 145.50,
        "Return_Rate": 15.0
    }
    pd.DataFrame([demo_record]).to_csv(os.path.join(output_dir, 'sample_single_customer.csv'), index=False)
    print("All datasets generated successfully!")

if __name__ == '__main__':
    generate_and_save_data('c:/Users/Nandhupriya/BI PROJECT/data')
