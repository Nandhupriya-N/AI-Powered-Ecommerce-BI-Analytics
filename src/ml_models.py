"""
High-Performance, Pure-Python/NumPy Machine Learning Suite
Provides robust, reliable models for:
- Churn Classification (Random Forest, Gradient Boosting, Logistic Regression)
- Sales Forecasting (Multi-variate Linear/Ridge Regressor with Lag features)
- Customer Segmentation (K-Means Clustering with K-Means++ initialization)
- Anomaly Detection (Statistical & Outlier Distance Scoring)
Fully compatible with Windows Application Control and cross-platform execution.
"""

import numpy as np
import scipy.optimize as opt
from collections import Counter

# ==========================================
# 1. LOGISTIC REGRESSION (L-BFGS Optimized)
# ==========================================
class LogisticRegressionCustom:
    def __init__(self, C=1.0, max_iter=200):
        self.C = C
        self.max_iter = max_iter
        self.weights = None
        self.bias = 0.0
        self.feature_names = None

    def _sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -25, 25)))

    def fit(self, X, y, feature_names=None):
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        self.feature_names = feature_names
        n_samples, n_features = X.shape

        def loss_and_grad(params):
            w = params[:-1]
            b = params[-1]
            z = np.dot(X, w) + b
            p = self._sigmoid(z)
            p = np.clip(p, 1e-12, 1.0 - 1e-12)
            
            # Binary Cross Entropy + L2 Regularization
            loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)) + (0.5 / self.C) * np.sum(w**2)
            grad_w = (np.dot(X.T, (p - y)) / n_samples) + (1.0 / self.C) * w
            grad_b = np.mean(p - y)
            grad = np.append(grad_w, grad_b)
            return loss, grad

        init_params = np.zeros(n_features + 1)
        res = opt.minimize(loss_and_grad, init_params, jac=True, method='L-BFGS-B', options={'maxiter': self.max_iter})
        self.weights = res.x[:-1]
        self.bias = res.x[-1]
        return self

    def predict_proba(self, X):
        X = np.asarray(X, dtype=np.float64)
        z = np.dot(X, self.weights) + self.bias
        p1 = self._sigmoid(z)
        p0 = 1.0 - p1
        return np.column_stack((p0, p1))

    def predict(self, X, threshold=0.5):
        probs = self.predict_proba(X)[:, 1]
        return (probs >= threshold).astype(int)

    @property
    def feature_importances_(self):
        abs_w = np.abs(self.weights)
        total = np.sum(abs_w)
        return abs_w / total if total > 0 else abs_w


# ==========================================
# 2. DECISION TREE & RANDOM FOREST
# ==========================================
class TreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None, prob=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.prob = prob

    @property
    def is_leaf(self):
        return self.value is not None


