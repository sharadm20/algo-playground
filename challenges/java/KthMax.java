import java.util.Collections;
import java.util.PriorityQueue;

public class KthMax {
    public static void main(String[] args) {
        int[] input = {1,1,35,35,5,34};
        System.out.println(findKthElement(input, 2));
    }
    static int findKthSmallestElement(int[] arrayList, int k){
        PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());
      //  int result = 0;
        for(int i = 0; i<arrayList.length; i++){
            pq.add(arrayList[i]);
            if(pq.size() > k ) pq.poll();
        }
        return pq.peek();
    }
    static int findKthElement(int[] arrayList, int k){
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        //  int result = 0;
        for(int i = 0; i<arrayList.length; i++){
            pq.add(arrayList[i]);
            if(pq.size() > k ) pq.poll();
        }
        return pq.peek();
    }
    int findRandomPivot(int arr[], int start, int end)
    {
        int n = end - start + 1;
        // Selecting the random pivot index
        int pivotInd = (int) ((Math.random()*1000000)%n);
        int temp = arr[end];
        arr[end] = arr[start+pivotInd];
        arr[start+pivotInd] = temp;
        int pivot = arr[end];
        //initialising pivoting point to start index
        pivotInd = start;
        for (int i = start; i < end; i++) {

            // If an element is lesser than pivot, swap it.
            if (arr[i] <= pivot) {
                int temp1 = arr[i];
                arr[i]= arr[pivotInd];
                arr[pivotInd] = temp1;

                // Incrementing pivotIndex for further
                // swapping.
                pivotInd++;
            }
        }

        // Lastly swapping or the
        // correct position of pivot
        int tep = arr[pivotInd];
        arr[pivotInd] =  arr[end];
        arr[end] = tep;
        return pivotInd;
    }

    void SmallestLargest(int a[], int low, int high, int k,
                                int n)
    {
        if (low == high)
            return;
        else {
            int pivotIndex = findRandomPivot(a, low, high);

            if (k == pivotIndex) {
                System.out.print(k+ " smallest elements are : ");
                for (int i = 0; i < pivotIndex; i++)
                    System.out.print(a[i]+ "  ");

                System.out.println();

                System.out.print(k+ " largest elements are : ");
                for (int i = (n - pivotIndex); i < n; i++)
                    System.out.print(a[i]+ "  ");
            }

            else if (k < pivotIndex)
                SmallestLargest(a, low, pivotIndex - 1, k, n);

            else if (k > pivotIndex)
                SmallestLargest(a, pivotIndex + 1, high, k, n);
        }
    }
    static void smallest(int[] a){
        int smallest = Integer.MAX_VALUE;
        for(int i = 0; i<a.length; i++){
            if(a[i]<smallest) smallest = a[i];
        }
        System.out.println(smallest);
    }
    static void secondSmallest(int[] a){
        int second, first;
        if(a.length < 2) {
            System.out.println("Array size is less than 2");
            return;
        }
        first = second  = Integer.MAX_VALUE;
        for(int i = 0; i<a.length; i++){
            if(a[i]<first) {
                second = first;
                first = a[i];
            } else if (a[i]<second && a[i]!= first) {
                second = a[i];
            }
        }
        if (second == Integer.MAX_VALUE)
            System.out.println("There is no second" +
                    "smallest element");
        System.out.println(second);
    }
    static void thirdSmallest(int[] a){
       int second, first, third;
        if(a.length < 2) {
            System.out.println("Array size is less than 2");
            return;
        }
        first = second = third = Integer.MAX_VALUE;
        for(int i = 0; i<a.length; i++){
            if(a[i]<first) {
                third = second;
                second = first;
                first = a[i];
            } else if (a[i]<second) {
                third = second;
                second = a[i];
            } else if (a[i]<third) {
                third = a[i];

            }
        }
        System.out.println(third);
    }
}
