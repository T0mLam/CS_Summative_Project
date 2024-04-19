import unittest

from graph_game.data_structures.heap import MinHeap
from graph_game.data_structures.node import Node


class TestHeap(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.nodes = [Node(i) for i in range(10)]

    def test_init_heap(self):
        """Test initializing heap"""
        heap = MinHeap([(3, self.nodes[3]), (1, self.nodes[1]), (2, self.nodes[2])])
        self.assertEqual(heap.pop()[0],1)
        self.assertEqual(heap.pop()[0],2)
        self.assertEqual(heap.pop()[0],3)

    def test_push_pop(self):
        """Test push and pop to the heap"""
        heap = MinHeap()
        heap.push((2, self.nodes[2]))
        heap.push((1, self.nodes[1]))
        heap.push((3, self.nodes[3]))
        self.assertEqual(heap.pop()[0], 1)
        self.assertEqual(heap.pop()[0], 2)
        self.assertEqual(heap.pop()[0], 3)

    def test_heap_property(self):
        """Test heap property"""
        heap = MinHeap()
        values = [1,2,3,4,5,6,7,8,9]
        for value in values:
            heap.push((value, Node(value)))
        result = []
        while len(heap) > 0:
            result.append(heap.pop()[0])
        self.assertEqual(result, sorted(values))

    def test_top(self):
        """Test the top element of the heap"""
        heap = MinHeap([(2, self.nodes[2]), (1, self.nodes[1]), (3, self.nodes[3])])
        self.assertEqual(heap.top()[0], 1)

    def test_empty_heap(self):
        """Test empty heap"""
        heap = MinHeap()
        self.assertIsNone(heap.top())
        self.assertIsNone(heap.pop())

    def test_duplicate(self):
        """Test duplicates into heap"""
        heap = MinHeap([(2, self.nodes[0]),(2, self.nodes[1]), (2, self.nodes[2])])
        heap.push((2, self.nodes[4]))
        heap.push((1, self.nodes[3]))
        self.assertEqual(heap.top()[0],1)
        heap.pop()
        for _ in range(4):
            self.assertEqual(heap.top()[0],2)
            heap.pop()

    def test_mixed_heap(self):
        """Test mixed situation"""
        heap = MinHeap()
        values = [(2, self.nodes[2]), (1, self.nodes[1]), (3, self.nodes[3])]
        for val in values:
            heap.push(val)
        self.assertEqual(heap.pop()[0],1)
        heap.push((0, self.nodes[0]))
        self.assertEqual(heap.pop()[0],0)


if __name__ == '__main__':
    unittest.main()


