from typing import List, Tuple
from node import Node


class MinHeap:
    """A minheap data structure that enables quick extraction of the minimum element.

    Time Complexity:
        Initialize / heapify O(n * log n)
        Insertion O(log n)
        Extract min O(log n)
        Peak min O(1)
    
    Methods:
        push: Push an element into the minheap.
        pop: Remove and return the smallest element from the minheap.
        top: Return the smallest element from the minheap without removing.
    """

    def __init__(self, arr: List[Tuple[int, type[Node]]] | None = None) -> None:
        """Construct a heap by heapifying the input array.

        Args:
            arr: A list of tuple to be heapified during the initializing stage.
                 For example: [(1, Node_Obj1), (2, Node_Obj2), ...]

        Raises:
            TypeError: An error due to the invalid input data type of arr.
        """
        # Check whether the input array is a list 
        if arr and not isinstance(arr, list):
            raise TypeError("The parameter 'arr' must be a python list")

        self.__heap = arr if arr else []
        self.__heapify()

    def __len__(self) -> int:
        """Return the number elements in the minheap.

        Returns:
            An integer representing the number of element in the current minheap.
            For example: 

            heap = MinHeap([1, 2, 3, 4, 5]) 
            print(len(heap))
            # Output: 5
        """
        return len(self.__heap)
    
    def push(self, val: Tuple[int, type[Node]]) -> None:
        """Push the value into MinHeap.

        Args:
            val: Tuple with the integer and a node that will be pushed to the heap.
        """
        #The current index where the new value will be put 
        curr = len(self.__heap)
        #Append the new value to the heap
        self.__heap.append(val)
        #Using the __get_parent_idx to get parent index
        parent = self.__get_parent_idx(curr)
        
        #Compare the new element with its parent to check if it is not bigger that its parent and swap if it is
        while self.__heap[curr] < self.__heap[parent]:
            self.__swap(curr, parent)
            curr = parent
            parent = self.__get_parent_idx(parent)
        
    def pop(self) -> Tuple[int, type[Node]]:
        """Returns and deletes the smallest element from the heap.

        Returns:
            A tuple consist of the an integer and a node object or None if the heap is empty.
            For example:

            heap = MinHeap([(1, Node_Obj1), (2, Node_Obj2), ...])
            print(heap.pop())
            # Output: (1, Node_Obj1)
        """
        if not self.__heap:
            return
        #Change the root noed for th last node using the __swap method
        self.__swap(0, len(self.__heap) - 1)
        #Creating the variable for the smalelst item
        min_element = self.__heap.pop()
        #Using __sift down method for keeping the heap property
        self.__sift_down(0)
        #return the element
        return min_element

    def top(self) -> Tuple[int, type[Node]]:
        """Return the smallest element from the heap.

        Returns:
            A tuple consist of the an integer and a node object or None if the heap is empty.
            For example:

            heap = MinHeap([(1, Node_Obj1), (2, Node_Obj2), ...])
            print(heap.top())
            # Output: (1, Node_Obj1)
        """
        if not self.__heap:
            return
        return self.__heap[0]

    def __heapify(self) -> None:
        """Heapify the input array by sifting down all the non-leaf nodes."""
        for idx in range(len(self.__heap) // 2, -1, -1):
            self.__sift_down(idx)

    def __sift_down(self, idx: int) -> None:
        """A heap operation thats maintain the min heap structure.

        It allocates the nodes with smallest values at the root and largest values at the leaves
        by sifting down every nodes in the wrong positions.
        """
        left_child_idx, right_child_idx = self.__get_left_child_idx(idx), self.__get_right_child_idx(idx)

        # Check whether the current node has 2 children
        if min(left_child_idx, right_child_idx) != -1:
            # Check whether the current node is smaller than both its children
            if min(self.__heap[idx],
                   self.__heap[left_child_idx],
                   self.__heap[right_child_idx]) != self.__heap[idx]:
                # If the left child is smaller than the right child,
                # swap the left child with the current node and sift down the left child
                if self.__heap[left_child_idx] < self.__heap[right_child_idx]:
                    self.__swap(idx, left_child_idx)
                    self.__sift_down(left_child_idx)
                # Otherwise, swap the right child with the current node and sift down the right child
                else:
                    self.__swap(idx, right_child_idx)
                    self.__sift_down(right_child_idx)
            
        # Else if the current node is larger than its only left child,
        # swap the left child with the current node and sift down the left child
        elif (left_child_idx != -1 and
              self.__heap[left_child_idx] < self.__heap[idx]):
            self.__swap(idx, left_child_idx)
            self.__sift_down(left_child_idx)
    
        # Else if the current node is larger than its only right child,
        # swap the right child with the current node and sift down the right child
        elif (right_child_idx != -1 and
              self.__heap[right_child_idx] < self.__heap[idx]):
            self.__swap(idx, right_child_idx)
            self.__sift_down(right_child_idx)
     
    def __swap(self, idx1: int, idx2: int) -> None:
        """Swap the elements with index idx1 and idx2 in the heap."""
        self.__heap[idx1], self.__heap[idx2] = self.__heap[idx2], self.__heap[idx1]

    def __get_parent_idx(self, idx: int) -> int:
        """Get the parent of the element with index idx.

        Returns:
            An integer representing the index of the parent, or -1 if no parent is found.
        """
        return idx // 2
    
    def __get_left_child_idx(self, idx: int) -> int:
        """Get the left child of the element with index idx.

        Returns:
            An integer representing the index of the left child, or -1 if no left child is found.
        """
        left_child_idx = 2 * idx + 1
        return left_child_idx if left_child_idx < len(self.__heap) else -1

    def __get_right_child_idx(self, idx: int) -> int:
        """Get the right child of the element with index idx.

        Returns:
            An integer representing the index of the right child, or -1 if no right child is found. 
        """
        right_child_idx = 2 * idx + 2
        return right_child_idx if right_child_idx < len(self.__heap) else -1