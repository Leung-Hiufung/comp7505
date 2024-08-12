"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

# so we can hint Node get_next
from __future__ import annotations

from typing import Any


class Node:
    """
    A simple type to hold data and a next pointer
    """

    def __init__(self, data: Any) -> None:
        self._data = data  # This is the payload data of the node
        self._next = None  # This is the "next" pointer to the next Node
        self._prev = None  # This is the "previous" pointer to the previous Node

    def set_data(self, data: Any) -> None:
        self._data = data

    def get_data(self) -> Any:
        return self._data

    def set_next(self, node: Node) -> None:
        self._next = node

    def get_next(self) -> Node | None:
        return self._next

    def set_prev(self, node: Node) -> None:
        self._prev = node

    def get_prev(self) -> Node | None:
        return self._prev


class DoublyLinkedList:
    """
    Your doubly linked list code goes here.
    """

    def __init__(self) -> None:
        # You probably need to track some data here...
        self.size = 0
        self.head = None
        self.tail = None
        self.is_reversed = False

    def __str__(self) -> str:
        """
        A helper that allows you to print a DoublyLinkedList type
        via the str() method.
        """
        elements = []
        if self.size > 0:
            elements = [None] * self.size
            if not self.is_reversed:
                node = self.head
                for i in range(self.size):
                    elements[i] = node.get_data()
                    node = node.get_next()
            else:
                node = self.tail
                for i in range(self.size):
                    elements[i] = node.get_data()
                    node = node.get_prev()

        return f"DoublyLinkedList({self.size}): {elements}"

    """
    Simple Getters and Setters below
    """

    def get_size(self) -> int:
        """
        Return the size of the list.
        Time complexity for full marks: O(1)
        """
        return self.size

    def get_head(self) -> Any | None:
        """
        Return the data of the leftmost node in the list, if it exists.
        Time complexity for full marks: O(1)
        """
        return self.head.get_data() if not self.is_reversed else self.tail.get_data()

    def set_head(self, data: Any) -> None:
        """
        Replace the leftmost node's data with the given data.
        If the list is empty, do nothing.
        Time complexity for full marks: O(1)
        """
        if self.size == 0:
            return
        if self.is_reversed:
            self.tail.set_data(data)
        else:
            self.head.set_data(data)

    def get_tail(self) -> Any | None:
        """
        Return the data of the rightmost node in the list, if it exists.
        Time complexity for full marks: O(1)
        """
        return self.tail.get_data() if not self.is_reversed else self.head.get_data()

    def set_tail(self, data: Any) -> None:
        """
        Replace the rightmost node's data with the given data.
        If the list is empty, do nothing.
        Time complexity for full marks: O(1)
        """
        if self.size == 0:
            return

        if self.is_reversed:
            self.head.set_data(data)
        else:
            self.tail.set_data(data)

    """
    More interesting functionality now.
    """

    def insert_to_front(self, data: Any) -> None:
        """
        Insert the given data to the front of the list.
        Hint: You will need to create a Node type containing
        the given data.
        Time complexity for full marks: O(1)
        """
        node = Node(data)

        if self.size == 0:
            self.__insert_into_empty_list(node)
            return

        if self.is_reversed:
            self.__insert_to_physical_back(node)
        else:
            self.__insert_to_physical_front(node)

    def insert_to_back(self, data: Any) -> None:
        """
        Insert the given data (in a node) to the back of the list
        Time complexity for full marks: O(1)
        """
        node = Node(data)

        if self.size == 0:
            self.__insert_into_empty_list(node)
            return

        if self.is_reversed:
            self.__insert_to_physical_front(node)
        else:
            self.__insert_to_physical_back(node)

    def remove_from_front(self) -> Any | None:
        """
        Remove the front node, and return the data it holds.
        Time complexity for full marks: O(1)
        """
        if self.size == 0:
            return

        # One node in list, then make list empty
        if self.size == 1:
            self.__pop_last_node_from_list().get_data()
            return
        if self.is_reversed:
            self.__pop_from_physical_back().get_data()
        else:
            self.__pop_from_physical_front().get_data()

    def remove_from_back(self) -> Node | None:
        """
        Remove the back node, and return the data it holds.
        Time complexity for full marks: O(1)
        """
        if self.size == 0:
            return

        # One node in list, then make list empty
        if self.size == 1:
            self.__pop_last_node_from_list()
            return
        if self.is_reversed:
            self.__pop_from_physical_front()
        else:
            self.__pop_from_physical_back()

    def find_element(self, elem: Any) -> bool:
        """
        Looks at the data inside each node of the list and returns True
        if a match is found; False otherwise.
        Time complexity for full marks: O(N)
        """
        if self.size == 0:
            return

        node = self.head

        # iterate the list
        while True:
            if node.get_data() == elem:
                return True
            node = node.get_next()

            # break when go to the end
            if node is None:
                return False

    def find_and_remove_element(self, elem: Any) -> bool:
        """
        Looks at the data inside each node of the list; if a match is
        found, this node is removed from the linked list, and True is returned.
        False is returned if no match is found.
        Time complexity for full marks: O(N)
        """
        if self.size == 0:
            return

        node = self.head
        # iterate the list
        while True:
            if node.get_data() == elem:
                break
            node = node.get_next()

            # break when go to the end
            if node is None:
                return False

        # Also contain the condition of len==1, (len==2 and the node is head)
        if self.head == node:
            self.remove_from_front()
        # Also contain the condition of len>=2 and the node is tail
        elif self.tail == node:
            self.remove_from_back()
        else:
            prev_node = node.get_prev()
            next_node = node.get_next()
            prev_node.set_next(next_node)
            next_node.set_prev(prev_node)
            self.size -= 1
        return True

    def reverse(self) -> None:
        """
        Reverses the linked list
        Time complexity for full marks: O(1)
        """
        self.is_reversed = not self.is_reversed

    def __insert_into_empty_list(self, node: Node) -> None:
        """
        Helper function. Used to insert the first node into an empty linked list.
        Premise: List is empty, i.e. size == 0
        """
        self.head = node
        self.tail = node
        self.size += 1

    def __pop_last_node_from_list(self) -> Node:
        """
        Helper function. Used to remove the last node from a linked list.
        Premise: List has only one node, i.e. size == 1
        """
        node = self.head
        self.head = None
        self.tail = None
        self.size -= 1
        return node

    def __insert_to_physical_front(self, node: Node) -> None:
        """
        Insert a node to the front of the list when not reversed
        Premise: List is not empty. `node` is not None.
        """
        node.set_next(self.head)
        self.head.get_prev(node)
        self.head = node
        self.size += 1

    def __insert_to_physical_back(self, node: Node) -> None:
        """
        Insert a node to the back of the list when not reversed
        Premise: List is not empty. `node` is not None.
        """
        node.set_prev(self.tail)
        self.tail.set_next(node)
        self.tail = node
        self.size += 1

    def __pop_from_physical_front(self) -> Node | None:
        """
        Remove and return the front element when not reversed
        Premises:
            List size > 1
        """
        node = self.head
        self.head = self.head.get_next()
        self.head.set_prev(None)
        self.size -= 1
        return node

    def __pop_from_physical_back(self) -> Node | None:
        """
        Remove and return the back element when not reversed
        Premises:
            List size > 1
        """
        node = self.tail
        self.tail = self.tail.get_prev()
        self.tail.set_next(None)
        self.size -= 1
        return node
