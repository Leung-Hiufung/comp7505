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
        self._kmer_error_message = f"Not a valid kmer with a size of {self._k} that only contains {self.NUCLEOTIDES}."

    def __str__(self) -> str:
        return str(self._trie)

    def read(self, infile: str) -> None:
        """
        Given a path to an input file, break the sequences into
        k-mers and load them into your data structure.
        """
        array = DynamicArray()
        with open(infile) as file:
            for line in file:
                array.append(line)

        num_sequences = array.get_size()
        # Validate the file
        for i in range(1, num_sequences):
            if binary_length(array[i - 1]) != binary_length(array[i]):
                raise IOError("Each line has different length in file.")

        length_sequence = binary_length(array[0]) - 1  # '\n' included
        # Validate the length of each line
        if length_sequence < 1:
            raise ValueError(f"Sequence is too short to generate a {self._k}-mer.")

        num_kmers_line = length_sequence - self._k + 1
        num_kmers = num_kmers_line * num_sequences
        kmers = [None] * num_kmers

        kmer_index = 0
        while kmer_index < num_kmers:
            for sequence_index in range(num_sequences):
                sequence = array[sequence_index]
                for index in range(num_kmers_line):
                    kmer = ""
                    for i in range(self._k):
                        kmer += sequence[index + i]
                    kmers[kmer_index] = kmer
                    kmer_index += 1

        self.batch_insert(kmers)
        self.kmers = kmers
        # for k in kmers:
        #     print(k)

    # def batch_delete_t(self, kmers: list[str]) -> None:
    #     ks = []
    #     for kmer in self.kmers:
    #         if kmer not in kmers:
    #             ks.append(kmer)
    #     self.kmers = ks

    # def feq_geq_t(self, m: int) -> list[str]:
    #     k = {}
    #     result = []
    #     for kmer in self.kmers:
    #         feq = k.get(kmer)
    #         if feq is None:
    #             k[kmer] = 1
    #         else:
    #             k[kmer] += 1
    #     for kmer in k:
    #         if k[kmer] >= m:
    #             result.append(kmer)
    #     return result

    # def count_t(self, kmer: str) -> int:
    #     count = 0
    #     for k in self.kmers:
    #         if k == kmer:
    #             count += 1
    #     return count

    # def count_geq_t(self, kmer: str) -> int:
    #     count = 0
    #     ks = []
    #     for k in self.kmers:
    #         if k >= kmer:
    #             count += 1
    #             ks.append(k)
    #     # print(sorted(ks))
    #     return count

    # def compatible_t(self, kmer: str) -> int:
    #     suffix = kmer[-2:]
    #     prefix = [None] * 2
    #     for i in range(2):
    #         if suffix[i] == "A":
    #             prefix[i] = "T"
    #         elif suffix[i] == "C":
    #             prefix[i] = "G"
    #         elif suffix[i] == "G":
    #             prefix[i] = "C"
    #         elif suffix[i] == "T":
    #             prefix[i] = "A"

    #     count = 0
    #     for k in self.kmers:
    #         if k[1] == prefix[1] and k[0] == prefix[0]:
    #             count += 1
    #     return count

    def batch_insert(self, kmers: list[str]) -> None:
        """
        Given a list of k-mers, insert them (maintaining
        duplicates) in O(n) time.
        """
        for kmer in kmers:
            # if not self._is_valid_kmer(kmer):
            #     raise ValueError(self._kmer_error_message)
            self._trie.insert(kmer)

    def batch_delete(self, kmers: list[str]) -> None:
        """
        Given a list of k-mers, delete the matching ones
        (including all duplicates) in O(n) time.
        """

        for kmer in kmers:
            # if not self._is_valid_kmer(kmer):
            #     raise ValueError(self._kmer_error_message)
            self._trie.delete(kmer)

    def freq_geq(self, m: int) -> list[str]:
        """
        Given an integer m, return a list of k-mers that occur
        >= m times in your data structure.
        Time complexity for full marks: O(n)
        """

        root = self._trie.get_root()
        array = DynamicArray()
        self._freq_geq_recursion(m, root, "", array)
        return array.to_python_list()

    def _freq_geq_recursion(
        self, m: int, node: Node, kmer: str, array: DynamicArray
    ) -> None:
        # base case 1: reaches the depth
        if node.get_depth() == self._k:
            if node.get_occurance() < m:
                return
            else:
                array.append(kmer)

        for nucleotide in self.NUCLEOTIDES:
            child = node.get_child(nucleotide)
            if child is None:
                # Not such child node
                continue
            elif child.get_occurance() < m:
                # This node has smaller occurance, no need to visit its children
                continue
            else:
                self._freq_geq_recursion(m, child, kmer + child.get_data(), array)

    def count_prefix(self, sequence: str = "") -> int:
        # for char in sequence:
        # if not (char == "A" or char == "C" or char == "G" or char == "T"):
        #     raise ValueError(f"Sequence can only contains {self.NUCLEOTIDES}")
        return self._trie.get_occurance(sequence)

    def count(self, kmer: str) -> int:
        """
        Given a k-mer, return the number of times it appears in
        your data structure.
        Time complexity for full marks: O(log n)
        """
        # if not self._is_valid_kmer(kmer):
        #     raise ValueError(self._kmer_error_message)
        return self._trie.get_occurance(kmer)

    def count_geq(self, kmer: str) -> int:
        """
        Given a k-mer, return the total number of k-mers that
        are lexicographically greater or equal.
        Time complexity for full marks: O(log n)
        """
        # if not self._is_valid_kmer(kmer):
        #     raise ValueError(self._kmer_error_message)

        count = 0
        node = self._trie.get_root()

        # Should consider kmer is not in trie
        for nucleotide in kmer:
            for i in self.NUCLEOTIDES:
                if i > nucleotide:
                    greater_node = node.get_child(i)
                    if greater_node is not None:
                        count += greater_node.get_occurance()

            child = node.get_child(nucleotide)
            if child is None:
                break
            node = child

        if node.get_depth() == self._k:
            count += node.get_occurance()
        return count  # `1` is kmer itself

    def compatible(self, kmer: str) -> int:
        """
        Given a k-mer, return the total number of compatible
        k-mers. You will be using the two suffix characters
        of the input k-mer to compare against the first two
        characters of all other k-mers.
        Time complexity for full marks: O(1) :-)
        """
        # if not self._is_valid_kmer(kmer):
        #     raise ValueError

        suffix = [kmer[-2], kmer[-1]]
        prefix = [None] * 2
        suffix[0] = kmer[-2]
        suffix[1] = kmer[-1]
        for i in range(2):
            if suffix[i] == "A":
                prefix[i] = "T"
            elif suffix[i] == "C":
                prefix[i] = "G"
            elif suffix[i] == "G":
                prefix[i] = "C"
            else:
                prefix[i] = "A"
        return self._trie.get_occurance(prefix[0] + prefix[1])

    # Any other functionality you may need

    def _is_valid_kmer(self, kmer: str) -> bool:
        length = binary_length(kmer)
        for char in kmer:
            if not (char == "A" or char == "C" or char == "G" or char == "T"):
                return False

        return length == self._k


