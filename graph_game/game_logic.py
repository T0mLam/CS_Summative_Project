from __future__ import annotations
from typing import List
import random as rand

from graph import Graph


class GraphGame(Graph):
    """A subclass inherited from the Graph class which handles the operation and the winning conditions of the game.

    Attributes:
        starting_node: An integer index of the starting node defined by the user.
        ending_node: An integer index of the ending node defined by the user.

    Methods:
        set_starting_node: A setter method for the starting node.
        set_ending_node: A setter method for the ending node.
    """

    def __init__(self,
                 init_num_nodes: int = 0, 
                 init_num_edges: int = 0) -> None:
        """Construct the attributes of the graph.

        Args:
            init_num_nodes: Number of randomly generated nodes during initialization.
            add_num_edges: Number of additional randomly generated edges, after 
                           generating n - 1 edges to connect all nodes, n = init_num_nodes.
        """
        super().__init__(init_num_nodes, init_num_edges)
        self.starting_node = None
        self.ending_node = None

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
        
        # add node color change here ...

        self.starting_node = idx

    def set_ending_node(self, idx: int) -> None:
        """A setter method for the ending_node attribute.

        Args:
            idx: A integer index of the node to be set as the ending node.
        
        Raises:
            TypeError: Error caused by non-integer parameter input.
            ValueError: Error caused by non-existing node parameter input.
        """
        if not isinstance(idx, int):
            raise TypeError("Input parameters 'idx' must be an integer")
        if idx not in self.node_map:
            raise ValueError("The node with index 'idx' does not exist in the graph") 
        
        self.ending_node = idx

    def calculate_node_scores(self) -> List[float]:
        pass

    def generate_cutoff(self) -> int:  
        pass

    def check_player_wins(self) -> bool:
        pass

    @classmethod
    def random_start(cls) -> type[GraphGame]:
        """An alternative initization method which generates a new game with a random graph.

        Returns:
            A GraphGame object with random nodes and weighted edges.

        To instantiate:
            game = GraphGame.new_game()
        """
        init_num_nodes = rand.randint(8, 12)
        add_num_edges = init_num_nodes // rand.randint(2, 3)
        return cls(init_num_nodes, add_num_edges)


if __name__ == '__main__':
    game = GraphGame.random_start()
    game.node_map.keys()
    game.graph_visualize()