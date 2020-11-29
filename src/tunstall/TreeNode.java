package tunstall;

import java.util.BitSet;
import java.util.List;

public class TreeNode {
    public double getProbability() {
        return probability;
    }

    public void setProbability(double probability) {
        this.probability = probability;
    }

    public byte getSymbol() {
        return symbol;
    }

    public void setSymbol(byte symbol) {
        this.symbol = symbol;
    }

    public BitSet getCode() {
        return code;
    }

    public void setCode(BitSet code) {
        this.code = code;
    }

    public boolean isLeaf() {
        return isLeaf;
    }

    public void setLeaf(boolean leaf) {
        isLeaf = leaf;
    }

    public List<TreeNode> getSubTree() {
        return subTree;
    }

    public void setSubTree(List<TreeNode> subTree) {
        this.subTree = subTree;
    }

    public TreeNode getParent() {
        return parent;
    }

    public void setParent(TreeNode parent) {
        this.parent = parent;
    }

    private double probability;
    private byte symbol;
    private BitSet code;
    boolean isLeaf;
    List<TreeNode> subTree;
    private TreeNode parent;

    public TreeNode(double probability, byte symbol, BitSet code, boolean isLeaf, List<TreeNode> subTree, TreeNode parent) {
        this.probability = probability;
        this.symbol = symbol;
        this.code = code;
        this.isLeaf = isLeaf;
        this.subTree = subTree;
        this.parent = parent;
    }


}
