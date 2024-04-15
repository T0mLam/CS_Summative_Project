from __future__ import annotations
from typing import List
import random as rand
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from .graph import Graph
from .score_generation import RandomScoreGenerator 


class GraphGame(Graph):
    """A subclass inherited from the Graph class which handles the operation and the winning conditions of the game.

    Attributes:
        score_generator: An instance of the RandomScoreGenerator class used for generating scores for each node.
        starting_node: An integer index of the starting node defined by the user.
        ending_node: An integer index of the ending node defined by the user.
        cutoff_distance: The random distance generated by RandomScoreGenerator to determine the game outcome.
        base_score: An integer base score of the game.

    Methods:
        get_nodes: A getter method for all node indcies in the graph.
        set_base_score: A setter method for the base_score attribute.
        set_starting_node: A setter method for the starting node.
        set_ending_node: A setter method for the ending node.
        generate_cutoff: Generate and store the random distance in the cutoff_distance variable.
        calculate_node_scores: Calculate the score of each nodes based on its distance and update the plot.
        check_player_wins: Check whether the player wins.
        random_start: A classmethod for generating a random game.
    """

    def __init__(self,
                 init_num_nodes: int = 0, 
                 init_num_edges: int = 0) -> None:
        """Construct the attributes of the graph.

        Args:
            init_num_nodes (int): Number of randomly generated nodes during initialization.
            add_num_edges (int): Number of additional randomly generated edges, after 
                           generating n - 1 edges to connect all nodes, n = init_num_nodes.
        """
        super().__init__(init_num_nodes, init_num_edges)
        self.score_generator = None
        self.starting_node = None
        self.ending_node = None
        self.cutoff_distance = None
        self.base_score = None

    def get_nodes(self) -> List[int]:
        """The method for getting the list of nodes in the graph which is needed for tkinter combobox.

        Returns: 
            The list of nodes in the graph.
        """
        return sorted(list(self.node_map.keys()))

    def set_base_score(self, score: int) -> None:
        """A setter method for the base_score attribute.

        Args:
            score (int): A integer to be set as the base score.
        
        Raises:
            TypeError: Error caused by non-integer parameter input.
        """
        if not isinstance(score, int):
            raise TypeError("Input parameters 'score' must be an integer")
        
        self.base_score = score
        self.score_generator = RandomScoreGenerator(base_score=score)

    def set_starting_node(self, idx: int) -> None:
        """A setter method for the starting_node attribute.

        Args:
            idx: A integer index of the node to be set as the starting node.
        
        Raises:
            TypeError: Error caused by non-integer parameter input.
            ValueError: Error caused by non-existing node parameter input.
        """
        if not isinstance(idx, int):
            raise TypeError("Input parameters 'idx' must be an integer")
        if idx not in self.node_map:
            raise ValueError("The node with index 'idx' does not exist in the graph") 

        self.starting_node = idx

    def set_ending_node(self, idx: int) -> None:
        """A setter method for the ending_node attribute.

        Args:
            idx (int): A integer index of the node to be set as the ending node.
        
        Raises:
            TypeError: Error caused by non-integer parameter input.
            ValueError: Error caused by non-existing node parameter input.
        """
        if not isinstance(idx, int):
            raise TypeError("Input parameters 'idx' must be an integer")
        if idx not in self.node_map:
            raise ValueError("The node with index 'idx' does not exist in the graph") 
        
        self.ending_node = idx

    def generate_cutoff(self) -> None: 
        """ Generate and store the random distance in the cutoff_distance variable.
        
        Raises:
            NameError: if the score_generator has not been defined.
        """
        if not self.score_generator:
            raise NameError('The score_generator has not been defined')

        # Get the shortest distances from the starting node to all other nodes
        node_to_dist = self.shortest_path(starting_node=self.starting_node)
        dist_values = list(node_to_dist.values())

        # Calculate the mean and sd of the shortest distances using the numpy library
        mean_dist = int(np.mean(dist_values))
        sd_dist = np.std(dist_values)

        # Configure the mean and sd of the score_generator
        self.score_generator.set_mean(mean_dist)
        self.score_generator.set_sd(sd_dist)

        # Generate a random distance
        self.cutoff_distance = self.score_generator.generate_random_distance()

    def calculate_node_scores(self) -> None:
        """Calculate the score of each nodes based on its distance and update the plot.
        
        Raises:
            NameError: if the score_generator or the starting node have not been defined.
        """
        if not self.starting_node or not self.score_generator:
            raise NameError('The score_generator or the starting node have not been defined.')

        # Get the shortest distances from the starting node to all other nodes
        node_to_dist = self.shortest_path(starting_node=self.starting_node)

        # Map the distance to each node to its score using the score_generator
        for node, dist in node_to_dist.items():
            node_to_dist[node] = self.score_generator.calculate_score(dist)

        # Create score labels for the networkx graph visualization
        label_pos = {}
        for node, coords in self.node_position.items():
            # Set the label to be 0.135 units above the original node position
            label_pos[node] = (coords[0], coords[1] + 0.135)

        nx.draw_networkx_labels(self.G, 
                                pos=label_pos,
                                labels=node_to_dist,
                                font_size=10, 
                                font_weight='bold')
        
    def check_player_wins(self) -> bool:
        """Check whether the player wins.
        
        Returns:
            True if the player wins, false otherwise.

        Raises:
            NameError: Error raised if the starting_node, ending_node or cutoff_distance have not been defined.
        """
        if (not self.starting_node or not self.ending_node):
            raise NameError('The starting node and ending node have not been defined')
        if self.cutoff_distance is None:
            raise NameError('The generate_cutoff method has to be called before this method')
        
        # Find the shortest distance between the starting node and the ending node
        shortest_dist = self.shortest_path(self.starting_node, self.ending_node)

        # Return a boolean of whether the player wins
        return shortest_dist < self.cutoff_distance
    
    def get_player_score(self) -> int:
        """Get the score awarded for the player for the current round.

        Returns:
            An integer representing the score.

        Raises:
            NameError: Error raised if the starting_node, ending_node or cutoff_distance have not been defined.
        """
        if (not self.starting_node or not self.ending_node):
            raise NameError('The starting node and ending node have not been defined')
        if self.cutoff_distance is None:
            raise NameError('The generate_cutoff method has to be called before this method')

        # Find the shortest distance between the starting node and the ending node
        shortest_dist = self.shortest_path(self.starting_node, self.ending_node)

        # Generate the potential score of the player based on the distance
        score = self.score_generator.calculate_score(shortest_dist)

        # Return the calculated score if the player wins, otherwise return negative base score which indicates a loss
        return score if self.check_player_wins() else -self.base_score

    @classmethod
    def random_start(cls) -> type[GraphGame]:
        """An alternative initization method which generates a new game with a random graph.

        Returns:
            A GraphGame object with random nodes and weighted edges.

        To instantiate:
            game = GraphGame.random_start()
        """
        init_num_nodes = rand.randint(8, 10)
        add_num_edges = init_num_nodes // rand.randint(2, 3)
        return cls(init_num_nodes, add_num_edges)

if __name__ == '__main__':
    game = GraphGame.random_start()
    #print(game.get_node_numbers())
    game.set_base_score(100)
    
    game.set_starting_node(1)
    game.generate_cutoff()
    game.calculate_node_scores()
    game.set_ending_node(4)
    print(game.check_player_wins())
    print(game.get_player_score())
    game.graph_visualize(with_labels=False)

    