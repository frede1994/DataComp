package tunstall;

import org.apache.commons.lang3.ArrayUtils;

import java.nio.ByteBuffer;
import java.nio.IntBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.BitSet;
import java.util.List;

public class Tunstall {

    private int N = 256;
    private int[] nrOfBits;
    private byte[] byteArray;
    private double[] probability;
    private int K, k;
    private TunstallTree tunstallTree;


    public Tunstall(byte[] byteArray, int k) throws Exception {
        this.byteArray = byteArray;
        this.nrOfBits = countBytes(byteArray);
        this.probability = calculateProbability(nrOfBits, byteArray.length);
        this.k = k;
        this.K = (int) Math.pow(2, k);
        if (K <= N) {
            throw new Exception();
        }
        this.tunstallTree = new TunstallTree(N, K, k, probability);
    }

    public int getN() {
        return N;
    }

    public List<Byte> getInputBytes() {
        return Arrays.asList(ArrayUtils.toObject(byteArray));
    }

    public double getProbability(final Byte ofByte) {
        return probability[ofByte & 0xFF];
    }

    public Tunstall(byte[] byteArray) {
        int[] header = getHeader(byteArray);
        this.byteArray = Arrays.copyOfRange(byteArray, header.length*4, byteArray.length);
        this.k = header[1];
        this.K=(int)Math.pow(2,k);
        this.nrOfBits = Arrays.copyOfRange(header,2,N+2);
        this.probability = calculateProbability(this.nrOfBits, header[0]);
        this.tunstallTree = new TunstallTree(N, K, k, probability);
    }

    private int[] getHeader(byte[] byteArray) {
        byte[] byteHeader = Arrays.copyOfRange(byteArray,0,(N+2)*4);
        ByteBuffer buffer = ByteBuffer.wrap(byteHeader);
        int[] header = new int[byteHeader.length / 4];
        for(int i=0;i<header.length;i++){
            header[i] = buffer.getInt(4*i);
        }
        return header;
    }

    private int[] countBytes(byte[] byteArray){
        int[] nrOfBytes = new int[N];
        for (int i = 0; i < N; i++) {
            nrOfBytes[i] = 0;
        }
        for (byte number : byteArray) {
            nrOfBytes[number & 0xFF]++;
        }
        return nrOfBytes;
    }

    private double[] calculateProbability(int[] nrOfBytes, int size){
        double[] probability = new double[N];
        for(int i =0;i<N;i++) {
            probability[i]=(double)nrOfBytes[i]/size;
        }
        return probability;
    }

    public byte[] generateCodedFile() throws Exception {
        BitSet bits = generateHeader();
        int nrOfBitsInHeader = (N+2)*4*8;
        int nrOfWords = 0;
        List<Byte> temp = new ArrayList<Byte>();
        for (int i = 0; i < byteArray.length; i++) {
            temp.add(byteArray[i]);
            BitSet code = tunstallTree.getCode(temp);
            if (code == null) {
                if (byteArray.length - 1 == i) {
                    for (int j = 0; j < k; j++) {
                        bits.set(nrOfBitsInHeader + nrOfWords * k + j);
                    }
                    nrOfWords++;
                    BitSet lastSymbols = BitSet.valueOf(ArrayUtils.toPrimitive(temp.toArray(new Byte[temp.size()])));
                    for(int j=0;j<temp.size()*8;j++){
                        if(lastSymbols.get(j)){
                            bits.set(nrOfBitsInHeader+nrOfWords*k+j);
                        }
                    }
                }
                continue;
            }
            for (int j = 0; j < k; j++) {
                if (code.get(j)) {
                    bits.set(nrOfBitsInHeader + nrOfWords * k + j);
                }
            }
            nrOfWords++;
            temp.clear();
        }
        return bits.toByteArray();
    }

    private BitSet generateHeader() {
        int[] intHeader = new int[N+2];
        intHeader[0] = byteArray.length;
        intHeader[1] = k;
        for(int i=0;i<nrOfBits.length;i++){
            intHeader[i+2] = nrOfBits[i];
        }
        ByteBuffer byteBuffer = ByteBuffer.allocate(intHeader.length * 4);
        IntBuffer intBuffer = byteBuffer.asIntBuffer();
        intBuffer.put(intHeader);

        byte[] byteArray = byteBuffer.array();
        return BitSet.valueOf(byteArray);
    }

    public byte[] decodeFile(){
        List<Byte> bytesInList = new ArrayList<Byte>();

        BitSet bitsInFile = BitSet.valueOf(this.byteArray);
        int nrOfCycles = (int) Math.ceil((double)this.byteArray.length*8/this.k);
        for(int i=0;i<nrOfCycles;i++){
            List<Byte> temp = tunstallTree.getSymbolsFromCode(bitsInFile.get(i*k, (i+1)*k));
            if(temp==null){
                temp = Arrays.asList(ArrayUtils.toObject(bitsInFile.get(i*k, this.byteArray.length*8).toByteArray()));
                bytesInList.addAll(temp);
                break;
            }
            bytesInList.addAll(temp);
        }

        return ArrayUtils.toPrimitive(bytesInList.toArray(new Byte[bytesInList.size()]));
    }
}
