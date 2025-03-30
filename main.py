"""CSC111 Project 2:
Top Hoops: NBA Optimal Basketball Lineup
Abdullah Alhidary, Houssam Yaacoub, Justin Peng, Muhammad Rafie

This module is the main file for the project. This file contains the 'LineupSimulation' class: This is where
users will run the file, create a LineupSimulation instance by initializing it with a datafile. The user can then
run 'visualize_heatmap()' and 'show_graph()' to see the passes made between players and the connections between
players as well as the optimal lineup based on this program calculating each player's player impact estimate.
"""
from __future__ import annotations
import json

from classes import Graph, _Player
from visualization import create_heatmap


class LineupSimulation:
    """A lineup simulation storing the graph and all player info.

        Instance Attributes:
            - team_graph: Graph object of given datafile
            - lineup: List of top 5 players as _Player classes based on their positions and player_impact_estimate
            - players: Dictionary mapping player name to a tuple consisting of the player object and its interactions
            - team_name: Name of the datafile team
        """
    team_graph: Graph
    lineup: list[_Player]
    players: dict
    team_name: str

    def __init__(self, filename: str) -> None:
        """
        Initialize a new LineupSimulation class with given filename.
        """
        self.players = {}
        self.team_graph = self._load_game_data(filename)
        self.lineup = self.generate_lineup()
        self.team_name = filename

    def _load_game_data(self, filename: str) -> Graph:
        """Load players from a JSON file with the given filename and
        return a Graph object"""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        graph = Graph()

        # Instanciating player objects
        for loc_data in data:
            passes = loc_data['passes_to']
            defense_stats = loc_data['defensive_stats']
            assists, interactions = self.process_assists(passes)
            defense = self.process_defense(defense_stats)

            player_obj = _Player(loc_data['name'], loc_data['team'], loc_data['positions'], defense['points'],
                                 defense['rebounds'], assists, defense['minutes'],
                                 defense['steals'], defense['blocks'])
            graph.add_player(player_obj)

            # Maps name to a tuple of _Player object and the passes_to dict seen in the json files
            self.players[player_obj.name] = (player_obj, interactions)

        for player in self.players:
            player_interactions = self.players[player][1]

            for player_name in self.players[player][1]:
                assists = player_interactions[player_name]['assists']
                total_passes = player_interactions[player_name]['total_passes']
                minutes_together = player_interactions[player_name]['minutes_together']
                graph.add_connection(self.players[player][0], player_name, assists, total_passes, minutes_together)

        return graph

    def process_assists(self, raw_info: dict[dict]) -> tuple[int, dict[str, dict]]:
        """Returns the assists, passes, and minutes together of the player in a dict

        Preconditions:
            - raw_info in same format as "passes_to" dict in LAL.json and DAL.json files
        """
        pass_stats = {}
        assists = 0
        for player in raw_info:
            assists += raw_info[player]["assists"]
            pass_stats[player] = raw_info[player]

        return (assists, pass_stats)

    def process_defense(self, raw_info: dict[str, int]) -> dict:
        """Returns the points, rebounds, blocks, and steals alongside total minutes in a dict.

        Preconditions:
            - raw_info in same format as "defensive_stats" dict in LAL.json and DAL.json files
        """
        minutes = raw_info['minutes']
        points = raw_info['points']
        rebounds = raw_info['rebounds']
        steals = raw_info['steals']
        blocks = raw_info['blocks']

        defense = {'points': points, 'rebounds': rebounds, 'steals': steals, 'blocks': blocks, 'minutes': minutes}

        return defense

    def generate_lineup(self) -> list[_Player]:
        """
        Return a list of 5 _Player class, two guards, two forwards, one center. Call on function 'highest_in_position'
        to return the top players in each position.
        """
        lst = []

        guards = self.highest_in_position("Guard")
        lst.append(guards[0])
        lst.append(guards[1])

        forwards = self.highest_in_position("Forward")
        lst.append(forwards[0])
        lst.append(forwards[1])

        center = self.highest_in_position("Center")
        lst.append(center[0])

        return lst

    def highest_in_position(self, pos: str) -> tuple[_Player, _Player]:
        """
        Return top two players in given position in self.players based on highest player_impact_estimate
        """
        lst = []
        for player in self.players:
            p = self.players[player][0]
            if p.position[0] == pos:
                lst.append(p)

        max_player = lst[0]
        max_pie = max_player.player_impact_estimate
        for player in lst:
            if player.player_impact_estimate > max_pie:
                max_player = player
                max_pie = max_player.player_impact_estimate

        player_pos1 = max_player
        lst.remove(max_player)

        max_player = lst[0]
        max_pie = max_player.player_impact_estimate
        for player in lst:
            if player.player_impact_estimate > max_pie:
                max_player = player
                max_pie = max_player.player_impact_estimate

        player_pos2 = max_player
        return player_pos1, player_pos2

    def visualize_heatmap(self) -> None:
        """
        Open a GUI displaying heatmap of passes between players. Call on function in 'visualization.py' that
        creates the heatmap.
        """
        pass_data = {}
        for player in self.players:
            pass_data[player] = self.team_graph.get_passes_per_minute_dict(player, self.players[player][1])

        # Calls visuaize_heatmap from visualization.py
        create_heatmap(pass_data, self.team_name)

    def show_graph(self) -> None:
        """
        Open a GUI displaying the connections between players. Call on function in 'classes.py' that creates
        the graph.
        """
        self.team_graph.visualize_graph(self.lineup)


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['json', 'classes', 'visualization'],
        'disable': ['E9998', 'R0914']
    })
