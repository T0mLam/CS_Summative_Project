from typing import Tuple, List
import random as rand


class RandomisedSet:
    """A randomised set which enables the insertion, deletion and random extraction of edges in O(1) (constant) time.

    Attributes:
        edges: A list storing non-duplicate edges that are not connected in the graph.
        edge_to_idx: A hashmap mapping the edges to the indices they are stored in the edges list.

    Methods:
        add_edges_from_node: Add available edges connected to all nodes from the input node.
        add_edge_to_set: Add an edge to the randomised set.
        remove_edge_from_set: Remove an edge from the randomised set.
        get_random_edge: Extract a random available edge.
    """

    def __init__(self) -> None:
        """Construct the attributes of the set."""
        self.edges = []
        self.edge_to_idx = {}

    def __contains__(self, item: Tuple[int, int]) -> bool:
        """Enable the use of membership test operators (in & not in) for the class.

        Args:
            item: A tuple to be checked whether it is contained in the edges set.

        Returns:
            True if the edge is found, false otherwise.
        """
        idx1, idx2 = item
        return (idx1, idx2) in self.edge_to_idx or (idx2, idx1) in self.edge_to_idx

    def add_edges_from_node(self, idx: int, nodes: List[int]) -> None:
        """Add outcoming edges to the set from a new node.
        
        For example:
        idx: 5
        nodes: [1, 3, 7, 8]
        # New edges created: (1, 5), (3, 5), (5, 7), (5, 8)

        Notes: 
            Adding n edges in O(n) time, where n = num of input nodes.
            Amortized time complexity for adding an edge: O(1).

        Args:
            idx: The index of the new node.
            nodes: The indices of the existing nodes.

        Raises:
            TypeError: Errors caused by incompatible input data type of 'idx' and 'nodes'.
        """
        # Check data types of parameters 'idx' and 'nodes'
        if not isinstance(idx, int):
            raise TypeError("The input parameter 'idx' must be an integer")
        if (not isinstance(nodes, list) or 
            not all([isinstance(node, int) for node in nodes])):
            raise TypeError("The input parameter 'nodes' must be a list of integers")

        # Add the new edges to the set
        for node_idx in nodes:
            # Skip to the next iteration if the index of starting node = ending node
            if node_idx == idx:
                continue
            # Format the new edge as (u, v), where u < v
            mn, mx = min(idx, node_idx), max(idx, node_idx)
            new_edge = (mn, mx)

            # Check whether the new edge exists
            if new_edge not in self.edge_to_idx:
                # If not, add it to the list and map the edge to its indices in the list
                self.edge_to_idx[new_edge] = len(self.edges)
                self.edges.append(new_edge)

    def add_edge_to_set(self, idx1: int, idx2: int) -> None:
        """Add an edge to the randomised set.

        Args:
            idx1: Index of the first node.
            idx2: Index of the second node.

        Raises:
            TypeError: Error occurs if the node indices are not integers.
            ValueError: Error occurs if the node indices are out of bounds.
        """
        # Check if indices are integers
        if not isinstance(idx1, int) or not isinstance(idx2, int):
            raise TypeError("Node indices must be integers.")

        # Check if indices are greater than 0
        if idx1 < 1 or idx2 < 1:
            raise ValueError("Node indices must be positive.")
        
        # making sure idx1 is less than idx2 to maintain consistency
        idx1, idx2 = min(idx1, idx2), max(idx1, idx2)
        new_edge = (idx1, idx2)

        if new_edge not in self.edge_to_idx:
            self.edge_to_idx[new_edge] = len(self.edges)
            self.edges.append(new_edge)

    def remove_edge_from_set(self, idx1: int, idx2: int) -> None:
        """Remove an edge from the set.

        Args:
            idx1: Index of the first node.
            idx2: Index of the second node.

        Raises:
            TypeError: Error occurs if the node indices are not integers.
            ValueError: Error occurs if the edge does not exist.
        """
        # Check if indices are integers
        if not isinstance(idx1, int) or not isinstance(idx2, int):
            raise TypeError("Node indices must be integers.")

        # Check if indices exist in the set
        removing_edge = (min(idx1, idx2), max(idx1, idx2))
        if removing_edge not in self.edge_to_idx:
            raise ValueError("The edge does not exist in the set") 
        
        # Get the indices of the edge to be removed and the last edge in the list
        removing_edge_index = self.edge_to_idx[removing_edge]
        last_edge = self.edges[-1]
        last_edge_index = self.edge_to_idx[last_edge]

        # Replace the edge to be removed with the last edges and change the corresponding index in the node map
        self.edge_to_idx[last_edge] = removing_edge_index
        self.edges[removing_edge_index] = last_edge

        # Remove the last entry in the edges list and delete the index map for the removed edge 
        self.edges.pop()
        del self.edge_to_idx[removing_edge]

    def get_random_edge(self) -> Tuple[int, int]:
        """Extract and remove a random available edge from the set.

        Returns:
            A tuple consists of the start and end of the edge. For example: (1, 2).
        """
        if not self.edges:
            return
        edge_idx = rand.randint(0, len(self.edges) - 1)
        edge = self.edges[edge_idx]
        self.remove_edge_from_set(*edge)
        return edge
