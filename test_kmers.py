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

    # 初始化 KmerStore，设置 k 为 20
    k = 45
    store = KmerStore(k)

    # 从文件中读取序列并插入到 KmerStore 中
    store.read(filepath)

    frequency = 8
    result = store.freq_geq(frequency)
    print(result)
    for i in result:
        print(store.count(i), end="\t")
    # print(store.freq_geq(frequency))
    print()
    kmer = "TTTT"
    print(store.count(kmer))
    store.batch_delete([kmer])
    print(store.count(kmer))
    print(f'Size = {store.count_prefix('T')}')

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
