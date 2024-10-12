"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

 Each problem will be assessed on three sets of tests:

1. "It works":
       Basic inputs and outputs, including the ones peovided as examples, with generous time and memory restrictions.
       Large inputs will not be tested here.
       The most straightforward approach will likely fit into these restrictions.

2. "Exhaustive":
       Extensive testing on a wide range of inputs and outputs with tight time and memory restrictions.
       These tests won't accept brute force solutions, you'll have to apply some algorithms and optimisations.

 3. "Welcome to COMP3506":
       Extensive testing with the tightest possible time and memory restrictions
       leaving no room for redundant operations.
       Every possible corner case will be assessed here as well.

There will be hidden tests in each category that will be published only after the assignment deadline.

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
from structures.entry import Entry, Compound, Offer
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
from structures.bit_vector import BitVector
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable
import math

class TreeNode:
    def __init__(self, data: str, frequency: int) -> None:
        self.frequency = frequency
        self.data = data
        self.left = None
        self.right = None


def maybe_maybe_maybe(database: list[str], query: list[str]) -> list[str]:
    """
    Task 3.1: Maybe Maybe Maybe

    @database@ is an array of k-mers in our database.
    @query@ is an array of k-mers we want to search for.

    Return a list of query k-mers that are *likely* to appear in the database.

    Limitations:
        "It works":
            @database@ contains up to 1000 elements;
            @query@ contains up to 1000 elements.

        "Exhaustive":
            @database@ contains up to 100'000 elements;
            @query@ contains up to 100'000 elements.

        "Welcome to COMP3506":
            @database@ contains up to 1'000'000 elements;
            @query@ contains up to 500'000 elements.

    Each test will run over three false positive rates. These rates are:
        fp_rate = 10%
        fp_rate = 5%
        fp_rate = 1%.

    You must pass each test in the given time limit and be under the given
    fp_rate to get the associated mark for that test.
    """
    answer = [] 

    # DO THE THING
    bloom_filter = BloomFilter(len(database))

    for kmer in database:
        bloom_filter.insert(kmer)

    for kmer in query:
        if bloom_filter.contains(kmer):
            answer.append(kmer)

    return answer



def dora(graph: Graph, start: int, symbol_sequence: str,
         ) -> tuple[BitVector, list[Entry]]:
    """
    Task 3.2: Dora and the Chin Bicken

    @graph@ is the input graph G; G might be disconnected; each node contains
    a single symbol in the node's data field.
    @start@ is the integer identifier of the start vertex.
    @symbol_sequence@ is the input sequence of symbols, L, with length n.
    All symbols are guaranteed to be found in G. 

    Return a BitVector encoding symbol_sequence via a minimum redundancy code.
    The BitVector should be read from index 0 upwards (so, the first symbol is
    encoded from index 0). You also need to return your codebook as a
    Python list of unique Entries. The Entry key should correspond to the
    symbol, and the value should be a string. More information below.

    Limitations:
        "It works":
            @graph@ has up to 1000 vertices and up to 1000 edges.
            the alphabet consists of up to 26 characters.
            @symbol_sequence@ has up to 1000 characters.

        "Exhaustive":
            @graph@ has up to 100'000 vertices and up to 100'000 edges.
            the alphabet consists of up to 1000 characters.
            @symbol_sequence@ has up to 100'000 characters.

        "Welcome to COMP3506":
            @graph@ has up to 1'000'000 vertices and up to 1'000'000 edges.
            the alphabet consists of up to 300'000 characters.
            @symbol_sequence@ has up to 1'000'000 characters.

    """
    coded_sequence = BitVector()

    """
    list of Entry objects, each entry has key=symbol, value=str. The str
    value is just an ASCII representation of the bits used to encode the
    given key. For example: x = Entry("c", "1101")
    """
    codebook = []

    # DO THE THING
    # DFS Traversal
    freq_table = Map()
    visited = BitVector()
    visited.allocate(len(graph._nodes))
    frontier = [start]

    while len(frontier) > 0:
        node_id = frontier.pop()
        visited[node_id] = 1
        node_char = graph.get_node(node_id).get_data()
        freq_table[node_char] = 1 if freq_table[node_char] is None else freq_table[node_char] + 1
        node_neighbours = graph.get_neighbours(node_id)

        for neighbour in node_neighbours:
            if isinstance(neighbour, tuple):
                neighbour = neighbour[0]

            neighbour_id = neighbour.get_id()
            
            if visited[neighbour_id] == 0:
                frontier.append(neighbour_id)
    
    freq_list = freq_table.get_items()
    heap = PriorityQueue()
    for freq in freq_list:
        key = freq.get_key()
        value = freq.get_value()
        heap.insert(value, TreeNode(key, value))

    while heap.get_size() > 1:
        node1 = heap.remove_min()
        node2 = heap.remove_min()

        merged = TreeNode(None, node1.frequency + node2.frequency)
        merged.left = node1
        merged.right = node2
        heap.insert(merged.frequency, merged)
    
    huffman_tree_root = heap.remove_min()

    # huffman encoding
    codebook_map = Map()
    build_huffman_codebook_dfs(huffman_tree_root, "", codebook_map)

    for s in symbol_sequence:
        code = codebook_map[s]
        for bit in code:
            coded_sequence.append(0 if bit == '0' else 1)
    
    codebook = codebook_map.get_items()
    return (coded_sequence, codebook)