class DecisionTreeCustom:
    def __init__(self, max_depth=5, min_samples_split=5):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def _gini(self, y):
        m = len(y)
        if m == 0:
            return 0
        p = np.bincount(y, minlength=2) / m
        return 1.0 - np.sum(p**2)

    def _best_split(self, X, y):
        best_gain = -1
        split_feat, split_thresh = None, None
        n_samples, n_features = X.shape
        parent_gini = self._gini(y)

        # Subsample features if random
        feature_indices = np.random.choice(n_features, size=int(np.sqrt(n_features)) + 1, replace=False)

        for f in feature_indices:
            thresholds = np.percentile(X[:, f], [20, 40, 60, 80])
            for t in thresholds:
                left_mask = X[:, f] <= t
                right_mask = ~left_mask
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue

                g_left = self._gini(y[left_mask])
                g_right = self._gini(y[right_mask])
                p_left = np.sum(left_mask) / n_samples
                gain = parent_gini - (p_left * g_left + (1 - p_left) * g_right)

                if gain > best_gain:
                    best_gain = gain
                    split_feat = f
                    split_thresh = t

        return split_feat, split_thresh

    def _build_tree(self, X, y, depth=0):
        n_samples = len(y)
        unique_classes = np.unique(y)

        if depth >= self.max_depth or n_samples < self.min_samples_split or len(unique_classes) == 1:
            val = Counter(y).most_common(1)[0][0]
            prob = np.mean(y == 1) if n_samples > 0 else 0.0
            return TreeNode(value=val, prob=prob)

        feat, thresh = self._best_split(X, y)
        if feat is None:
            val = Counter(y).most_common(1)[0][0]
            prob = np.mean(y == 1)
            return TreeNode(value=val, prob=prob)

        left_mask = X[:, feat] <= thresh
        right_mask = ~left_mask

        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1)
        right_child = self._build_tree(X[right_mask], y[right_mask], depth + 1)

        return TreeNode(feature=feat, threshold=thresh, left=left_child, right=right_child)

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.int64)
        self.root = self._build_tree(X, y)
        return self

    def _traverse_one(self, x, node):
        if node.is_leaf:
            return node.value, node.prob
        if x[node.feature] <= node.threshold:
            return self._traverse_one(x, node.left)
        return self._traverse_one(x, node.right)

    def predict_proba(self, X):
        X = np.asarray(X, dtype=np.float64)
        probs = np.array([self._traverse_one(x, self.root)[1] for x in X])
        return np.column_stack((1.0 - probs, probs))

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)


class RandomForestCustom:
    def __init__(self, n_estimators=40, max_depth=6, min_samples_split=5):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []
        self.feature_importances_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.int64)
        n_samples, n_features = X.shape
        self.trees = []
        
        # Track feature usage for importance
        feat_counts = np.zeros(n_features)

        for _ in range(self.n_estimators):
            indices = np.random.choice(n_samples, size=n_samples, replace=True)
            X_boot = X[indices]
            y_boot = y[indices]

            tree = DecisionTreeCustom(max_depth=self.max_depth, min_samples_split=self.min_samples_split)
            tree.fit(X_boot, y_boot)
            self.trees.append(tree)

            def tally(node):
                if node and not node.is_leaf:
                    feat_counts[node.feature] += 1
                    tally(node.left)
                    tally(node.right)
            tally(tree.root)

        total = np.sum(feat_counts)
        self.feature_importances_ = feat_counts / total if total > 0 else feat_counts
        return self

    def predict_proba(self, X):
        X = np.asarray(X, dtype=np.float64)
        all_probs = np.array([tree.predict_proba(X)[:, 1] for tree in self.trees])
        avg_p1 = np.mean(all_probs, axis=0)
        return np.column_stack((1.0 - avg_p1, avg_p1))

    def predict(self, X, threshold=0.5):
        probs = self.predict_proba(X)[:, 1]
        return (probs >= threshold).astype(int)


# ==========================================
# 3. GRADIENT BOOSTING CLASSIFIER
# ==========================================
class GradientBoostingCustom:
    def __init__(self, n_estimators=30, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.init_log_odds = 0.0

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        n_samples = len(y)

        # Baseline log-odds
        p_mean = np.clip(np.mean(y), 1e-4, 1 - 1e-4)
        self.init_log_odds = np.log(p_mean / (1 - p_mean))
        current_logits = np.full(n_samples, self.init_log_odds)

        self.trees = []
        for _ in range(self.n_estimators):
            p = 1.0 / (1.0 + np.exp(-current_logits))
            residuals = y - p

            # Pseudo-tree approximating residuals
            tree = DecisionTreeCustom(max_depth=self.max_depth, min_samples_split=5)
            # Binary target approximation
            pseudo_target = (residuals > 0).astype(int)
            tree.fit(X, pseudo_target)
            self.trees.append(tree)

            pred_p = tree.predict_proba(X)[:, 1] - 0.5
            current_logits += self.lr * pred_p * 2.0

        return self

    def predict_proba(self, X):
        X = np.asarray(X, dtype=np.float64)
        n_samples = len(X)
        logits = np.full(n_samples, self.init_log_odds)

        for tree in self.trees:
            pred_p = tree.predict_proba(X)[:, 1] - 0.5
            logits += self.lr * pred_p * 2.0

        p1 = 1.0 / (1.0 + np.exp(-np.clip(logits, -20, 20)))
        return np.column_stack((1.0 - p1, p1))

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X)[:, 1] >= threshold).astype(int)


