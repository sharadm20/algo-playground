public class TrappingWater {
    public static void main(String[] args) {

    }
    public int trap(int[] height) {
        int res =0;
        int left = 0, right = height.length -1;
        int lh = 0 , rh =0;

        while(left<right){
            lh = Math.max(lh, height[left]);
            rh = Math.max(rh,height[right]);
            if(lh<rh){
                res += lh - height[left];
                left++;
            }
            else{
                res += rh - height[right];
                right--;
            }
        }
        return res;
    }
}
