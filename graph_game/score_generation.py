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
        pass

    def generate_random_distance(self) -> int:
        pass
    
    def calculate_score(self, dist: int) -> int:
        pass

