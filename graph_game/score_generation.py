from typing import List
from scipy.stats import norm 


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
        pass
    def generate_random_edge(self) -> int:
        """
        Generate a weight using a normal distribution.

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

