import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

/* Finding the next number in sequence of given n digit number
* For example, 34279 is the input number
* output will be 34297 as it is the next big number combination out of the given input number's digits
* */
public class NextNumberInDigit {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            // Create a Scanner object
            System.out.println("Input number must be withing int length");

            int n = sc.nextInt();
            System.out.println(bruteForceMethod(n));
            sc.close();
        }catch(Exception e){

        }
      
    }

    static int bruteForceMethod(int n) {
        int next = 0;
        ArrayList<Integer> arr = new ArrayList<>();
        while (n / 10 != 0) {
            arr.add(n % 10);
            n /= 10;
        }
        arr.add(n);
        Collections.reverse(arr);
        int len = arr.size();
        System.out.println(arr);
        arr = nextNumber(len, arr);
        System.out.println(arr);
        for (Integer integer : arr) {
            next = next * 10 + integer;
        }

        return next;
    }
    static ArrayList<Integer> nextNumber(int n, ArrayList<Integer> arr){
    // If number of digits is 1 then just return the vector
    if(n ==1)
        return arr;

    // Start from the right most digit and find the first
    // digit that is
    // smaller than the digit next to it.
    int i;
    for(i =n -1;i >0;i--) {
        if (arr.get(i) > arr.get(i - 1))
            break;
    }
    System.out.println(i);
    if(i !=0) {

        // Find the smallest digit on right side of (i-1)'th
        // digit that is
        // greater than number[i-1]
        for (int j = n - 1; j >= i; j--) {
            if (arr.get(i - 1) < arr.get(j)) {

                // Swap the found smallest digit i.e. arr[j]
                // with arr[i-1]
                int temp = arr.get(j);
                arr.set(j,arr.get(i - 1));
                arr.set((i - 1),  temp);
                break;
            }
        }
    }

    // Reverse the digits after (i-1) because the digits
    // after (i-1) are in decreasing order and thus we will
    // get the smallest element possible from these digits
    ArrayList<Integer> res = new ArrayList<>();
    int ind = n-1;

    // copying the first i elements of arr
    // into res
    for(int j = 0; j<i; j++)
        res.add(j, arr.get(j));

    // copying the rest of the elements
    // in reverse order
    for(int j = i; j< arr.size() ;j++)
        res.add(j, arr.get(ind--));

    // If i is 0 that means elements are in decreasing order
    // Therefore, no greater element possible then we just
    // return the lowest possible
    // order/element formed from these digits by just
    // reversing the vector
    return res;
    }
}
