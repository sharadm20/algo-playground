import java.util.TreeMap;

public class SortArrayAccordingly {
    public static void main(String[] args) {

    }
    public static int[] sortFirstArrayBySecondArrayOrder(int[] arr1, int m, int[] arr2, int n){
        int[] ans = new int[m];
        TreeMap<Integer, Integer> frequency = new TreeMap<>();
        for(int i: arr1){
            frequency.put(i, frequency.getOrDefault(i,0)+1);
        }
        return ans;
    }
}
