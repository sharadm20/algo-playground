package sorts;

public class Quicksort implements Sort {
    Quicksort(){

    }
     void sort(int[] arr, int low, int high){
        if(low < high){
            int pivot = partition(arr, low, high);
            sort(arr, low, pivot - 1);
            sort(arr, pivot +1, high);
        }
    }
     int partition(int[] arr, int low, int high){
        int pivot = arr[high];
        int i = low - 1;
        for(int j  = low; j< high; j++){
            if(arr[j]<=pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return i + 1;
    }

    @Override
    public void sort(int[] array) {
        sort(array, 0, array.length - 1);
    }

}
