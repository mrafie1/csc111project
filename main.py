# MAIN FILE FOR PYTHON PROJECT
from __future__ import annotations
import json
from typing import Optional

from classes import Graph, _Player, _Connection


class LineupSimulation:
    """A lineup simulation  storing the graph and all player info.

        Instance Attributes:
            -

        """

    # Private Instance Attributes:
    #   -

    players = {}

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
