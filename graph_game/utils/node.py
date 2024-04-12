from __future__ import annotations
from typing import List, Tuple


class Node:
    """Creation of a Node class to represent nodes in the graph data structure."""

    def __init__(self, idx: int) -> None:
        """Initializes a Node object with the parameter value.

        Args:
            idx (int): This are the values associated with the node.
        """
        self.idx = idx
        self.neighbours = {}  # A dictionary to keep the neighbours and their weight

    def __lt__(self, other: type[Node]) -> bool:
        """Compares two nodes based on their values.

        Args:
            other (Node): Another node in the graph to compare with.

        Returns:
            True if the value of the other node is greater than the value of the this node, False otherwise.
        """
        return self.idx < other.idx

    def add_neighbour(self, neighbour: type[Node], weight: int | float) -> None: 
        """Adds a neighbour to the nodes in the graph with an associated weight.

        Args:
            neighbour (Node): Neighbour node to be added.
            weight (int, float): the Weight of the edge connecting the neighbour to the node.
            
        Raises:
            TypeError: If neighbour is not an instance of Node in the graph or if the weight inputed is not numeric (eg" writing a word instead of a number").
        """
        if not isinstance(neighbour, Node):
            raise TypeError("Neighbour must be an instance of Node.")
        if not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a numeric value.")
        
        self.neighbours[neighbour] = weight

    def get_index(self) -> int:
        """A getter method for the idx attribute.

        Returns:
            An integer index of the node.
        """
        return self.idx
    
    def get_neighbours(self) -> List[Tuple[int, int]]:
        """A getter method for the neighbours attribute.

        Returns:
            A List of tuples (idx, wei) consist of the index (idx) and the weight (wei) of each node.
        """
        return self.neighbours.items()