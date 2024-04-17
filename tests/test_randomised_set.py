import random
import unittest

from graph_game.utils.randomised_set import RandomisedSet


class TestRandomisedSet(unittest.TestCase):
    def setUp(self):
        """INITIALIZE a RandomisedSet object"""
        self.randomised_set = RandomisedSet()
        random.seed(0)

    def test_initialization(self):
        """The edges and edge_to_idx of the RandomisedSet should be empty"""
        self.assertFalse(self.randomised_set.edges)
        self.assertFalse(self.randomised_set.edge_to_idx)

    def test_add_edge(self):
        """Add an edge to the RandomisedSet"""
        self.randomised_set.add_edge_to_set(1, 2)
        self.assertEqual(self.randomised_set.edges, [(1, 2)])
        self.assertEqual(self.randomised_set.edge_to_idx, {(1, 2): 0})

    def test_remove_edge(self):
        """Remove an edge from the RandomisedSet"""
        self.randomised_set.add_edge_to_set(1, 2)
        self.randomised_set.remove_edge_from_set(1, 2)
        self.assertNotIn((1, 2),self.randomised_set.edge_to_idx)
        self.assertFalse(self.randomised_set.edges)

    def test_add_duplicate_edges(self):
        """Can not add duplicate edges to the RandomisedSet"""
        self.randomised_set.add_edge_to_set(1, 2)
        self.randomised_set.add_edge_to_set(2, 1)
        self.assertEqual(len(self.randomised_set.edges), 1)

    def test_random_edge(self):
        """Random edge extraction should correctly remove the edge from the set."""
        edges_to_add = [(1, 2), (3, 4)]
        for edge in edges_to_add:
            self.randomised_set.add_edge_to_set(*edge)
        extracted_edges = self.randomised_set.get_random_edge()
        self.assertIn(extracted_edges, edges_to_add)
        self.assertEqual(len(self.randomised_set.edges), 1)
        self.assertNotIn(extracted_edges, self.randomised_set.edge_to_idx)


if __name__ == '__main__':
    unittest.main()








