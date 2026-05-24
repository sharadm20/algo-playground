package strings;
import java.util.Arrays;

class UniqueSub {
    public static void main(String args[]) {
        String s = "heHAgreat";
        System.out.println("Longest unique substring : " + findUniqueSubstring(s));
    }

    public static int findUniqueSubstring(String s) {
        int [] charVisited = new int[256];
        Arrays.fill(charVisited, -1);
        int window = 0;
        int result = 0;
        for(int first =0; first < s.length(); first++ ){
            window = Math.max(window, charVisited[s.charAt(first)] + 1);
            result = Math.max(result, first - window +1);
            charVisited[s.charAt(first)] = first;
        }
        return result;
    }

}