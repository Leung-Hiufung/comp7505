"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Compression Utilities for Task 4.
"""

from pathlib import Path
from typing import Any
import sys
import hashlib
from structures.map import Map
from structures.pqueue import PriorityQueue

codemap = Map()
codemap_reversed = Map()

class TreeNode:
    def __init__(self, byte: bytes, freq: int) -> None:
        self.char = byte
        self.frequency = freq
        self.left = None
        self.right = None

    def __lt__(self, other) -> bool:
        return self.freq < other.freq
    

def build_huffman_tree(freq_table: Map) -> TreeNode:
    heap = PriorityQueue()
    for freq in freq_table.get_items():
        byte = freq.get_key()
        value = freq.get_value()
        heap.insert(value, TreeNode(byte, value))
    
    while heap.get_size() > 1:
        node1 = heap.remove_min()
        node2 = heap.remove_min()

        merged = TreeNode(None, node1.frequency + node2.frequency)
        merged.left = node1
        merged.right = node2
        heap.insert(merged.frequency, merged)
    
    root = heap.remove_min()
    return root

def build_huffman_map(root: TreeNode) -> Map:
    global codemap
    global codemap_reversed

    def build_code_recursion(node: TreeNode, current_code: str) -> str:
        if node is None:
            return
        if node.char is not None:
            codemap[node.char] = current_code
            codemap_reversed[current_code] = node.char
        
        build_code_recursion(node.left, current_code + '0')
        build_code_recursion(node.right, current_code + '1')
    
    build_code_recursion(root, '')

    return codemap

def huffman_encoding(data: bytes) -> bytes:
    global codemap

    if data == '':
        return b''
    
    bitstring = ''
    for byte in data:
        bitstring += codemap[byte]
    
    padded_bitstring = bitstring + '0' * (8 - len(bitstring) % 8)

    compressed_bytes = bytearray()
    for i in range(0, len(padded_bitstring), 8):
        byte = padded_bitstring[i:i+8]
        compressed_bytes.append(int(byte, 2))
    return bytes(compressed_bytes)

def run_length_encoding(data: bytes) -> bytes:
    if not data:
        return b""
    
    compressed = bytearray()
    previous_byte = data[0]
    count = 1

    for i in range(1, len(data)):
        current_byte = data[i]
        if current_byte == previous_byte:
            count += 1
        else:
            compressed.append(previous_byte)
            compressed.append(count)
            previous_byte = current_byte
            count = 1
    
    compressed.append(previous_byte)
    compressed.append(count)
    return bytes(compressed)
    
def run_length_decoding(data: bytes) -> bytes:
    if not data:
        return b""
    
    decompressed = bytearray()
    for i in range(0, len(data), 2):
        byte = data[i]
        count = data[i + 1]
        for _ in range(count):
            decompressed.append(byte)
    return bytes(decompressed)

def huffman_decoding(compressed: bytes) -> bytes:
    global codemap_reversed
    bitstring = ""
    for byte in compressed:
        bitstring += f"{byte:08b}"
    
    decoded_bytes = bytearray()
    t = ''
    for bit in bitstring:
        t += bit
        if codemap_reversed[t] is not None:
            decoded_bytes.append(codemap_reversed[t])
            t = ''
    return bytes(decoded_bytes)

def file_to_bytes(path: str) -> bytes:
    """
    Read a file into a byte array
    """
    with open(path, 'rb') as f:
        data = f.read()
    return data

def bytes_to_file(path: str, data: bytes) -> None:
    """
    Write a sequence of bytes to a file
    """
    with open(path, 'wb') as f:
        f.write(data)

def my_compressor(in_bytes: bytes) -> bytes:
    """
    Your compressor takes a bytes object and returns a compressed
    version of the bytes object. We have put xz here just as a 
    baseline general purpose compression tool.
    """
    # Implement me!
    # Get frequency table
    freq_table = Map()
    
    for byte in in_bytes:
        freq_table[byte] = 1 if freq_table[byte] is None else freq_table[byte] + 1
    
    root = build_huffman_tree(freq_table)
    codemap = build_huffman_map(root)
    huffman_encoded_data = huffman_encoding(in_bytes)
    # rle_compressed_data = run_length_encoding(huffman_encoded_data)
    return huffman_encoded_data
    

def my_decompressor(compressed_bytes: bytes) -> bytes:
    """
    Your decompressor is given a compressed bytes object (from your own
    compressor) and must recover and return the original bytes.
    Once again, we've just used xz.
    """ 
    # Implement me!
    global codemap_reversed
    # huffman_encoded_data = run_length_decoding(compressed_bytes)
    original_data = huffman_decoding(compressed_bytes)
    return original_data

def compress_file(in_path: str, out_path: str) -> None:
    """
    Consume a file from in_path, compress it, and write it to out_path.
    """
    in_size = Path(in_path).stat().st_size
    in_data = file_to_bytes(in_path)
   
    compressed = my_compressor(in_data)
    
    bytes_to_file(out_path, compressed)
    out_size = Path(out_path).stat().st_size

    print("Compression Benchmark...")
    print("Input File:", in_path)
    print("Input Size:", in_size)
    print("Output File:", out_path)
    print("Output Size:", out_size)
    print("Ratio:", out_size/in_size)

def decompress_file(compressed_path: str, out_path: str) -> None:
    """
    Consume a compressed file from compressedpath, decompress it, and
    write it to outpath.
    """
    compressed_data = file_to_bytes(compressed_path)
    
    decompressed = my_decompressor(compressed_data)

    bytes_to_file(out_path, decompressed)

def recovery_check(in_path: str, compressed_path: str) -> bool:

    original = file_to_bytes(in_path)
    expected_checksum = hashlib.md5(original).hexdigest()

    decompress_file(compressed_path, "tmp")
    recovered = file_to_bytes("tmp")
    recovered_checksum = hashlib.md5(recovered).hexdigest()

    assert expected_checksum == recovered_checksum, "Uh oh!"




sys.argv = ['test.py', 'original_text.txt', 'compressed.txt']
if __name__ == "__main__":
    compress_file(sys.argv[1], sys.argv[2])
    recovery_check(sys.argv[1], sys.argv[2])
