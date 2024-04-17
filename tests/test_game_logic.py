import unittest
from graph_game.game_logic  import GraphGame, RandomScoreGenerator

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        """Start the game logic."""
        self.game = GraphGame.random_start()
        self.game.set_base_score(100)
        self.game.set_starting_node(1)
        self.game.set_ending_node(4)

    def test_set_base_score(self):
        """Test the set_base_score function."""
        self.assertEqual(self.game.base_score, 100)
        with self.assertRaises(ValueError):
            self.game.set_base_score('one hundred')




