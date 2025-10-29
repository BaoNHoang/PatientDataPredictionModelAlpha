import numpy as np
from collections import Counter
from treeUtility import node

# DECISION TREE CLASS
class DecisionTree:
    """
    A simple Decision Tree Classifier built from scratch using entropy (information gain).

    Parameters:
      - min_samples_split: minimum number of samples to attempt a split
      - max_depth: maximum depth allowed for recursion
      - n_features: number of random features to consider at each split (used for randomness)
    """
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.root = None 

    def fit(self, X, y):
        """
        Fit (train) the decision tree using dataset X (features) and y (labels).
        """
        self.n_features = X.shape[1] if self.n_features is None else min(X.shape[1], self.n_features)
        self.root = self.grow_tree(X, y)

    def grow_tree(self, X, y, depth=0):
        """
        Recursively grow the decision tree and determine the best split at each node.
        """
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        if (depth >= self.max_depth or n_labels == 1 or n_samples < self.min_samples_split):
            leaf_value = self.common_label(y)
            return node.Node(value=leaf_value)

        feat_idxs = np.random.choice(n_features, self.n_features, replace=False)

        best_gain = -1
        best_feature = None
        best_threshold = None

        for feat_idx in feat_idxs:
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)

            for threshold in thresholds:
                IG = self.information_gain(y, X_column, threshold)
                if IG > best_gain:
                    best_gain = IG
                    best_feature = feat_idx
                    best_threshold = threshold

        left_idxs, right_idxs = self.split(X[:, best_feature], best_threshold)

        left_child = self.grow_tree(X[left_idxs, :], y[left_idxs], depth + 1)
        right_child = self.grow_tree(X[right_idxs, :], y[right_idxs], depth + 1)

        return node.Node(feature=best_feature, threshold=best_threshold, left=left_child, right=right_child)

    def information_gain(self, y, X_column, threshold):
        """Compute information gain based on entropy."""
        parent_entropy = self.calculate_entropy(y)
        left_idxs, right_idxs = self.split(X_column, threshold)

        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0

        n = len(y)
        n_left, n_right = len(left_idxs), len(right_idxs)
        e_left, e_right = self.calculate_entropy(y[left_idxs]), self.calculate_entropy(y[right_idxs])
        child_entropy = (n_left / n) * e_left + (n_right / n) * e_right

        return parent_entropy - child_entropy

    def split(self, X_column, split_threshold):
        """Split dataset based on threshold."""
        left_idxs = np.argwhere(X_column <= split_threshold).flatten()
        right_idxs = np.argwhere(X_column > split_threshold).flatten()
        return left_idxs, right_idxs

    def calculate_entropy(self, y):
        """Calculate entropy of label distribution."""
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log(p) for p in ps if p > 0])

    def common_label(self, y):
        """Return most frequent class label."""
        return Counter(y).most_common(1)[0][0]

    def predict(self, X):
        """Predict class labels for all samples in X."""
        return np.array([self.traverse(x, self.root) for x in X])

    def traverse(self, x, node):
        """Traverse the tree recursively for prediction."""
        if node.is_leaf_node():
            return node.value
        if x[node.feature] <= node.threshold:
            return self.traverse(x, node.left)
        else:
            return self.traverse(x, node.right)