import unittest
from unittest.mock import MagicMock, patch
from graph_game.search_engine.search_engine import SearchEngine


class TestSearchEngine(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.search_engine = SearchEngine()
        self.search_engine.trie = MagicMock()
        self.search_engine.fetch_all_users_to_trie = MagicMock()

    def test_complete_search(self):
        """Test the complete search method"""
        self.search_engine.trie.complete = MagicMock(return_value=["Femi", "Femu", "Femo"])
        result = self.search_engine.complete_search("Fem")
        self.assertEqual(result, ["Femi", "Femu", "Femo"])
        self.search_engine.trie.complete.assert_called_with("Fem")

    @patch('graph_game.search_engine.search_engine.DatabaseConnection')
    def test_search_results(self, mock_db):
        """Test the search results method"""
        mock_conn = mock_db.return_value.__enter__.return_value
        mock_conn.cursor.return_value.execute.return_value.fetchone.return_value = ("Femi", 100)
        mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = [("Femi", 100)]
        self.search_engine.trie.fizzy_search = MagicMock(return_value=["Femi"])

        result = self.search_engine.search_results("Femi")
        self.assertEqual(result, [("Femi", 100)])

    @patch('graph_game.search_engine.search_engine.DatabaseConnection')
    def test_get_leaders(self, mock_db):
        """Test the get_leaders method"""
        mock_conn = mock_db.return_value.__enter__.return_value
        mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = [("Femi", 100), ("Tom", 90)]
        result = self.search_engine.get_leaders(2)
        self.assertEqual(result, [("Femi", 100), ("Tom", 90)])
        self.assertRaises(ValueError, self.search_engine.get_leaders, 0)

    def test_fetch_all_users_to_trie(self):

        """Test the fetch_all_users_to_trie method"""
        self.search_engine.trie = None
        self.trie = MagicMock()
        with patch('graph_game.search_engine.search_engine.DatabaseConnection') as mock_db:
            mock_conn = mock_db.return_value.__enter__.return_value
            mock_conn.cursor.return_value.execute.return_value.fetchall.return_value = [("Femi",), ("Tom",)]
            self.search_engine.fetch_all_users_to_trie()
            self.assertIsNotNone(self.search_engine)


if __name__ == '__main__':
    unittest.main()
