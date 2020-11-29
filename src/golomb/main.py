import os
import time
import sys
from src.codificador import Codificador
from src.decodificador import Decodificador

if len(sys.argv) < 2:
	print("Please provide a path for a directory with testfiles")
	sys.exit(0)

FILE_PATH =  sys.argv[1]

##### Encoder configuration #####
result_path = ""

def creat_result_directory():
    result_path = os.getcwd()+"/results"
    try:
        os.stat(result_path)
    except:
        os.mkdir(result_path)
    return result_path

def execution_time(start_time):
    return (time.time() - start_time)*1000

def print_file_size(file_name):
    file_size = os.path.getsize(file_name)
    return file_size 

def get_decompression_size(data):
    file = os.getcwd()
    file = file+ "/"+ data
    # print("here"+file)
    return print_file_size(file)


# If you want to code:
encoding = True

''' Tipos
    0 = Golomb
'''

# Choose the type of encoding
tipo = 0

golomb_divisor = 16 # Deve ser potencia de 2 (2, 4, 8, 16,...)

#########################################

##### Decoder configuration #####

# If you want to decode:
decoding = True

GOLOMB=".golomb"
extention_file = 'dat'

#########################################
# FILE_PATH = "/Users/smart/Desktop/golomb/encode_decode/data_group5"
# FILE_PATH = "/Users/smart/Desktop/golomb/data_g"

conpression_time = 0.0
original_size=0
compressed_size =0
uncompress_size=0
decompress_time =0.0
compressed_file_name =""


result_path = creat_result_directory()
# print (result_path)


for filename in sorted (os.listdir(FILE_PATH)):
    if filename.endswith(".dat"): 
        original_input_file = os.path.join(FILE_PATH, filename)
        print("\n")
        print("Golomb ON : %s " %filename.split(".")[0])
        if encoding:
            codifica = Codificador()
            original_size = print_file_size(original_input_file)
            start_time = time.time()
            # print(original_input_file)
            codifica.codificar(original_input_file, tipo, golomb_divisor)
            conpression_time = execution_time(start_time)

        if decoding:
            file_name_modified = original_input_file
            file_name_modified = file_name_modified.split("/")[-1]
            file_name_modified = file_name_modified.split(".")[0]
            file_name_modified = file_name_modified+GOLOMB
            compressed_file_name = file_name_modified

            compressed_size = print_file_size(file_name_modified)
            start_time =time.time()
            decodifica = Decodificador()
            decodifica.decodificar(file_name_modified, extention_file )
            decompress_time = execution_time(start_time)
        print("Finished compression of : %s in %s ms" %(filename,conpression_time))
        print("Original size : %s bytes " % original_size ) 
        print("Compressed size : %s bytes" % compressed_size )
        print("Compressed ratio : %s " % (original_size/compressed_size) )
        print("Finished decompression of %s in %s ms" % (compressed_file_name,decompress_time) )
        print("Uncompressed size : %s bytes" % get_decompression_size(filename))  



# for path in sorted (pathlib.Path(FILE_PATH).iterdir()):
#     if path.is_file():
#         data = str(path)
#         data = data.split("/")[-1]
#         print("\n")
#         print("Golomb ON : %s " %data.split(".")[0])
#        # Coding:
#         if encoding:
#             file_name = str(path)
#             print(file_name)
            # codifica = Codificador()
            # original_size = print_file_size(file_name)
            # start_time = time.time()
            # codifica.codificar(file_name, tipo, golomb_divisor)
#             conpression_time = execution_time(start_time)

#         # Decoding:
#         if decoding:
#             file_name_modified = str(path)
#             file_name_modified = file_name_modified.split("/")[-1]
#             file_name_modified = file_name_modified.split(".")[0]
#             file_name_modified = file_name_modified+GOLOMB
#             compressed_file_name = file_name_modified

#             compressed_size = print_file_size(file_name_modified)
#             start_time =time.time()
#             decodifica = Decodificador()
#             decodifica.decodificar(file_name_modified, extention_file )
#             decompress_time = execution_time(start_time)
            
            
#         print("Finished compression of : %s in %s ms" %(data,conpression_time))
#         print("Original size : %s bytes " % original_size ) 
#         print("Compressed size : %s bytes" % compressed_size )
#         print("Compressed ratio : %s " % (original_size/compressed_size) )
#         print("Finished decompression of %s in %s ms" % (compressed_file_name,decompress_time) )
#         print("Uncompressed size : %s bytes" % get_decompression_size(data))

# print("\n")