import LZ77.LZ77;
import arithmeticCoding.*;
import org.apache.commons.io.FileUtils;
import huffman.AdaptiveHuffmanCompress;
import huffman.HuffmanCompress;
import huffman.HuffmanDecompress;
import tunstall.Tunstall;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.apache.commons.lang3.ArrayUtils;

public class Main {
    //Colors for easier terminal readings
    private static final String ANSI_RESET = "\u001B[0m";   //Reset color
    private static final String ANSI_RED = "\u001B[31m";    //Red for compression
    private static final String ANSI_GREEN = "\u001B[32m";  //Green for decompression
    private static String results;

    public static void main(String[] args) {
        File datasetsFolder = null;
        if (args.length > 0) {
            datasetsFolder = new File(args[0]);
            results = args[0] + "/results";
        } else {
            System.out.println("Please provide a path for a directory with testfiles");
            System.exit(0);
        }
        String compressedPath;
        String decompressedPath;
        for (final File fileEntry : datasetsFolder.listFiles()) {
            if (!fileEntry.getName().equals("results")) {
                String datasetName = fileEntry.getName(); // Current dataset
                datasetName = datasetName.substring(0, datasetName.length() - 4); // Strip .dat
                printDatasetData(fileEntry.getAbsolutePath(), fileEntry.getName());

                //Static Huffman
                compressedPath = createFile(datasetName + "_compressed_statichuffman");
                decompressedPath = createFile(datasetName + "_decompressed_statichuffman");
                staticHuffman(fileEntry.getAbsolutePath(), compressedPath, decompressedPath, datasetName);

                //Adaptive Huffman
                compressedPath = createFile(datasetName + "_compressed_adaptivehuffman");
                decompressedPath = createFile(datasetName + "_decompressed_adaptivehuffman");
                adaptiveHuffman(fileEntry.getAbsolutePath(), compressedPath, decompressedPath, datasetName);

                //Arithmetic Coding
                compressedPath = createFile(datasetName + "_compressed_arithmeticcoding");
                decompressedPath = createFile(datasetName + "_decompressed_arithmeticcoding");
                arithmeticCoding(fileEntry.getAbsolutePath(), compressedPath, decompressedPath, datasetName);

                //Tunstall
                compressedPath = createFile(datasetName + "_compressed_tunstall");
                decompressedPath = createFile(datasetName + "_decompressed_tunstall");
                tunstall(fileEntry.getAbsolutePath(), compressedPath, decompressedPath, datasetName);

                //LZ77
                compressedPath = createFile(datasetName + "_compressed_lz77");
                decompressedPath = createFile(datasetName + "_decompressed_lz77");
                lz77(fileEntry.getAbsolutePath(), compressedPath, decompressedPath, datasetName);
            }
        }
    }

