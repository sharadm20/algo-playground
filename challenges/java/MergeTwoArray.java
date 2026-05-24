import java.util.Arrays;

public class MergeTwoArray {
    public static void main(String[] args) {
        int [] nums1 = {0};
        int [] nums2= {1};
        int m = 0;
        int n =1;
        System.out.println(Arrays.toString(merge(nums1, m, nums2, n)));
    }
    public static int[] merge(int[] nums1, int m, int[] nums2, int n) {
        int j = m-1;
        int k = n-1;
        int i = m+n-1;
        while(j>=0 && k>=0){
            if(nums2[k]>nums1[j]){
                nums1[i--] = nums2[k--];
            }else {
                nums1[i--] = nums1[j--];
            }
        }
        while(k>=0 && i>=0){
            nums1[i--] = nums2[k--];
        }
        return nums1;
    }
}
