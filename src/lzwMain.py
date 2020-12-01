import os   
import glob
import lzwEncoder as encoder
import lzwDecoder as decoder
import sys
original_size=0
compressed_size =0
decompressed_size =0

if len(sys.argv) < 2:
	print("Please provide a path for a directory with testfiles")
	sys.exit(0)
file_path = sys.argv[1]

result_path = ""

def creat_result_directory():
    result_path = file_path+"/results"
    try:
        os.stat(result_path)
    except:
        os.mkdir(result_path)
    return result_path

def get_file_size(file_name):
    file_size = os.path.getsize(file_name)
    return file_size 

result_path = creat_result_directory()
print(result_path)

for filename in sorted (os.listdir(file_path)):
    if filename.endswith(".dat"): 
        original_input_file = os.path.join(file_path, filename)
        
        print("\n")
        print("LZW ON : %s " % filename.split(".")[0])
        original_size = get_file_size(original_input_file)
        #compress
        encoder.compress(original_input_file,result_path,filename)
        compressed_input_file = result_path+"/"+filename.split(".")[0] + ".lzw"
        compressed_size = get_file_size(compressed_input_file)
        #decompress
        decoder.decompress(compressed_input_file)
        decompressed_size = get_file_size(compressed_input_file.split(".")[0]+".dat")

        print("Finished compression of : %s in %s ms" %(filename,encoder.conpression_time))
        print("Original size : %s bytes " % original_size ) 
        print("Compressed size : %s bytes" % compressed_size )
        print("Compressed ratio : %f " % (float(original_size)/compressed_size ))
        print("Finished decompression of %s in %s ms" % (filename.split(".")[0]+ ".lzw",decoder.decompress_time))
        print("Uncompressed size : %s bytes" % decompressed_size)
       










