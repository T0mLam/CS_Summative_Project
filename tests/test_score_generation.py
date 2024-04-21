import numpy as np
import scipy.stats as stats
import unittest
from unittest.mock import patch

from graph_game.game.score_generation import RandomScoreGenerator


class TestRandomScoreGenerator(unittest.TestCase):
    def setUp(self):
        """set up the test case"""
        self.generator = RandomScoreGenerator()

    def test_init(self):
        """Test the __init__ method."""
        self.assertEqual(self.generator.base_score, 100)
        self.assertIsNone(self.generator._mean)
        self.assertIsNone(self.generator._sd)
        self.assertIsNone(self.generator._generated_distance)

    def test_set_mean_raises_value_error(self):
        """Test set_mean method raises a ValueError"""
        with self.assertRaises(ValueError):
            self.generator.set_mean(-1)
        with self.assertRaises(ValueError):
            self.generator.set_mean(1.1)

    def test_set_mean(self):
        """Test set_mean"""
        self.generator.set_mean(1)
        self.assertEqual(self.generator._mean, 1)

    def test_set_sd_raises_value_error(self):
        """Test set_sd method raises a ValueError"""
        with self.assertRaises(ValueError):
            self.generator.set_sd(-1)
        with self.assertRaises(ValueError):
            self.generator.set_sd("10")

    def test_set_sd(self):
        """Test set_sd correctly sets the sd"""
        self.generator.set_sd(5.0)
        self.assertEqual(self.generator._sd, 5.0)

    @patch('numpy.random.normal')
    def test_generate_random_distance(self, mock_normal):
        """Test generate_random_distance"""
        mock_normal.return_value = 5
        self.generator.set_mean(10)
        self.generator.set_sd(2)
        distance = self.generator.generate_random_distance()
        self.assertEqual(distance, 5)

    def test_generate_random_distance_raises_value_error(self):
        """Test generate_random_distance raises ValueError"""
        with self.assertRaises(ValueError):
            self.generator.generate_random_distance()
        self.generator.set_mean(10)
        with self.assertRaises(ValueError):
            self.generator.generate_random_distance()

    @patch('numpy.random.normal')
    def test_calculate_score(self, mock_normal):
        """Test calculate_score calculates correctly."""
        mean = 10
        sd = 5
        self.generator.set_mean(mean)
        self.generator.set_sd(sd)
        mock_normal.return_value = 10
        '''calculate score'''
        dist = 20
        expected_score = self.generator.calculate_score(dist)
        '''check if score is correct'''
        norm_distribution = stats.norm(mean, sd)
        prob = 1 - norm_distribution.cdf(dist)
        manual_score = int(np.exp(1 / prob) + self.generator.base_score / 2)
        self.assertEqual(expected_score, manual_score)

    @patch('numpy.random.normal')
    def test_generate_random_edge(self, mock_normal):
        """Test generate_random_edge returns weights"""
        mock_normal.return_value = 5
        weight = RandomScoreGenerator.generate_random_edge(10, 2)
        self.assertEqual(weight, 5)

    def test_generate_random_edge_raises_value_error(self):
        """Test generate_random_edge raises ValueError"""
        with self.assertRaises(ValueError):
            RandomScoreGenerator.generate_random_edge(-10, 2)
        with self.assertRaises(ValueError):
            RandomScoreGenerator.generate_random_edge(10, -2)
        with self.assertRaises(ValueError):
            RandomScoreGenerator.generate_random_edge(10, "2")


if __name__ == '__main__':
    unittest.main()
