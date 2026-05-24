import java.util.*;

public class BinaryTree {
    TreeNode root;
    int max=0;
    BinaryTree(int item){
        root = new TreeNode(item);
    }
    BinaryTree(){
        root = null;
    }
    public TreeNode makeTree(){
       // BinaryTree tree = new BinaryTree();
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        root.left.left = new TreeNode(4);
        root.left.right = new TreeNode(5);
        root.right.left = new TreeNode( 6);
        return root;
    }
    public int height(TreeNode root){
        if (root == null) return 0;
        return (1 + Math.max(height(root.left), height(root.right)));
    }
//    public int diameterOfBinaryTree(TreeNode root){
//        if(root == null) {
//            return 0;
//        }
//        int leftSubtreeDiameter = diameterOfBinaryTree(root.left);
//        int rightSubtreeDiameter = diameterOfBinaryTree(root.right);
//        int diameter = height(root.left) + height(root.right);
//        diameter = Math.max(diameter, Math.max(leftSubtreeDiameter, rightSubtreeDiameter));
//        return diameter;
//    }

    public int diameterOfBinaryTree(TreeNode root) {
        diameter(root);
        return max;

    }
    public int diameter(TreeNode start) {
        if(start==null){
            return 0;
        }
        int left=diameter(start.left);
        int right=diameter(start.right);
        max=Math.max(max,left+right);
        return Math.max(left,right)+1;
    }
    public int numUniqueBST(int n) {
        int [] G = new int[n+1];
        G[0] = G[1] = 1;

        for(int i=2; i<=n; ++i) {
            for(int j=1; j<=i; ++j) {
                G[i] += G[j-1] * G[i-j];
            }
        }
        return G[n];
    }
    //Implementation of Binary Tree Inorder Traverse without recursion
    List<Integer> inOrderTraversal(TreeNode root){
        List<Integer> result = new ArrayList<>();
        Stack<TreeNode> stack = new Stack<>();
        TreeNode cur = root;
        while(cur != null || !stack.isEmpty()){
            while(cur != null){
                stack.add(cur);
                cur = cur.left;
            }
            cur = stack.pop();
            result.add(cur.val);
            cur = cur.right;
        }
        return result;
    }
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if(root == null) return result;
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        while (!stack.isEmpty())
        {

            TreeNode curr = stack.pop();

            result.add(curr.val);

            if (curr.right != null) {
                stack.push(curr.right);
            }

            if (curr.left != null) {
                stack.push(curr.left);
            }
        }
        return result;
    }
    public List<Integer> postOrderTraversal( TreeNode root){
        Deque<Integer> out = new ArrayDeque<>();
        if(root == null) return out.stream().toList();
        Deque<TreeNode> stack = new ArrayDeque<>();
       // Deque<Integer> out = new ArrayDeque<>();
        stack.push(root);
        while (!stack.isEmpty())
        {

            TreeNode curr = stack.pop();

            out.addFirst(curr.val);

            if (curr.left != null) {
                stack.push(curr.left);
            }

            if (curr.right != null) {
                stack.push(curr.right);
            }

        }


        return  out.stream().toList();
    }
    public boolean isSymmetric(TreeNode root) {
        if(root == null) return true;
        return checkSymmetry(root.left,root.right);
    }
    public static boolean checkSymmetry(TreeNode lr, TreeNode rr){
        if(lr==null && rr == null) return true;
        if(lr==null && rr!=null) return false;
        if(lr!=null && rr==null) return false;
        if(lr.val != rr.val) return false;
        boolean leftside = checkSymmetry(lr.left,rr.right);
        boolean rightside = checkSymmetry(lr.right,rr.left);
        return (leftside && rightside);
    }

    public TreeNode sortedArrayToBST(int[] nums) {
        return sortArrayToBST(nums,0,nums.length - 1);
    }
    public static TreeNode sortArrayToBST(int [] nums, int start, int end){
        if(start>end) return null;
        int mid = (start + end)/2 ;
        TreeNode node = new TreeNode(nums[mid]);
        node.left = sortArrayToBST(nums, start, mid - 1 );
        node.right = sortArrayToBST(nums, mid + 1, end);
        return node;
    }

}
