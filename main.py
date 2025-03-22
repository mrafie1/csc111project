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

    players = set

    def _load_game_data(self, filename: str) -> Graph:
        """Load players from a JSON file with the given filename and
        return a Graph object"""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        players = {}
        graph = Graph()
        for loc_data in data:
            passes = loc_data['passes_to']
            defense_stats = loc_data['defensive_stats']
            assists = self.process_passes(passes)
            defense = self.process_defense(defense_stats)

            player_obj = _Player(loc_data['name'], loc_data['team'], loc_data['positions'], defense['points'],
                                 defense['rebounds'], assists, defense['minutes'],
                                 defense['steals'], defense['blocks'])
            players[player_obj.name] = player_obj

        graph._players = players
        # print(players)
        return graph

    def process_passes(self, raw_info: dict[dict]) -> float:
        """Returns the assists of the player

        Representation Invariant:
            - raw_info in same format as "passes_to" dict in LAL.json and DAL.json files

        """

        assists = 0
        for player in raw_info:
            assists += raw_info[player]["assists"]
        assists = assists

        return assists

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
