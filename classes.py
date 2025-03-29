"""CSC111 Project 2:
Top Hoops: NBA Optimal Basketball Lineup
Abdullah Alhidary, Houssam Yaacoub, Justin Peng, Muhammad Rafie

This module contains the necessary classes and methods required for this project.
Contains:
- _Player: 'Vertex' of our graph
- _Connection: 'Edge' representation as a class
- Graph: Graph whose vertices are _Player and ddges are _Connection

This file also contains the method that creates the graph showing all the interactions between players
as well as the optimal lineup in the graph.
"""
from __future__ import annotations
from typing import Optional

import networkx as nx
import matplotlib.pyplot as plt

CENTER_WEIGHTS = {'points': 1, 'rebound': 1.5, 'blocks': 1, 'steals': 1, 'assists': 1.1}
FORWARD_WEIGHTS = {'points': 1.3, 'rebound': 1.3, 'blocks': 1, 'steals': 1.1, 'assists': 1.3}
GUARD_WEIGHTS = {'points': 1.6, 'rebound': 0.9, 'blocks': 0.7, 'steals': 1.6, 'assists': 1.7}

POSITION_WEIGHTS = {"Center": CENTER_WEIGHTS, "Forward": FORWARD_WEIGHTS, "Guard": GUARD_WEIGHTS}


