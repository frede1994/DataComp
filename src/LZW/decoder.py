# LZW Decoder
# Name: Aditya Gupta
# ID: 800966229
# ITCS 6114
import time
import sys
from sys import argv
import struct
from struct import *

decompress_time =0.0

def execution_time(start_time):
    return (time.time() - start_time)*1000

# taking the compressed file input and the number of bits from command line
# defining the maximum table size
# opening the compressed file
# defining variable
bit_size = 12 
def decompress(input_file):         
    maximum_table_size = pow(2,int(bit_size))
    file = open(input_file, "rb")
    compressed_data = []
    next_code = 256
    decompressed_data = ""
    string = ""
    # Reading the compressed file.
    while True:
        rec = file.read(2)
        if len(rec) != 2:
            break
        (data, ) = unpack('>H', rec)
        compressed_data.append(data)
    # Building and initializing the dictionary.
    dictionary_size = 256
    dictionary = dict([(x, chr(x)) for x in range(dictionary_size)])
    start_time = time.time()
    # iterating through the codes.
    # LZW Decompression algorithm
    for code in compressed_data:
        if not (code in dictionary):
            dictionary[code] = string + (string[0])
        decompressed_data += dictionary[code]
        if not(len(string) == 0):
            dictionary[next_code] = string + (dictionary[code][0])
            next_code += 1
        string = dictionary[code]

    # storing the decompressed string into a file.
    out = input_file.split(".")[0]
    output_file = open(out + ".dat", "w")
    for data in decompressed_data:
        output_file.write(data)
        
    output_file.close()
    file.close()
    global decompress_time
    decompress_time = execution_time(start_time)