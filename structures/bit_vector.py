"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any

from structures.dynamic_array import DynamicArray

import math


class BitVector:
    """
    A compact storage for bits that uses DynamicArray under the hood.
    Each element stores up to 64 bits, making BitVector 64 times more memory-efficient
    for storing bits than plain DynamicArray.
    """

    BITS_PER_ELEMENT = 64
    FLIP_MASK = (1 << BITS_PER_ELEMENT) - 1

    def __init__(self) -> None:
        """
        We will use the dynamic array as our data storage mechanism
        """
        self._data = DynamicArray()
        # you may want or need more stuff here in the constructor
        self._size = 0
        self._is_reversed = False
        self._is_flipped = False
        # The position where the rightmost bit is in the rightmost element in the dynamic array
        # start from left (0) to right (BITS_PER_ELEMENT-1)
        self._rightmost_index_in_elem = None
        # The position where the leftmost bit is in the leftmost element in the dynamic array
        self._leftmost_index_in_elem = None

    def __str__(self) -> str:
        """
        A helper that allows you to print a BitVector type
        via the str() method.
        """
        bits = ""
        if self._size == 0:
            return ""

        if self._data.get_size() == 1:
            if self._is_flipped:
                element = self._data.get_at(0) ^ self.FLIP_MASK
            else:
                element = self._data.get_at(0)

            element = (
                element >> self.BITS_PER_ELEMENT - 1 - self._rightmost_index_in_elem
            )
            bits += f"{element:0{self._size}b}"
            return bits

        if self._data.get_size() > 0:
            # Add bits in the first element
            length = self.BITS_PER_ELEMENT - self._leftmost_index_in_elem
            if self._is_flipped:
                # not use entire mask, use mask just covering existed bits
                mask = (1 << length) - 1
                element = self._data.get_at(0) ^ mask
            else:
                element = self._data.get_at(0)

            bits += f"{element:0{length}b}"

        if self._data.get_size() > 2:
            # Add bits in the middle elements
            if self._size > (1 << 10):
                bit += "......"
            else:
                for i in range(1, self._data.get_size() - 1):
                    if self._is_flipped:
                        element = self._data.get_at(i) ^ self.FLIP_MASK
                    else:
                        element = self._data.get_at(i)
                    bits += f"{element:0{self.BITS_PER_ELEMENT}b}"

        if self._data.get_size() > 1:
            # Add bits in the last element
            if self._is_flipped:
                element = self._data.get_at(-1) ^ self.FLIP_MASK
            else:
                element = self._data.get_at(-1)
            bits += f"{element >> (self.BITS_PER_ELEMENT - 1 -self._rightmost_index_in_elem):0{self._rightmost_index_in_elem+1}b}"

        if self._is_reversed:
            reversed_bits = ""
            for i in range(self._size):
                reversed_bits += bits[self._size - i - 1]
            return reversed_bits
        return bits

    def __repr__(self) -> str:
        return self.__str__()

    def __resize(self) -> None:
        pass

    def _get_real_index(self, index: int) -> int | None:
        if -self._size <= index < 0:
            return self._size + index if not self._is_reversed else -1 - index
        elif 0 <= index < self._size:
            return index if not self._is_reversed else self._size - 1 - index
        else:
            return None

    def get_at(self, index: int) -> int | None:
        """
        Get bit at the given index.
        Return None if index is out of bounds.
        Time complexity for full marks: O(1)
        """

        real_index = self._get_real_index(index)
        if real_index is None:
            return
        # bit = self.__getitem__(real_index)
        positions = self._get_position_in_array(real_index)
        index_in_array = positions[0]
        index_in_elem = positions[1]
        bit = f"{self._data.get_at(index_in_array):0{self.BITS_PER_ELEMENT}b}"[
            index_in_elem
        ]
        bit = 1 if bit == "1" else 0
        bit = bit ^ 1 if self._is_flipped else bit
        return bit

    def __getitem__(self, index: int) -> int | None:
        """
        Same as get_at.
        Allows to use square brackets to index elements.
        """
        return self.get_at(index)

    def set_at(self, index: int) -> None:
        """
        Set bit at the given index to 1.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        # real_index = self._get_real_index(index)
        # if real_index is None:
        #     return
        self._set_status(index, 1 if not self._is_flipped else 0)

    def unset_at(self, index: int) -> None:
        """
        Set bit at the given index to 0.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        # real_index = self._get_real_index(index)
        # if real_index is None:
        #     return
        self._set_status(index, 0 if not self._is_flipped else 1)

    def _set_status(self, index: int, state: int) -> None:
        real_index = self._get_real_index(index)
        if real_index is None:
            return

        positions = self._get_position_in_array(real_index)
        index_in_array = positions[0]
        index_in_elem = positions[1]
        target_element = self._data[index_in_array]

        mask = 1 << (self.BITS_PER_ELEMENT - index_in_elem - 1)
        if state == 0:
            new_element = target_element & ~mask
        else:
            new_element = target_element | mask

        self._data[index_in_array] = new_element

    def __setitem__(self, index: int, state: int) -> None:
        """
        Set bit at the given index.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Do not modify the vector if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if state == 0:
            self.unset_at(index)
        else:
            self.set_at(index)

    def append(self, state: int) -> None:
        """
        Add a bit to the back of the vector.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        if self._is_reversed:
            self._prepend_physically(state if not self._is_flipped else state ^ 1)
        else:
            self._append_physically(state if not self._is_flipped else state ^ 1)

    def prepend(self, state: Any) -> None:
        """
        Add a bit to the front of the vector.
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        if self._is_reversed:
            self._append_physically(state if not self._is_flipped else state ^ 1)
        else:
            self._prepend_physically(state if not self._is_flipped else state ^ 1)

    def reverse(self) -> None:
        """
        Reverse the bit-vector.
        Time complexity for full marks: O(1)
        """
        self._is_reversed = not self._is_reversed

    def flip_all_bits(self) -> None:
        """
        Flip all bits in the vector.
        Time complexity for full marks: O(1)
        """
        self._is_flipped = not self._is_flipped

    def shift(self, dist: int) -> None:
        """
        Make a bit shift.
        If dist is positive, perform a left shift by `dist`.
        Otherwise perform a right shift by `dist`.
        Time complexity for full marks: O(N)
        """
        while dist > 0:
            self._pop_from_logical_left()
            self.append(0)
            dist -= 1

        while dist < 0:
            self._pop_from_logical_right()
            self.prepend(0)
            dist += 1

    def rotate(self, dist: int) -> None:
        """
        Make a bit rotation.
        If dist is positive, perform a left rotation by `dist`.
        Otherwise perform a right rotation by `dist`.
        Time complexity for full marks: O(N)
        """
        while dist > 0:
            bit = self._pop_from_logical_left()
            self.append(bit)
            dist -= 1

        while dist < 0:
            bit = self._pop_from_logical_right()
            self.prepend(bit)
            dist += 1

    def get_size(self) -> int:
        """
        Return the number of *bits* in the list
        Time complexity for full marks: O(1)
        """
        return self._size

    def _get_position_in_array(self, index: int) -> list[int]:
        # `index_in_array` is the element index where the index is in terms of the dynamic array,
        #  `BITS_PER_ELEMENT` is a unit
        # `index_in_binary_elem` is the position where the target is in that element

        # Check which element the bit is in array
        # index_in_array = (
        #     index - self._leftmost_index_in_elem + self.BITS_PER_ELEMENT
        # ) // self.BITS_PER_ELEMENT

        index_in_array = index // self.BITS_PER_ELEMENT

        # Check the index in an array element
        index_in_elem = index % self.BITS_PER_ELEMENT + self._leftmost_index_in_elem
        if index_in_elem >= self.BITS_PER_ELEMENT:
            index_in_elem = index_in_elem - self.BITS_PER_ELEMENT
            index_in_array += 1

        return [index_in_array, index_in_elem]

    def _append_physically(self, state: int) -> None:
        """
        Add a bit to the back of the physical vector disregarding `_is_reversed` status
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        if self._size == 0:
            self._leftmost_index_in_elem = 0
            self._rightmost_index_in_elem = 0
        else:
            self._rightmost_index_in_elem += 1

        self._size += 1
        if self._rightmost_index_in_elem >= self.BITS_PER_ELEMENT or self._size == 1:
            # Bit Overflow
            self._rightmost_index_in_elem = 0
            new_element = 0 if state == 0 else 1 << self.BITS_PER_ELEMENT - 1
            self._data.append(new_element)
            # self._size += 1
        else:
            ### Process array approach
            # old_element = self._data.get_at(-1)
            # mask = 1 << 63 - self._rightmost_index_in_elem
            # new_element = old_element & ~mask if state == 0 else old_element | mask
            # self._data.set_at(-1, new_element)

            ### Process bit approach

            self[-1] = state

    def _prepend_physically(self, state: int) -> None:
        """
        Add a bit to the front of the physical vector disregarding `_is_reversed` status
        Treat the integer in the same way Python does:
        if state is 0, set the bit to 0, otherwise set the bit to 1.
        Time complexity for full marks: O(1*)
        """
        if self._size == 0:
            return self._append_physically(state)

        self._leftmost_index_in_elem -= 1

        self._size += 1
        if self._leftmost_index_in_elem < 0:
            # Bit Overflow
            self._leftmost_index_in_elem = self.BITS_PER_ELEMENT - 1
            new_element = 0 if state == 0 else 1
            self._data.prepend(new_element)
        else:
            # old_element = self._data.get_at(0)
            # mask = 1 << 63 - self._leftmost_index_in_elem
            # new_element = old_element & ~mask if state == 0 else old_element | mask
            # self._data.set_at(0, new_element)
            self[0] = state

    def _pop_from_logical_left(self) -> int:
        if self._is_reversed:
            return self._pop_from_physical_right()
        else:
            return self._pop_from_physical_left()

    def _pop_from_logical_right(self) -> int:
        if self._is_reversed:
            return self._pop_from_physical_left()
        else:
            return self._pop_from_physical_right()

    def _pop_from_physical_left(self) -> int:
        """
        Pop the bit from the physical left, and return this bit
        """
        bit = self[0]
        self[0] = 0
        self._size -= 1
        self._leftmost_index_in_elem += 1

        if self._leftmost_index_in_elem >= self.BITS_PER_ELEMENT:
            self._leftmost_index_in_elem = 0
            self._data.remove_at(0)

        if self._size == 0:
            self._leftmost_index_in_elem = None
            self._rightmost_index_in_elem = None

        return bit

    def _pop_from_physical_right(self) -> int:
        """
        Pop the bit from the physical left, and return this bit
        """
        bit = self[-1]
        self[-1] = 0
        self._size -= 1
        self._rightmost_index_in_elem -= 1

        if self._rightmost_index_in_elem < 0:
            self._rightmost_index_in_elem = self.BITS_PER_ELEMENT - 1
            self._data.remove_at(-1)

        if self._size == 0:
            self._leftmost_index_in_elem = None
            self._rightmost_index_in_elem = None

        return bit

    def initialise(self, state: int, amount: int) -> None:
        """
        Initialise a bitvector with a given amount of states.
        Premise:

        """
        amount_elements = amount // self.BITS_PER_ELEMENT
        rest_amount = amount % self.BITS_PER_ELEMENT

        if rest_amount != 0:
            amount_elements += 1

        number = 0 if state == 0 else (1 << self.BITS_PER_ELEMENT) - 1
        self._data.initialise(number, amount_elements)
        self._size = amount
        self._leftmost_index_in_elem = 0
        self._rightmost_index_in_elem = self.BITS_PER_ELEMENT - 1
        self._is_reversed = False
        self._is_flipped = False

        # append rest states
        for _ in range(rest_amount):
            self.append(state)
