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

from malloclabs.kmer_structure import KmerStore


def test_kmer_store_build(filepath: str):
    """
    A set of tests for building a kmer store
    This is not marked and is just here for you to test your code.
    """
    # ks = KmerStore(50)  # test using 50-mers
    # # ks.read(filepath)

    # sequences = [
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATT",
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATT",  # Same as the first one
    #     "CTGTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATT",  # Modify index 2 C->G
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATG",  # Modify index -1 T->G
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATC",  # Modify index -1 T->C
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATA",  # Modify index -1 T->A
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATA",
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATA",
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATA",
    #     "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAAGA",
    # ]

    # ks.batch_insert(sequences)
    # print("Count the number of kmers")
    # print(ks.count_prefix())

    # prefix = "CTG"
    # print(f'Count the number of kmers starting with "{prefix}"')
    # print(ks.count_prefix(prefix))

    # prefix = "CTC"
    # print(f'Count the number of kmers starting with "{prefix}"')
    # print(ks.count_prefix(prefix))

    # sequence = "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATT"
    # print(f'Count the number of kmer: "{sequence}"')
    # print(ks.count_prefix(sequence))

    # sequence = "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATA"
    # print(f'Count the number of kmer: "{sequence}"')
    # print(ks.count_prefix(sequence))

    # sequence = "CTGTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATT"
    # print(f'Count the number of kmer that is lexicographically >= "{sequence}"')
    # print(ks.count_geq(sequence))

    # sequence = "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATT"
    # print(f'Count the number of kmer that is lexicographically >= "{sequence}"')
    # print(ks.count_geq(sequence))

    # sequence = "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATG"
    # print(f'Count the number of kmer that is lexicographically >= "{sequence}"')
    # print(ks.count_geq(sequence))

    # sequence = "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATC"
    # print(f'Count the number of kmer that is lexicographically >= "{sequence}"')
    # print(ks.count_geq(sequence))

    # sequence = "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAATA"
    # print(f'Count the number of kmer that is lexicographically >= "{sequence}"')
    # print(ks.count_geq(sequence))

    # m = 4
    # print(f"Get kmers that occurs >= {m} times")
    # result = ks.freq_geq(m)
    # for kmer in result:
    #     print(kmer)

    # sequence = "CTCTTCAAACTTGATTAGCTCACTCTACGTACCCTGAGGATTGGGGAAGA"
    # print(f"Count the compatitable kmer with {sequence}")
    # print(ks.compatible(sequence))
    # 设置DNA文件的路径
    filepath = "malloclabs/dna.txt"

    # 1. 初始化 KmerStore，设置 k 为 3, 4, 5 进行测试
    store1 = KmerStore(3)
    store2 = KmerStore(4)
    store3 = KmerStore(5)

    # 2. 从文件中读取序列并插入到 KmerStore 中
    store1.read(filepath)
    store2.read(filepath)
    store3.read(filepath)

    # 3. 测试 count 函数
    assert store1.count("GCA") == 1, "Failed test case: count('GCA')"
    assert store2.count("GCAG") == 1, "Failed test case: count('GCAG')"
    assert store3.count("GCAGA") == 1, "Failed test case: count('GCAGA')"

    assert store1.count("TGG") >= 1, "Failed test case: count('TGG')"
    assert store2.count("TGGA") >= 1, "Failed test case: count('TGGA')"
    assert store3.count("TGGAC") >= 1, "Failed test case: count('TGGAC')"

    assert store1.count("AAA") == 0, "Failed test case: count('AAA')"
    assert store2.count("AAAA") == 0, "Failed test case: count('AAAA')"
    assert store3.count("AAAAA") == 0, "Failed test case: count('AAAAA')"

    # 4. 测试 freq_geq 函数
    assert store1.freq_geq(2) == [], "Failed test case: freq_geq(2)"
    assert store2.freq_geq(2) == [], "Failed test case: freq_geq(2)"
    assert store3.freq_geq(2) == ["GGGGA"], "Failed test case: freq_geq(2)"

    # 5. 测试 count_prefix 函数
    assert store1.count_prefix("G") > 0, "Failed test case: count_prefix('G')"
    assert store2.count_prefix("GC") > 0, "Failed test case: count_prefix('GC')"
    assert store3.count_prefix("GCA") > 0, "Failed test case: count_prefix('GCA')"

    # 6. 测试删除功能
    store3.batch_delete(["GGGGG"])
    assert store3.count("GGGGG") == 0, "Failed test case: delete('GGGGG')"

    # 7. 添加更多测试数据，确保代码的稳定性和正确性
    kmers_to_test = [
        ("CAG", 1),
        ("TAG", 1),
        ("GTC", 1),
        ("CGC", 1),
        ("TCT", 1),
        ("GAC", 1),
        ("AAT", 1),
        ("TGA", 1),
        ("CCT", 1),
        ("CTC", 1),
        ("GCG", 1),
        ("ACT", 1),
        ("CAT", 1),
        ("GTT", 1),
        ("CCC", 1),
        ("TGG", 1),
        ("GGA", 1),
        ("TCA", 1),
        ("CGA", 1),
        ("TAC", 1),
        ("GGT", 1),
        ("CAGC", 1),
        ("TAGT", 1),
        ("GTCA", 1),
        ("CGCT", 1),
        ("TCTG", 1),
        ("GACC", 1),
        ("AATC", 1),
        ("TGAT", 1),
        ("CCTG", 1),
    ]
    for kmer, expected_count in kmers_to_test:
        assert (
            store1.count(kmer) == expected_count
        ), f"Failed test case: count('{kmer}')"

    print("All 30 test cases passed.")


sys.argv = ["test_kmers.py", "--build", "malloclabs/dna.txt"]
# The actual program we're running here
if __name__ == "__main__":
    # Get and parse the command line arguments
    parser = argparse.ArgumentParser(
        description="COMP3506/7505 Assignment One: Testing K-mer structure"
    )
    parser.add_argument(
        "--build", type=str, help="Path to a file containing DNA sequences."
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
    if args.build:
        test_kmer_store_build(args.build)

    # You probably want to expand with more testing!