class Node:

    def __init__(self, nucleotide: str = "ROOT", depth: int = 0) -> None:
        # if not self._is_valid_char(nucleotide) and not nucleotide == "ROOT":
        #     raise ValueError
        self._nucleotide = nucleotide
        self._child = [None] * 4
        self._parent = None
        self._depth = depth
        # The number of DNA sequence this node involves
        self._occurance = 0  # if self._nucleotide == "ROOT" else 1

    def __str__(self) -> str:
        return self._nucleotide

    def __repr__(self) -> str:
        return self.__str__()

    def to_string(self, level: int = 0) -> str:
        result = " " * (level * 2) + f"{self._nucleotide}({self._occurance})\n"
        for child in self._child:
            # child = self.get_child(nucleotide)
            if child is not None:
                result += child.to_string(level + 1)
        return result

    def get_data(self) -> str:
        return self._nucleotide

    def set_child(self, node: Node) -> None:
        """
        Set the child node as the given node and set child node's parent (i.e. self).
        If self has a corresponding code, do nothing
        """
        nucleotide = node.get_data()
        index = self._nucleotide_hash(nucleotide)

        if self._child[index] is None:
            self._child[index] = node
            node.set_parent(self)
        # else:
        #     self._occurance += 1
        #     node.increase_occurance()

    def get_child(self, nucleotide: str = "") -> Node | list[Node]:
        if nucleotide == "":
            return self._child
        else:
            index = self._nucleotide_hash(nucleotide)
            return self._child[index]

    def has_child(self, nucleotide: str = "") -> bool:
        if nucleotide == "":
            return [_ for _ in self._child if _ is not None] == []
        else:
            index = self._nucleotide_hash(nucleotide)
            return self._child[index] is not None

    def remove_child(self, nucleotide: str) -> None:
        index = self._nucleotide_hash(nucleotide)
        self._child[index] = None
        # self._occurance -= 1

    def get_parent(self) -> Node:
        return self._parent

    def set_parent(self, node: Node) -> None:
        self._parent = node

    def get_occurance(self) -> int:
        return self._occurance

    def increase_occurance(self) -> None:
        self._occurance += 1

    def reduce_occurance(self, num: int) -> None:
        self._occurance -= num

    def get_depth(self) -> int:
        return self._depth

    def _is_valid_char(self, char: str) -> bool:
        try:
            self._nucleotide_hash(char)
            return True
        except ValueError:
            return False

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

    # def __eq__(self, other: Node) -> bool:
    #     return self._nucleotide == other.get_data()

    # def __ne__(self, other: Node) -> bool:
    #     return self._nucleotide != other.get_data()

    # def __gt__(self, other: Node) -> bool:
    #     return self._nucleotide > other.get_data()

    # def __ge__(self, other: Node) -> bool:
    #     return self._nucleotide >= other.get_data()

    # def __lt__(self, other: Node) -> bool:
    #     return self._nucleotide < other.get_data()

    # def __le__(self, other: Node) -> bool:
    #     return self._nucleotide <= other.get_data()


