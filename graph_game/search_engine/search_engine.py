from typing import List
from db.database import DatabaseConnection
from utils.trie import Trie


class SearchEngine:
    def __init__(self) -> None:
        self.trie = Trie()
        self.fetch_all_users()
        
    def complete_search(self, name: str) -> List[str]:
        return self.trie.complete(name)
    
    def search_result(self, name: str) -> List[str]:
        players = self.trie.fizzy_search(name, threshold=3, num_return=10)

    def get_leaders(self, n: int) -> List[str]:
        pass

    def fetch_all_users(self) -> None:  
        pass