"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any


class DynamicArray:
    def __init__(self) -> None:
        self._capacity = 4
        self._array = [None] * self._capacity
        self._size = 0
        self._is_reversed = False
        self._zero_index = None

    def __str__(self) -> str:
        """
        A helper that allows you to print a DynamicArray type
        via the str() method.
        """
        if self._size == 0:
            return "[]"

        array = [None] * self._size
        for i in range(self._size):
            array[i] = self.get_at(i)
        return f"{array}"

    def __repr__(self) -> str:
        return self.__str__()

    def __resize(self) -> None:
        # Should be extended
        if self._size >= self._capacity / 2:
            new_capacity = self._capacity * 2
        # Should be collapsed
        elif self._size < self._capacity // 4:
            new_capacity = self._capacity // 2
        # No size adjusted, redistribute element
        elif self._zero_index == 0 or self._zero_index == self._size:
            new_capacity = self._capacity
        else:
            return

        new_array = [None] * new_capacity
        new_zero_index = new_capacity // 3
        for i in range(self._size):
            new_array[i + new_zero_index] = self._array[i + self._zero_index]
        self._array = new_array
        self._capacity = new_capacity
        self._zero_index = new_zero_index

    def _get_real_index(self, index: int) -> int | None:
        if 0 <= index < self._size:
            # self._set_at_no_bound(index, element)
            index = index
        elif -self._size <= index < 0:
            # return self._set_at_no_bound(self._size + index, element)
            index = self._size + index
        else:
            return None

        if self._is_reversed:
            index = self._zero_index + self._size - index - 1
        else:
            index += self._zero_index
        return index

    def get_at(self, index: int) -> Any | None:
        """
        Get element at the given index.
        Return None if index is out of bounds.
        Time complexity for full marks: O(1)
        """
        real_index = self._get_real_index(index)

        if real_index is None:
            return
        else:
            return self._array[real_index]
        # try:
        #     return self._array[real_index]
        # except IndexError:
        #     return None

        # if 0 <= index < self._size:
        #     return self.__getitem__(index)
        # elif -self._size <= index < 0:
        #     return self.__getitem__(self._size + index)
        # else:
        #     return None

    def __getitem__(self, index: int) -> Any | None:
        """
        Same as get_at.
        Allows to use square brackets to index elements.
        """
        # real_index = (
        #     self._zero_index + self._size - index - 1
        #     if self._is_reversed
        #     else index + self._zero_index
        # )
        # try:
        #     return self._array[real_index]
        # except IndexError:
        #     return None
        return self.get_at(index)

    def set_at(self, index: int, element: Any) -> None:
        """
        Get element at the given index.
        Do not modify the list if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        real_index = self._get_real_index(index)
        if real_index is None:
            return
        else:
            try:
                self._array[real_index] = element
            except IndexError:
                pass

    def __setitem__(self, index: int, element: Any) -> None:
        """
        Same as set_at.
        Allows to use square brackets to index elements.
        """
        self.set_at(index, element)

    # def _set_at_no_bound(self, index: int, element: Any) -> None:
    #     if self._is_reversed:
    #         real_index = self._zero_index + self._size - index - 1
    #     else:
    #         real_index = index + self._zero_index
    #     self._array[real_index] = element

    def append(self, element: Any) -> None:
        """
        Add an element to the back of the array.
        Time complexity for full marks: O(1*) (* means amortized)
        """
        if self._size == 0:
            self._zero_index = 1

        self._size += 1

        if self._size + self._zero_index >= self._capacity or self._zero_index == 0:
            self.__resize()
        # self._set_at_no_bound(self._size, element)

        if self._is_reversed:
            self._zero_index -= 1
        self[-1] = element

    def prepend(self, element: Any) -> None:
        """
        Add an element to the front of the array.
        Time complexity for full marks: O(1*)
        """
        if self._size == 0:
            self.append(element)
            return

        self._size += 1
        if self._size + self._zero_index >= self._capacity or self._zero_index == 0:
            self.__resize()
        # self._set_at_no_bound(-1, element)

        if not self._is_reversed:
            self._zero_index -= 1

        self.set_at(0, element)

    def reverse(self) -> None:
        """
        Reverse the array.
        Time complexity for full marks: O(1)
        """
        self._is_reversed = not self._is_reversed

    def remove(self, element: Any) -> None:
        """
        Remove the first occurrence of the element from the array.
        If there is no such element, leave the array unchanged.
        Time complexity for full marks: O(N)
        """
        is_found = False
        for i in range(self._size):
            if self.get_at(i) == element:
                is_found = True
                target_index = i
                break
        if not is_found:
            return
        for i in range(target_index, self._size + 1):
            self.set_at(i, self.get_at(i + 1))
        self._size -= 1

        if self._size == 0:
            self._zero_index = None

        # self.__resize()

    def remove_at(self, index: int) -> Any | None:
        """
        Remove the element at the given index from the array and return the removed element.
        If there is no such element, leave the array unchanged and return None.
        Time complexity for full marks: O(N)
        """
        if self[index] is None:
            return
        element = self[index]

        if index == 0 or index == -self._size:
            # Remove the first element, O(1)
            self[0] = None
            self._zero_index += 1
        elif index == self._size - 1 or index == -1:
            # Remove the back element, O(1)
            self[-1] = None
        else:
            # Remove other elements, O(N)
            index = self._size + index if index < 0 else index
            for i in range(index, self._size - 1):
                self[i] = self[i + 1]
        self._size -= 1

        if self._size == 0:
            self._zero_index = None

        # self.__resize()
        return element

    # def _pop_from_front(self) -> None:
    #     """
    #     Pop the first element. O(1)
    #     Before:
    #         self._size > 0
    #     """
    #     self.set_at(0, None)
    #     self._size -= 1
    #     self._zero_index = None if self.is_empty() else self._zero_index + 1

    # def _pop_from_back(self) -> None:
    #     """
    #     Pop the back element. O(1)
    #     Before:
    #         self._size > 0
    #     """
    #     self.set_at(-1, None)
    #     self._size -= 1
    #     if self.is_empty():
    #         self._zero_index = None

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        return self._size == 0

    def is_full(self) -> bool:
        """
        Boolean helper to tell us if the structure is full or not
        Time complexity for full marks: O(1)
        """
        return self._size == self._capacity

    def get_size(self) -> int:
        """
        Return the number of elements in the list
        Time complexity for full marks: O(1)
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of slots) of the list
        Time complexity for full marks: O(1)
        """
        return self._capacity

    def sort(self) -> None:
        """
        Sort elements inside _data based on < comparisons.
        Time complexity for full marks: O(NlogN)
        """
        # Change to merge sort
        sorted_array = self._merge_sort_helper(0, self._size)
        for i in range(self._size):
            self.set_at(i, sorted_array[i])
        # self._quick_sort_helper(0, self._size)

    def quicksort(self) -> None:
        self._quick_sort_helper(0, self._size)

    def _merge_sort_helper(self, low: int, high: int) -> Any:
        """
        A Merge Sort helper, recursion function.
        Parameters:
            low: The start index in the sorting interval, inclusive. (Logically, use get_at())
            high: The end index in the sorting interval, exclusive. (Logically, use get_at())
        """
        # Base Case
        # No number in sub-array
        if high <= low:
            return DynamicArray()
        # One number in sub-array
        if high - low == 1:
            sub_array = DynamicArray()
            sub_array.append(self.get_at(low))
            return sub_array
        # Two numbers in sub-array
        if high - low == 2:
            sub_array = DynamicArray()
            num_1 = self.get_at(low)
            num_2 = self.get_at(low + 1)
            sub_array.append(num_1)
            if num_2 < num_1:
                sub_array.prepend(num_2)
            else:
                sub_array.append(num_2)
            return sub_array

        # Recursion, get sorted left_sorted part and right_sorted part
        middle_index = (low + high) // 2
        left_sorted = self._merge_sort_helper(low, middle_index)
        right_sorted = self._merge_sort_helper(middle_index, high)

        # Merge Sort left_sorted and right_sorted
        sorted_subarray = DynamicArray()
        left_flag = 0
        right_flag = 0
        while (
            left_flag < left_sorted.get_size() and right_flag < right_sorted.get_size()
        ):
            left_num = left_sorted[left_flag]
            right_num = right_sorted[right_flag]
            if left_num < right_num:
                sorted_subarray.append(left_num)
                left_flag += 1
            else:
                sorted_subarray.append(right_num)
                right_flag += 1

        # Merge the remaining numbers
        if left_flag == left_sorted.get_size():
            for i in range(right_flag, right_sorted.get_size()):
                sorted_subarray.append(right_sorted[i])
        else:
            for i in range(left_flag, left_sorted.get_size()):
                sorted_subarray.append(left_sorted[i])
        return sorted_subarray

    def _quick_sort_helper(self, low: int, high: int) -> None:
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
            while self[i] > self[pivot]:
                self.swap(i, pivot - 1)
                self.swap(pivot - 1, pivot)
                pivot -= 1
            i += 1
        # Recursion. Left part of pivot, and then the right part.
        self._quick_sort_helper(low, pivot)
        self._quick_sort_helper(pivot + 1, high)

    def swap(self, index1, index2):
        """
        Swap two values with the given two indexes.
        """
        temp = self[index1]
        self[index1] = self[index2]
        self[index2] = temp

    def get_physical_array(self) -> list[Any]:
        return self._array

    def initialise(self, number: int, amount: int) -> None:
        self._array = [number] * amount
        self._capacity = amount
        self._size = amount
        self._is_reversed = False
        self._zero_index = 0

    def initialise_from_list(self, array: list[Any]) -> None:
        size = binary_length(array)
        self._array = array
        self._capacity = size
        self._size = size
        self._is_reversed = False
        self._zero_index = 0

    def to_python_list(self) -> list[Any]:
        python_list = [None] * self._size
        for i in range(self._size):
            python_list[i] = self[i]

        return python_list


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
