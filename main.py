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

    @staticmethod
    def _load_game_data(filename: str) -> Graph:
        """Load locations and items from a JSON file with the given filename and
        return a Teamgraph object"""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        graph = Graph()
        return graph
