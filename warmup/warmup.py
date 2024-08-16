"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

WARMUP PROBLEMS

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
"""

"""
You may wish to import your data structures to help you with some of the
problems. Or maybe not. We did it for you just in case.
"""
from structures.bit_vector import BitVector
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList, Node

import math
from typing import Any


def main_character(instring: list[int]) -> int:
    """
    @instring@ is an array of integers in the range [0, 2^{32}-1].
    Return the first position a repeat integer is encountered, or -1 if
    there are no repeated ints.

    Limitations:
        "It works":
            @instring@ may contain up to 10'000 elements.

        "Exhaustive":
            @instring@ may contain up to 300'000 elements.

        "Welcome to COMP3506":
            @instring@ may contain up to 5'000'000 elements.

    Examples:
    main_character([1, 2, 3, 4, 5]) == -1
    main_character([1, 2, 1, 4, 4, 4]) == 2
    main_character([7, 1, 2, 7]) == 3
    main_character([60000, 120000, 654321, 999, 1337, 133731337]) == -1
    """

    # bitvector = BitVector()
    # bitvector.initialise(0, 2**32)

    # for index, num in enumerate(instring):
    #     if bitvector.get_at(num) == 0:
    #         bitvector.set_at(num)
    #     else:
    #         return index
    # return -1
    bitset = BitSet(1 << 32)
    for index, value in enumerate(instring):
        if bitset.contains(value):
            return index
        bitset.add(value)

    return -1


class BitSet:
    def __init__(self, size: int):
        self.size = size
        self.bitvector = [0] * (self.size // 64 + 1)  # 每个元素是一个64位的int

    def add(self, value: int) -> None:
        index = value // 64
        position = value % 64
        self.bitvector[index] |= 1 << position

    def contains(self, value: int) -> bool:
        index = value // 64
        position = value % 64
        return (self.bitvector[index] & (1 << position)) != 0


def missing_odds(inputs: list[int]) -> int:
    """
    @inputs@ is an unordered array of distinct integers.
    If @a@ is the smallest number in the array and @b@ is the biggest,
    return the sum of odd numbers in the interval [a, b] that are not present in @inputs@.
    If there are no such numbers, return 0.

    Limitations:
        "It works":
            @inputs@ may contain up to 10'000 elements.
            Each element is in range 0 <= inputs[i] <= 10^4
        "Exhaustive":
            @inputs@ may contain up to 300'000 elements.
            Each element is in range 0 <= inputs[i] <= 10^6
        "Welcome to COMP3506":
            @inputs@ may contain up to 5'000'000 elements.
            Each element is in range 0 <= inputs[i] <= 10^16

    Examples:
    missing_odds([1, 2]) == 0
    missing_odds([1, 3]) == 0
    missing_odds([1, 4]) == 3
    missing_odds([4, 1]) == 3
    missing_odds([4, 1, 8, 5]) == 10    # 3 and 7 are missing
    """

    # YOUR CODE GOES HERE
    minimum = inputs[0]
    maximum = inputs[0]
    sum_odd_in_array = 0

    # find max and min
    for num in inputs:
        if num < minimum:
            # Get the max
            minimum = num
        if num > maximum:
            # Get the min
            maximum = num
        if num % 2 == 1:
            # Add all odd numbers in array to `sum`
            sum_odd_in_array += num

    # Let interval collapse to "both sides are odd"
    if maximum % 2 == 0:
        maximum += 1
        sum_odd_in_array += maximum
    if minimum % 2 == 0:
        minimum -= 1
        sum_odd_in_array += minimum

    # Case 1: No odd number in the interval
    if maximum - minimum <= 2:
        return 0

    # Case 2: Add all odd numbers in the interval (inclusive)
    sum_odd_sequence = (maximum**2 - minimum**2 + 2 * (minimum + maximum)) // 4
    return sum_odd_sequence - sum_odd_in_array


def k_cool(k: int, n: int) -> int:
    """
    Return the n-th largest k-cool number for the given @n@ and @k@.
    The result can be large, so return the remainder of division of the result
    by 10^16 + 61 (this constant is provided).

    Limitations:
        "It works":
            2 <= k <= 128
            1 <= n <= 10000
        "Exhaustive":
            2 <= k <= 10^16
            1 <= n <= 10^100     (yes, that's ten to the power of one hundred)
        "Welcome to COMP3506":
            2 <= k <= 10^42
            1 <= n <= 10^100000  (yes, that's ten to the power of one hundred thousand)

    Examples:
    k_cool(2, 1) == 1                     # The first 2-cool number is 2^0 = 1
    k_cool(2, 3) == 3                     # The third 2-cool number is 2^1 + 2^0 = 3
    k_cool(3, 5) == 10                    # The fifth 3-cool number is 3^2 + 3^0 = 10
    k_cool(10, 42) == 101010
    k_cool(128, 5000) == 9826529652304384 # The actual result is larger than 10^16 + 61,
                                          # so k_cool returns the remainder of division by 10^16 + 61
    """

    MODULUS = 10**16 + 61

    # Use Mathematical approach,
    # From small to large, take n=1~16 as example, each digit in number indicate the addends' powers
    # 0, 1, 10, 2, 20, 21, 210, 3, 30, 31, 310, 32, 320, 321, 3210.
    # Use binary to encode the number, 1 means occur, 0 mean absence
    # **** each digit stands for the existence of the power (3,2,1,0)
    # 0000, 0001, 0010, 0011, 0100, 0101, 0110, 0111, 1000, 1001, 1010, 1011, 1100, 1101, 1110, 1111
    # exactly encodes to binary number 0-15

    # addend_amount = int(math.log2(n)) + 1
    # binary_str = f"{(n):0b}"
    # answer = 0
    # for index, char in enumerate(binary_str):
    #     bit = 0 if char == "0" else 1
    #     answer += bit * k ** (addend_amount - index - 1)
    # return answer % MODULUS

    result = 0
    power = 1  # power is the result of k^n, initial is k^0 =1
    while n > 0:
        # calculate last bit each iteration
        if n & 1:
            # if n is odd, then the bit is 1, this power exists, add k^i, 0<=i<max_power
            result += power
            result %= MODULUS
        # calculate next iteration's result, which is k^(i+1)
        power *= k
        power %= MODULUS
        # n divided by 2
        n >>= 1

    return result


def number_game(numbers: list[int]) -> tuple[str, int]:
    """
    @numbers@ is an unordered array of integers. The array is guaranteed to be of even length.
    Return a tuple consisting of the winner's name and the winner's score assuming that both play optimally.
    "Optimally" means that each player makes moves that maximise their chance of winning
    and minimise opponent's chance of winning.
    You are ALLOWED to use a tuple in your return here, like: return (x, y)
    Possible string values are "Alice", "Bob", and "Tie"

    Limitations:
        "It works":
            @numbers@ may contain up to 10'000 elements.
            Each element is in range 0 <= numbers[i] <= 10^6
        "Exhaustive":
            @numbers@ may contain up to 100'000 elements.
            Each element is in range 0 <= numbers[i] <= 10^16
        "Welcome to COMP3506":
            @numbers@ may contain up to 300'000 elements.
            Each element is in range 0 <= numbers[i] <= 10^16

    Examples:
    number_game([5, 2, 7, 3]) == ("Bob", 5)
    number_game([3, 2, 1, 0]) == ("Tie", 0)
    number_game([2, 2, 2, 2]) == ("Alice", 4)

    For the second example, if Alice picks 2 to increase her score, Bob will pick 3 and win. Alice does not want that.
    The same happens if she picks 1 or 0, but this time she won't even increase her score.
    The only scenario when Bob does not win immediately is if Alice picks 3.
    Then, Bob faces the same choice:
    pick 1 to increase his score knowing that Alice will pick 2 and win, or pick 2 himself.
    The same happens on the next move.
    So, nobody picks any numbers to increase their score, which results in a Tie with both players having scores of 0.
    """

    # YOUR CODE GOES HERE
    # alice = 0
    # bob = 0

    # length = binary_length(numbers)
    # quick_sort(numbers, 0, length)
    # i = length - 1
    # while i > 0:
    #     alice_pick = numbers[i]
    #     bob_pick = numbers[i - 1]
    #     alice += alice_pick * ((alice_pick & 1) ^ 1)
    #     bob += bob_pick * (bob_pick & 1)
    #     i -= 2

    evens = [num for num in numbers if num & 1 == 0]
    odds = [num for num in numbers if num & 1 == 1]

    evens_length = binary_length(evens)
    odds_length = binary_length(odds)
    # odd numbers and even numbers sort respectively
    quick_sort(evens, 0, evens_length)
    quick_sort(odds, 0, odds_length)

    even_index = evens_length - 1  # the last element index in evens
    odd_index = odds_length - 1  # the last element index in odds

    alice_score = 0
    bob_score = 0
    turn = 0  # 0 is Alice's turn , 1 is Bob's turn

    # even/odd index == 1: no element in the array, i.e. none
    # even/odd index > -1: array has element, i.e. not none
    while even_index > -1 or odd_index > -1:
        # Alice turn
        if turn == 0:
            if even_index > -1 and (
                odd_index == -1 or evens[even_index] >= odds[odd_index]
            ):
                alice_score += evens[even_index]
                # Pop the element
                evens[even_index] = None
                even_index -= 1
            elif odd_index > -1:
                odds[odd_index] = None
                odd_index -= 1
        # Bob turn
        else:
            if odd_index > -1 and (
                even_index == -1 or odds[odd_index] >= evens[even_index]
            ):
                bob_score += odds[odd_index]
                odds[odd_index] = None
                odd_index -= 1
            elif even_index > -1:
                evens[even_index] = None
                even_index -= 1
        turn ^= 1

    if alice_score > bob_score:
        return ("Alice", alice_score)
    elif alice_score < bob_score:
        return ("Bob", bob_score)
    else:
        return ("Tie", alice_score)


def road_illumination(road_length: int, poles: list[int]) -> float:
    """
    @poles@ is an unordered array of integers.
    Return a single floating point number representing the smallest possible radius of illumination
    required to illuminate the whole road.
    Floating point numbers have limited precision. Your answer will be accepted
    if the relative or absolute error does not exceed 10^(-6),
    i.e. |your_ans - true_ans| <= 0.000001 OR |your_ans - true_ans|/true_ans <= 0.000001

    Limitations:
        "It works":
            @poles@ may contain up to 10'000 elements.
            0 <= @road_length@ <= 10^6
            Each element is in range 0 <= poles[i] <= 10^6
        "Exhaustive":
            @poles@ may contain up to 100'000 elements.
            0 <= @road_length@ <= 10^16
            Each element is in range 0 <= poles[i] <= 10^16
        "Welcome to COMP3506":
            @poles@ may contain up to 300'000 elements.
            0 <= @road_length@ <= 10^16
            Each element is in range 0 <= poles[i] <= 10^16

    Examples:
    road_illumination(15, [15, 5, 3, 7, 9, 14, 0]) == 2.5
    road_illumination(5, [2, 5]) == 2.0
    """

    # YOUR CODE GOES HERE

    length = binary_length(poles)
    quick_sort(poles, 0, length)

    # Ensure the first light covers the start of the road, compare (0, [0])
    radius = poles[0]

    for i in range(length - 1):
        # Ensure lights can cover the middle part of the road
        # Compare ([0], [1]), ([1], [2]), ..., ([-2], [-1])
        distance = poles[i + 1] - poles[i]
        if distance / 2 > radius:
            radius = distance / 2

    # Ensure the final light covers the end of the road, compare (-1, road_length)
    distance = road_length - poles[-1]
    radius = distance if distance > radius else radius
    return radius


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


def heap_sort(arr: list[int]) -> None:
    """"""
    last_index = binary_length(arr) - 1

    def holds_heap(index: int) -> None:

        left_index = index * 2 + 1
        right_index = index * 2 + 2

        # case 1: no children
        if left_index > last_index:
            return

        # case 2: only one child
        if left_index == last_index:
            max_value = arr[index] if arr[index] >= arr[left_index] else arr[left_index]
        else:
            # case 3: has two children
            if arr[index] >= arr[left_index]:
                max_value = (
                    arr[index] if arr[index] >= arr[right_index] else arr[right_index]
                )
            else:
                max_value = (
                    arr[left_index]
                    if arr[left_index] >= arr[right_index]
                    else arr[right_index]
                )

        # base case: parent is biggest
        if arr[index] == max_value:
            return

        # recursion: swap bigger child with parent, then holds the heap
        if arr[left_index] == max_value:
            arr[index], arr[left_index] = arr[left_index], arr[index]
            holds_heap(left_index)

        else:
            # right one is bigger
            arr[index], arr[right_index] = arr[right_index], arr[index]
            holds_heap(right_index)

    # build heap
    for index in range((len(arr) - 2) // 2, -1, -1):
        holds_heap(index)

    # heap sort
    while last_index >= 0:
        arr[0], arr[last_index] = arr[last_index], arr[0]
        last_index -= 1
        holds_heap(0)

    # return arr
