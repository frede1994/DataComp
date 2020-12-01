import os
import time
import sys
from golombEncoder import Encoder
from golombDecoder import Decoder

if len(sys.argv) < 2:
	print("Please provide a path for a directory with testfiles")
	sys.exit(0)

FILE_PATH =  sys.argv[1]
result_path = ""

def creat_result_directory():
    result_path = FILE_PATH+"/results" #CHANGED THIS FROM os.getcwd TO FILE_PATH
    try:
        os.stat(result_path)
    except:
        os.mkdir(result_path)
    return result_path

def execution_time(start_time):
    return (time.time() - start_time)*1000

def get_file_size(file_name):
    file_size = os.path.getsize(file_name)
    return file_size 


# If you want to code:
encoding = True
# If you want to decode:
decoding = True

''' Type
    0 = Golomb
'''
# Choose the type of encoding
tipo = 0
golomb_divisor = 16 # Must be a power of 2 (2, 4, 8, 16, ...)

GOLOMB=".golomb"
extention_file = '.dat'

conpression_time = 0.0
original_size=0
compressed_size =0
decompress_time =0.0
compressed_file_name =""

result_path = creat_result_directory()

for filename in sorted (os.listdir(FILE_PATH)):
    if filename.endswith(".dat"): 
        original_input_file = os.path.join(FILE_PATH, filename)
        print("\n")
        print("Golomb ON : %s " %filename.split(".")[0])
        if encoding:
            compress = Encoder()
            original_size = get_file_size(original_input_file)
            start_time = time.time()
            compress.code(original_input_file, tipo,result_path, golomb_divisor)
            conpression_time = execution_time(start_time)
            compressed_input_file = result_path+"/"+filename.split(".")[0] +GOLOMB
            compressed_size = get_file_size(compressed_input_file)

        if decoding:    
            start_time =time.time()
            decompress = Decoder() 
            decompress.decode(compressed_input_file, extention_file,result_path )
            decompress_time = execution_time(start_time)
            decompressed_size = get_file_size(compressed_input_file.split(".")[0]+".dat")
        print("Finished compression of : %s in %s ms" %(filename,conpression_time))
        print("Original size : %s bytes " % original_size ) 
        print("Compressed size : %s bytes" % compressed_size )
        print("Compressed ratio : %s " % (original_size/compressed_size) )
        print("Finished decompression of %s in %s ms" % (compressed_file_name,decompress_time) )
        print("Uncompressed size : %s bytes" % decompressed_size)  

