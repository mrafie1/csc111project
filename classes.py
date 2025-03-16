from __future__ import annotations
from typing import Any, Optional


class _Player:
    """ Player class representing the statistics of each player.
    Analogous to the _vertex class in a graph.
    """
    name: str
    team: str
    position: list
    avg_points: float
    avg_rebounds: float
    avg_assists: float
    avg_steals: float
    avg_blocks: float
    minutes: int
    player_impact_estimate: float
    connections: list[_Connection]

    # Add further statistics attributes

    def __init__(self, name: str, team: str, position: list, points: int, rebounds: int, assists: int, minutes: int, steals: int, blocks: int) -> None:
        self.name = name
        self.team = team
        self.position = position
        self.avg_points = points/minutes
        self.avg_rebounds = rebounds/minutes
        self.avg_assists = assists/minutes
        self.avg_steals = steals/minutes
        self.avg_blocks = blocks/minutes
        self.minutes = minutes

        self.connections = []
        # Change later
        self.player_impact_estimate = 0




class _Connection:
    """ An 'edge' class connecting two _player classes and representing their shared statistics.
    Representation Invariants:
        - len(player_connection) == 2 or len(player_connection) == 0
    """
    player_connection: list[_Player]
    # We can possibly just combine both of these later
    player1_avg_assists_per_pass: Optional[float]
    player2_avg_assists_per_pass: Optional[float]
    max_avg_assists_per_pass: Optional[float]
    avg_passes_per_minute: float

    def __init__(self, player1: _Player, player2: _Player):
        self.player_connection = [player1, player2]
        self.player1_avg_assists_per_pass = 0
        self.player2_avg_assists_per_pass = 0
        self.avg_passes_per_minute = 0



class Graph:
    """ A graph whose vertices are _player class.
    Representation Invariants:
    - all(name == self._players[name].name for name in self._players)
    """
    # Private Instance Attributes:
    #     - _players: A collection of the players contained in this graph.
    #                  Maps name to _Player instance.
    _players: dict[str, _Player]
    _connections: set[_Connection]

    def __init__(self):
        self._players = {}

    def add_player(self, player: _Player):
        if player.name not in self._players:
            self._players[player.name] = player
