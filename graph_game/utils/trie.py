"""
The implementation of the Trie data structure is based on the work submitted in a formative assessment.

References:
Tom Lam. 2024. Word Ladder Game. [Software]. [Accessed 10 April 2024]. 
Available from: https://github.com/T0mLam/Word-Ladder-Game
"""
from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def find(self, word: str) -> bool:
        """Search whether the word is stored in the trie.
        
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
        def dfs(node):
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

    def find_neighbors(self, word: str) -> List[str]:
        if not word:
            return []
        
        original_word = word
        n = len(word)
        res = set()
        # Create permutations of the word
        # e.g. 'cow' -> ['*ow', 'c*w', 'co*'], 
        # (* indicates any alphabets)
        permutations = [word[:i] + '*' + word[i + 1:] for i in range(n)]

        cache = []
        def dfs(i, node):
            # 1. Check i == n (whether the search reaches the end of the word)
            # 2. Check node.end_of_word (whether the word exists in the Trie)
            # 3. Add the found word to res
            if i == n and node.end_of_word:
                res.add(''.join(cache))
                return
            
            # Stop the recursion if ...
            # 1. The search reaches the end of the word but no valid words are found
            # 2. The character is not a child of the node nor is it a '*'
            if (i == n or
                word[i] != '*' and 
                word[i] not in node.children):
                return 
        
            for child in node.children:
                # Continue the recursion only on the subtree of the current character
                # or all children if the character is a '*'
                if word[i] == '*' or word[i] == child:
                    # Backtracking 
                    # Using a cache variable to store the combinations of the word
                    # Add char -> dfs -> remove char when dfs returns
                    # Instead of passing combination as parameter, dfs(i, node, combination)
                    # Reusing the variable to reduce memory usage 
                    cache.append(child)
                    # Move pointer i to the next character and set the child node to be the new root
                    dfs(i + 1, node.children[child])
                    cache.pop()
        
        for word in permutations:
            dfs(0, self.root)

        res.discard(original_word)
        return list(res)
    
    def insert(self, word: str) -> None:
        """Insert the word into the trie.

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