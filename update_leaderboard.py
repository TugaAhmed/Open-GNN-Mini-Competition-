import json
import pandas as pd

submission = pd.read_csv("submissions/submission.csv")
ground_truth = np.load("data/gossipcop/graph_labels.npy")

from sklearn.metrics import accuracy_score, f1_score
y_true = [ground_truth[i] for i in submission["graph_id"]]
y_pred = submission["label"]

acc = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

# Load old leaderboard
with open("leaderboard.json", "r") as f:
    leaderboard = json.load(f)

leaderboard.append({"submission": "latest", "accuracy": acc, "f1": f1})
leaderboard = sorted(leaderboard, key=lambda x: x["f1"], reverse=True)

with open("leaderboard.json", "w") as f:
    json.dump(leaderboard, f, indent=2)
