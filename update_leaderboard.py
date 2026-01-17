import json
import pandas as pd

# Inputs: submission evaluation
submission_file = "submissions/submission.csv"
name = "Your Name"  # could be extracted from PR or config
accuracy = 0.90     # calculated in scoring script
f1 = 0.88           # calculated in scoring script

# Load current leaderboard
try:
    with open("leaderboard.json", "r") as f:
        leaderboard = json.load(f)
except FileNotFoundError:
    leaderboard = []

# Add new entry
leaderboard.append({
    "name": name,
    "submission": submission_file.split("/")[-1],
    "accuracy": accuracy,
    "f1": f1
})

# Sort by accuracy (or any metric)
leaderboard.sort(key=lambda x: x["accuracy"], reverse=True)

# Save updated JSON
with open("leaderboard.json", "w") as f:
    json.dump(leaderboard, f, indent=2)

# Generate HTML table
html_rows = "\n".join([
    f"<tr><td>{i+1}</td><td>{entry['name']}</td><td>{entry['submission']}</td><td>{entry['accuracy']:.4f}</td><td>{entry['f1']:.4f}</td></tr>"
    for i, entry in enumerate(leaderboard)
])

html_content = f"""
<html>
<head><title>Leaderboard</title></head>
<body>
<h1>Leaderboard</h1>
<table border='1'>
<tr><th>Rank</th><th>Name</th><th>Submission</th><th>Accuracy</th><th>F1 Score</th></tr>
{html_rows}
</table>
</body>
</html>
"""

with open("leaderboard.html", "w") as f:
    f.write(html_content)
