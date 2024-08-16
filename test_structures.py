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
from structures.bit_list import BitList


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
    bv = BitVector()
    bl = BitList()
    for i in range(1000):
        bit = random.randint(0, 1)
        bv.append(bit)
        bl.append(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.prepend(bit)
        bl.prepend(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bv.flip_all_bits()
        bl.flip_all_bits()
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        for k in range(1000):
            bv.prepend(bit)
            bl.prepend(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.append(bit)
        bl.append(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bv.flip_all_bits()
        bl.flip_all_bits()
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.prepend(bit)
        bl.prepend(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.append(bit)
        bl.append(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bv.reverse()
        bl.reverse()
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.prepend(bit)
        bl.prepend(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.append(bit)
        bl.append(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bv.reverse()
        bl.reverse()
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bv.flip_all_bits()
        bl.flip_all_bits()
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.prepend(bit)
        bl.prepend(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.append(bit)
        bl.append(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bv.reverse()
        bl.reverse()
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.prepend(bit)
        bl.prepend(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        bit = random.randint(0, 1)
        bv.append(bit)
        bl.append(bit)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]

        dist = random.randint(-1000000, 10000000)
        bv.rotate(dist)
        bl.rotate(dist)
        bv.flip_all_bits()
        bl.flip_all_bits()
        bv.reverse()
        bl.reverse()
        dist = random.randint(-1000000, 10000000)
        bv.rotate(dist)
        bl.rotate(dist)
        assert str(bv) == str(bl)
        for i in range(bv.get_size()):
            assert bl[i] == bv[i]
    print(str(bv))
    print(str(bl))
    assert str(bv) == str(bl)


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
