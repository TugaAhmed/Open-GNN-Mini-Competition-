import sys
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import json

submission_path = sys.argv[1]

# Load submission
submission = pd.read_csv(submission_path)

# Load hidden ground truth
gt = np.load("data/private/graph_labels.npy")
test_idx = np.load("data/private/test_idx.npy")

y_true = gt[test_idx]
y_pred = submission["label"].values

acc = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# Write results for next step
with open("score.json", "w") as f:
    json.dump({"accuracy": acc, "f1": f1}, f)
