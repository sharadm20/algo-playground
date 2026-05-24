import java.util.*;

public class PlusOne {
    public static void main(String[] args) {
        int [] arr  = {7,9,7};
        //int [] arr = {1,2,3};
        //System.out.println("Here's Long.MAX_VALUE: " + Long.MAX_VALUE);
        System.out.println(Arrays.toString(plusOne(arr)));
    }
    public static int[] plusOne(int[] digits) {
        int i = digits.length - 1 ;
        while(i >=0 && digits[i] == 9){
            i--;
        }
        //for every 9, 99, 999 cases i will be -1
        if(i == -1){
            int [] result = new int[digits.length + 1];
            result[0] = 1;
            return result;
        }
        int[] result = new int[digits.length];

        result[i] = digits[i] + 1;
        for (int j = 0; j < i; j ++) {
            result[j] = digits[j];
        }

        return result;
    }
}

