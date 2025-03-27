import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

import classes


def visualize_heatmap(pass_data: dict, team_name: str) -> None:
    """
    Constructs a heatmap for player passing synergy, and displays it.
    """
    # pass_data dict is in the following format:
    # pass_data = {
    #     "Alex Len": {"Bronny James": 5, "Dalton Knecht": 4, "Jordan Goodwin": 6, "Austin Reaves": 21,
    #     "Gabe Vincent": 8, "Rui Hachimura": 3, "Luka Dončić": 12, "Jarred Vanderbilt": 2, "Shake Milton": 7,
    #     "Dorian Finney-Smith": 2, "Markieff Morris": 1, "LeBron James": 8}....}
    players_list = sorted(set(pass_data.keys()).union(*[set(v.keys()) for v in pass_data.values()]))
    matrix = pd.DataFrame(np.zeros((len(players_list), len(players_list))), index=players_list, columns=players_list)

    for passer, receivers in pass_data.items():
        for receiver, passes in receivers.items():
            if receiver in matrix.columns:
                matrix.loc[passer, receiver] = passes

    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, cmap="Blues", fmt=".0f", linewidths=0.5)
    plt.title(f"Player Passing Synergy Heatmap for {team_name}")
    plt.xlabel("Players")
    plt.ylabel("Players")
    plt.show()

