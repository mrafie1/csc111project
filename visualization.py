"""CSC111 Project 2:
Top Hoops: NBA Optimal Basketball Lineup
Abdullah Alhidary, Houssam Yaacoub, Justin Peng, Muhammad Rafie

This module contains the necessary function needed to create the heatmap of player passes which is displayed
in the 'main.py' file.

This function is in a seperate file as it uses many libraries seldom used in 'main.py' and 'classes.py'

"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


def create_heatmap(pass_data: dict, team_name: str) -> None:
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

    plt.figure(figsize=(12, 10))
    sns.heatmap(matrix, annot=True, cmap="Blues", fmt=".3f", linewidths=1)
    plt.title(f"Player Passing per Minute Synergy Heatmap for {team_name}\n "
              f"(Note That a Value of 0 Means the Two Players Have Not Played Together)")
    plt.xlabel("Players (Receiving the Pass)")
    plt.ylabel("Players (Making the Pass)")
    plt.subplots_adjust(left=0.17, right=1.05, top=0.90, bottom=0.28)
    plt.show()


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['numpy', 'pandas', 'seaborn', 'matplotlib', 'matplotlib.pyplot'],
        'disable': ['E9992']
    })
