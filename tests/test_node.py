import unittest
from graph_game.data_structures.node import Node


class TestNode(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(1)
        self.node2 = Node(2)
        self.node3 = Node(3)

    def test_node_creation(self):
        """Tests whether the node is created correctly"""
        self.assertEqual(self.node1.idx, 1)
        self.assertEqual(self.node2.idx, 2)

    def test_add_edge(self):
        """Testing the neighbor addition function"""
        self.node1.add_neighbour(self.node2, 10)
        self.assertIn(self.node2, self.node1.neighbours)
        self.assertEqual(self.node1.neighbours[self.node2], 10)

        with self.assertRaises(TypeError):
            self.node1.add_neighbour("not_a_node", 5)
        with self.assertRaises(TypeError):
            self.node1.add_neighbour(self.node3,"not_a_number")

    def test_node_comparison(self):
        """Testing the node comparison function"""
        self.assertTrue(self.node1 < self.node2)
        self.assertFalse(self.node1 > self.node2)

    def test_get_index(self):
        """Testing gets the index of the node"""
        self.assertEqual(self.node1.get_index(), 1)

    def test_get_neighbours(self):
        """Testing gets the neighbours of the node"""
        self.node1.add_neighbour(self.node2, 10)
        self.node1.add_neighbour(self.node3, 5)
        expected_neighbours = [(self.node2, 10), (self.node3, 5)]
        actual_neighbours = list(self.node1.neighbours.items())
        self.assertEqual(sorted(actual_neighbours, key=lambda x: x[0].idx),
                         sorted(expected_neighbours, key=lambda x: x[0].idx))


if __name__ == '__main__':
    unittest.main()