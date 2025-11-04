# randomForest.py
import numpy as np
from collections import Counter
from treeUtility import decisionTree
from sklearn.preprocessing import StandardScaler

# RANDOM FOREST CLASS 
class RandomForest:
    """
    Random Forest — collection of Decision Trees.
    Improves stability and accuracy using bootstrap sampling.
    """
    def __init__(self, n_trees=850, max_depth=30, min_samples_split=2, n_features=None, criterion="gini"):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_features = n_features
        self.criterion = criterion
        self.trees = []
        self.scaler = StandardScaler()

    def fit(self, X, y):
        """Train multiple trees on random bootstrap samples."""
        X = self.scaler.fit_transform(X)
        self.trees = []

        for _ in range(self.n_trees):
            tree = decisionTree.DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                n_features=self.n_features,
                criterion=self.criterion
            )
            X_sample, y_sample = self.bootstrap_sample(X, y)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def bootstrap_sample(self, X, y):
        """Randomly sample with replacement with boostrap sampling."""
        n_samples = X.shape[0]
        idxs = np.random.choice(n_samples, n_samples, replace=True)
        return X[idxs], y[idxs]

    def predict(self, X):
        """Aggregate predictions by majority vote."""
        X = self.scaler.transform(X)
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        tree_preds = np.swapaxes(tree_preds, 0, 1)
        return np.array([self.majority_vote(preds) for preds in tree_preds])

    def majority_vote(self, preds):
        """Returns the most voted"""
        return Counter(preds).most_common(1)[0][0]
    