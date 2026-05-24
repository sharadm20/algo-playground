package arrays;
public class MaxDifference {
    public static int maxDifference(int[] arr) {
        if (arr.length < 2) {
            return 0; // Not enough elements to find a difference
        }

        int minElement = arr[0];
        int maxDiff = arr[1] - arr[0];

        for (int i = 1; i < arr.length; i++) {
            if (arr[i] - minElement > maxDiff) {
                maxDiff = arr[i] - minElement;
            }
            if (arr[i] < minElement) {
                minElement = arr[i];
            }
        }

        return maxDiff;
    }

    public static void main(String[] args) {
        int[] arr = {30, 20, 10};
        System.out.println("Maximum difference is " + maxDifference(arr));
    }
}
