public class BinarySearch {
    public static void main(String[] args) {
        int [] arr = {1,2,3,4,5,6};
        System.out.println(binarySearchR(arr,0,arr.length -1, 4));
    }
    public static int binarySearch(int []arr, int low, int high, int target){

        while(high-low>1) {
            int mid = (low + high)/2;
            if (arr[mid] == target) return mid;
            if(arr[mid]<target) low = mid + 1;
            else  high = mid;
            if(arr[low] == target) return low;
            else if(arr[high] == target) return high;
            else return -1;
        }
        return -1;
    }
    public static int binarySearchR(int []arr, int low, int high, int target){

        while(high>=low) {
            int mid = (low + high)/2;
            if (arr[mid] == target) return mid;
            if(arr[mid]>target) return binarySearchR(arr,low, mid, target);
            return binarySearchR(arr,mid+1,high,target);

        }
        return -1;
    }
}
