# MAIN FILE FOR PYTHON PROJECT
from __future__ import annotations
import json
from typing import Optional

from classes import Graph

class LineupSimulation:
    """A lineup simulation  storing the graph and all player info.

        Instance Attributes:
            -

        """

    # Private Instance Attributes:
    #   -

    players = set

    @staticmethod
    def _load_game_data(filename: str) -> Teamgraph:
        """Load locations and items from a JSON file with the given filename and
        return a Teamgraph object"""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        players = {}
        graph = Teamgraph()
        for player_data in data:  # Go through each element associated with the 'locations' key in the file

            interactions = data['passes_to']


            player_obj = _Player(data['name'], data['positions'], data['team'])
        return graph
