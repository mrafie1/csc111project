import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# this is a sample data set, use json importing when team finished
players = ["Alex Len", "Cam Reddish", "Jarred Vanderbilt"]
pass_data = {
    "Alex Len": {"Bronny James": 5, "Dalton Knecht": 4, "Jordan Goodwin": 6, "Austin Reaves": 21, "Gabe Vincent": 8, "Rui Hachimura": 3, "Luka Dončić": 12, "Jarred Vanderbilt": 2, "Shake Milton": 7, "Dorian Finney-Smith": 2, "Markieff Morris": 1, "LeBron James": 8},
    "Cam Reddish": {"Bronny James": 5, "Dalton Knecht": 16, "Christian Koloko": 7, "Max Christie": 20, "Austin Reaves": 71, "Jaxson Hayes": 7, "Gabe Vincent": 17, "Rui Hachimura": 12, "Shake Milton": 8, "Dorian Finney-Smith": 1, "LeBron James": 72},
    "Jarred Vanderbilt": {"Austin Reaves": 19, "LeBron James": 48, "Rui Hachimura": 4, "Gabe Vincent": 31, "Dorian Finney-Smith": 16, "Luka Dončić": 53, "Jaxson Hayes": 4, "Christian Koloko": 1, "Shake Milton": 18, "Jordan Goodwin": 25}
}
players_list = sorted(set(pass_data.keys()).union(*[set(v.keys()) for v in pass_data.values()]))
matrix = pd.DataFrame(np.zeros((len(players_list), len(players_list))), index=players_list, columns=players_list)

for passer, receivers in pass_data.items():
    for receiver, passes in receivers.items():
        if receiver in matrix.columns:
            matrix.loc[passer, receiver] = passes

plt.figure(figsize=(10, 8))
sns.heatmap(matrix, annot=True, cmap="Blues", fmt=".0f", linewidths=0.5)
plt.title("Player Passing Synergy Heatmap")
plt.xlabel("Players")
plt.ylabel("Players")
plt.show()
