"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

MallocLabs K-mer Querying Structure
"""

from __future__ import annotations
from typing import Any


"""
You may wish to import your data structures to help you with some of the
problems. Or maybe not.
"""
from structures.bit_vector import BitVector
from structures.dynamic_array import DynamicArray

# from structures.linked_list import DoublyLinkedList, Node


class KmerStore:
    """
    A data structure for maintaining and querying k-mers.
    You may add any additional functions or member variables
    as you see fit.
    At any moment, the structure is maintaining n distinct k-mers.
    """

    NUCLEOTIDES = "ACGT"

    def __init__(self, k: int) -> None:
        self._k = k
        self._trie = Trie()

    def __str__(self) -> str:
        return str(self._trie)

    def read(self, infile: str) -> None:
        """
        Given a path to an input file, break the sequences into
        k-mers and load them into your data structure.
        """
        with open(infile) as file:
            array = file.read().split("\n")

        kmers = []

        for line in array[:-1]:
            for i in range(len(array[0]) - self._k + 1):
                kmers.append(line[i : i + self._k])
        self.batch_insert(kmers)
        self.kmers = kmers

    def batch_insert(self, kmers: list[str]) -> None:
        """
        Given a list of k-mers, insert them (maintaining
        duplicates) in O(n) time.
        """
        length = len(kmers)
        middle = length // 2
        # Sort two part seperately, make it faster.
        quick_sort(kmers, 0, middle)
        quick_sort(kmers, middle, length)

        left = middle - 1
        right = length - 1
        left_end = -1
        right_end = middle - 1
        has_picked = 0
        occurance = 1

        # Always pick the biggest kmer, like the final merge step in the merge sort
        # left/right == left/right_end: no non-added element in the left/right,
        while left > left_end or right > right_end:
            # Two sides has kmers
            if left > left_end and right > right_end:
                if kmers[left] > kmers[right]:
                    picked = kmers[left]
                    left -= 1
                else:
                    picked = kmers[right]
                    right -= 1
            # Only left side has element
            elif left > left_end and right == right_end:
                picked = kmers[left]
                left -= 1
            # Only right side has element
            else:
                picked = kmers[right]
                right -= 1

            has_picked += 1

            if 1 < has_picked < length:
                if last_picked == picked:
                    occurance += 1
                else:
                    self._trie.insert(last_picked, occurance)
                    occurance = 1
            elif has_picked == length:
                if last_picked == picked:
                    occurance += 1
                    self._trie.insert(picked, occurance)
                else:
                    self._trie.insert(last_picked, occurance)
                    self._trie.insert(picked, 1)

            last_picked = picked

        # for kmer in kmers:
        #     self._trie.insert(kmer)

    def batch_delete(self, kmers: list[str]) -> None:
        """
        Given a list of k-mers, delete the matching ones
        (including all duplicates) in O(n) time.
        """
        for kmer in kmers:
            self._trie.delete(kmer)

    def freq_geq(self, m: int) -> list[str]:
        """
        Given an integer m, return a list of k-mers that occur
        >= m times in your data structure.
        Time complexity for full marks: O(n)
        """

        root = self._trie._root
        array = []
        # Use a simulated call stack
        stack = [[root, ""]]
        while stack:
            popped = stack.pop()
            node = popped[0]
            kmer = popped[1]

            if node._depth == self._k:
                if node._occurance >= m:
                    array.append(kmer)
                continue

            for i in range(3, -1, -1):
                child = node._child[i]
                if child is not None and child._occurance >= m:
                    stack.append([child, kmer + child._nucleotide])
        return array

    def count_prefix(self, sequence: str = "") -> int:
        """
        Get the occurance of the given prefix.
        Return the final char's associated node's occurance.
        When sequence = '', return the occurance of root, i.e the size of trie
        """
        return self._trie.get_occurance(sequence)

    def count(self, kmer: str) -> int:
        """
        Given a k-mer, return the number of times it appears in
        your data structure.
        Time complexity for full marks: O(log n)
        """
        return self._trie.get_occurance(kmer)

    def count_geq(self, kmer: str) -> int:
        """
        Given a k-mer, return the total number of k-mers that
        are lexicographically greater or equal.
        Time complexity for full marks: O(log n)
        """
        count = 0
        node = self._trie._root

        # Should consider kmer is not in trie
        for nucleotide in kmer:
            code = self._nucleotide_hash(nucleotide)
            for i in range(4):
                if i > code:
                    greater_node = node._child[i]
                    if greater_node is not None:
                        count += greater_node._occurance

            child = node._child[code]
            if child is None:
                break
            node = child

        if node._depth == self._k:
            count += node._occurance
        return count

    def compatible(self, kmer: str) -> int:
        """
        Given a k-mer, return the total number of compatible
        k-mers. You will be using the two suffix characters
        of the input k-mer to compare against the first two
        characters of all other k-mers.
        Time complexity for full marks: O(1) :-)
        """

        first = self._nucleotide_hash(kmer[-2])
        second = self._nucleotide_hash(kmer[-1])

        first_node = self._trie._root._child[3 - first]
        if first_node is not None:
            second_node = first_node._child[3 - second]
            if second_node is not None:
                return second_node._occurance

        return 0

    def _nucleotide_hash(self, nucleotide: str) -> int:
        """
        Hash-like function, map A,C,G,T to 0,1,2,3 for indexing.
        """
        if nucleotide == "A":
            return 0
        elif nucleotide == "C":
            return 1
        elif nucleotide == "G":
            return 2
        elif nucleotide == "T":
            return 3
        else:
            raise ValueError


class TrieNode:

    def __init__(self, code: int, nucleotide: str = "ROOT", depth: int = 0) -> None:
        self._nucleotide = nucleotide
        self._child = [None] * 4
        self._parent = None
        self._depth = depth
        self._code = code
        # The number of DNA sequence this node involves
        self._occurance = 0

    def __str__(self) -> str:
        return self._nucleotide

    def __repr__(self) -> str:
        return self.__str__()

    def to_string(self, level: int = 0) -> str:
        """
        Return a hierachical presentation of the trie.
        """
        result = " " * (level * 2) + f"{self._nucleotide}({self._occurance})\n"
        for child in self._child:
            # child = self.get_child(nucleotide)
            if child is not None:
                result += child.to_string(level + 1)
        return result

    def get_data(self) -> str:
        """Return the nucleotide sign of the node"""
        return self._nucleotide

    def set_child(self, node: TrieNode) -> None:
        """
        Set the child node as the given node and set child node's parent (i.e. self).
        If self has a corresponding code, do nothing
        """
        nucleotide = node._nucleotide
        code = node._code

        if self._child[code] is None:
            self._child[code] = node
            node.set_parent(self)
        # else:
        #     self._occurance += 1
        #     node.increase_occurance()

    def get_child(self, code: int = -1) -> TrieNode | list[TrieNode]:
        """
        Return the child node with the given code.
        If no code gives, (default=-1), return all the chilren in a list.
        """
        if code == -1:
            return self._child
        else:
            return self._child[code]

    def has_child(self, code: int = -1) -> bool:
        """
        Return True if the child node exists with the given code.
        If no code gives, (default=-1), return True if the code has any children.
        """
        if code == -1:
            return [_ for _ in self._child if _ is not None] == []
        else:
            return self._child[code] is not None

    def remove_child(self, code: int) -> None:
        """
        Remove the chilren with the given code.
        """
        self._child[code] = None

    def get_parent(self) -> TrieNode:
        """Return the parent node"""
        return self._parent

    def set_parent(self, node: TrieNode) -> None:
        """Set the parent as the given node."""
        self._parent = node

    def get_occurance(self) -> int:
        """Return the occurance of this node"""
        return self._occurance

    def increase_occurance(self, num: int = 1) -> None:
        """Increase the occurance by the given num"""
        self._occurance += num

    def reduce_occurance(self, num: int = 1) -> None:
        """Decrease the occurance by the given num"""
        self._occurance -= num

    def get_depth(self) -> int:
        """Return the depth of this node"""
        return self._depth


class Trie:
    NUCLEOTIDES = "ACGT"

    def __init__(self) -> None:
        self._root = TrieNode(-1, "ROOT", 0)

    def _nucleotide_hash(self, nucleotide: str) -> int:
        if nucleotide == "A":
            return 0
        elif nucleotide == "C":
            return 1
        elif nucleotide == "G":
            return 2
        elif nucleotide == "T":
            return 3
        else:
            raise ValueError

    def get_root(self) -> TrieNode:
        """Return the root node of this trie"""
        return self._root

    def get_occurance(self, kmer: str = "") -> int:
        """
        Get the occurance of a string stored in the trie, it can be whole string or sub-string starting from index 0.
        if not provided, return the occurance of root
        """
        parent = self._root
        for nucleotide in kmer:
            code = self._nucleotide_hash(nucleotide)
            node = parent._child[code]
            if node is None:
                return 0
            parent = node
        return parent._occurance

    def insert(self, kmer: str, occurance: int = 1) -> None:
        """
        Insert `kmer` to the trie. Allow duplication.
        """
        node = self._root
        node._occurance += occurance
        for index, nucleotide in enumerate(kmer):
            code = self._nucleotide_hash(nucleotide)
            if not node._child[code]:
                child = TrieNode(code, nucleotide, index + 1)
                node._child[code] = child
                child._parent = node
            else:
                child = node._child[code]
            node = child
            node._occurance += occurance

    def delete(self, kmer: str) -> None:
        """Delete the given kmer from the trie. Delete all duplicate kmers."""
        node = self._root
        length = len(kmer)

        for nucleotide in kmer:
            code = self._nucleotide_hash(nucleotide)
            child = node._child[code]
            if child is None:
                break
            node = child

        if length > node._depth:
            return

        reduce_times = node._occurance

        while True:
            node._occurance -= reduce_times
            parent = node._parent

            # If occurance reduces to 0, remove that node
            if node._occurance == 0:
                parent._child[node._code] = None
            node = parent
            if node is self._root:
                # `parent` is root
                node._occurance -= reduce_times
                break


def binary_length(array: list[Any]) -> int:
    """
    Get the size of an array with the restriction of using len()
    Using binary search to find the final index of array.
    Inspiration from Tut W3 Q4.
    """
    # Exponential search to find upper limit
    low = 0
    high = 1
    # Double `high` until IndexError occurs
    while True:
        try:
            _ = array[high]
            high *= 2
        except IndexError:
            break

    # Binary search between low and high
    while low < high:
        mid = (low + high) // 2
        try:
            _ = array[mid]
            low = mid + 1
        except IndexError:
            high = mid

    return low


def quick_sort(array: list[str], low: int, high: int) -> None:
    """
    A Quick Sort helper, recursion function.
    Parameters:
        low: The start index in the sorting interval, inclusive. (Logically, use get_at())
        high: The end index in the sorting interval, exclusive. (Logically, use get_at())
    """
    pivot = high - 1
    # Base case:
    if low >= high:
        return
    # Comparison. Let all bigger number move to pivot's right.
    i = low
    while i < pivot:
        while array[i] > array[pivot]:
            array[i], array[pivot - 1] = array[pivot - 1], array[i]
            array[pivot - 1], array[pivot] = array[pivot], array[pivot - 1]
            pivot -= 1
        i += 1
    # Recursion. Left part of pivot, and then the right part.
    quick_sort(array, low, pivot)
    quick_sort(array, pivot + 1, high)
