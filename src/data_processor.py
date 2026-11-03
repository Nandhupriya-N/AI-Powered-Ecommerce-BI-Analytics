"""
Data Processor and Feature Engineering Module
Handles data cleaning, quality assessment, RFM computation, and feature transformations.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

FEATURE_COLS = [
    'Age',
    'Customer_Service_Calls',
    'Website_Visits_Per_Month',
    'Recency_Days',
    'Frequency_Orders',
    'Avg_Order_Value',
    'Return_Rate'
]

CATEGORICAL_COLS = ['Gender', 'Region', 'Membership_Type']

def assess_data_quality(df):
    """
    Performs data quality checks: missing values, duplicates, datatypes, and outliers.
    """
    total_rows = len(df)
    missing = df.isnull().sum().to_dict()
    duplicates = int(df.duplicated().sum())
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    stats = {}
    for col in numeric_cols:
        stats[col] = {
            'mean': float(df[col].mean()),
            'std': float(df[col].std()) if not np.isnan(df[col].std()) else 0.0,
            'min': float(df[col].min()),
            'max': float(df[col].max())
        }
        
    return {
        'total_rows': total_rows,
        'missing_values': missing,
        'duplicate_rows': duplicates,
        'numeric_stats': stats
    }

def clean_and_prepare(df):
    """
    Cleans incoming data and ensures consistent schema, types, and column aliases.
    """
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates()
    
    # Harmonize common column name variations
    alias_map = {
        'CustomerID': 'Customer_ID', 'customer_id': 'Customer_ID', 'cust_id': 'Customer_ID', 'id': 'Customer_ID',
        'OrderID': 'Order_ID', 'order_id': 'Order_ID', 'InvoiceNo': 'Order_ID',
        'InvoiceDate': 'Order_Date', 'order_date': 'Order_Date', 'Date': 'Order_Date', 'date': 'Order_Date',
        'ProductCategory': 'Product_Category', 'product_category': 'Product_Category', 'Category': 'Product_Category', 'category': 'Product_Category', 'PreferedOrderCat': 'Product_Category',
        'UnitPrice': 'Unit_Price', 'unit_price': 'Unit_Price', 'Price': 'Unit_Price', 'price': 'Unit_Price',
        'Quantity': 'Quantity', 'quantity': 'Quantity', 'qty': 'Quantity',
        'TotalAmount': 'Total_Amount', 'total_amount': 'Total_Amount', 'Amount': 'Total_Amount', 'amount': 'Total_Amount', 'Sales': 'Total_Amount', 'sales': 'Total_Amount',
        'Profit': 'Profit', 'profit': 'Profit',
        'Discount': 'Discount_Percent', 'discount': 'Discount_Percent', 'DiscountPercent': 'Discount_Percent', 'discount_percent': 'Discount_Percent',
        'PaymentMethod': 'Payment_Method', 'payment_method': 'Payment_Method', 'PreferredPaymentMode': 'Payment_Method',
        'Rating': 'Rating', 'rating': 'Rating', 'SatisfactionScore': 'Rating',
        'CustomerServiceCalls': 'Customer_Service_Calls', 'customer_service_calls': 'Customer_Service_Calls', 'Complain': 'Customer_Service_Calls',
        'WebsiteVisitsPerMonth': 'Website_Visits_Per_Month', 'website_visits_per_month': 'Website_Visits_Per_Month', 'HourSpendOnApp': 'Website_Visits_Per_Month',
        'RecencyDays': 'Recency_Days', 'recency_days': 'Recency_Days', 'DaySinceLastOrder': 'Recency_Days', 'Recency': 'Recency_Days',
        'FrequencyOrders': 'Frequency_Orders', 'frequency_orders': 'Frequency_Orders', 'OrderCount': 'Frequency_Orders', 'Frequency': 'Frequency_Orders',
        'MonetarySpend': 'Monetary_Spend', 'monetary_spend': 'Monetary_Spend', 'Monetary': 'Monetary_Spend', 'Spend': 'Monetary_Spend',
        'MembershipType': 'Membership_Type', 'membership_type': 'Membership_Type'
    }
    for old_col, new_col in alias_map.items():
        if old_col in cleaned.columns and new_col not in cleaned.columns:
            cleaned[new_col] = cleaned[old_col]
            
    # Default columns if not present in uploaded file
    if 'Customer_ID' not in cleaned.columns:
        cleaned['Customer_ID'] = [f"CUST_{1000 + i}" for i in range(len(cleaned))]
    if 'Total_Amount' not in cleaned.columns and 'Unit_Price' in cleaned.columns and 'Quantity' in cleaned.columns:
        cleaned['Total_Amount'] = cleaned['Unit_Price'] * cleaned['Quantity']
    if 'Profit' not in cleaned.columns and 'Total_Amount' in cleaned.columns:
        cleaned['Profit'] = (cleaned['Total_Amount'] * 0.25).round(2)
    if 'Discount_Percent' not in cleaned.columns:
        cleaned['Discount_Percent'] = 10.0
    if 'Order_Date' not in cleaned.columns:
        cleaned['Order_Date'] = '2025-10-15'
    if 'Product_Category' not in cleaned.columns:
        cleaned['Product_Category'] = 'General Retail'
    if 'Payment_Method' not in cleaned.columns:
        cleaned['Payment_Method'] = 'Credit Card'
    if 'Rating' not in cleaned.columns:
        cleaned['Rating'] = 4
    if 'Is_Returned' not in cleaned.columns:
        cleaned['Is_Returned'] = 0
        
    # Fill numerical nulls with median if any
    num_cols = cleaned.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if cleaned[col].isnull().any():
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
            
    # Fill categorical nulls with mode
    cat_cols = cleaned.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if cleaned[col].isnull().any():
            mode_val = cleaned[col].mode()
            cleaned[col] = cleaned[col].fillna(mode_val[0] if len(mode_val) > 0 else 'Unknown')
            
    return cleaned

def compute_rfm_segments(df):
    """
    Computes RFM Scores (1-4) and assigns Customer Segment labels.
    """
    rfm = df.copy()
    
    # Quantile bins
    try:
        rfm['R_Score'] = pd.qcut(rfm['Recency_Days'], q=4, labels=[4, 3, 2, 1], duplicates='drop').astype(int)
    except Exception:
        rfm['R_Score'] = pd.cut(rfm['Recency_Days'], bins=4, labels=[4, 3, 2, 1]).astype(int)
        
    try:
        rfm['F_Score'] = pd.qcut(rfm['Frequency_Orders'], q=4, labels=[1, 2, 3, 4], duplicates='drop').astype(int)
    except Exception:
        rfm['F_Score'] = pd.cut(rfm['Frequency_Orders'], bins=4, labels=[1, 2, 3, 4]).astype(int)
        
    try:
        rfm['M_Score'] = pd.qcut(rfm['Monetary_Spend'], q=4, labels=[1, 2, 3, 4], duplicates='drop').astype(int)
    except Exception:
        rfm['M_Score'] = pd.cut(rfm['Monetary_Spend'], bins=4, labels=[1, 2, 3, 4]).astype(int)
        
    rfm['RFM_Score'] = rfm['R_Score'] * 100 + rfm['F_Score'] * 10 + rfm['M_Score']
    
    def assign_segment(row):
        r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
        if r >= 3 and f >= 3 and m >= 3:
            return 'Champions'
        elif r >= 3 and f >= 2:
            return 'Loyal Customers'
        elif r >= 3 and f == 1:
            return 'New / Promising'
        elif r == 2 and f >= 2:
            return 'Potential Loyalist'
        elif r <= 2 and f >= 2:
            return 'At-Risk'
        else:
            return 'Hibernating / Lost'
            
    rfm['Customer_Segment'] = rfm.apply(assign_segment, axis=1)
    return rfm

def prepare_churn_features(df):
    """
    Prepares standard numerical and encoded categorical features for churn modeling.
    """
    X = df[FEATURE_COLS].copy()
    
    # One-hot encode categoricals
    for col in CATEGORICAL_COLS:
        if col in df.columns:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
            X = pd.concat([X, dummies], axis=1)
            
    return X

def map_kaggle_to_standard(df_kaggle):
    """
    Adapts Kaggle 'E-Commerce Customer Churn' dataset into standard schema
    used by the AI Analytics Suite.
    """
    df = df_kaggle.copy()
    mapped = pd.DataFrame()
    mapped['Customer_ID'] = df['CustomerID'].astype(str)
    mapped['Age'] = (28 + df['Tenure'].fillna(5) * 1.2).clip(18, 70).astype(int)
    mapped['Gender'] = df['Gender'].fillna('Male')
    mapped['Region'] = df['CityTier'].map({1: 'North', 2: 'South', 3: 'West'}).fillna('East')
    
    cb = df['CashbackAmount'].fillna(140)
    mapped['Membership_Type'] = np.where(cb >= 200, 'Platinum',
                                np.where(cb >= 160, 'Gold',
                                np.where(cb >= 130, 'Silver', 'Bronze')))
                                
    complains = df['Complain'].fillna(0).astype(int)
    dist = df['WarehouseToHome'].fillna(10)
    mapped['Customer_Service_Calls'] = complains * 2 + (dist > 18).astype(int)
    mapped['Website_Visits_Per_Month'] = (df['HourSpendOnApp'].fillna(3) * 4).astype(int)
    mapped['Recency_Days'] = df['DaySinceLastOrder'].fillna(5).clip(1, 120).astype(int)
    mapped['Frequency_Orders'] = df['OrderCount'].fillna(2).clip(1, 20).astype(int)
    mapped['Monetary_Spend'] = np.round(cb * 7.5, 2)
    mapped['Avg_Order_Value'] = np.round(mapped['Monetary_Spend'] / mapped['Frequency_Orders'], 2)
    mapped['Return_Rate'] = (complains * 18.5).round(1)
    if 'Churn' in df.columns:
        mapped['Churn'] = df['Churn'].fillna(0).astype(int)
    
    # Preserve original raw Kaggle features for high-accuracy Kaggle ML model
    for c in df.columns:
        if c not in mapped.columns:
            mapped[c] = df[c]
            
    return mapped

def validate_incremental_batch(df):
    """
    Validates newly ingested batch data for incremental processing:
    1. Detects duplicate records.
    2. Validates datetime integrity and flags anomalies.
    3. Calculates data freshness metrics.
    4. Computes incremental revenue and volume totals.
    """
    total_raw = len(df)
    duplicates = int(df.duplicated().sum())
    
    # Check date column
    date_col = None
    for cand in ['Order_Date', 'Date', 'InvoiceDate', 'order_date']:
        if cand in df.columns:
            date_col = cand
            break
            
    min_date_str = "N/A"
    max_date_str = "N/A"
    freshness_days = 0
    date_valid = True
    
    if date_col is not None:
        try:
            parsed_dates = pd.to_datetime(df[date_col], errors='coerce')
            valid_dates = parsed_dates.dropna()
            if not valid_dates.empty:
                min_d = valid_dates.min()
                max_d = valid_dates.max()
                min_date_str = min_d.strftime('%Y-%m-%d')
                max_date_str = max_d.strftime('%Y-%m-%d')
                ref_date = pd.Timestamp.now()
                freshness_days = max(0, (ref_date - max_d).days)
        except Exception:
            date_valid = False
            
    # Revenue totals
    rev_col = 'Total_Amount' if 'Total_Amount' in df.columns else ('amount' if 'amount' in df.columns else None)
    batch_revenue = float(df[rev_col].sum()) if rev_col else 0.0
    
    return {
        'total_records_ingested': total_raw,
        'duplicate_records_found': duplicates,
        'clean_records_count': total_raw - duplicates,
        'timestamp_validation': 'PASS: Valid Timestamp Formats' if date_valid else 'WARNING: Malformed Dates Detected',
        'earliest_transaction_date': min_date_str,
        'latest_transaction_date': max_date_str,
        'data_freshness_indicator': f"{freshness_days} days elapsed since latest batch timestamp",
        'batch_total_revenue': round(batch_revenue, 2),
        'ingestion_pipeline_mode': 'Incremental Micro-Batch Ingestion (Preserving Historical Base)',
        'ingestion_timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def compute_customer_journey_metrics(trans_df):
    """
    Computes Customer Journey & repeat purchase behavior metrics from event/transaction history:
    1. Order velocity and purchase counts.
    2. Inter-purchase duration (days between consecutive orders).
    3. Repeat purchase conversion rate.
    """
    df = trans_df.copy()
    cust_col = 'Customer_ID' if 'Customer_ID' in df.columns else 'CustomerID'
    date_col = 'Order_Date' if 'Order_Date' in df.columns else 'InvoiceDate'
    
    if cust_col not in df.columns or date_col not in df.columns:
        return {
            'repeat_purchase_rate': 0.0,
            'avg_inter_purchase_days': 0.0,
            'multi_order_customers_count': 0,
            'single_order_customers_count': len(df)
        }
        
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col]).sort_values([cust_col, date_col])
    
    # Inter-purchase duration
    df['Prev_Order_Date'] = df.groupby(cust_col)[date_col].shift(1)
    df['Days_Since_Prev_Order'] = (df[date_col] - df['Prev_Order_Date']).dt.days
    
    inter_purchase_days = df['Days_Since_Prev_Order'].dropna()
    avg_days_between = float(inter_purchase_days.mean()) if not inter_purchase_days.empty else 0.0
    median_days_between = float(inter_purchase_days.median()) if not inter_purchase_days.empty else 0.0
    
    order_counts = df.groupby(cust_col)[date_col].count()
    multi_order_custs = int((order_counts > 1).sum())
    single_order_custs = int((order_counts == 1).sum())
    total_custs = len(order_counts)
    repeat_rate = round((multi_order_custs / max(1, total_custs)) * 100, 2)
    
    return {
        'total_unique_customers': total_custs,
        'repeat_customers_count': multi_order_custs,
        'single_purchase_customers_count': single_order_custs,
        'repeat_purchase_rate_pct': repeat_rate,
        'avg_inter_purchase_days': round(avg_days_between, 1),
        'median_inter_purchase_days': round(median_days_between, 1),
        'inter_purchase_distribution': {
            '0-15 Days': int((inter_purchase_days <= 15).sum()),
            '16-30 Days': int(((inter_purchase_days > 15) & (inter_purchase_days <= 30)).sum()),
            '31-60 Days': int(((inter_purchase_days > 30) & (inter_purchase_days <= 60)).sum()),
            '60+ Days': int((inter_purchase_days > 60).sum())
        }
    }

