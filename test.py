from typing import Any


def quick_sort(array: list[int], low: int, high: int) -> None:
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


# def swap(array, index1, index2):
#     """
#     Swap two values with the given two indexes.
#     """
#     temp = array[index1]
#     array[index1] = array[index2]
#     array[index2] = temp
#     set_at(index1, get_at(index2))
#     set_at(index2, temp)
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
