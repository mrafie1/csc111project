# MAIN FILE FOR PYTHON PROJECT
from __future__ import annotations
import json
from typing import Optional

import networkx as nx

from classes import Graph, _Player
from visualization import create_heatmap


class LineupSimulation:
    """A lineup simulation storing the graph and all player info.

        Instance Attributes:
            - team_graph
            - lineup_graph

        """

    # Private Instance Attributes:
    #   -
    team_graph: Graph
    lineup: list[_Player]
    players: dict
    team_name: str

    def __init__(self, filename: str):
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

        # graph._players = players
        # print(players)

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

        Representation Invariant:
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

                Representation Invariant:
                    - raw_info in same format as "defensive_stats" dict in LAL.json and DAL.json files

        """
        minutes = raw_info['minutes']
        points = raw_info['points']
        rebounds = raw_info['rebounds']
        steals = raw_info['steals']
        blocks = raw_info['blocks']

        defense = {'points': points, 'rebounds': rebounds, 'steals': steals, 'blocks': blocks, 'minutes': minutes}

        return defense

    """def get_player(self, player_name: str) -> Optional[_Player]:

        Returns the player object in self.players from the give player_name


        for player in self.players:
            if player == player_name:
                return self.players[player][0]
        return None
    """

    def generate_lineup(self) -> list[_Player]:
        """

        """
        lst = []

        guards = self.highest_in_position("Guard")
        lst.append(guards[0])
        lst.append(guards[1])

        forwards = self.highest_in_position("Forward")
        lst.append(forwards[0])
        lst.append(forwards[1])

        center = self.highest_in_position("Forward")
        lst.append(center[0])

        return lst

    def highest_in_position(self, pos: str) -> tuple[_Player, _Player]:
        """
        Return top two players in each position
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
        Visualzes the pass synergy of each player in a heatmap

        >>>x=LineupSimulation("DAL.json")
        >>>x.visualize_heatmap()

        >>>x=LineupSimulation("LAL.json")
        >>>x.visualize_heatmap()
        """
        pass_data = {}
        for player in self.players:
            pass_data[player] = self.team_graph.get_passes_per_minute_dict(player, self.players[player][1])

        # Calls visuaize_heatmap from visualization.py
        create_heatmap(pass_data, self.team_name)
