import unittest
from unittest.mock import patch

from graph_game.data_structures.graph import Graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        """initialize graph object"""
        self.graph = Graph(init_num_nodes=10, add_num_edges=5, edge_sd=5, edge_mean=10)

    def test_graph_initialization(self):
        """Test graph initialization"""
        self.assertEqual(self.graph.num_nodes, 10)
        self.assertGreaterEqual(self.graph.num_edges, 9)

    def test_add_edge(self):
        """Test add edge and validate graph"""
        initial_edges = self.graph.num_edges
        self.graph.add_edge_to_graph(1, 3)
        self.assertEqual(self.graph.num_edges, initial_edges + 1)
        self.assertTrue((1, 3) in self.graph.G.edges() or (2, 3) in self.graph.G.edges())

    def test_add_edge_invalid_edge(self):
        """Test add edge with invalid"""
        with self.assertRaises(ValueError):
            self.graph.add_edge_to_graph(100, 200)

    def test_shortest_path(self):
        """Test shortest path algorithm"""
        path = self.graph.shortest_path(1, 2)
        self.assertIsInstance(path, int)
        self.assertGreater(path, 0)

    def test_random_nodes_edge(self):
        """Test random nodes and edges generator"""
        self.graph.generate_random_nodes(num=2)
        self.assertEqual(self.graph.num_nodes, 12)
        self.graph.generate_random_edges(num=1)
        self.assertGreaterEqual(self.graph.num_edges, 10)

    def test_graph_str_repr(self):
        """Test graph string representation"""
        graph_str = str(self.graph)
        self.assertIn('|E| =', graph_str)
        self.assertIn('|V| =', graph_str)
        self.assertIn('E.x̄ =', graph_str)
        self.assertIn('E.σ =', graph_str)

if __name__ == '__main__':
    unittest.main()




