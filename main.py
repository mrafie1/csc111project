# MAIN FILE FOR PYTHON PROJECT
from __future__ import annotations
import json
from typing import Optional

from classes import Graph


class display_stats:
    """
    sjiodnowsnodw
    """

    team_graph: Graph
    best_team_graph: Graph

    def __init__(self, data_file: str) -> None:
        self.team_graph = self._load_game_data(data_file)

    @staticmethod
    def _load_game_data(filename: str) -> Optional[Graph]:
        with open(filename, 'r') as f:
            data = json.load(f)

        # Adding players first
        return None
