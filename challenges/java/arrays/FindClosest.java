package arrays;

import java.util.Arrays;
//find closest to zero
public class FindClosest {
    public int findClosestNumber(int[] nums) {
        int ans = 0;
        Arrays.sort(nums);
        for(int i=0; i<nums.length; i++){
            if(Math.abs(nums[i]) < Math.abs(nums[ans])) {
                ans = i;
            }
        }
        return nums[ans];
    }
}
