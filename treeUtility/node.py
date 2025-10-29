# NODE CLASS — basic unit of a decision tree
class Node:
    """
    A single node in a decision tree.
    Each node represents a condition (feature + threshold).
    Leaf nodes store a final prediction value (class label).
    """
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None):
        self.feature = feature          # Index of the feature used for splitting
        self.threshold = threshold      # Threshold value for the feature
        self.left = left                # Left child node
        self.right = right              # Right child node
        self.value = value              # Class label if leaf node
