from __future__ import annotations
from typing import Any, Optional


class _Player:
    """ Player class representing the statistics of each player.
    Analogous to the _vertex class in a graph.
    """
    name: str
    avg_points: float
    avg_rebounds: float
    avg_assists: float
    player_impact_estimate: float
    connections: list[_Connection]

    # Add further statistics attributes


class _Connection:
    """ An 'edge' class connecting two _player classes and representing their shared statistics.
    Representation Invariants:
        - len(player_connection) == 2 or len(player_connection) == 0
    """
    player_connection: list[_Player]
    player1_avg_assists: Optional[float]
    player2_avg_assists: Optional[float]
    # Add further statistic attributes


class Teamgraph:
    """ A graph whose vertices are _player class.
    Representation Invariants:
    - all(name == self._players[name].name for name in self._players)
    """
    # Private Instance Attributes:
    #     - _players: A collection of the players contained in this graph.
    #                  Maps name to _Player instance.
    _players: dict[str, _Player]