    //All arithmeticCoding-code from https://github.com/nayuki/Reference-arithmetic-coding/
    private static void arithmeticCoding(String original, String compressed, String decompressed, String datasetName) {
        System.out.println("ARITHMETIC CODING ON: " + datasetName);
        File inputFile = new File(original);
        File outputFile = new File(compressed);

        // Read input file once to compute symbol frequencies
        FrequencyTable freqs = null;
        try {
            freqs = ArithmeticCompress.getFrequencies(inputFile);
        } catch (IOException e) {
            e.printStackTrace();
        }
        freqs.increment(256);  // EOF symbol gets a frequency of 1

        //Encode
        try (InputStream in = new BufferedInputStream(new FileInputStream(inputFile));
             BitOutputStream out = new BitOutputStream(new BufferedOutputStream(new FileOutputStream(outputFile)))) {
            ArithmeticCompress.writeFrequencies(out, freqs);
            long tEnc = System.nanoTime();
            ArithmeticCompress.compress(freqs, in, out);
            long atEnc = System.nanoTime();
            System.out.println(ANSI_RED + "Finished compression of: " + inputFile.getName() + " in " + (float) (atEnc - tEnc) / 1000000 + " ms");
            System.out.println("Original size: " + inputFile.length() + " bytes");
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("Compressed size: " + outputFile.length() + " bytes");
        System.out.println("Compression ratio: " + ((float) inputFile.length() / (float) outputFile.length()));

        inputFile = new File(compressed);
        outputFile = new File(decompressed);

        //Decode
        try (BitInputStream in = new BitInputStream(new BufferedInputStream(new FileInputStream(inputFile)));
             OutputStream out = new BufferedOutputStream(new FileOutputStream(outputFile))) {
            FrequencyTable freqsDecompress = ArithmeticDecompress.readFrequencies(in);
            long tEnc = System.nanoTime();
            ArithmeticDecompress.decompress(freqsDecompress, in, out);
            long atEnc = System.nanoTime();
            System.out.println(ANSI_GREEN + "Finished decompression of: " + inputFile.getName() + " in " + (float) (atEnc - tEnc) / 1000000 + " ms");
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("Uncompressed size: " + outputFile.length() + " bytes");
        System.out.println(ANSI_RESET);
    }

    //All staticHuffman-code from https://github.com/nayuki/Reference-Huffman-coding
    private static void staticHuffman(String original, String compressed, String decompressed, String datasetName) {
        System.out.println("STATIC HUFFMAN ON: " + datasetName);
        //Encode
        try {
            File inputFile = new File(original);
            long t = System.nanoTime();
            HuffmanCompress.huffmanCompress(original, compressed);
            long at = System.nanoTime();
            File outputFile = new File(compressed);
            System.out.println(ANSI_RED + "Finished compression of: " + inputFile.getName() + " in " + (float) (at - t) / 1000000 + " ms");
            System.out.println("Original size: " + inputFile.length() + " bytes");
            System.out.println("Compressed size: " + outputFile.length() + " bytes");
            System.out.println("Compression ratio: " + ((float) inputFile.length() / (float) outputFile.length()));
        } catch (IOException e) {
            e.printStackTrace();
        }

        //Decode
        try {
            File inputFile = new File(compressed);
            long t = System.nanoTime();
            HuffmanDecompress.huffmanDecompress(compressed, decompressed);
            long at = System.nanoTime();
            File outputFile = new File(decompressed);
            System.out.println(ANSI_GREEN + "Finished compression of: " + inputFile.getName() + " in " + (float) (at - t) / 1000000 + " ms");
            System.out.println("Uncompressed size: " + outputFile.length() + " bytes");
            System.out.println(ANSI_RESET);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //All adaptiveHuffman-code from https://github.com/nayuki/Reference-Huffman-coding
    private static void adaptiveHuffman(String original, String compressed, String decompressed, String datasetName) {
        System.out.println("ADAPTIVE HUFFMAN ON: " + datasetName);
        //Encode
        try {
            File inputFile = new File(original);
            long t = System.nanoTime();
            AdaptiveHuffmanCompress.AdaptiveHuffmanCompress(original, compressed);
            long at = System.nanoTime();
            File outputFile = new File(compressed);
            System.out.println(ANSI_RED + "Finished compression of: " + inputFile.getName() + " in " + (float) (at - t) / 1000000 + " ms");
            System.out.println("Original size: " + inputFile.length() + " bytes");
            System.out.println("Compressed size: " + outputFile.length() + " bytes");
            System.out.println("Compression ratio: " + ((float) inputFile.length() / (float) outputFile.length()));
        } catch (IOException e) {
            e.printStackTrace();
        }

        //Decode
        try {
            File inputFile = new File(compressed);
            long t = System.nanoTime();
            AdaptiveHuffmanCompress.AdaptiveHuffmanCompress(compressed, decompressed);
            long at = System.nanoTime();
            File outputFile = new File(decompressed);
            System.out.println(ANSI_GREEN + "Finished compression of: " + inputFile.getName() + " in " + (float) (at - t) / 1000000 + " ms");
            System.out.println("Uncompressed size: " + outputFile.length() + " bytes");
            System.out.println(ANSI_RESET);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //All Tunstall-code from https://github.com/MBajdowski/TunstallCoding
    private static void tunstall(String original, String compressed, String decompressed, String datasetName) {
        System.out.println("Tunstall ON: " + datasetName);
        File inputFile = new File(original);
        File outputFile = new File(compressed);
        try {
            //Encode
            long t = System.nanoTime();
            Tunstall coder = new Tunstall(FileUtils.readFileToByteArray(inputFile), 16);
            FileUtils.writeByteArrayToFile(outputFile, coder.generateCodedFile());
            long at = System.nanoTime();
            System.out.println(ANSI_RED + "Finished compression of: " + inputFile.getName() + " in " + (float) (at - t) / 1000000 + " ms");
            System.out.println("Original size: " + inputFile.length() + " bytes");
            System.out.println("Compressed size: " + outputFile.length() + " bytes");
            System.out.println("Compression ratio: " + ((float) inputFile.length() / (float) outputFile.length()));

            inputFile = new File(compressed);
            outputFile = new File(decompressed);

            //Decode
            t = System.nanoTime();
            Tunstall decoder = new Tunstall(FileUtils.readFileToByteArray(inputFile));
            FileUtils.writeByteArrayToFile(outputFile, decoder.decodeFile());
            at = System.nanoTime();
            outputFile = new File(decompressed);
            System.out.println(ANSI_GREEN + "Finished decompression of: " + inputFile.getName() + " in " + (float) (at - t) / 1000000 + " ms");
            System.out.println("Uncompressed size: " + outputFile.length() + " bytes");
            System.out.println(ANSI_RESET);
        } catch (IOException e) {
            System.out.println("Exception while reading/saving the file");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    //All LZ77-code from https://opencores.org/websvn/filedetails?repname=lzrw1-compressor-core&path=%2Flzrw1-compressor-core%2Ftrunk%2FLZ77.java
    private static void lz77(String original, String compressed, String decompressed, String datasetName) {
        System.out.println("LZ77 ON: " + datasetName);
        //Encode
        LZ77 compressor = new LZ77();
        try {
            File inputFile = new File(original);
            File outputFile = new File(compressed);
            long t = System.nanoTime();
            compressor.encode(inputFile, outputFile);
            long at = System.nanoTime();
            System.out.println(ANSI_RED + "Finished compression of: " + inputFile.getName() + " in " + (float) (at - t) / 1000000 + " ms");
            System.out.println("Original size: " + inputFile.length() + " bytes");
            System.out.println("Compressed size: " + outputFile.length() + " bytes");
            System.out.println("Compression ratio: " + ((float) inputFile.length() / (float) outputFile.length()) + ANSI_RESET);
        } catch (IOException e) {
            e.printStackTrace();
        }

        //Decode
        try {
            File inputFile = new File(compressed);
            File outputFile = new File(decompressed);
            long t = System.nanoTime();
            compressor.decode(inputFile, outputFile, null);
            long at = System.nanoTime();
            System.out.println(ANSI_GREEN + "Finished decompression of: " + inputFile.getName() + " in " + (float) (at - t) / 1000000 + " ms");
            System.out.println("Uncompressed size: " + outputFile.length() + " bytes");
            System.out.println(ANSI_RESET);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    //Helper method
    private static String createFile(String fileName) {
        Path filePath = Paths.get(results + "/" + fileName + ".txt");
        try {
            Files.deleteIfExists(filePath);
            Files.createFile(filePath);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return filePath.toString();
    }

    public static void printDatasetData(String path, String name) {
        System.out.println("File: " + name);
        countUniqueCharacters(path, name);
        printFileSize(path, name);
        System.out.println(ANSI_RESET);
    }

    public static void countUniqueCharacters(String s, String dataset) {
        String datasetString = "";
        try {
            datasetString = new String(Files.readAllBytes(Paths.get(s)));
        } catch (IOException e) {
            e.printStackTrace();
        }

        char characters[] = datasetString.toCharArray();
        int countOfUniqueChars = datasetString.length();
        for (int i = 0; i < characters.length; i++) {
            if (i != datasetString.indexOf(characters[i])) {
                countOfUniqueChars--;
            }
        }
        System.out.println("Alphabet size: " + countOfUniqueChars);
    }

    public static void printFileSize(String path, String fileName) {
        File file = new File(path);
        System.out.println("Size: " + file.length() + " bytes");
    }
}