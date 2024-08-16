def compatible(kmer: str) -> int:
    """
    Given a k-mer, return the total number of compatible
    k-mers. You will be using the two suffix characters
    of the input k-mer to compare against the first two
    characters of all other k-mers.
    Time complexity for full marks: O(1) :-)
    """
    sequences = [
        "AA",
        "AC",
        "AG",
        "AT",
        "CA",
        "CC",
        "CG",
        "CT",
        "GA",
        "GC",
        "GT",
        "GT",
        "TA",
        "TC",
        "TG",
        "TT",
    ]
    suffix = kmer[-2:]

    low, high = 0, 16
    while low < high:
        middle = (low + high) // 2
        if sequences[middle] == suffix:
            break
        elif sequences[middle] > suffix:
            high = middle
        else:
            low = middle
    prefix = sequences[15 - middle]

    # suffix = [kmer[-2], kmer[-1]]
    # prefix = [None] * 2
    # for i in range(2):
    #     if suffix[i] == "A":
    #         prefix[i] = "T"
    #     elif suffix[i] == "C":
    #         prefix[i] = "G"
    #     elif suffix[i] == "G":
    #         prefix[i] = "C"
    #     else:
    #         prefix[i] = "A"
    return prefix


print(compatible("AGCTTTG"))
