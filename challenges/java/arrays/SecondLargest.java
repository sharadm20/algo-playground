package arrays;

public class SecondLargest {
    public static void main(String[] args) {
        int [] nums = {1,2,1,34,35,35};
        System.out.println(getSecondLargest(nums));
    }
    public static int getSecondLargest(int [] nums){
        int largest = Integer.MIN_VALUE, secondLargest = Integer.MIN_VALUE;
        for(int i = 0; i < nums.length; i++){
            if(nums[i] > largest){
                secondLargest = largest;
                largest = nums[i];
            } else if (nums[i] > secondLargest && nums[i] < largest) {
                secondLargest = nums[i];
            }
        }
        return secondLargest;
    }
}
