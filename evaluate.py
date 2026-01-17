import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

# Load submission
submission = pd.read_csv("submissions/submission.csv")

# Load full ground truth labels and test graph indices
ground_truth = np.load("data/gossipcop/graph_labels.npy")
test_graphs = np.load("data/gossipcop/test_idx.npy")  # indices of graphs in the test set

# Ensure submission matches the test graphs
# submission['graph_id'] should be 0..len(test_graphs)-1 or the actual graph_id from test_graphs
y_true = [ground_truth[i] for i in test_graphs]
y_pred = submission["label"].values

# Check length matches
assert len(y_true) == len(y_pred), "Mismatch between submission and test set length!"

# Compute metrics
acc = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print(f"Submission Accuracy: {acc:.4f}")
print(f"Submission F1 Score: {f1:.4f}")
