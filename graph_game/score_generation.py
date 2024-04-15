from typing import List

import numpy as np
from scipy.stats import norm 


class RandomScoreGenerator:
    """A random score generator which based on a normal distribution.

    Attributes:
        base_score: The base score of the game which determines the range of score generated for each node.

    Methods:
        set_mean: Set the mean value for generating random distances.
        set_sd: Set the standard deviation for generating random distances.
        generate_random_distance: Generates a random distance using a normal distribution.
        calculate_score: Calculates a score based on the given distance and base score.
        generate_random_edge: Generates a random weight using a normal distribution.
    """
    def __init__(self, base_score: int = 100) -> None:
        """Construct the attributes of the random score generator.

        Args:
            base_score (int): The base score of the game which determines the range of score generated for each node.

        Raises:
            ValueError: If the base score is not a integer.
        """
        self._mean = None
        self._sd = None
        self._generated_distance = None
        self.base_score = base_score

    def set_mean(self, mean: int) -> None:
        """Set the mean value for generating random distances.

        Args:
            mean (int): The mean value to set.

        Raises:
            ValueError: If the mean is a non numeric number.
        """
        # Check if mean is a non-negative integer
        if not isinstance(mean, int) or mean < 0:
            raise ValueError("Mean must be a non-negative integer.")
        # Set mean
        self._mean = mean

    def set_sd(self, sd: int | float) -> None:
        """Set the standard deviation for generating random distances.

        Args:
            sd (int | float): The standard deviation value to set.

        Raises:
            ValueError: If the standard deviation is not a non negative number.
        """
        # Check if sd is a non-negative numeric value
        if not isinstance(sd, (int, float)) or sd < 0:
            raise ValueError("Standard deviation must be a non-negative numeric value.")
        # Set standard deviation
        self._sd = sd

    def generate_random_distance(self) -> int:
        """Generates a random distance using a normal distribution.

        Returns:
            int: A randomly generated distance.
        
        Raises:
            ValueError: If mean or standard deviation is not set.
        """
        # Check if mean and standard deviation are set
        if self._mean is None or self._sd is None:
            raise ValueError("Mean and standard deviation must be set.")
        # Generate random distance
        return int(np.random.normal(loc=self._mean, scale=self._sd))

    def calculate_score(self, dist: int) -> int:
        """Calculates a score based on the given distance and base score.

        Args:
            dist (int): The distance to calculate the score for.

        Returns:
            int: The calculated score.

        Raises:
            ValueError: If the distance is not an integer.
        """
        # Check if distance is a non-negative integer
        if not isinstance(dist, int) or dist < 0:
            raise ValueError("Distance must be a non-negative integer.")
        # If generated distance is not already set, generate it    
        if self._generated_distance is None:
            self._generated_distance = self.generate_random_distance()
        # Calculate score
        score = self.base_score - dist + self._generated_distance
        return max(score, 0)
    
    @staticmethod
    def generate_random_edge(mean: int, sd: int | float) -> int:
        """Generates a random weight using a normal distribution.

        Returns:
            int: A randomly generated weight.
        
        Raises:
            ValueError: If mean is not an integer or standard deviation is neither an integer nor a float num.
        """
        # Check if mean is a non-negative integer
        if not isinstance(mean, int) or mean < 0:
            raise ValueError("Mean must be a non-negative integer.")
        # Check if sd is a non-negative numeric value
        if not isinstance(sd, (int, float)) or sd < 0:
            raise ValueError("Standard deviation must be a non-negative numeric value.")
        # Generate random weight, ensuring it's at least 1
        return max(int(np.random.normal(loc=mean, scale=sd)), 1)