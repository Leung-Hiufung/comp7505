"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation.
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""

from typing import Any
from structures.entry import Entry
from structures.linked_list import DoublyLinkedList
from structures.dynamic_array import DynamicArray
import math
import structures.util as util


class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    LOAD_FACTOR = 0.75

    def __init__(self) -> None:
        """
        Construct the map.
        You are free to make any changes you find suitable in this function
        to initialise your map.
        """
        self._size = 0
        self._arr = DynamicArray()
        self._arr.build_from_list([None] * 1031)
        self._capacity = 1031

    def get_items(self) -> list[Entry]:
        if self._size == 0:
            return []
        l = [None] * self._size
        i = 0
        for elem in self._arr:
            if isinstance(elem, Entry):
                l[i] = elem
                i += 1
            elif isinstance(elem, DoublyLinkedList):
                cur = elem.get_head_node()
                while cur is not None:
                    l[i] = cur.get_data()
                    i += 1
                    cur = cur.get_next()
        return l

    def __repr__(self) -> str:
        return str(self.get_items())

    def __str__(self) -> str:
        return self.__repr__()

    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. If k already exists
        in your map, you must return the old value associated with k. Return
        None otherwise. (We will not use None as a key or a value in our tests).
        Time complexity for full marks: O(1*)
        """
        # check load percentage
        if self._size / self._capacity > self.LOAD_FACTOR:
            self.__resize()

        old_value = self.__insert_only(entry)
        if old_value is None:
            # no existing key, so no old value
            self._size += 1
        return old_value

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which takes a key and value explicitly.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind. You can modify this if you want, as long as it behaves.
        Time complexity for full marks: O(1*)
        """
        # hint: entry = Entry(key, value)
        entry = Entry(key, value)
        return self.insert(entry)

    def __insert_only(self, entry: Entry) -> Any | None:
        """
        Insert only, no resize, if key exists, return value
        """
        index = self.__to_index(entry.get_key())
        old_value = None

        if self._arr[index] is None:
            self._arr[index] = entry
        elif isinstance(self._arr[index], Entry):
            if entry.get_key() == self._arr[index].get_key():
                old_value = self._arr[index].get_value()
                self._arr[index] = entry
            else:
                # already has entry element, hash collision, build linked list
                linked_list = DoublyLinkedList()
                linked_list.insert_to_back(self._arr[index])
                linked_list.insert_to_back(entry)
                self._arr[index] = linked_list
        else:
            # already linked list
            old_value = self._arr[index].find_and_return_element(entry)
            if old_value is None:
                self._arr[index].insert_to_back(entry)
            else:
                old_value.update_value(entry.get_value())
        return old_value

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        Time complexity for full marks: O(1*)
        """
        self.insert_kv(key, value)

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        Time complexity for full marks: O(1*)
        """
        index = self.__to_index(key)
        elem = self._arr[index]

        if isinstance(elem, Entry) and elem.get_key() == key:
            self._arr[index] = None
        elif isinstance(elem, DoublyLinkedList):
            deleted_entry = elem.find_and_remove_element(Entry(key, 0))
            if deleted_entry is None:
                # no entry is deleted
                return
            if elem.get_size() == 0:
                self._arr[index] = None
        else:
            return
        self._size -= 1

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        Time complexity for full marks: O(1*)
        """
        index = self.__to_index(key)
        elem = self._arr[index]

        if isinstance(elem, Entry) and elem.get_key() == key:
            return elem.get_value()
        elif isinstance(elem, DoublyLinkedList):
            entry = elem.find_and_return_element(Entry(key, 0))
            if entry is not None:
                return entry.get_value()

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        Time complexity for full marks: O(1*)
        """
        return self.find(key)

    def get_size(self) -> int:
        """
        Time complexity for full marks: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Time complexity for full marks: O(1)
        """
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __to_index(self, key: Any) -> int:
        return util.get_hash(key) % self._capacity

    def __resize(self) -> None:
        old_array = self._arr
        # new array with a prime-number size
        new_array = DynamicArray()
        new_capacity = get_prime_ge(self._capacity * 2)
        new_array.build_from_list([None] * new_capacity)
        self._capacity = new_capacity
        self._arr = new_array

        for elem in old_array:
            if isinstance(elem, Entry):
                self.__insert_only(elem)
            elif isinstance(elem, DoublyLinkedList):
                while elem.get_size() > 0:
                    entry = elem.remove_from_back()
                    self.__insert_only(entry)


def get_prime_ge(n: int) -> int:
    """
    Return the smallest prime number that is greater than or equal to n.
    """
    # ensure n is odd
    n = n + 1 if n & 1 == 0 else n
    while True:
        for i in range(3, int(math.sqrt(n)) + 1):
            if n % i == 0:
                # composite, to next odd
                n += 2
                continue
        return n
