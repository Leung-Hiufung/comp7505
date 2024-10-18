"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.bit_vector import BitVector
import structures.util as util
import math


class BloomFilter:
    """
    A BloomFilter uses a BitVector as a container. To insert a given key, we
    hash the key using a series of h unique hash functions to set h bits.
    Looking up a given key follows the same logic, but only checks if all
    bits are set or not.

    Note that a BloomFilter is considered static. It is initialized with the
    number of total keys desired (as a parameter) and will not grow. You
    must decide what this means in terms of allocating your bitvector space
    accordingly.

    You can add functions if you need to.

    *** A NOTE ON KEYS ***
    We will only ever use int or str keys.
    We will not use `None` as a key.
    You might like to look at the `object_to_byte_array` function
    stored in util.py -- This function can be used to convert a string
    or integer key into a byte array, and then you can use the byte array
    to make your own hash function (bytes are just integers in the range
    [0-255] of course).
    """

    def __init__(self, max_keys: int) -> None:
        # You should use max_keys to decide how many bits your bitvector
        # should have, and allocate it accordingly.
        self._data = BitVector()

        # More variables here if you need, of course
        self._size = 0
        self._capacity = math.ceil((-max_keys * math.log(0.01) / (math.log(2) ** 16)))
        self._data.allocate(self._capacity)

    def __str__(self) -> str:
        """
        A helper that allows you to print a BloomFilter type
        via the str() method.
        This is not marked. <<<<
        """
        pass

    def insert(self, key: Any) -> None:
        """
        Insert a key into the Bloom filter.
        Time complexity for full marks: O(1)
        """
        index = self._get_index_from_hashed_key(key)
        self._data.set_at(index)
        self._size += 1

    def contains(self, key: Any) -> bool:
        """
        Returns True if all bits associated with the h unique hash functions
        over k are set. False otherwise.
        Time complexity for full marks: O(1)
        """
        index = self._get_index_from_hashed_key(key)
        return self._data[index] == 1

    def __contains__(self, key: Any) -> bool:
        """
        Same as contains, but lets us do magic like:
        `if key in my_bloom_filter:`
        Time complexity for full marks: O(1)
        """
        return self.contains(key)

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        return self._size == 0

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of bits) that the underlying
        BitVector can currently maintain.
        Time complexity for full marks: O(1)
        """
        return self._capacity
    
    def _get_index_from_hashed_key(self, key: str) -> int:
        hashed_value = self.get_hash1(key)
        hashed_value = self.get_hash2(hashed_value)
        hashed_value = self.get_hash3(hashed_value)
        hashed_value = self.get_hash4(hashed_value)
        index = hashed_value % self._capacity
        return index
    
    def get_hash1(self, key: Any) -> int:
        key_bytes = util.object_to_byte_array(key)
        hash_value = 0

        for byte in key_bytes:
            hash_value = (hash_value * 29 + byte)# % (1 << 32)

        return hash_value
    
    def get_hash2(self, key: Any) -> int:
        key_bytes = util.object_to_byte_array(key)
        hash_value = 0

        for byte in key_bytes:
            hash_value = (hash_value * 43 + byte)# % (1 << 32)

        return hash_value
    
    def get_hash3(self, key: Any) -> int:
        key_bytes = util.object_to_byte_array(key)
        hash_value = 0

        for byte in key_bytes:
            hash_value = (hash_value * 37 + byte)# % (1 << 32)

        return hash_value
    
    def get_hash4(self, key: Any) -> int:
        key_bytes = util.object_to_byte_array(key)
        hash_value = 0

        for byte in key_bytes:
            hash_value = (hash_value * 31 + byte) % (1 << 32)

        return hash_value