class Trie:
    NUCLEOTIDES = "ACGT"

    def __init__(self) -> None:
        self._root = Node()

    # def __str__(self) -> str:
    #     return self._root.to_string()

    def get_root(self) -> Node:
        return self._root

    def get_occurance(self, kmer: str = "") -> int:
        """
        Get the occurance of a string stored in the trie, it can be whole string or sub-string starting from index 0.
        if not provided, return the occurance of root
        """
        parent = self._root
        for nucleotide in kmer:
            node = parent.get_child(nucleotide)
            if node is None:
                return 0
            parent = node
        return parent.get_occurance()

    def insert(self, kmer: str) -> None:
        node = self._root
        node.increase_occurance()
        for index, nucleotide in enumerate(kmer):
            if not node.has_child(nucleotide):
                child = Node(nucleotide, index + 1)
                node.set_child(child)
            else:
                child = node.get_child(nucleotide)
            node = child
            node.increase_occurance()

    def delete(self, kmer: str) -> None:
        if kmer == "GTCG":
            pass
        node = self._root
        length = binary_length(kmer)

        for nucleotide in kmer:
            child = node.get_child(nucleotide)
            if child is None:
                break
            node = child

        if length > node.get_depth():
            return

        reduce_times = node.get_occurance()

        while True:
            node.reduce_occurance(reduce_times)
            parent = node.get_parent()

            # If occurance reduces to 0, remove that node
            if node.get_occurance() == 0:
                parent.remove_child(node.get_data())
                # for nucleotide in self.NUCLEOTIDES:
                #     if parent.get_child(nucleotide) == node:
                #         parent.remove_child(nucleotide)
                #         break
            node = parent
            if node is self._root:
                # `parent` is root
                node.reduce_occurance(reduce_times)
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
