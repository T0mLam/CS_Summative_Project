from typing import List, Tuple
from ..db.database import DatabaseConnection
from ..utils.trie import Trie


class SearchEngine:
    def __init__(self) -> None:
        """A search engine that provides searching functionality for the leaderboard in the Graph Game.

        Attributes:
            trie: An instance of the trie data structure.
        
        Methods:
            complete_search: Complete a word based on the input and return the list of word combinations ordered by their length.
            search_result: Get a list of the players with their balance according to the user input.
            get_leaders: Get the n players with the highest balance.
            fetch_all_users_to_trie: Fetch all the players from the database to the trie.
        """
        self.trie = None
        self.fetch_all_users_to_trie()
        
    def complete_search(self, input_str: str) -> List[str]:
        """Complete a word based on the input and return the list of word combinations ordered by their length.

        Args:
            input_str (str): The user input.

        Returns:
            A list of word combinations ordered by their length.
        """
        return self.trie.complete(input_str)
    
    def search_result(self, name: str) -> List[str]:
        # Get at most 10 users with at most 2 Levenshtein distance away from the name input
        players = self.trie.fizzy_search(name, threshold=2, num_return=10)

        res = []

        with DatabaseConnection('db') as conn:
            for player in players:
                # Fetch the player name and score from the database
                player_name_score = conn.get_cursor().execute(
                    'SELECT name, balance FROM players WHERE name = ?', (player,)
                ).fetchone()

                # Append the records of the players to the res list
                res.append(player_name_score)

        return res

    def get_leaders(self, n: int) -> List[Tuple[str]]:
        with DatabaseConnection('db') as conn:
            leaders_name_score = conn.get_cursor().execute(
                'SELECT name, balance FROM players ORDER BY balance DESC'
            ).fetchall()
            
        return leaders_name_score[:n]

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