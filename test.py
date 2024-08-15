from structures.dynamic_array import DynamicArray

array = DynamicArray()
with open("malloclabs/dna.txt") as file:
    for line in file:
        array.append(line)
print(array)
