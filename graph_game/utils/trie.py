"""
The implementation of the Trie data structure is based on the work submitted in a formative assessment.

References:
Tom Lam. 2024. Word Ladder Game. [Software]. [Accessed 10 April 2024]. 
Available from: https://github.com/T0mLam/Word-Ladder-Game
"""
from typing import List
from .heap import MinHeap


class TrieNode:
    """An individual trie node.
    
    Attributes:
        children: A dictionary mapping the char to its TrieNode object.
        end_of_word: A boolean value indicating whether the current char is the end of the word.
    """
    def __init__(self):
        """Consturct the children and end_of_word attributes."""
        self.children = {}
        self.end_of_word = False


class Trie:
    """A prefix tree data structure which stores an alphabet as value in each node.
    
    Attributes:
        root: A pointer to the root of the Trie.

    Methods:
        find: Return True if the word is in the dictionary else False
        complete: Complete a word based on the input of the user and return the list of words ordered by their length
    """
    def __init__(self) -> None:
        """Construct the root of the trie."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert the word into the trie.

        Args:
            word (str): A word to be inserted into the trie.

        Raises:
            TypeError: Errors caused by non-string input of 'word'.
        """
        if not isinstance(word, str):
            raise TypeError("The input parameter 'word' must be a string")

        # Create a pointer to the root
        node = self.root

        # Check if the character is a child of the root
        for char in word:
            # Create a new branch if the character is not found
            if char not in node.children:
                node.children[char] = TrieNode()
            # Traverse to the node storing the character 
            node = node.children[char]
            
        # Set the node storing the last character of the word to be the end_of_word
        node.end_of_word = True

    def find(self, word: str) -> bool:
        """Search whether the word is stored in the trie.

        Args:
            word (str): A word to be searched for in the trie.
        
        Returns:
            True if the word is found else false.

        Raises:
            TypeError: Errors caused by non-string input of 'word'.
        """
        if not isinstance(word, str):
            raise TypeError("The input parameter 'word' must be a string")

        node = self.root
        # Check every character in the word
        for char in word:
            # Return false if any char is not found
            if char not in node.children:
                return False
            # Traverse to the next char
            node = node.children[char]
        
        # Return true if the last char is marked as the end of word
        return node.end_of_word
    
    def complete(self, word: str) -> List[str]:
        """Complete the given word by searching words in the trie with the same prefix.

        Args:
            word (str): A word to be completed.
        
        Returns:
            A list of possible words in the trie.

        Raises:
            TypeError: Errors caused by non-string input of 'word'.
        """
        if not isinstance(word, str):
            raise TypeError("The input parameter 'word' must be a string")

        node = self.root
        res = []

        # Find the node storing the last character of the input string
        for char in word:
            # Return an empty list if the input string is not found
            if char not in node.children:
                return []
            node = node.children[char]

        # Use backtracking to find all the combinations of words starting at the last char of the input str
        cache = []
        def dfs(node: type[TrieNode]) -> None:
            # Append the word to res if it is marked as the end of word
            if node.end_of_word and cache:
                res.append(word + ''.join(cache)) 

            for child in node.children:
                # Backtracking 
                # Use a cache variable to store the combinations of the word
                cache.append(child)
                # Continue recursion on each child of the subtree
                dfs(node.children[child])
                # Remove the char from the cache once a combination have been added to res
                cache.pop()

        dfs(node)
        # Return the list sorted by the length of each word
        return sorted(res, key=len)
    
    def fizzy_search(self, 
                     word: str,
                     threshold: int, 
                     num_return: int = int(1e9)) -> List[str]:
        """A search method which returns all similar words in the trie with at most (threshold) Levenshtein distance. 

        Args:
            word (str): The target word.
            threshold (int): The maximum Levenshtein distance difference.
            num_return (int): The maximum number of return words sorted by ascending levenshtein distance.

        Returns:
            A list of words that are within the Levenshtein distance threshold.

        Raises:
            TypeError: Invalid data type of input parameter 'word'.
            ValueError: Invalid data type and range of input parameters 'threshold' or 'num_return'.
        
        Notes:
            This implementation of the fizzy search method is inspired by a software blog post.

        References:
        Hanov, S. 2011. Fast and Easy Levenshtein distance using a Trie. [Online]. [Accessed 11 April 2024].
        Available from: http://stevehanov.ca/blog/?id=114.
        """
        if not isinstance(word, str):
            raise TypeError("The input parameter 'word' must be a string")
        
        if not isinstance(threshold, int) or threshold < 0:
            raise ValueError("The input parameter 'threshold' must be a non-negative integer")
        if not isinstance(num_return, int) or num_return < 1:
            raise ValueError("The input parameter 'num_return' must be a positive integer")

        heap = MinHeap()
        root = self.root
        res = []
        curr_row = range(len(word) + 1)

        def dfs(node: type[TrieNode],
                letter: str,
                curr_str: str,
                prev_row: int) -> None:
            curr_str += letter

            cols = len(word) + 1
            curr_row = [prev_row[0] + 1]

            for col in range(1, cols):
                if word[col - 1] == letter:
                    curr_row.append(prev_row[col - 1])
                    continue
            
                replace_cost = prev_row[col - 1] + 1
                insert_cost = curr_row[col - 1] + 1
                delete_cost = prev_row[col] + 1

                curr_row.append(min(replace_cost, insert_cost, delete_cost))

            if curr_row[-1] <= threshold and node.end_of_word:
                heap.push((curr_row[-1], curr_str))

            if min(curr_row) <= threshold:
                for child in node.children:
                    dfs(node.children[child], child, curr_str, curr_row)

        for child in root.children:
            dfs(root.children[child], child, '', curr_row)

        while len(heap) and num_return:
            res.append(heap.pop()[1])
            num_return -= 1

        return res
    

if __name__ == '__main__':
    trie = Trie()
    trie.insert('goober')
    trie.insert('goobers')
    trie.insert('gowier')
    trie.insert('goobr')
    print(trie.fizzy_search('goober', threshold=3))