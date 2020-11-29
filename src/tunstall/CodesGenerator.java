package tunstall;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.List;

public class CodesGenerator {

    private static List<BitSet> codeBook = new ArrayList<BitSet>();
    private static BitSet bs = new BitSet();

    public static List<BitSet> getCodeList(int k){
        codeBook.clear();
        bs.clear();
        fill(0,k);

        return codeBook;
    }

    private static void fill(int n, int k)
    {
        if (n == k)
        {
            codeBook.add((BitSet) bs.clone());
            return;
        }
        bs.set(n, false);
        fill(n+1, k);
        bs.set(n, true);
        fill(n+1, k);
    }
}
