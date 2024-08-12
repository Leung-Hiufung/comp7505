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

from warmup.warmup import *


def test_main_character():
    """
    A simple set of tests for the main character problem.
    This is not marked and is just here for you to test your code.
    """
    assert main_character([1, 2, 3, 4, 5]) == -1
    assert main_character([1, 2, 1, 4, 4, 4]) == 2
    assert main_character([7, 1, 2, 7]) == 3
    assert main_character([60000, 120000, 654321, 999, 1337, 133731337]) == -1


def test_missing_odds():
    """
    A simple set of tests for the missing odds problem.
    This is not marked and is just here for you to test your code.
    """
    assert missing_odds([1, 2]) == 0
    assert missing_odds([1, 3]) == 0
    assert missing_odds([1, 4]) == 3
    assert missing_odds([4, 1]) == 3
    assert missing_odds([4, 1, 8, 5]) == 10  # 3 and 7 are missing


def test_k_cool():
    """
    A simple set of tests for the k cool problem.
    This is not marked and is just here for you to test your code.
    """
    assert k_cool(2, 1) == 1  # The first 2-cool number is 2^0 = 1
    assert k_cool(2, 3) == 3  # The third 2-cool number is 2^1 + 2^0 = 3
    assert k_cool(3, 5) == 10  # The fifth 3-cool number is 3^2 + 3^0 = 10
    assert k_cool(10, 42) == 100010000
    print(k_cool(128, 5000))
    # The actual result is larger than 10^16 + 61,
    # so k_cool returns the remainder of division by 10^16 + 61


def test_number_game():
    """
    A simple set of tests for the number game problem.
    This is not marked and is just here for you to test your code.
    """


def test_road_illumination():
    """
    A simple set of tests for the road illumination problem.
    This is not marked and is just here for you to test your code.
    """
    assert road_illumination(15, [15, 5, 3, 7, 9, 14, 0]) == 2.5
    assert road_illumination(5, [2, 5]) == 2.0

    assert (
        abs(road_illumination(15, [15, 5, 3, 7, 9, 14, 0]) - 2.5) <= 0.000001
    ), "Test 1 Failed"
    assert abs(road_illumination(5, [2, 5]) - 2.0) <= 0.000001, "Test 2 Failed"
    assert abs(road_illumination(100, [0, 100]) - 50.0) <= 0.000001, "Test 3 Failed"
    assert abs(road_illumination(50, [25]) - 25.0) <= 0.000001, "Test 4 Failed"
    assert abs(road_illumination(1, [0, 1]) - 0.5) <= 0.000001, "Test 5 Failed"

    assert abs(road_illumination(10, [0]) - 10.0) <= 0.000001, "Test 6 Failed"
    assert abs(road_illumination(10, [10]) - 10.0) <= 0.000001, "Test 7 Failed"
    assert abs(road_illumination(10, [5]) - 5.0) <= 0.000001, "Test 8 Failed"
    assert abs(road_illumination(0, []) - 0.0) <= 0.000001, "Test 9 Failed"
    assert (
        abs(road_illumination(1000, list(range(0, 1001, 100))) - 50.0) <= 0.000001
    ), "Test 10 Failed"

    # 构造大规模数据测试
    large_poles = [i for i in range(100001)]
    assert (
        abs(road_illumination(100000, large_poles) - 0.5) <= 0.000001
    ), "Test 11 Failed"

    # 构造数据，间隔最大
    max_distance_poles = [0, 10**6]
    assert (
        abs(road_illumination(10**6, max_distance_poles) - 500000.0) <= 0.000001
    ), "Test 12 Failed"

    # 测试仅两个极端位置的灯
    assert (
        abs(road_illumination(10**6, [0, 10**16]) - 5 * 10**15) <= 0.000001
    ), "Test 13 Failed"

    # 随机分布的大数据测试
    # import random

    # random_poles = random.sample(range(10**16), 300000)
    # assert (
    #     abs(road_illumination(10**16, random_poles) - 16666.666667) <= 0.000001
    # ), "Test 14 Failed"

    # 极端单点情况
    assert (
        abs(road_illumination(10**16, [10**8]) - (10**16 - 10**8)) <= 0.000001
    ), "Test 15 Failed"

    # 所有灯在中间聚集
    assert abs(road_illumination(100, [50] * 100) - 50.0) <= 0.000001, "Test 16 Failed"

    # 重复的极端位置
    assert (
        abs(road_illumination(1000, [0] * 50 + [1000] * 50) - 500.0) <= 0.000001
    ), "Test 17 Failed"

    # 间隔大的稀疏分布
    sparse_poles = [10**i for i in range(6)]
    assert (
        abs(road_illumination(10**5, sparse_poles) - 45000.0) <= 0.000001
    ), "Test 18 Failed"

    # 全部灯在起点
    assert (
        abs(road_illumination(100, [0] * 10000) - 100.0) <= 0.000001
    ), "Test 19 Failed"

    # 全部灯在终点
    assert (
        abs(road_illumination(100, [100] * 10000) - 100.0) <= 0.000001
    ), "Test 20 Failed"


sys.argv = ["test_warmup.py", "--kcool"]
# The actual program we're running here
if __name__ == "__main__":
    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(
        description="COMP3506/7505 Assignment One: Testing Warmup Problems"
    )

    parser.add_argument(
        "--character", action="store_true", help="Test your main character sol."
    )
    parser.add_argument(
        "--odds", action="store_true", help="Test your missing odds sol."
    )
    parser.add_argument("--kcool", action="store_true", help="Test your k-cool sol.")
    parser.add_argument(
        "--numbergame", action="store_true", help="Test your number game sol."
    )
    parser.add_argument(
        "--road", action="store_true", help="Test your road illumination sol."
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
    if args.character:
        test_main_character()

    if args.odds:
        test_missing_odds()

    if args.kcool:
        test_k_cool()

    if args.numbergame:
        test_number_game()

    if args.road:
        test_road_illumination()
