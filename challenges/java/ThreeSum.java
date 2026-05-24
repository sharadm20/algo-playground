import java.util.*;
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<List<Integer>>();
        Arrays.sort(nums);
        for(int index = 0; index<nums.length -2; index++){
             if (index > 0 && nums[index] == nums[index - 1]) {
                continue;
            }
            int lhs = index + 1;
            int rhs = nums.length-1;
   
            while(lhs < rhs){
                int sum = nums[index] + nums[lhs] + nums[rhs];
                if (sum == 0){
                    result.add(Arrays.asList(nums[index], nums[lhs] , nums[rhs]));
                    while(lhs < rhs && nums[lhs] == nums[lhs + 1]){
                        lhs++;
                    }
                    while(lhs < rhs && nums[rhs] == nums[rhs - 1]){
                        rhs--;
                    }
                    lhs++;
                    rhs--;
                } else if( sum < 0 ){
                    lhs++;
                }
                else rhs--;
            }
        }
        return result;
    }
}