# ==========================================
# 4. SALES FORECASTING REGRESSOR (Ridge / Multi-Variate)
# ==========================================
class SalesForecasterCustom:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.weights = None
        self.intercept = 0.0
        self.mean_ = None
        self.scale_ = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        
        self.mean_ = np.mean(X, axis=0)
        self.scale_ = np.std(X, axis=0)
        self.scale_[self.scale_ == 0] = 1.0
        X_scaled = (X - self.mean_) / self.scale_
        
        n_samples, n_features = X_scaled.shape
        # Ridge Regression closed-form solution: w = (X^T X + alpha * I)^(-1) X^T y
        A = np.dot(X_scaled.T, X_scaled) + self.alpha * np.eye(n_features)
        b = np.dot(X_scaled.T, (y - np.mean(y)))
        self.weights = np.linalg.solve(A, b)
        self.intercept = np.mean(y)
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=np.float64)
        X_scaled = (X - self.mean_) / self.scale_
        return np.dot(X_scaled, self.weights) + self.intercept


# ==========================================
# 5. K-MEANS CLUSTERING (K-Means++ & Lloyd's algorithm)
# ==========================================
class KMeansCustom:
    def __init__(self, n_clusters=4, max_iter=100, random_state=42):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.cluster_centers_ = None
        self.labels_ = None

    def _init_centers(self, X):
        np.random.seed(self.random_state)
        n_samples = len(X)
        centers = [X[np.random.choice(n_samples)]]

        for _ in range(1, self.n_clusters):
            dists = np.min([np.sum((X - c)**2, axis=1) for c in centers], axis=0)
            probs = dists / np.sum(dists)
            next_c = X[np.random.choice(n_samples, p=probs)]
            centers.append(next_c)

        return np.array(centers)

    def fit(self, X):
        X = np.asarray(X, dtype=np.float64)
        centers = self._init_centers(X)

        for _ in range(self.max_iter):
            # Compute distances
            dists = np.array([np.linalg.norm(X - c, axis=1) for c in centers])
            labels = np.argmin(dists, axis=0)

            # Update centers
            new_centers = np.array([X[labels == k].mean(axis=0) if np.sum(labels == k) > 0 else centers[k] for k in range(self.n_clusters)])
            if np.allclose(centers, new_centers, atol=1e-4):
                break
            centers = new_centers

        self.cluster_centers_ = centers
        self.labels_ = labels
        return self

    def predict(self, X):
        X = np.asarray(X, dtype=np.float64)
        dists = np.array([np.linalg.norm(X - c, axis=1) for c in self.cluster_centers_])
        return np.argmin(dists, axis=0)


# ==========================================
# 6. ANOMALY DETECTOR (Robust Statistical & Mahalanobis)
# ==========================================
class AnomalyDetectorCustom:
    def __init__(self, contamination=0.015):
        self.contamination = contamination
        self.mean_ = None
        self.std_ = None
        self.threshold_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=np.float64)
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0)
        self.std_[self.std_ == 0] = 1.0

        z_scores = np.abs((X - self.mean_) / self.std_)
        anomaly_scores = np.max(z_scores, axis=1)
        self.threshold_ = np.percentile(anomaly_scores, 100 * (1 - self.contamination))
        return self

    def decision_function(self, X):
        X = np.asarray(X, dtype=np.float64)
        z_scores = np.abs((X - self.mean_) / self.std_)
        return np.max(z_scores, axis=1)

    def predict(self, X):
        scores = self.decision_function(X)
        # -1 for anomaly, 1 for normal (matching scikit-learn convention)
        return np.where(scores >= self.threshold_, -1, 1)
