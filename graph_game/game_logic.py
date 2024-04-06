from graph import Graph

class GraphGame(Graph):
    """
    A subclass inherited from the Graph class which handles the operation and the winning conditions of the game.

    Attributes:
        starting_node: An integer index of the starting node defined by the user.
        ending_node: An integer index of the ending node defined by the user.

    Methods:
        set_starting_node: A setter method for the starting node.
        set_ending_node: A setter method for the ending node.
    """

    def __init__(self, init_num_nodes: int = 0, init_num_edges: int = 0) -> None:
        super().__init__(init_num_nodes, init_num_edges)
        self.starting_node = None
        self.ending_node = None

    def set_starting_node(self, idx: int) -> None:
        """
        A setter method for the starting_node attribute.

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
        pass