def build_huffman_codebook_dfs(node: TreeNode, current_path: str, codebook_map: Map) -> None:
    if node.data is not None:
        codebook_map[node.data] = current_path
        return

    if node.left is not None:
        build_huffman_codebook_dfs(node.left, current_path + "0", codebook_map)
    
    if node.right is not None:
        build_huffman_codebook_dfs(node.right, current_path + "1", codebook_map)


def chain_reaction(compounds: list[Compound]) -> int:
    """
    Task 3.3: Chain Reaction

    @compounds@ is a list of Compound types, see structures/entry.py for the
    definition of a Compound. In short, a Compound has an integer x and y
    coordinate, a floating point radius, and a unique integer representing
    the compound identifier.

    Return the compound identifier of the compound that will yield the
    maximal number of compounds in the chain reaction if set off. If there
    are ties, return the one with the smallest identifier.

    Limitations:
        "It works":
            @compounds@ has up to 100 elements

        "Exhaustive":
            @compounds@ has up to 1000 elements

        "Welcome to COMP3506":
            @compounds@ has up to 10'000 elements

    """
    maximal_compound = -1
    
    # DO THE THING
    n = len(compounds)

    if n == 0:
        return maximal_compound
    if n == 1:
        return 0
    
    # adjacency stores which compounds (value) can be covered by a compund (index)
    adjacency = [BitVector() for _ in range(n)]
    reachables = [None] * n
    for i in range(n):
        adjacency[i].allocate(n)

    # cover_amount stores the amount of compounds covered by a compound (index)
    # Entry: key: amount, value: index (used to record original index after heapify)

    # result stores calculated result for each index.
    # The value is the number of compound that a compound can trigger in a chain reaction
    result = [1] * n
    
    # calculate the distance from one to others, update `adjacency`
    for i in range(n):
        for j in range(i + 1, n):
            xi, yi = compounds[i].get_coordinates()
            xj, yj = compounds[j].get_coordinates()
            distance = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

            if distance <= compounds[i].get_radius():
                adjacency[i][j] = 1
            if distance <= compounds[j].get_radius():
                adjacency[j][i] = 1 
    
    # adj_list = []
    # for i in range(n):
    #     adj_list[i] = [j for j, k in enumerate(adjacency[i]) if k== 1]
    
    for i in range(n):
        visited = [False] * n
        reachables[i] = dfs_helper(i, n, adjacency, visited, reachables)
        # if reachables[i].get_size_of_one() > reachables[maximal_compound].get_size_of_one():
        #     maximal_compound = i

    maximal_compound = 0
    maximal_compound_covers = reachables[0].get_size_of_one()
    for i in range(n):
        compound_covers = reachables[i].get_size_of_one()
        if compound_covers > maximal_compound_covers:
            maximal_compound, maximal_compound_covers = i, compound_covers

    return maximal_compound

