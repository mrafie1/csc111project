from __future__ import annotations
from typing import Any, Optional

import networkx as nx
import matplotlib.pyplot as plt

CENTER_WEIGHTS = {'points': 1, 'rebound': 1.5, 'blocks': 1, 'steals': 1, 'assists': 1.1}
FORWARD_WEIGHTS = {'points': 1.3, 'rebound': 1.3, 'blocks': 1, 'steals': 1.1, 'assists': 1.3}
GUARD_WEIGHTS = {'points': 1.6, 'rebound': 0.9, 'blocks': 0.7, 'steals': 1.6, 'assists': 1.7}

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
        self.player_impact_estimate = self.calculate_player_impact()

    def calculate_player_impact(self) -> float:
        """Compute the Player Impact Estimate using positional weights."""
        primary_position = self.position[0]

        # Get the weight dictionary for this position
        weights = POSITION_WEIGHTS[primary_position]

        # Compute player impact
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
    avg_passes_per_minute_player1: float
    avg_passes_per_minute_player2: float
    synergy_score: float

    def __init__(self, player1: _Player, player2: _Player):
        self.player_connection = [player1, player2]
        self.player1_avg_assists_per_pass = 0
        self.player2_avg_assists_per_pass = 0
        self.avg_passes_per_minute = 0
        self.synergy_score = self.calculate_synergy_score()

    def tweak_stats(self, player: _Player, assist, passes, minutes_together):
        # Check if this is player 1
        if self.player_connection[0] == player:
            self.player1_avg_assists_per_pass = round(assist/passes, 3)
            self.avg_passes_per_minute_player1 = round(passes / minutes_together, 3)
        # This is player 2
        else:
            self.player2_avg_assists_per_pass = round(assist/passes, 3)
            self.avg_passes_per_minute_player2 = round(passes / minutes_together, 3)

    def finalize_stats(self):
        self.max_avg_assists_per_pass = max(self.player1_avg_assists_per_pass, self.player2_avg_assists_per_pass)

    def calculate_synergy_score(self) -> float:
        """
        Returns the synergy score between the two players by getting the average of their player impact estimates.
        Returns 0 if self.player_connection is empty (i.e. the connection hasn't been formed yet)
        """
        if len(self.player_connection) == 2:
            return (self.player_connection[0].player_impact_estimate +
                    self.player_connection[1].player_impact_estimate) / 2
        else:
            return 0

    def get_avg_passes_per_minute(self, player_name: str) -> float:
        """
        Returns the average passes per minute of the given player_name to the other player in this connection
        """
        if self.player_connection[0].name == player_name:
            return self.avg_passes_per_minute_player1
        else:
            return self.avg_passes_per_minute_player2


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

        connection_key = self.get_connection_key(player1.name, player2)
        self._connections[connection_key].tweak_stats(player1, assist, passes, minutes_together)

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

    def get_passes_per_minute_dict(self, player1_name: str, player_names: list) -> dict:
        """
        Returns a dict of the average passes per minute of the given player1_name to all the players player1_name
        has passed to
        """
        pass_data = {}
        for player2_name in player_names:
            curr_key = self.get_connection_key(player1_name, player2_name)
            pass_data[player2_name] = self._connections[curr_key].get_avg_passes_per_minute(player1_name)
        print(pass_data)
        return pass_data

    def get_connection_key(self, player1_name: str, player2_name: str) -> tuple[str, str]:
        """
        Returns the key in self._connections assiosiated with the given player1_name and player2_name
        """
        if (player1_name, player2_name) in self._connections:
            return (player1_name, player2_name)
        else:
            return (player2_name, player1_name)

    def visualize_graph(self, ideal_lineup: list[_Player]) -> None:
        nxgraph = nx.Graph()

        node_colors = []
        for vertex in self._players:
            nxgraph.add_node(vertex)
            if self._players[vertex] in ideal_lineup:
                node_colors.append('green')
            else:
                node_colors.append('blue')

        for connection in self._connections:
            connection_object = self._connections[connection]
            connection_score = connection_object.synergy_score

            # init edge color
            col = None

            if connection_score >= 1.75:
                col = 'green'
            elif connection_score > 0.75:
                col = '#8A2BE2'
            else:
                col = 'darkred'

            nxgraph.add_edge(connection[0], connection[1])
            nxgraph.edges[connection[0], connection[1]]['color'] = col


        pos = nx.circular_layout(nxgraph)
        plt.figure(figsize=(10, 7))
        edge_colors_for_drawing = [nxgraph.edges[edge]['color'] for edge in nxgraph.edges]
        nx.draw(nxgraph, pos, with_labels=True, edge_color=edge_colors_for_drawing, node_color=node_colors, font_size=10, alpha=0.7)

    def get_connections(self):
        return self._connections.copy()
