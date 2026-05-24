import java.util.Arrays;

public class TwoSum {
    public static void main(String[] args) {
        int [] arr = {1,3,5,7};
        int target = 8;
        System.out.println(Arrays.toString(checkSum(arr, target)));

    }

    private static int[] checkSum(int[] arr, int target) {
        for(int i=1; i<arr.length;i++){
            for(int j=i; j<arr.length;j++){
                int sum = arr[j] + arr[j-i];
                if(sum == target) return new int []{j,j-i};
            }
        }
        return null;
    }
    public int mySqrt(int num) {
        long start = 0;
        long end = num;
        long ans=0;
        if(num == 1 || num == 0)
        {
            return num;
        }
        long mid = 0;
        while(start<=end)
        {
            mid = start + (end-start)/2;
            if(mid*mid <= num)
            {
                start = mid+1;
                ans = mid;

            }
            else
            {
                end = mid-1;
            }
        }
        return (int)ans;
    }
}
