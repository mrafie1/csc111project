from __future__ import annotations
from typing import Any, Optional


class _Player:
    """ Player class representing the statistics of each player.
    Analogous to the _vertex class in a graph.
    """
    name: str
    team: str
    position: list[str]
    avg_points: float
    avg_rebounds: float
    avg_assists: float
    avg_steals: float
    avg_blocks: float
    minutes: int
    player_impact_estimate: float
    connections: list[_Connection]

    # Add further statistics attributes

    def __init__(self, name: str, team: str, position: list[str], points: float, rebounds: float, assists: float,
                 minutes: int, steals: float, blocks: float) -> None:
        self.name = name
        self.team = team
        self.position = position
        self.avg_points = round(points / minutes, 3)
        self.avg_rebounds = round(rebounds / minutes, 3)
        self.avg_assists = round(assists / minutes, 3)
        self.avg_steals = round(steals / minutes, 3)
        self.avg_blocks = round(blocks / minutes, 3)
        self.minutes = minutes

        self.connections = []
        # Change later
        self.player_impact_estimate = 0


class _Connection:
    """ An 'edge' class connecting two _Player classes and representing their shared statistics.
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

    def tweak_stats(self, player: _Player, assist, passes, minutes_together):
        # Check if this is player 1
        if self.player_connection[0] == player:
            self.player1_avg_assists_per_pass = assist/passes
        # This is player 2
        else:
            self.player2_avg_assists_per_pass = assist/passes
        self.avg_passes_per_minute = passes/minutes_together

    def finalize_stats(self):
        self.max_avg_assists_per_pass = max(self.player1_avg_assists_per_pass, self.player2_avg_assists_per_pass)


class Graph:
    """ A graph whose vertices are _player class.
    Representation Invariants:
    - all(name == self._players[name].name for name in self._players)
    """
    # Private Instance Attributes:
    #     - _players: A collection of the players contained in this graph.
    #                  Maps name to _Player instance.
    _players: dict[str, _Player]
    _connections: dict[tuple[str, str], _Connection]

    def __init__(self):
        self._players = {}
        self._connections = {}

    def add_player(self, player: _Player):
        if player.name not in self._players:
            self._players[player.name] = player

    def add_connection(self, player1: _Player, player2: str, assist, passes, minutes_together):
        """
        Adds connection between two players using the _Connection class

        Representation Invariants:
            - player2 in self._players
        """
        if (player1.name, player2) not in self._connections:
            new_connection = _Connection(player1, self._players[player2])
            self._connections[(player1.name, player2)] = new_connection

        self._connections[(player1.name, player2)].tweak_stats(player1, assist, passes, minutes_together)

    def check_exists(self, player1_name: str, player2_name: str) -> bool:

        keys = self._players.keys()
        return (player1_name, player2_name) in keys or (player1_name, player2_name) in keys
