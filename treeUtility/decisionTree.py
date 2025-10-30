# decisionTree.py
import numpy as np
from collections import Counter
from treeUtility import node

# DECISION TREE CLASS
class DecisionTree:
    """
    Parameters:
      - min_samples_split: minimum number of samples to attempt a split
      - max_depth: maximum depth allowed for recursion
      - n_features: number of random features to consider at each split (used for randomness)   
      - criterion: "gini" or "entropy" (Choosing which impurity algorithm)

    """
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None, criterion="gini"):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.criterion = criterion
        self.root = None 

    def fit(self, X, y):
        """
        Fit (train) the decision tree using dataset X (features) and y (labels).
        """
        self.n_features = X.shape[1] if self.n_features is None else min(X.shape[1], self.n_features)
        self.root = self.grow_tree(X, y)

    def grow_tree(self, X, y, depth=0):
        """Recursively build the tree."""
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        if (depth >= self.max_depth or n_labels == 1 or n_samples < self.min_samples_split):
            leaf_value = self.common_label(y)
            return node.Node(value=leaf_value)

        feat_idxs = np.random.choice(n_features, self.n_features, replace=False)

        best_gain, best_feature, best_threshold = -1, None, None
        for index in feat_idxs:
            X_col = X[:, index]
            thresholds = np.unique(X_col)
            for threshold in thresholds:
                IG = self.information_gain(y, X_col, threshold)
                if IG > best_gain:
                    best_gain = IG
                    best_feature = index
                    best_threshold = threshold

        if best_gain == -1:
            return node.Node(value=self.common_label(y))

        left_idxs, right_idxs = self.split(X[:, best_feature], best_threshold)
        left_child = self.grow_tree(X[left_idxs, :], y[left_idxs], depth + 1)
        right_child = self.grow_tree(X[right_idxs, :], y[right_idxs], depth + 1)

        return node.Node(feature=best_feature, threshold=best_threshold, left=left_child, right=right_child)


    def information_gain(self, y, X_column, threshold):
        """Compute information gain using Gini or Entropy."""
        if self.criterion == "entropy":
            impurity_func = self.calculate_entropy
        else:
            impurity_func = self.calculate_gini

        parent_impurity = impurity_func(y)
        left_idxs, right_idxs = self.split(X_column, threshold)

        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0

        n = len(y)
        n_left, n_right = len(left_idxs), len(right_idxs)
        child_impurity = (n_left / n) * impurity_func(y[left_idxs]) + (n_right / n) * impurity_func(y[right_idxs])

        return parent_impurity - child_impurity

    def split(self, X_column, split_threshold):
        """Split dataset based on threshold."""
        left_idxs = np.argwhere(X_column <= split_threshold).flatten()
        right_idxs = np.argwhere(X_column > split_threshold).flatten()
        return left_idxs, right_idxs
    
    def calculate_gini(self, y):
        """Calculate gini of label distribution. (More efficient and foregoes Logorithms)"""
        ps = np.bincount(y) / len(y)
        return 1 - np.sum(ps ** 2)

    def calculate_entropy(self, y):
        """Calculate entropy of label distribution."""
        ps = np.bincount(y) / len(y)
        return -np.sum([p * np.log(p) for p in ps if p > 0])

    def common_label(self, y):
        """Return most frequent class label."""
        return Counter(y).most_common(1)[0][0]

    def predict(self, X):
        """Predict class labels for all samples in X."""
        return np.array([self.traverse(x, self.root) for x in X])

    def traverse(self, x, node):
        """Traverse the tree recursively for prediction."""
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self.traverse(x, node.left)
        else:
            return self.traverse(x, node.right)