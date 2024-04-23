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
        find: Return True if the word is in the dictionary else False.
        complete: Complete a word based on the input of the user and return the list of words ordered by their length.
        fizzy_search: A search method which returns all similar words in the trie with at most (threshold) Levenshtein distance.
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
        """
        if not isinstance(word, str):
            raise TypeError("The input parameter 'word' must be a string")
        
        if not isinstance(threshold, int) or threshold < 0:
            raise ValueError("The input parameter 'threshold' must be a non-negative integer")
        if not isinstance(num_return, int) or num_return < 1:
            raise ValueError("The input parameter 'num_return' must be a positive integer")
        '''
        Method: using a 2d matrix to find the the Levenshtein distance between 2 strings
        e.g.

            k a t e
          0 1 2 3 4
        c 1 1 2 3 4
        a 2 2 1 2 3
        t 3 3 2 1 2

        x: target_word
        y: possible combination in trie

        Steps:
        1. First fill the first row with range(len(target_word))
        2. Iterate through the rows from the second left grid to the right,
            set the first left grid as the index of the row.
        3. For each grid, if the letter of the target word != the letter of the combination,
            compute the lowest cost by taking the lowest values at the top left, left and the grid above + 1.
            Otherwise, just take the value of the top left grid (the previous cost) without adding 1.
        4. The difference between the 2 words will be grid[len(target_word)][len(combination)]
    
        Results:
        Difference between 'kate' and 'cat' = 2 (grid[4, 3])
        - Replace c by k and insert e

        Difference between 'kat' and 'ca' = 2 (grid[3, 2])
        - Replace c by k and insert t

        As this algorithm performs dfs on the trie while completing the grid, 
        new character will be added to the y-axis in every iteration. 
        We just have to keep track of the previous row and the current row of characters.
        '''
        # Use a minheap to extract words with the lower difference
        heap = MinHeap()
        root = self.root
        res = []
        # Create the first row of the 2d matrix
        curr_row = range(len(word) + 1)

        def dfs(node: type[TrieNode],
                letter: str,
                curr_str: str,
                prev_row: int) -> None:
            # Add the new letter to the string storing the combination
            curr_str += letter

            cols = len(word) + 1
            # Create the first value of the new row
            curr_row = [prev_row[0] + 1]

            for col in range(1, cols):
                # Add the value of the top left grid to curr_row 
                # if the combination and target share the same letter 
                if word[col - 1].lower() == letter.lower():
                    curr_row.append(prev_row[col - 1])
                    continue
                
                # Otherwise calculate each cost of the 3 grids at the 3 directions
                # according to the edit distance algorithm
                replace_cost = prev_row[col - 1] + 1
                insert_cost = curr_row[col - 1] + 1
                delete_cost = prev_row[col] + 1

                # Append the minimum cost to the curr_row
                curr_row.append(min(replace_cost, insert_cost, delete_cost))

            # If the last value of the row is less than the threshold
            # and it is a word stored in the trie, push the word along with the Levenshtein distance to the heap 
            if curr_row[-1] <= threshold and node.end_of_word:
                heap.push((curr_row[-1], curr_str))

            # If the minimum value of the row has not exceeded the threshold, 
            # it is possible that adding additional characters to the end of the word will still be valid
            if min(curr_row) <= threshold:
                for child in node.children:
                    dfs(node.children[child], child, curr_str, curr_row)

        # Start the recursion from every child of the trie root
        for child in root.children:
            dfs(root.children[child], child, '', curr_row)

        # Pop the words with the lowest Levenshtein distance from the heap and return
        while len(heap) and num_return:
            res.append(heap.pop()[1])
            num_return -= 1

        return res