package arrays;
import java.util.LinkedList;
import java.util.List;

public class ScoreRanges {
    public static int getTargetScore(int N) {
        
        List<Integer> targets = new LinkedList<>();
        for (int i =0; i < N; i++) {
            targets.add(i+1);
        }
        int score = targets.get(0);

        while (targets.size() > 1) {
            for (int i = 0; i < targets.size(); i += 2) {
                score += targets.remove(i);         
            }
        }

        return score;
    }

    public static void main(String[] args) {
        System.out.println(getTargetScore(5));  // Output: 11
        System.out.println(getTargetScore(6));  // Output: 17
    }
    
}



