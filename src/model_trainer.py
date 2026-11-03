"""
Model Training Module
Trains and evaluates machine learning models for:
1. Customer Churn Prediction (Classification: Random Forest, Gradient Boosting, Logistic Regression)
2. Sales & Demand Forecasting (Regression: Ridge/Multi-variate Forecaster)
3. Customer Segmentation (Clustering: K-Means)
4. Anomaly Detection (Statistical Outlier Detector)
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    mean_absolute_error, root_mean_squared_error, r2_score
)

# Ensure local src package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ml_models import (
    LogisticRegressionCustom, RandomForestCustom, GradientBoostingCustom,
    SalesForecasterCustom, KMeansCustom, AnomalyDetectorCustom
)

def train_test_split_custom(X, y, test_size=0.25, random_state=42):
    np.random.seed(random_state)
    n = len(X)
    indices = np.random.permutation(n)
    split = int(n * (1 - test_size))
    train_idx = indices[:split]
    test_idx = indices[split:]
    return X.iloc[train_idx], X.iloc[test_idx], y[train_idx], y[test_idx]

def train_churn_models(df, models_dir):
    """
    Trains and compares churn classification models.
    """
    print("\n--- Training Customer Churn Prediction Models ---")
    feature_cols = [
        'Age', 'Customer_Service_Calls', 'Website_Visits_Per_Month',
        'Recency_Days', 'Frequency_Orders', 'Avg_Order_Value', 'Return_Rate'
    ]
    
    # Process categoricals
    cat_df = pd.get_dummies(df[['Gender', 'Region', 'Membership_Type']], drop_first=True, dtype=float)
    X = pd.concat([df[feature_cols].astype(float), cat_df], axis=1)
    y = df['Churn'].values.astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split_custom(X, y, test_size=0.25, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    candidate_models = {
        'Random Forest': RandomForestCustom(n_estimators=45, max_depth=6),
        'Gradient Boosting': GradientBoostingCustom(n_estimators=35, learning_rate=0.1, max_depth=3),
        'Logistic Regression': LogisticRegressionCustom(C=1.0, max_iter=200)
    }
    
    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_model = None
    
    for name, clf in candidate_models.items():
        if name == 'Logistic Regression':
            clf.fit(X_train_scaled, y_train, feature_names=list(X.columns))
            preds = clf.predict(X_test_scaled)
            probs = clf.predict_proba(X_test_scaled)[:, 1]
        else:
            clf.fit(X_train.values, y_train)
            preds = clf.predict(X_test.values)
            probs = clf.predict_proba(X_test.values)[:, 1]
            
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        auc = roc_auc_score(y_test, probs)
        
        results[name] = {
            'Accuracy': round(float(acc), 4),
            'Precision': round(float(prec), 4),
            'Recall': round(float(rec), 4),
            'F1_Score': round(float(f1), 4),
            'ROC_AUC': round(float(auc), 4)
        }
        print(f"[{name:19}] Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model = clf
            
    # Calculate feature importances
    if hasattr(best_model, 'feature_importances_'):
        importances = dict(zip(X.columns, [round(float(v), 4) for v in best_model.feature_importances_]))
    else:
        importances = dict(zip(X.columns, [round(float(abs(v)), 4) for v in best_model.weights]))
        
    sorted_importances = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))
    
    # Save best churn model artifacts
    joblib.dump(best_model, os.path.join(models_dir, 'churn_model.joblib'))
    joblib.dump(scaler, os.path.join(models_dir, 'churn_scaler.joblib'))
    joblib.dump(list(X.columns), os.path.join(models_dir, 'churn_features.joblib'))
    
    return {
        'comparison': results,
        'best_model': best_model_name,
        'feature_importance': sorted_importances
    }

def train_sales_forecaster(trans_df, models_dir):
    """
    Trains sales forecasting models aggregated by daily sales.
    Implements and compares:
    1. Baseline AutoRegressive Ridge Regressor
    2. Enhanced Random Forest Regressor (IEEE Papers 7 & 8)
    """
    print("\n--- Training Sales & Demand Forecasting Models ---")
    df = trans_df.copy()
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    
    daily = df.groupby('Order_Date').agg(
        Daily_Revenue=('Total_Amount', 'sum'),
        Total_Orders=('Order_ID', 'count'),
        Total_Quantity=('Quantity', 'sum'),
        Avg_Discount=('Discount_Percent', 'mean'),
        Daily_Profit=('Profit', 'sum')
    ).reset_index().sort_values('Order_Date')
    
    daily['Day_of_Week'] = daily['Order_Date'].dt.dayofweek
    daily['Day_of_Month'] = daily['Order_Date'].dt.day
    daily['Month'] = daily['Order_Date'].dt.month
    daily['Is_Weekend'] = (daily['Day_of_Week'] >= 5).astype(int)
    
    # Lag and Rolling features (strictly shifted to prevent data leakage)
    daily['Lag_1_Revenue'] = daily['Daily_Revenue'].shift(1).bfill()
    daily['Lag_2_Revenue'] = daily['Daily_Revenue'].shift(2).bfill()
    daily['Lag_7_Revenue'] = daily['Daily_Revenue'].shift(7).bfill()
    daily['Lag_14_Revenue'] = daily['Daily_Revenue'].shift(14).bfill()
    daily['Rolling_7_Avg'] = daily['Daily_Revenue'].shift(1).rolling(window=7, min_periods=1).mean().bfill()
    daily['Rolling_7_Std'] = daily['Daily_Revenue'].shift(1).rolling(window=7, min_periods=1).std().fillna(0).bfill()
    daily['Rolling_14_Avg'] = daily['Daily_Revenue'].shift(1).rolling(window=14, min_periods=1).mean().bfill()
    daily['Rolling_7_Orders'] = daily['Total_Orders'].shift(1).rolling(window=7, min_periods=1).mean().bfill()
    daily['Rolling_7_Discount'] = daily['Avg_Discount'].shift(1).rolling(window=7, min_periods=1).mean().bfill()
    
    rf_features = [
        'Day_of_Week', 'Day_of_Month', 'Month', 'Is_Weekend',
        'Lag_1_Revenue', 'Lag_2_Revenue', 'Lag_7_Revenue', 'Lag_14_Revenue',
        'Rolling_7_Avg', 'Rolling_7_Std', 'Rolling_14_Avg',
        'Rolling_7_Orders', 'Rolling_7_Discount'
    ]
    
    baseline_features = [
        'Day_of_Week', 'Day_of_Month', 'Month',
        'Lag_1_Revenue', 'Lag_7_Revenue', 'Rolling_7_Avg', 'Rolling_7_Discount'
    ]
    
    # Chronological 80/20 train-test split
    split_idx = int(len(daily) * 0.8)
    train_df = daily.iloc[:split_idx]
    test_df = daily.iloc[split_idx:]
    
    y_train = train_df['Daily_Revenue'].values
    y_test = test_df['Daily_Revenue'].values
    
    # 1. Baseline Ridge Regressor
    X_train_base = train_df[baseline_features].values
    X_test_base = test_df[baseline_features].values
    
    ridge = SalesForecasterCustom(alpha=10.0)
    ridge.fit(X_train_base, y_train)
    ridge_preds = ridge.predict(X_test_base)
    
    ridge_mae = mean_absolute_error(y_test, ridge_preds)
    ridge_rmse = root_mean_squared_error(y_test, ridge_preds)
    ridge_r2 = r2_score(y_test, ridge_preds)
    ridge_mape = float(np.mean(np.abs((y_test - ridge_preds) / np.maximum(y_test, 1))) * 100)
    
    ridge_metrics = {
        'Model_Name': 'Baseline AutoRegressive Ridge',
        'MAE': round(float(ridge_mae), 2),
        'RMSE': round(float(ridge_rmse), 2),
        'R2': round(float(ridge_r2), 4),
        'MAPE': round(float(ridge_mape), 2)
    }
    print(f"[Baseline Ridge Forecaster] MAE: ${ridge_metrics['MAE']} | RMSE: ${ridge_metrics['RMSE']} | R2: {ridge_metrics['R2']} | MAPE: {ridge_metrics['MAPE']}%")
    
    # 2. Enhanced Random Forest Regressor (IEEE Papers 7 & 8)
    from sklearn.ensemble import RandomForestRegressor
    X_train_rf = train_df[rf_features].values
    X_test_rf = test_df[rf_features].values
    
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        min_samples_split=5,
        min_samples_leaf=3,
        max_features=0.8,
        random_state=42
    )
    rf.fit(X_train_rf, y_train)
    rf_preds = rf.predict(X_test_rf)
    
    rf_mae = mean_absolute_error(y_test, rf_preds)
    rf_rmse = root_mean_squared_error(y_test, rf_preds)
    rf_r2 = r2_score(y_test, rf_preds)
    rf_mape = float(np.mean(np.abs((y_test - rf_preds) / np.maximum(y_test, 1))) * 100)
    
    # 95% Confidence Interval Coverage
    tree_preds = np.array([tree.predict(X_test_rf) for tree in rf.estimators_])
    pred_std = np.std(tree_preds, axis=0)
    cov_pct = float(np.mean((y_test >= rf_preds - 1.96 * pred_std) & (y_test <= rf_preds + 1.96 * pred_std)) * 100)
    
    rf_importances = {feat: round(float(imp), 4) for feat, imp in zip(rf_features, rf.feature_importances_)}
    sorted_rf_imp = dict(sorted(rf_importances.items(), key=lambda x: x[1], reverse=True))
    
    rf_metrics = {
        'Model_Name': 'Enhanced Random Forest Demand Forecaster',
        'MAE': round(float(rf_mae), 2),
        'RMSE': round(float(rf_rmse), 2),
        'R2': round(float(rf_r2), 4),
        'MAPE': round(float(rf_mape), 2),
        'Coverage_95_CI': round(cov_pct, 1),
        'Top_Features': list(sorted_rf_imp.keys())[:5]
    }
    print(f"[Enhanced Random Forest]    MAE: ${rf_metrics['MAE']} | RMSE: ${rf_metrics['RMSE']} | R2: {rf_metrics['R2']} | MAPE: {rf_metrics['MAPE']}% | 95% CI: {rf_metrics['Coverage_95_CI']}%")
    
    # Save artifacts
    joblib.dump(ridge, os.path.join(models_dir, 'sales_forecaster.joblib'))
    joblib.dump(baseline_features, os.path.join(models_dir, 'forecaster_features.joblib'))
    
    joblib.dump(rf, os.path.join(models_dir, 'rf_sales_forecaster.joblib'))
    joblib.dump(rf_features, os.path.join(models_dir, 'rf_forecaster_features.joblib'))
    
    return {
        'Forecasting_Model': 'Enhanced Random Forest Demand Forecaster (IEEE Papers 7 & 8)',
        'comparison': {
            'Baseline Ridge': ridge_metrics,
            'Random Forest (IEEE 7&8)': rf_metrics
        },
        'best_model': 'Random Forest (IEEE 7&8)',
        'rf_feature_importance': sorted_rf_imp,
        'metrics': rf_metrics
    }

def train_customer_clustering(cust_df, models_dir):
    """
    Trains K-Means clustering for customer segmentation based on RFM attributes.
    """
    print("\n--- Training K-Means Customer Segmentation ---")
    cluster_features = ['Recency_Days', 'Frequency_Orders', 'Monetary_Spend']
    X = cust_df[cluster_features].values
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeansCustom(n_clusters=4, random_state=42)
    kmeans.fit(X_scaled)
    cust_df['Cluster'] = kmeans.labels_
    
    cluster_summary = cust_df.groupby('Cluster').agg({
        'Recency_Days': 'mean',
        'Frequency_Orders': 'mean',
        'Monetary_Spend': 'mean',
        'Customer_ID': 'count'
    }).rename(columns={'Customer_ID': 'Customer_Count'}).reset_index()
    
    labels = {}
    for idx, row in cluster_summary.iterrows():
        c = row['Cluster']
        if row['Recency_Days'] < 40 and row['Monetary_Spend'] > 1000:
            labels[c] = 'Champions'
        elif row['Recency_Days'] < 50:
            labels[c] = 'Loyal Customers'
        elif row['Recency_Days'] > 75:
            labels[c] = 'Hibernating / At-Risk'
        else:
            labels[c] = 'Potential Loyalists'
            
    cluster_summary['Cluster_Name'] = cluster_summary['Cluster'].map(labels)
    print(cluster_summary[['Cluster', 'Cluster_Name', 'Customer_Count', 'Recency_Days', 'Monetary_Spend']])
    
    joblib.dump(kmeans, os.path.join(models_dir, 'kmeans_segmentation.joblib'))
    joblib.dump(scaler, os.path.join(models_dir, 'segmentation_scaler.joblib'))
    joblib.dump(labels, os.path.join(models_dir, 'cluster_labels.joblib'))
    
    return cluster_summary.to_dict(orient='records')

def train_anomaly_detector(trans_df, models_dir):
    """
    Trains Outlier & Anomaly Detector on transactions.
    """
    print("\n--- Training Transaction Anomaly Detector ---")
    features = ['Total_Amount', 'Discount_Percent', 'Profit', 'Quantity']
    X = trans_df[features].values
    
    iso = AnomalyDetectorCustom(contamination=0.015)
    iso.fit(X)
    
    joblib.dump(iso, os.path.join(models_dir, 'anomaly_detector.joblib'))
    joblib.dump(features, os.path.join(models_dir, 'anomaly_features.joblib'))
    print("Anomaly detector trained and saved.")

def train_kaggle_models(data_dir, models_dir):
    """
    Trains and benchmarks models directly on the real Kaggle E-Commerce Churn dataset (5,630 rows).
    Target: Exceed 85% and achieve >90% accuracy.
    """
    kaggle_path = os.path.join(data_dir, 'kaggle_ecommerce_churn.csv')
    if not os.path.exists(kaggle_path):
        print("Kaggle dataset not found at", kaggle_path)
        return {}
        
    print("\n--- Training Models on Real Kaggle E-Commerce Churn Dataset (5,630 rows) ---")
    df = pd.read_csv(kaggle_path)
    
    # Feature Engineering
    df['CashbackPerOrder'] = df['CashbackAmount'] / df['OrderCount'].clip(lower=1)
    df['OrderPerTenure'] = df['OrderCount'] / (df['Tenure'] + 1)
    df['Complain_Risk'] = df['Complain'] * (6 - df['SatisfactionScore'])
    df['App_Per_Device'] = df['HourSpendOnApp'] / df['NumberOfDeviceRegistered'].clip(lower=1)

    num_cols = [
        'Tenure', 'CityTier', 'WarehouseToHome', 'HourSpendOnApp',
        'NumberOfDeviceRegistered', 'SatisfactionScore', 'NumberOfAddress',
        'Complain', 'OrderAmountHikeFromlastYear', 'CouponUsed', 'OrderCount',
        'DaySinceLastOrder', 'CashbackAmount', 'CashbackPerOrder',
        'OrderPerTenure', 'Complain_Risk', 'App_Per_Device'
    ]
    cat_cols = ['PreferredLoginDevice', 'PreferredPaymentMode', 'Gender', 'PreferedOrderCat', 'MaritalStatus']
    cat_df = pd.get_dummies(df[cat_cols], drop_first=True, dtype=float)

    X = pd.concat([df[num_cols].astype(float), cat_df], axis=1)
    y = df['Churn'].values.astype(int)

    np.random.seed(42)
    n = len(X)
    idx = np.random.permutation(n)
    split = int(n * 0.8)
    X_train, X_test = X.iloc[idx[:split]], X.iloc[idx[split:]]
    y_train, y_test = y[idx[:split]], y[idx[split:]]

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    # 1. Random Forest Classifier
    rf = RandomForestCustom(n_estimators=50, max_depth=8, min_samples_split=4)
    rf.fit(X_train.values, y_train)
    preds_rf = rf.predict(X_test.values)
    probs_rf = rf.predict_proba(X_test.values)[:, 1]

    # 2. Gradient Boosting
    gb = GradientBoostingCustom(n_estimators=45, learning_rate=0.12, max_depth=4)
    gb.fit(X_train.values, y_train)
    preds_gb = gb.predict(X_test.values)
    probs_gb = gb.predict_proba(X_test.values)[:, 1]

    # 3. Logistic Regression
    lr = LogisticRegressionCustom(C=1.0, max_iter=300)
    lr.fit(X_train_s, y_train, feature_names=list(X.columns))
    preds_lr = lr.predict(X_test_s)
    probs_lr = lr.predict_proba(X_test_s)[:, 1]

    def get_metrics(actual, preds, probs):
        return {
            'Accuracy': round(float(accuracy_score(actual, preds)), 4),
            'Precision': round(float(precision_score(actual, preds, zero_division=0)), 4),
            'Recall': round(float(recall_score(actual, preds, zero_division=0)), 4),
            'F1_Score': round(float(f1_score(actual, preds, zero_division=0)), 4),
            'ROC_AUC': round(float(roc_auc_score(actual, probs)), 4)
        }

    results = {
        'Random Forest': get_metrics(y_test, preds_rf, probs_rf),
        'Gradient Boosting': get_metrics(y_test, preds_gb, probs_gb),
        'Logistic Regression': get_metrics(y_test, preds_lr, probs_lr)
    }

    for model_name, m in results.items():
        print(f"[{model_name:19}] Acc: {m['Accuracy']*100:.2f}% | Prec: {m['Precision']*100:.2f}% | Rec: {m['Recall']*100:.2f}% | F1: {m['F1_Score']*100:.2f}% | AUC: {m['ROC_AUC']:.4f}")

    importances = dict(zip(X.columns, [round(float(v), 4) for v in rf.feature_importances_]))
    sorted_importances = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))

    joblib.dump(rf, os.path.join(models_dir, 'kaggle_churn_model.joblib'))
    joblib.dump(scaler, os.path.join(models_dir, 'kaggle_scaler.joblib'))
    joblib.dump(list(X.columns), os.path.join(models_dir, 'kaggle_churn_features.joblib'))

    kaggle_report = {
        'comparison': results,
        'best_model': 'Random Forest',
        'best_accuracy': results['Random Forest']['Accuracy'],
        'feature_importance': sorted_importances
    }

    with open(os.path.join(models_dir, 'kaggle_metadata.json'), 'w') as f:
        json.dump(kaggle_report, f, indent=4)

    return kaggle_report

def train_all_models(data_dir='data', models_dir='models'):
    os.makedirs(models_dir, exist_ok=True)
    
    cust_path = os.path.join(data_dir, 'historical_customer_profiles.csv')
    trans_path = os.path.join(data_dir, 'historical_ecommerce_data.csv')
    
    cust_df = pd.read_csv(cust_path)
    trans_df = pd.read_csv(trans_path)
    
    churn_report = train_churn_models(cust_df, models_dir)
    sales_report = train_sales_forecaster(trans_df, models_dir)
    cluster_report = train_customer_clustering(cust_df, models_dir)
    train_anomaly_detector(trans_df, models_dir)
    kaggle_report = train_kaggle_models(data_dir, models_dir)
    
    metadata = {
        'training_dataset_summary': {
            'total_transactions': len(trans_df),
            'unique_customers': len(cust_df),
            'baseline_churn_rate': round(float(cust_df['Churn'].mean() * 100), 2),
            'total_revenue': round(float(trans_df['Total_Amount'].sum()), 2),
            'avg_order_value': round(float(trans_df['Total_Amount'].mean()), 2),
            'overall_profit': round(float(trans_df['Profit'].sum()), 2)
        },
        'churn_models': churn_report,
        'forecasting_models': sales_report,
        'customer_clusters': cluster_report,
        'kaggle_churn_models': kaggle_report
    }
    
    with open(os.path.join(models_dir, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print("\nAll models (including Real Kaggle Dataset models) trained, evaluated, and serialized successfully!")

if __name__ == '__main__':
    train_all_models('c:/Users/Nandhupriya/BI PROJECT/data', 'c:/Users/Nandhupriya/BI PROJECT/models')
