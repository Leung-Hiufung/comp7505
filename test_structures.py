"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

NOTE: This file is not used for assessment. It is just a driver program for
you to write your own test cases and execute them against your data structures.
"""

# Import helper libraries
import random
import sys
import time
import argparse

# Import our data structures
from structures.linked_list import Node, DoublyLinkedList
from structures.dynamic_array import DynamicArray
from structures.bit_vector import BitVector


def test_linked_list():
    """
    A simple set of tests for the linked list implementation.
    This is not marked and is just here for you to test your code.
    """
    print("==== Executing Linked List Tests ====")

    # Consider expanding these tests into your own methods instead of
    # just doing a bunch of stuff here - this is just to get you started

    # OK, let's add some strings to a list
    my_list = DoublyLinkedList()
    assert my_list.get_size() == 0

    my_list.insert_to_front("hello")
    my_list.insert_to_back("algorithms")

    # Have a look - we can do this due to overriding __str__ in the class
    print(str(my_list))

    # Now lets try to find a node
    elem = my_list.find_element("algorithms")
    if elem is not None:
        print("Found node with data? ", elem)

    # And try to delete one
    elem = my_list.find_and_remove_element("1337")
    if elem is not None:
        print("Deleted ", elem)
    else:
        print("Didn't find element = 1337")

    # And try to delete another one
    elem = my_list.find_and_remove_element("hello")
    if elem is not None:
        print("Deleted ", elem)
    else:
        print("Didn't find element = world")

    # Have another look
    print(str(my_list))

    # OK, now check size
    assert my_list.get_size() == 1


def test_dynamic_array():
    """
    A simple set of tests for the dynamic array implementation.
    This is not marked and is just here for you to test your code.
    """
    print("==== Executing Dynamic Array Tests ====")
    array = DynamicArray()

    print("Sort empty array")
    array.sort()
    assert str(array) == "[]"

    print("Prepend 1:")
    array.prepend(1)
    assert array.get_at(0) == 1
    assert array.get_size() == 1
    assert str(array) == "[1]"

    print("Sort one-element array")
    array.sort()
    assert str(array) == "[1]"

    array.prepend(2)
    assert str(array) == "[2, 1]"
    array.prepend(3)
    assert str(array) == "[3, 2, 1]"

    print("Remove index 0")
    array.remove_at(0)
    assert array.get_at(0) == 2
    assert array.get_size() == 2
    assert str(array) == "[2, 1]"

    print("Append 2")
    array.append(2)
    assert array.get_at(0) == 2
    assert array.get_size() == 3
    assert str(array) == "[2, 1, 2]"

    print("Remove index 0")
    array.remove_at(0)
    assert array.get_at(0) == 1
    assert array.get_size() == 2
    assert str(array) == "[1, 2]"
    print(array)

    print("Remove index -2")
    array.remove_at(-2)
    assert array.get_at(0) == 2
    assert array.get_size() == 1
    assert str(array) == "[2]"

    print("Remove index -1")
    array.remove_at(-1)
    assert array.get_at(0) == None
    assert array.get_size() == 0
    assert str(array) == "[]"

    print("Append 1,9,8,9. Then prepend 4,0,6")
    array.append(1)
    assert str(array) == "[1]"
    print(array)
    array.append(9)
    assert str(array) == "[1, 9]"
    print(array)
    array.append(8)
    assert str(array) == "[1, 9, 8]"
    print(array)
    array.append(9)
    assert str(array) == "[1, 9, 8, 9]"
    print(array)
    array.prepend(4)
    assert str(array) == "[4, 1, 9, 8, 9]"
    print(array)
    array.prepend(0)
    assert str(array) == "[0, 4, 1, 9, 8, 9]"
    print(array)
    array.prepend(6)
    assert str(array) == "[6, 0, 4, 1, 9, 8, 9]"
    print(array)
    assert array.get_size() == 7
    array.prepend(0)
    assert str(array) == "[0, 6, 0, 4, 1, 9, 8, 9]"

    print("Remove 8")
    array.remove(8)
    assert str(array) == "[0, 6, 0, 4, 1, 9, 9]"
    print("The following should be:\n[0, 6, 0, 4, 1, 9, 9]")
    print(array)

    print("Reverse")
    array.reverse()
    print("The following should be:\n[9, 9, 1, 4, 0, 6, 0]")
    print(array)
    assert str(array) == "[9, 9, 1, 4, 0, 6, 0]"

    print("Append 7")
    array.append(7)
    assert str(array) == "[9, 9, 1, 4, 0, 6, 0, 7]"
    print(array)
    assert array.get_size() == 8
    assert array.get_at(8) == None
    assert array.get_at(7) == 7
    assert array.get_at(-3) == 6

    print("Prepend 0")
    array.prepend(0)
    assert str(array) == "[0, 9, 9, 1, 4, 0, 6, 0, 7]"
    assert array.get_at(7) == 0
    assert array.get_at(0) == 0

    print("Set 2 to index 2")
    array.set_at(2, 2)
    assert array.get_at(2) == 2
    assert str(array) == "[0, 9, 2, 1, 4, 0, 6, 0, 7]"

    print("Set 4 to index -2")
    array.set_at(-2, 4)
    assert array.get_at(7) == 4
    assert str(array) == "[0, 9, 2, 1, 4, 0, 6, 4, 7]"

    print(array)

    print("Sort")
    array.sort()
    print(array)
    assert str(array) == "[0, 0, 1, 2, 4, 4, 6, 7, 9]"

    print("Reverse")
    array.reverse()
    assert str(array) == "[9, 7, 6, 4, 4, 2, 1, 0, 0]"
    print(array)
    print("Sort")
    array.sort()
    assert str(array) == "[0, 0, 1, 2, 4, 4, 6, 7, 9]"
    print(array)

    print("Remove index 2")
    array.remove_at(567)
    print(array)
    assert str(array) == "[0, 0, 1, 2, 4, 4, 6, 7, 9]"

    # for i in range(10000):
    #     array.prepend(i)
    #     array[0] = i
    # print(array)


def test_bitvector():
    """
    A simple set of tests for the bit vector implementation.
    This is not marked and is just here for you to test your code.
    """
    print("==== Executing Bit Vector Tests ====")
    # bitvector = BitVector()

    # # Test 1: Append single bit
    # print("Append 1")
    # bitvector.append(1)
    # assert bitvector[0] == 1
    # print(bitvector)  # Expect: '1'

    # # Test 2: Append multiple bits
    # print("Append 0")
    # bitvector.append(0)
    # print(bitvector)  # Expect: '10'

    # print("Append 1")
    # bitvector.append(1)
    # print(bitvector)  # Expect: '101'

    # # Test 3: Prepend bits
    # print("Prepend 0")
    # bitvector.prepend(0)
    # print(bitvector)  # Expect: '0101'

    # print("Prepend 1")
    # bitvector.prepend(1)
    # print(bitvector)  # Expect: '10101'

    # # Test 4: Set bit at index 1
    # print("Set bit at index 1")
    # bitvector.set_at(1)
    # print(bitvector)  # Expect: '11101'

    # # Test 5: Unset bit at index
    # print("Unset bit at index 2")
    # bitvector.unset_at(2)
    # print(bitvector)  # Expect: '11001'

    # # Test 6: Get bit at index
    # print("Get bit at index 0")
    # print(bitvector.get_at(0))  # Expect: 1

    # print("Get bit at index 4")
    # print(bitvector.get_at(4))  # Expect: 1

    # # Test 7: Flip all bits
    # print("Flip all bits")
    # bitvector.flip_all_bits()
    # print(bitvector)  # Expect: '00110'

    # # Test 8: Reverse the bit vector
    # print("Reverse the bit vector")
    # bitvector.reverse()
    # print(bitvector)  # Expect: '01100'

    # # Test 9: Left shift
    # print("Left shift by 1")
    # bitvector.shift(1)
    # print(bitvector)  # Expect: '11000'

    # # Test 10: Right shift
    # print("Right shift by 2")
    # bitvector.shift(-2)
    # print(bitvector)  # Expect: '00110'

    # # Test 11: Append bits to full word
    # print("BitVector with 64 ones")
    # bitvector = BitVector()
    # for _ in range(64):
    #     bitvector.append(1)
    # print(bitvector)  # Expect: '111...111' (64 times)

    # # Test 12: Left shift on full word
    # print("Shift left by 4")
    # bitvector.shift(4)
    # print(bitvector)  # Expect: '111...10000' (60 ones followed by 4 zeros)

    # # Test 13: Right shift on full word
    # print("Shift right by 8")
    # bitvector.shift(-8)
    # print(bitvector)  # Expect: '000000001111...111' (8 zeros followed by 56 ones)

    # # Test 14: Rotate left
    # print("Rotate left by 16")
    # bitvector.rotate(16)
    # print(bitvector)  # Expect: '1111...1110000000' (56 ones followed by 8 zeros)

    # # Test 15: Rotate right
    # print("Rotate right by 8")
    # bitvector.rotate(-8)
    # print(bitvector)  # Expect: '000000001111...111' (8 zeros followed by 56 ones)

    # # Test 16: Flip all bits on full word
    # print("Flip all bits on full word")
    # bitvector.flip_all_bits()
    # print(bitvector)  # Expect: '111111110000...000' (8 ones followed by 56 zeros)

    # # Test 17: Prepend to an empty vector
    # print("Prepend 1 to empty vector")
    # empty_vector = BitVector()
    # empty_vector.prepend(1)
    # print(empty_vector)  # Expect: '1'

    # # Test 18: Append to an empty vector
    # print("Append 0 to vector")
    # empty_vector.append(0)
    # print(empty_vector)  # Expect: '10'

    # # Test 19: Flip on an empty vector
    # print("Flip all bits on empty vector")
    # empty_vector = BitVector()
    # empty_vector.flip_all_bits()
    # print(empty_vector)  # Expect: '' (remains empty)

    # # Test 20: Reverse on an empty vector
    # print("Reverse on empty vector")
    # empty_vector.reverse()
    # print(empty_vector)  # Expect: '' (remains empty)

    # # Test 21: Large vector operations
    # print("Large BitVector with 128 ones")
    # large_vector = BitVector()
    # for _ in range(128):
    #     large_vector.append(1)
    # print(large_vector)

    # print("Shift left by 64")
    # large_vector.shift(64)
    # print(large_vector)  # Expect: '1...1000000' (64 ones followed by 64 zeros)

    # print("Shift right by 32")
    # large_vector.shift(-32)
    # print(large_vector)  # Expect: '000000001...1' (32 zeros followed by 96 ones)

    # # Test 22: Get out of bounds
    # print("Get bit at index 130")
    # print(large_vector.get_at(130))  # Expect: None

    # # Test 23: Set out of bounds
    # print("Set bit at index 130")
    # large_vector.set_at(130)
    # print(large_vector.get_at(130))  # Expect: None (no change)

    # # Test 24: Unset out of bounds
    # print("Unset bit at index 130")
    # large_vector.unset_at(130)
    # print(large_vector.get_at(130))  # Expect: None (no change)

    # # Test 25: Rotate on large vector
    # print("Rotate left by 32")
    # large_vector.rotate(32)
    # print(large_vector)  # Expect: '1...10000000' (96 ones followed by 32 zeros)

    # # Test 26: Rotate on large vector
    # print("Rotate right by 64")
    # large_vector.rotate(-64)
    # print(large_vector)  # Expect: '000000001...1' (64 zeros followed by 64 ones)

    # # Test 27: Set, unset, get on large vector
    # large_vector.set_at(0)
    # print("Set bit at index 0")
    # print(large_vector)  # Expect: '100000001...1'

    # large_vector.unset_at(63)
    # print("Unset bit at index 63")
    # print(
    #     large_vector
    # )  # Expect: '100000000...1' (first and last ones, zero in between)

    # print("Get bit at index 0")
    # print(large_vector.get_at(0))  # Expect: 1

    # print("Get bit at index 63")
    # print(large_vector.get_at(63))  # Expect: 0

    # print("Get bit at index 127")
    # print(large_vector.get_at(127))  # Expect: 1

    # # Test 28: Flip all bits on large vector
    # print("Flip all bits on large vector")
    # large_vector.flip_all_bits()
    # print(large_vector)  # Expect: '011111110...0' (64 zeros followed by 64 ones)

    # # Test 29: Reverse large vector
    # print("Reverse large vector")
    # large_vector.reverse()
    # print(large_vector)  # Expect: '0000...01111111' (64 ones followed by 64 zeros)

    # # Test 30: Append after operations
    # print("Append 0 after operations")
    # large_vector.append(0)
    # print(large_vector)  # Expect: '0000...011111110'

    # # Test 31: Prepend after operations
    # print("Prepend 1 after operations")
    # large_vector.prepend(1)
    # print(large_vector)  # Expect: '10000...011111110'

    # # Test 32: Check size of bitvector
    # print("Get size of bitvector")
    # print(large_vector.get_size())  # Expect: 130 (128 original + 2 append/prepend)

    # # Test 33: Shift on varied vector
    # print("Shift varied vector left by 3")
    # varied_vector = BitVector()
    # for i in range(1, 10):
    #     varied_vector.append(i % 2)
    # varied_vector.shift(3)
    # print(varied_vector)  # Expect: '010000000'

    # print("Shift varied vector right by 3")
    # varied_vector.shift(-3)
    # print(varied_vector)  # Expect: '000000010'

    # # Test 34: Rotate on varied vector
    # print("Rotate varied vector left by 3")
    # varied_vector.rotate(3)
    # print(varied_vector)  # Expect: '000010000'

    # print("Rotate varied vector right by 3")
    # varied_vector.rotate(-3)
    # print(varied_vector)  # Expect: '000000010'

    # # Test 35: Append and flip operations
    # print("Flip all bits in small vector")
    # flipped_vector = BitVector()
    # flipped_vector.append(0)
    # flipped_vector.append(1)
    # flipped_vector.flip_all_bits()
    # print(flipped_vector)  # Expect: '10'

    # # Test 36: Prepend and reverse operations
    # print("Reverse small vector")
    # reversed_vector = BitVector()
    # reversed_vector.prepend(1)
    # reversed_vector.prepend(0)
    # reversed_vector.reverse()
    # print(reversed_vector)  # Expect: '10'

    # # Test 37: Rotate on full ones
    # print("Rotate full ones vector left by 32")
    # ones_vector = BitVector()
    # for _ in range(64):
    #     ones_vector.append(1)
    # ones_vector.rotate(32)
    # print(ones_vector)  # Expect: '111111111111111

    print("\n new flipped reversed")
    bitvector = BitVector()
    is1 = False
    bitvector.flip_all_bits()
    bitvector.reverse()
    # for i in range(1000):
    #     bitvector.append(1)
    #     is1 = not is1

    print(bitvector)
    print("append 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1")
    for bit in [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]:
        bitvector.append(bit)
    print(bitvector)

    for i in range(7739):
        print(i, bitvector._data._zero_index)
        bit = bitvector._pop_from_logical_left()
        bitvector.append(bit)


# sys.argv = ["test_structures.py", "--linkedlist"]
# sys.argv = ["test_structures.py", "--dynamicarray"]
sys.argv = ["test_structures.py", "--bitvector"]

# The actual program we're running here
if __name__ == "__main__":
    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(
        description="COMP3506/7505 Assignment One: Testing Data Structures"
    )

    parser.add_argument(
        "--linkedlist", action="store_true", help="Test your linked list."
    )
    parser.add_argument(
        "--dynamicarray", action="store_true", help="Test your dynamic array."
    )
    parser.add_argument(
        "--bitvector", action="store_true", help="Test your bit vector."
    )
    parser.add_argument("--seed", type=int, default="42", help="Seed the PRNG.")

    args = parser.parse_args()

    # No arguments passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    # Seed the PRNG in case you are using randomness
    random.seed(args.seed)

    # Now check/run the selected algorithm
    if args.linkedlist:
        test_linked_list()

    if args.dynamicarray:
        test_dynamic_array()

    if args.bitvector:
        test_bitvector()
