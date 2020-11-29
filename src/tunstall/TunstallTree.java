package tunstall;

import java.util.*;

public class TunstallTree {

    private List<TreeNode> tree;
    private int N,Q,K,k;
    private double[] probability;
    private List<BitSet> codeBook;

    public TunstallTree(int N, int K, int k, double[] probability){
        this.N=N;
        this.K=K;
        this.k=k;
        this.Q=0;
        this.probability = probability;
        this.codeBook = CodesGenerator.getCodeList(k);
        tree = generateTunstallTree();

    }

    public BitSet getCode(List<Byte> temp) throws Exception {
        TreeNode code = findSpecificNode(tree, temp, 0);

        return code==null?null:code.getCode();
    }

    private List<TreeNode> generateTunstallTree() {
        List<TreeNode> tree = new ArrayList<TreeNode>();

        //Initialize the tree
        for(int i=0;i<N;i++){
            tree.add(new TreeNode(probability[i], (byte)i, codeBook.get(i), true, null, null));
        }
        Q+=N;

        //Main tree loop
        while(K-Q>N-1){
            TreeNode maxProbNode = getFirstLeaf(tree.get(0));
            maxProbNode = searchForBiggestProb(tree, maxProbNode);
            BitSet freeCode = maxProbNode.getCode();
            double maxProb = maxProbNode.getProbability();
            maxProbNode.setCode(null);
            maxProbNode.setLeaf(false);
            maxProbNode.setSubTree(new ArrayList<TreeNode>());

            //Initialize subtree
            maxProbNode.getSubTree().add(new TreeNode(maxProb*probability[0], (byte)0, freeCode, true, null, maxProbNode));
            for(int i=1;i<N;i++) {
                maxProbNode.getSubTree().add(new TreeNode(maxProb * probability[i], (byte) i, codeBook.get(Q), true, null, maxProbNode));
                Q++;
            }
        }
        return tree;
    }

    private TreeNode getFirstLeaf(TreeNode treeNode) {
        if(treeNode.isLeaf) return treeNode;
        return getFirstLeaf(treeNode.getSubTree().get(0));
    }

    private TreeNode searchForBiggestProb(List<TreeNode> tree, TreeNode maxProbNode) {
        for (TreeNode node:tree) {
            if (!node.isLeaf) {
                maxProbNode = searchForBiggestProb(node.getSubTree(), maxProbNode);
            }else {
                if (node.getProbability() > maxProbNode.getProbability()) {
                    maxProbNode = node;
                }
            }
        }
        return maxProbNode;
    }

    private TreeNode findSpecificNode(List<TreeNode> tree, List<Byte> temp, int index) throws Exception {
        for(TreeNode node: tree){
            if(node.getSymbol()==temp.get(index)){
                if(index==temp.size()-1) return node;
                return findSpecificNode(node.getSubTree(), temp, index+1);
            }
        }
        throw new Exception();
    }

    public List<Byte> getSymbolsFromCode(BitSet bitSet) {
        TreeNode node = findNodeWithCode(tree, bitSet);
        if(node==null){
            return null;
        }
        List<Byte> listOfSymbols = new ArrayList<Byte>();
        do{
            listOfSymbols.add(node.getSymbol());
            node = node.getParent();
        }while(node!=null);

        Collections.reverse(listOfSymbols);
        return listOfSymbols;
    }

    private TreeNode findNodeWithCode(List<TreeNode> tree, BitSet code) {
        for (TreeNode node:tree) {
            if (!node.isLeaf) {
                TreeNode temp = findNodeWithCode(node.getSubTree(), code);
                if(temp!=null){
                    return temp;
                }
            }else {
                if (node.getCode().equals(code)) {
                    return node;
                }
            }
        }
        return null;
    }


}
