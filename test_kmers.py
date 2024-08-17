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
    k = 4
    store = KmerStore(k)

    # 从文件中读取序列并插入到 KmerStore 中
    store.read(filepath)

    for frequency in range(20):
        assert str(sorted(store.freq_geq(frequency))) == str(
            sorted(store.feq_geq_t(frequency))
        )

        # print(sorted(store.feq_geq_t(frequency)))

    assert len(store.kmers) == store.count_prefix("")

    # print(str(store))
    kmers = [
        "CTCT",
        "TCTT",
        "CTTC",
        "TTCA",
        "TCAA",
        "CAAA",
        "AAAC",
        "AACT",
        "ACTT",
        "CTTG",
        "TTGA",
        "TGAT",
        "GATT",
        "ATTA",
        "TTAG",
        "TAGC",
        "AGCT",
        "GCTC",
        "CTCA",
        "TCAC",
        "CACT",
        "ACTC",
        "CTCT",
        "TCTA",
        "CTAC",
        "TACG",
        "ACGT",
        "CGTA",
        "GTAC",
        "TACC",
        "ACCC",
        "CCCT",
        "CCTG",
        "CTGA",
        "TGAG",
        "GAGG",
        "AGGA",
        "GGAT",
        "GATT",
        "ATTG",
        "TTGG",
        "TGGG",
        "GGGG",
        "GGGA",
        "GGAA",
        "GAAT",
        "AATT",
        "ACCC",
        "CCCC",
        "CCCC",
        "CCCG",
        "CCGA",
        "CGAC",
        "GACT",
        "ACTT",
        "CTTC",
        "TTCT",
        "TCTG",
        "CTGG",
        "TGGA",
        "GGAG",
        "GAGT",
        "AGTG",
        "GTGT",
        "TGTC",
        "GTCC",
        "TCCT",
        "CCTC",
        "CTCG",
        "TCGA",
        "CGAT",
        "GATT",
        "ATTG",
        "TTGA",
        "TGAG",
        "GAGT",
        "AGTG",
        "GTGG",
        "TGGA",
        "GGAG",
        "GAGA",
        "AGAT",
        "GATA",
        "ATAC",
        "TACG",
        "ACGG",
        "CGGC",
        "GGCG",
        "GCGA",
        "CGAG",
        "GAGC",
        "AGCA",
        "GCAG",
        "CAGT",
        "GGTC",
        "GTCT",
        "TCTT",
        "CTTA",
        "TTAG",
        "TAGT",
        "AGTT",
        "GTTC",
        "TTCC",
        "TCCC",
        "CCCC",
        "CCCT",
        "CCTC",
        "CTCT",
        "TCTA",
        "CTAC",
        "TACA",
        "ACAG",
        "CAGG",
        "AGGA",
        "GGAG",
        "GAGG",
        "AGGT",
        "GGTG",
        "GTGA",
        "TGAA",
        "GAAA",
        "AAAT",
        "AATC",
        "ATCG",
        "TCGA",
        "CGAA",
        "GAAT",
        "AATG",
        "ATGA",
        "TGAC",
        "GACA",
        "ACAT",
        "CATT",
        "ATTA",
        "TTAC",
        "TACT",
        "ACTT",
        "CTTG",
        "TTGA",
        "TGAT",
        "GATA",
        "TATT",
        "ATTT",
        "TTTA",
        "TTAT",
        "TATC",
        "ATCT",
        "TCTT",
        "CTTA",
        "TTAG",
        "TAGG",
        "AGGC",
        "GGCG",
        "GCGT",
        "CGTG",
        "GTGT",
        "TGTG",
        "GTGT",
        "TGTT",
        "GTTG",
        "TTGA",
        "TGAG",
        "GAGG",
        "AGGA",
        "GGAA",
        "GAAT",
        "AATG",
        "ATGA",
        "TGAG",
        "GAGA",
        "AGAA",
        "GAAT",
        "AATC",
        "ATCT",
        "TCTT",
        "CTTT",
        "TTTT",
        "TTTT",
        "TTTC",
        "TTCA",
        "TCAC",
        "CACT",
        "ACTC",
        "CTCC",
        "TCCG",
        "CCGG",
        "CGGA",
        "GGAC",
        "TGAG",
        "GAGG",
        "AGGC",
        "GGCC",
        "GCCG",
        "CCGT",
        "CGTG",
        "GTGA",
        "TGAT",
        "GATC",
        "ATCT",
        "TCTA",
        "CTAT",
        "TATG",
        "ATGA",
        "TGAG",
        "GAGA",
        "AGAG",
        "GAGC",
        "AGCA",
        "GCAT",
        "CATA",
        "ATAA",
        "TAAT",
        "AATC",
        "ATCC",
        "TCCT",
        "CCTT",
        "CTTG",
        "TTGT",
        "TGTA",
        "GTAT",
        "TATC",
        "ATCC",
        "TCCC",
        "CCCC",
        "CCCA",
        "CCAC",
        "CACC",
        "ACCT",
        "CCTG",
        "CTGA",
        "TGAA",
        "GAAT",
        "AATT",
        "ATTG",
        "TTGA",
        "GATC",
        "ATCT",
        "TCTG",
        "CTGC",
        "TGCA",
        "GCAT",
        "CATC",
        "ATCT",
        "TCTG",
        "CTGC",
        "TGCT",
        "GCTA",
        "CTAT",
        "TATG",
        "ATGG",
        "TGGA",
        "GGAA",
        "GAAT",
        "AATA",
        "ATAA",
        "TAAC",
        "AACG",
        "ACGG",
        "CGGT",
        "GGTC",
        "GTCA",
        "TCAC",
        "CACT",
        "ACTA",
        "CTAC",
        "TACG",
        "ACGC",
        "CGCG",
        "GCGA",
        "CGAA",
        "GAAT",
        "AATT",
        "ATTA",
        "TTAC",
        "TACG",
        "ACGT",
        "CGTT",
        "GTTA",
        "TTAG",
        "TAGT",
        "AGTC",
        "GTCT",
        "AGGC",
        "GGCG",
        "GCGA",
        "CGAC",
        "GACG",
        "ACGG",
        "CGGT",
        "GGTG",
        "GTGG",
        "TGGG",
        "GGGA",
        "GGAG",
        "GAGT",
        "AGTT",
        "GTTG",
        "TTGA",
        "TGAA",
        "GAAC",
        "AACT",
        "ACTG",
        "CTGC",
        "TGCC",
        "GCCA",
        "CCAC",
        "CACT",
        "ACTA",
        "CTAT",
        "TATC",
        "ATCC",
        "TCCC",
        "CCCC",
        "CCCT",
        "CCTT",
        "CTTG",
        "TTGT",
        "TGTT",
        "GTTG",
        "TTGT",
        "TGTA",
        "GTAA",
        "TAAG",
        "AAGC",
        "AGCA",
        "GCAA",
        "CAAA",
        "AAAT",
        "AATC",
        "TGTT",
        "GTTT",
        "TTTT",
        "TTTC",
        "TTCG",
        "TCGG",
        "CGGG",
        "GGGG",
        "GGGA",
        "GGAC",
        "GACG",
        "ACGC",
        "CGCC",
        "GCCT",
        "CCTC",
        "CTCA",
        "TCAC",
        "CACC",
        "ACCA",
        "CCAT",
        "CATT",
        "ATTC",
        "TTCC",
        "TCCA",
        "CCAG",
        "CAGC",
        "AGCA",
        "GCAC",
        "CACA",
        "ACAA",
        "CAAT",
        "AATG",
        "ATGA",
        "TGAG",
        "GAGA",
        "AGAT",
        "GATA",
        "ATAT",
        "TATG",
        "ATGC",
        "TGCG",
        "GCGC",
        "CGCT",
        "GCTC",
        "CTCT",
        "TCTA",
        "CTAG",
        "GACA",
        "ACAG",
        "CAGC",
        "AGCC",
        "GCCT",
        "CCTG",
        "CTGT",
        "TGTC",
        "GTCT",
        "TCTT",
        "CTTC",
        "TTCT",
        "TCTA",
        "CTAC",
        "TACC",
        "ACCA",
        "CCAA",
        "CAAT",
        "AATT",
        "ATTG",
        "TTGC",
        "TGCC",
        "GCCG",
        "CCGG",
        "CGGA",
        "GGAC",
        "GACC",
        "ACCC",
        "CCCC",
        "CCCG",
        "CCGA",
        "CGAC",
        "GACT",
        "ACTT",
        "CTTG",
        "TTGA",
        "TGAT",
        "GATT",
        "ATTG",
        "TTGA",
        "TGAG",
        "GAGG",
        "AGGA",
        "GGAG",
        "GAGC",
        "AGCA",
        "GCAT",
        "ATCG",
        "TCGG",
        "CGGT",
        "GGTG",
        "GTGA",
        "TGAC",
        "GACC",
        "ACCG",
        "CCGA",
        "CGAA",
        "GAAA",
        "AAAA",
        "AAAC",
        "AACT",
        "ACTC",
        "CTCT",
        "TCTA",
        "CTAA",
        "TAAC",
        "AACC",
        "ACCC",
        "CCCT",
        "CCTA",
        "CTAA",
        "TAAG",
        "AAGG",
        "AGGA",
        "GGAG",
        "GAGA",
        "AGAT",
        "GATG",
        "ATGA",
        "TGAA",
        "GAAA",
        "AAAA",
        "AAAG",
        "AAGG",
        "AGGG",
        "GGGC",
        "GGCG",
        "GCGA",
        "CGAG",
        "GAGG",
        "AGGT",
        "GGTC",
        "GTCG",
        "TCGC",
    ]

    for kmer in kmers:
        assert store.compatible(kmer) == store.compatible_t(kmer)

    for i in range(100):
        assert str(sorted(store.freq_geq(i))) == str(sorted(store.feq_geq_t(i)))
    store.batch_delete(kmers)
    store.batch_delete_t(kmers)
    print("TGAG" in store.kmers)
    print(len(store.kmers), store.count_prefix(""))
    assert len(store.kmers) == store.count_prefix("")

    # print(str(store))

    kmer = "TTAA"
    # for i in sorted(store.kmers):
    #     print(i)
    print(kmer, store.count_geq(kmer), store.count_geq_t(kmer))
    # permutation = []
    # for a in "ACGT":
    #     for b in "ACGT":
    #         for c in "ACGT":
    #             for d in "ACGT":
    #                 permutation.append(a + b + c + d)

    # for p in permutation:
    #     assert store.count(p) == store.count_t(p)
    #     print(p, store.count_geq(p), store.count_geq_t(p))
    #     assert store.count_geq(p) == store.count_geq_t(p)
    #     assert store.compatible(p) == store.compatible_t(p)


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
