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
        """Load locations and items from a JSON file with the given filename and
        return a Teamgraph object"""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        players = {}
        graph = Graph()
        for loc_data in data:
            passes = loc_data['passes_to']
            defense_stats = loc_data['defensive_stats']
            avg_passes = self.process_passes(passes)
            avg_defense = self.process_defense(defense_stats)

            player_obj = _Player(loc_data['name'], loc_data['team'], loc_data['positions'], avg_defense['avg_points'],
                                 avg_defense['avg_rebounds'], avg_passes, avg_defense['minutes'],
                                 avg_defense['avg_steals'], avg_defense['avg_blocks'])
            players[player_obj.name] = player_obj

        graph._players = players
        print(players)
        return graph

    def process_passes(self, raw_info: dict[dict]) -> float:
        """Returns the average assists of the player as a float rounded to two decimal places

        Representation Invariant:
            - raw_info in same format as "passes_to" dict in LAL.json and DAL.json files

        """

        assists = 0
        total_minutes = 0
        for player in raw_info:
            assists += raw_info[player]["assists"]
            total_minutes += raw_info[player]["minutes_together"]
        avg_assists = round((assists / total_minutes), 2)

        return avg_assists

    def process_defense(self, raw_info: dict[str, int]) -> dict:
        """Returns the average points, rebounds, blocks, and steals alongside total minutes in a dict. Floats rounded to two decimals.

                Representation Invariant:
                    - raw_info in same format as "defensive_stats" dict in LAL.json and DAL.json files

                """

        minutes = raw_info['minutes']
        points = raw_info['points']
        rebounds = raw_info['rebounds']
        steals = raw_info['steals']
        blocks = raw_info['blocks']

        avg_points = round((points / minutes), 2)
        avg_rebounds = round((rebounds / minutes), 2)
        avg_steals = round((steals / minutes), 2)
        avg_blocks = round((blocks / minutes), 2)
        avg_defense = {'avg_points': avg_points, 'avg_rebounds': avg_rebounds, 'avg_steals': avg_steals,
                       'avg_blocks': avg_blocks, 'minutes': minutes}

        return avg_defense
