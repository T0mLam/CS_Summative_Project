
import unittest
from graph_game.utils.trie import  Trie, TrieNode

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        words = ["apple", "hello", "goodbye", "warwick", "warw", "warwi", "warwic"]
        for word in words:
            self.trie.insert(word)

    def test_insert_and_find(self):
        """Test insert and find"""
        self.assertTrue(self.trie.find("apple"))
        self.assertFalse(self.trie.find("UK"))

    def test_complete(self):
        """Test the complete_function"""
        self.assertIn('warwick', self.trie.complete('warw'))
        self.assertNotIn('apple', self.trie.complete('warw'))

    def test_fizzy_search(self):
        """Test the fizzy_search function"""
        self.assertIn('warwi', self.trie.fizzy_search('warwi', 1))
        self.assertIn('warwic', self.trie.fizzy_search('warwi', 1))
        self.assertNotIn('warwick', self.trie.fizzy_search('warwi', 1))


if __name__ == '__main__':
    unittest.main()



