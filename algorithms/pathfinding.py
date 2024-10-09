"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""

from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.graph import Graph, LatticeGraph
from structures.map import Map
from structures.pqueue import PriorityQueue
from structures.bloom_filter import BloomFilter
from structures.util import Hashable
from structures.bit_vector import BitVector


def bfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.1: Breadth First Search

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.
    """
    return frontier_traversal(graph, origin, goal, 0)


def dijkstra_traversal(graph: Graph, origin: int) -> DynamicArray:
    """
    Task 2.2: Dijkstra Traversal

    @param: graph
      The *weighted* graph to process (POSW graphs)
    @param: origin
      The ID of the node from which to start traversal.

    @returns: DynamicArray containing Entry types.
      The Entry key is a node identifier, Entry value is the cost of the
      shortest path to this node from the origin.

    NOTE: Dijkstra does not work (by default) on LatticeGraph types.
    This is because there is no inherent weight on an edge of these
    graphs. It should of course work where edge weights are uniform.
    """
    valid_locations = DynamicArray()  # This holds your answers

    # ALGO GOES HERE
    # heap stores not-selected nodes
    heap = PriorityQueue()
    # bit_vector is used to flag which nodes are selected
    selected_nodes = BitVector()
    selected_nodes.allocate(len(graph._nodes))
    all_locations = [None] * len(graph._nodes)

    # get intial adjacent nodes from origin
    initial_reachables = graph.get_neighbours(origin)
    for index, (node, weight) in enumerate(initial_reachables):
        node_id = node.get_id()
        # Entry: weight as key for comparison
        initial_reachables[index] = Entry(weight, node_id)
        all_locations[node_id] = weight
        # selected_nodes[node_id] = 1

    reachables = DynamicArray()
    reachables.build_from_list(initial_reachables)
    heap.ip_build(reachables)

    # mark origin as selected
    selected_nodes[origin] = 1
    all_locations[origin] = 0


    while heap.get_size() > 0:
        entry = heap.pop_min_entry()
        base_cost = entry.get_key()
        current_id = entry.get_value()
        selected_nodes[current_id] = 1
        
        neighbours = graph.get_neighbours(current_id)
        for node, weight in neighbours:
            node_id = node.get_id()
            total_cost = base_cost + weight
            # Update if lower cost
            if all_locations[node_id] is None:
                all_locations[node_id] = total_cost
            elif total_cost < all_locations[node_id]:
                all_locations[node_id] = total_cost
            
            # insert to heap if not selected yet
            if selected_nodes[node_id] == 0:
                heap.insert(total_cost, node_id)

    valid_locations.build_from_list([Entry(node_id, cost) for node_id, cost in enumerate(all_locations) if cost is not None and cost > 0])
      
            



    # Return the DynamicArray containing Entry types
    return valid_locations


def dfs_traversal(
    graph: Graph | LatticeGraph, origin: int, goal: int
) -> tuple[DynamicArray, DynamicArray]:
    """
    Task 2.3: Depth First Search **** COMP7505 ONLY ****
    COMP3506 students can do this for funsies.

    @param: graph
      The general graph or lattice graph to process
    @param: origin
      The ID of the node from which to start traversal
    @param: goal
      The ID of the target node

    @returns: tuple[DynamicArray, DynamicArray]
      1. The ordered path between the origin and the goal in node IDs
      (or an empty DynamicArray if no path exists);
      2. The IDs of all nodes in the order they were visited.

    """
    return frontier_traversal(graph, origin, goal, -1)



def frontier_traversal(graph: Graph | LatticeGraph, origin: int, goal: int, type: int) -> tuple[DynamicArray, DynamicArray]:
    """
    merged used for bfs and dfs,
    @param: type
      0: bfs, 1:dfs
    """
    # Stores the keys of the nodes in the order they were visited
    visited_order = DynamicArray()
    # Stores the path from the origin to the goal
    path = DynamicArray()

    # ALGO GOES HERE
    visited = BitVector()
    visited.allocate(len(graph._nodes))
    # Stores the parent id of the current node, index: current node id
    parents = DynamicArray()
    parents.allocate(len(graph._nodes), None)
    parents[origin] = None
    frontier = DynamicArray()
    frontier.append(origin)

    while len(frontier) > 0:
        node_id = frontier.remove_at(type)
        if node_id == goal:
            break
        
        visited_order.append(node_id)
        visited[node_id] = 1
        node_neighbours = graph.get_neighbours(node_id)  # Node, not id

        for neighbour in node_neighbours:
            if isinstance(neighbour, tuple):
                neighbour = neighbour[0]

            neighbour_id = neighbour.get_id()
            
            if visited[neighbour_id] == 0:
                frontier.append(neighbour_id)
                parents[neighbour_id] = node_id
        
    # backtrack path
    path.append(node_id)
    while node_id is not None:
        parent = parents[node_id]
        if parent is None:
            break
        path.append(parent)
        node_id = parent
    path.reverse()

    # Return the path and the visited nodes list
    return (path, visited_order)