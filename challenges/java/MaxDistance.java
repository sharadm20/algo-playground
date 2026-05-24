//Array of pillars and two frog can leap only on higher or equal pillar than previous one find the max distance the two frog can make assuming they start  at optimal position
public class MaxDistance {
    public static void main(String[] args) {
        int xor = 0;
       // int [] blocks = { 1, 5, 5, 2, 6, 5, 7 };
        int [] nums = {2,11,2,11,2};
       // System.out.println(findDistance(blocks));
        for (int num : nums) {
            xor ^= num;
            System.out.println(xor);
        }
    }
    static public int findDistance(int [] blocks){
        int max = 0;
        if(blocks == null || blocks.length <= 1) return max;
        int n = blocks.length;
        int [] left = new int[n];
        int [] right = new int[n];
        left[0] = 0;
        for(int i = 1; i< n; i++){
            if(blocks[i] <= blocks[i-1]) left[i] = left[i-1] + 1;
            else left[i] = 0;
        }
        right[n-1] = 0;
        for(int j = n-2; j>=0; j--){
            if(blocks[j] <= blocks[j+1]) right[j] = right[j+1] + 1;
            else right[j] = 0;
        }
        for(int k=0; k<n; k++ ) max = Math.max(max, left[k]+right[k]+1);
        return max;
    }
}
