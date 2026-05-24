import java.util.Map;
import java.util.TreeMap;

public class Occurence {
    public static void main(String[] args) {
        int[] arr = {1,2,2,2,5,6,3,3,5,7,9,9,9};
        count(arr);
    }
    static void count(int[] arr){
        Map<Integer, Integer> countOccurence = new TreeMap<>();
        for(int i =0; i< arr.length; i++){
            if(countOccurence.containsKey(arr[i])){
                countOccurence.put(arr[i],countOccurence.get(arr[i])+1);
            }
            else{
                countOccurence.put(arr[i], 1);
            }
        }
        System.out.println(countOccurence);
    }
}
