from typing import List, Tuple
from ..db.database import DatabaseConnection
from ..utils.trie import Trie


class SearchEngine:
    def __init__(self) -> None:
        self.trie = None
        self.fetch_all_users_to_trie()
        
    def complete_search(self, name: str) -> List[str]:
        return self.trie.complete(name)
    
    def search_result(self, name: str) -> List[str]:
        players = self.trie.fizzy_search(name, threshold=2, num_return=10)

        res = []

        with DatabaseConnection('db') as conn:
            for player in players:
                player_name_score = conn.get_cursor().execute(
                    'SELECT name, balance FROM players WHERE name = ?', (player,)
                ).fetchone()

                res.append(player_name_score)

        return res

    def get_leaders(self, n: int) -> List[Tuple[str]]:
        with DatabaseConnection('db') as conn:
            leaders_name_score = conn.get_cursor().execute(
                'SELECT name, balance FROM players ORDER BY balance DESC'
            ).fetchall()
            
        return leaders_name_score

    def fetch_all_users_to_trie(self) -> None:  
        with DatabaseConnection('db') as conn:
            players = conn.get_cursor().execute(
                'SELECT name FROM players'
            ).fetchall()
        
        self.trie = Trie()

        for player in players:
            self.trie.insert(*player)


if __name__ == '__main__':
    se = SearchEngine()
    print(se.complete_search('Fem'))
    print('success')