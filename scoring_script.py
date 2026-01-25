# import sys
# import pandas as pd
# import numpy as np
# from sklearn.metrics import accuracy_score, f1_score
# import json

# submission_path = sys.argv[1]

# # Load submission
# submission = pd.read_csv(submission_path)

# # Load hidden ground truth
# gt = np.load("data/private/graph_labels.npy")
# test_idx = np.load("data/private/test_idx.npy")

# y_true = gt[test_idx]
# y_pred = submission["label"].values

# acc = accuracy_score(y_true, y_pred)
# f1 = f1_score(y_true, y_pred)

# # Write results for next step
# with open("score.json", "w") as f:
#     json.dump({"accuracy": acc, "f1": f1}, f)


# scoring_script.py
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import sys

submission_file = sys.argv[1]  # CSV file passed by workflow

# Load submission
submission = pd.read_csv(submission_file)

# Load ground truth
ground_truth = np.load("data/gossipcop/graph_labels.npy")
test_graphs = np.load("data/gossipcop/test_idx.npy")

y_true = [ground_truth[i] for i in test_graphs]
y_pred = submission["label"].values

# Compute metrics
acc = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# Save metrics to a small JSON file for workflow to read
import json
metrics = {"accuracy": float(acc), "f1": float(f1), "submission": submission_file}
with open("metrics.json", "w") as f:
    json.dump(metrics, f)

print(f"Accuracy: {acc:.4f}, F1: {f1:.4f}")
