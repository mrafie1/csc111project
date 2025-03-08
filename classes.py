from __future__ import annotations
from typing import Any


class _Player:
    """ Player class representing the statistics of each player.
    Analogous to the _vertex class in a graph.
    """
    name: str
    avg_points: int
    avg_rebounds: int
    avg_assists: int
    player_impact_estimate: int
    # Add further statistics attributes


class _Connection:
    """ An 'edge' class connecting two _player classes and representing their shared statistics.
    Representation Invariants:
        - len(player_connection) == 2 or len(player_connection) == 0
    """
    player_connection: list[_Player]
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
