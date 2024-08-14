with open("malloclabs/kmers.txt") as f:
    dnas = f.read().split("\n")

dna_set = set()
for dna in dnas:
    dna_set.add(dna)

print(len(dna_set))
print(len(dnas))
