from typing import List
from scipy.stats import norm 
import numpy as np

class RandomScoreGenerator:
    def __init__(self, base_score: int = 100) -> None:
        self.__mean = None
        self.__sd = None
        self.__generated_distance = None
        self.base_score = base_score

    def set_mean(self, mean: int) -> None:
        self._mean = mean

    def set_sd(self, sd: int | float) -> None:
        self._sd = sd

    def generate_random_distance(self) -> int:
         """
        method generates a random distance using a normal distribution.

        Returns:
            int: A randomly generated distance.
        
        Raises:
            ValueError: If mean or standard deviation is not set.
        """
        if self.__mean is None or self.__sd is None:
            raise ValueError("Mean and standard deviation must be set.")
        return int(np.random.normal(loc=self.__mean, scale=self.__sd))

    def generate_random_edge(self) -> int:
        """
        method genertate a random weight using a normal distribution.

        Returns:
            integer: A randomly generated weight.
        
        Raises:
            ValueError: If mean or standard deviation is not set.
        """
        if self._mean is None or self._sd is None:
            raise ValueError("Mean and standard deviation must be set.")
        return int(np.random.normal(loc=self._mean, scale=self._sd))

    def calculate_score(self, dist: int) -> int:
        pass

