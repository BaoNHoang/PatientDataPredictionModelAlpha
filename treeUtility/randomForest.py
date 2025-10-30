# randomForest.py
import numpy as np
from collections import Counter
from treeUtility import decisionTree

# RANDOM FOREST CLASS 
class RandomForest:
    """
    Random Forest — collection of Decision Trees.
    Improves stability and accuracy using bootstrap sampling.
    """
    def __init__(self, n_trees=10, max_depth=10, min_samples_split=2, n_features=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_features = n_features
        self.trees = []

    def fit(self, X, y):
        """Train multiple trees on random bootstrap samples."""
        self.trees = []
        for _ in range(self.n_trees):
            tree = decisionTree.DecisionTree(max_depth=self.max_depth, min_samples_split=self.min_samples_split, n_features=self.n_features)
            X_sample, y_sample = self.randomized_samples(X, y)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def randomized_samples(self, X, y):
        """Randomly sample with replacement with boostrap sampling."""
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, n_samples, replace=True)
        return X[idxs], y[idxs]

    def common_label(self, y):
        """Return the most common label in predictions."""
        return Counter(y).most_common(1)[0][0]

    def predict(self, X):
        """Predict using majority vote from all trees."""
        tree_predictions = np.array([tree.predict(X) for tree in self.trees])
        tree_predictions = np.swapaxes(tree_predictions, 0, 1) 
        return np.array([self.common_label(preds) for preds in tree_predictions])
    