def dfs_helper(origin: int, n: int, adjacency: list[BitVector], visited: list[bool], reachables: list[BitVector]) -> BitVector:
    """
    
    """
    if reachables[origin] is not None:
        # cache
        return reachables[origin]

    # mark as visited
    visited[origin] = True
    reachable_from_origin = BitVector()
    reachable_from_origin.allocate(n)
    reachable_from_origin[origin] = 1

    # 遍歷所有可以被觸發的化合物
    for neighbor in range(n):
        if adjacency[origin][neighbor] == 1 and not visited[neighbor]:
            neighbor_reachables = dfs_helper(neighbor, n, adjacency, visited, reachables)
            reachable_from_origin.or_operation(neighbor_reachables)

    # cache
    reachables[origin] = reachable_from_origin
    return reachable_from_origin

def labyrinth(offers: list[Offer]) -> tuple[int, int]:
    """
    Task 3.4: Labyrinth

    @offers@ is a list of Offer types, see structures/entry.py for the
    definition of an Offer. In short, an Offer stores n (number of nodes),
    m (number of edges), and k (diameter) of the given Labyrinth. Each
    Offer also has an associated cost, and a unique offer identifier.
    
    Return the offer identifier and the associated cost for the cheapest
    labyrinth that can be constructed from the list of offers. If there
    are ties, return the one with the smallest identifier. 
    You are guaranteed that all offer ids are distinct.

    Limitations:
        "It works":
            @offers@ contains up to 1000 items.
            0 <= n <= 1000
            0 <= m <= 1000
            0 <= k <= 1000

        "Exhaustive":
            @offers@ contains up to 100'000 items.
            0 <= n <= 10^6
            0 <= m <= 10^6
            0 <= k <= 10^6

        "Welcome to COMP3506":
            @offers@ contains up to 5'000'000 items.
            0 <= n <= 10^42
            0 <= m <= 10^42
            0 <= k <= 10^42

    """
    best_offer_id = -1
    best_offer_cost = float('inf')

    # DO THE THING
    if len(offers) > 0:
        for offer in offers:
            n = offer.get_num_nodes()
            edge = offer.get_num_edges()
            diameter = offer.get_diameter()
            max_edge, min_edge = n * (n - 1) // 2, n - 1
            max_diameter, min_diameter =  n - 1, 1

            print(f"n = {n}, edge = {edge}, diameter = {diameter}, max_edge = {max_edge}", end="\t")
            
            # case 1: complete connected graph, one-line graph, lowerbound and upperbound
            if not (min_edge <= edge <= max_edge and min_diameter <= diameter <= max_diameter):
                # print("Case 1 not OK")
                continue
            
            # case 2: one-line graph
            if (edge == min_edge) != (diameter == max_diameter):
                # print("Case 2 not OK")
                continue
            
            # # case 3: add one edge to one-line graph
            # if (edge == n) != (n // 2 <= diameter <= n - 2):
            #     # print("Case 3 not OK")
            #     continue
            
            # # case 4: middle cases
            # if (n < edge <= max_edge - n) != (2 < diameter < n // 2):
            #     # print("Case 4 not OK")
            #     continue
            
            # # case 5: substract 1 ~ n - 1 edge from complete connected graph
            # if (max_edge - n + 1 <= edge <= max_edge - 1) != (diameter == 2):
            #     # print("Case 5 not OK")
            #     continue
            
            # case 6: complete connected graph
            if (edge == max_edge) != (diameter == min_diameter):
                # print("Case 6 not OK")
                continue
            
            # print("this one OK")

            if offer.get_cost() < best_offer_cost:
                best_offer_cost = offer.get_cost()
                best_offer_id = offer.get_offer_id()
                # print("updated")

    return (best_offer_id, best_offer_cost)