class _Player:
    """ Player class representing the statistics of each player.
    Analogous to the _vertex class in a graph.

    Instance Attributes:
        - name: Name of player
        - team: The team the player is on
        - position: A list of the positions this player plays
        - avg_points: The average amount of points this player scores in a minute
        - avg_rebounds: The average amount of rebounds this player has in a minute
        - avg_assists: The average amount of assists this player has in a minute
        - avg_steals: The average amount of steals this player has in a minute
        - avg_blocks: The average amount of blocks this player has in a minute
        - minutes: The total number of minutes this player has played
        - player_impact_estimate: A rating of the player based on their average statistics and weights
        - connections: A list of _Connection classes this player is a part of

    Representation Invariants:
        - self.avg_points >= 0
        - self.avg_rebounds >= 0
        - self.avg_assists >= 0
        - self.avg_steals >= 0
        - self.avg_blocks >= 0
        - self.minutes >= 0

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

    def __init__(self, name: str, team: str, position: list[str], points: float, rebounds: float, assists: float,
                 minutes: int, steals: float, blocks: float) -> None:
        """
        Initialize a new _Player class with given name, team, position, points, rebounds, assists, minutes, steals
        and blocks.

        Then calculate with in-class methods avg_points, avg_rebounds, avg_assists, avg_steals, avg_blocks, and
        player_impact_estimate

        Leave this player connections empty.

        Preconditions:
            - points >= 0
            - rebounds >= 0
            - assists >= 0
            - minutes >= 0
            - steals >= 0
            - blocks >= 0
        """
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
        """Compute the Player Impact Estimate using positional weights given in the header
        of classes.py file."""
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
    """ A class connecting two _Player classes and representing their shared statistics.
    Analogous to a class representation of an 'edge'.

    Instance Attributes:
        - player_connection: A list containing the two _Player classes of the two connected players
        - player1_avg_assists_per_pass: The average amount of assist per pass player 1 has passing to player 2
        - player2_avg_assists_per_pass: The average amount of assist per pass player 2 has passing to player 1
        - max_avg_assists_per_pass: The maximum value of the avg_assists_per_pass of both player 1 and 2
        - avg_passes_per_minute_player1: The average amount of passes per minute player 1 makes to player 2
        - avg_passes_per_minute_player2: The average amount of passes per minute player 2 makes to player 1
        - synergy_score: Average of both players player_impact_estimate attribute



    Representation Invariants:
        - len(self.player_connection) == 2
        - self.player1_avg_assists_per_pass >= 0
        - self.player2_avg_assists_per_pass >= 0
        - self.max_avg_assists_per_pass >= 0
        - self.avg_passes_per_minute_player1 >= 0
        - self.avg_passes_per_minute_player2 >= 0

    """
    player_connection: list[_Player]
    player1_avg_assists_per_pass: Optional[float]
    player2_avg_assists_per_pass: Optional[float]
    max_avg_assists_per_pass: Optional[float]
    avg_passes_per_minute_player1: float
    avg_passes_per_minute_player2: float
    synergy_score: float

    def __init__(self, player1: _Player, player2: _Player) -> None:
        """
        Initializes a new _Connection class. Takes in two _Player classes player1 and player2.

        All attributes except for synergy_score are set to zero.

        Note: We designate which player is player1 and player2. This is for the sake of keeping track of
        passing statistics which could be different between players. For example, assists per pass for player1
        and player2 could be different if one player scores more assists per pass given.
        """
        self.player_connection = [player1, player2]
        self.player1_avg_assists_per_pass = 0
        self.player2_avg_assists_per_pass = 0
        self.synergy_score = self.calculate_synergy_score()

    def tweak_stats(self, player: _Player, assist: [int, float], passes: [int, float],
                    minutes_together: [int, float]) -> None:
        """
        Determine if given _Player class is player1 or player2 of _Connection class.
        Then change instance attributes as needed.

        Preconditions:
            - not (minutes_together == 0) or (assist == 0 and passes == 0)
        """
        # Check if this is player 1
        if self.player_connection[0] == player:
            self.player1_avg_assists_per_pass = round(assist/passes, 3)
            self.avg_passes_per_minute_player1 = round(passes / minutes_together, 3)
        # This is player 2
        else:
            self.player2_avg_assists_per_pass = round(assist/passes, 3)
            self.avg_passes_per_minute_player2 = round(passes / minutes_together, 3)

    def finalize_stats(self) -> None:
        """
        Finalize the _Connection class by taking the maximum of avergae assits per pass of both players
        and assigning that value to max_avg_assists_per_pass.
        """
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

        Preconditions:
            - player_name in [p.name for p in self.player_connection]
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
    #     - _connections: A mapping of a tuple containing the names of two connected players to a _Connection
    #                       class containing the _Player class of the two connected players
    _players: dict[str, _Player]
    _connections: dict[tuple[str, str], _Connection]

    def __init__(self) -> None:
        """
        Initializes and empty Graph with dictionaries _players and _connections being empty.
        """
        self._players = {}
        self._connections = {}

    def add_player(self, player: _Player) -> None:
        """
        If _Player class name is not in self._players dictionary,
        create a mapping between _Player name and the _PLayer class itself.

        >>> p = _Player("Bob", "LAL", ["Center"], 5, 5, 5, 5, 5, 5)
        >>> g = Graph()
        >>> g.add_player(p)
        >>> p.name in g._players
        True
        """
        if player.name not in self._players:
            self._players[player.name] = player

    def add_connection(self, player1: _Player, player2: str, assist: [int, float], passes: [int, float],
                       minutes_together: [int, float]) -> None:
        """
        Adds connection between two players using the _Connection class

        Preconditions:
            - player2 in self._players
        """
        if not self.check_exists(player1.name, player2):
            new_connection = _Connection(player1, self._players[player2])
            self._connections[(player1.name, player2)] = new_connection

        connection_key = self.get_connection_key(player1.name, player2)
        self._connections[connection_key].tweak_stats(player1, assist, passes, minutes_together)

    def check_exists(self, player1_name: str, player2_name: str) -> bool:
        """
        Check whether the tuple (player1_name, player2_name) or (player2_name, player1_name) exists
        in self._connections as a key.

        Preconditions:
            - player1_name in self._players and player2_name in self._players
        """
        keys = self._connections.keys()
        return (player1_name, player2_name) in keys or (player2_name, player1_name) in keys

    def __str__(self) -> str:
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

        Preconditions:
            - player1_name in self._players
            - all([player in self._players for player in player_names])
        """
        pass_data = {}
        for player2_name in player_names:
            curr_key = self.get_connection_key(player1_name, player2_name)
            pass_data[player2_name] = self._connections[curr_key].get_avg_passes_per_minute(player1_name)
        print(pass_data)
        return pass_data

    def get_connection_key(self, player1_name: str, player2_name: str) -> tuple[str, str]:
        """
        Returns the key in self._connections associated with the given player1_name and player2_name

        Preconditions:
            - player1_name in self._players and player2_name in self._players
        """
        if (player1_name, player2_name) in self._connections:
            return (player1_name, player2_name)
        else:
            return (player2_name, player1_name)

    def visualize_graph(self, ideal_lineup: list[_Player]) -> None:
        """
        Function creates a graph and returns it.
        Each player's name is self._players is a blue color nodes. If player name
        is in ideal_lineup, the node is colored blue.

        Each connection is drawn as an edge in the graph.
        If connection synergy score is above 1.75: it is colored green
        If it is between 0.75 and 1.75: it is colored purple
        If it is below 0.75: it is colored dark red
        """
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

    def get_connections(self) -> dict:
        """
        Return a copy of this instance _connections attributes.

        >>> a = Graph()
        >>> a.get_connections() == {}
        True
        """
        return self._connections.copy()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 200,
        'extra-imports': ['networkx', 'matplotlib.pyplot'],
        'disable': ['E9998', 'R0914', 'R0902', 'R0913', 'E9959', 'C0201', 'E9972', 'E9989']
    })
