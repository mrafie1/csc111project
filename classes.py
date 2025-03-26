from __future__ import annotations
from typing import Any, Optional


CENTER_WEIGHTS = {'points': 1, 'rebound': 1.5, 'blocks': 1, 'steals': 1, 'assists': 1.1}
FORWARD_WEIGHTS = {'points': 1.3, 'rebound': 1.3, 'blocks': 1, 'steals': 1.1, 'assists': 1.3}
GUARD_WEIGHTS = {'points': 1.6, 'rebound': 0.9, 'blocks': 0.65, 'steals': 1.6, 'assists': 1.7}

POSITION_WEIGHTS = {"Center": CENTER_WEIGHTS, "Forward": FORWARD_WEIGHTS, "Guard": GUARD_WEIGHTS}

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
        self.player_impact_estimate = 0

    def calculate_pie(self) -> float:
        """Compute the Player Impact Estimate (PIE) using positional weights."""
        # Determine primary position (first in the list)
        primary_position = self.position[0]  # Default to SF if unknown

        # Get the weight dictionary for this position
        weights = POSITION_WEIGHTS[primary_position]  # Default to SF

        # Compute PIE (No Division)
        self.player_impact_estimate = (
                (self.avg_points * weights['points']) +
                (self.avg_rebounds * weights['rebound']) +
                (self.avg_assists * weights['assists']) +
                (self.avg_steals * weights['steals']) +
                (self.avg_blocks * weights['blocks'])
        )

        return round(self.player_impact_estimate, 3)  # Return rounded PIE value


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
            self.player1_avg_assists_per_pass = round(assist/passes, 3)
        # This is player 2
        else:
            self.player2_avg_assists_per_pass = round(assist/passes, 3)
        self.avg_passes_per_minute = round(passes/minutes_together, 3)

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

    def add_connection(self, player1: _Player, player2: str, assist, passes, minutes_together) -> None:
        """
        Adds connection between two players using the _Connection class

        Representation Invariants:
            - player2 in self._players
        """
        if not self.check_exists(player1.name, player2):
            new_connection = _Connection(player1, self._players[player2])
            self._connections[(player1.name, player2)] = new_connection

        if (player1.name, player2) in self._connections:
            self._connections[(player1.name, player2)].tweak_stats(player1, assist, passes, minutes_together)
        else:
            self._connections[(player2, player1.name)].tweak_stats(player1, assist, passes, minutes_together)

    def check_exists(self, player1_name: str, player2_name: str) -> bool:

        keys = self._connections.keys()
        return (player1_name, player2_name) in keys or (player2_name, player1_name) in keys

    def __str__(self):
        str_so_far = "PLAYERS\n"
        for player in self._players:
            str_so_far += f'\n{self._players[player].name}'

        str_so_far += '\n=================================\nCONNECTIONS\n'
        for (player1, player2) in self._connections.keys():
            str_so_far += f'\n{player1} <---> {player2}'

        return str_so_far
