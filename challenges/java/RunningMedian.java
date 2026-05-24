import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

public class RunningMedian {
    public static List<Double> runningMedian(List<Integer> a) {
        // Write your code here
        List<Double> medians = new ArrayList<>();
        PriorityQueue<Double> g = new PriorityQueue<>();
        PriorityQueue<Double> s = new PriorityQueue<>();
        for (Integer val : a) {
            
            s.add(-1.0 * val);
            g.add(-1.0 * s.poll());
            if (g.size() > s.size())
                s.add(-1.0 * g.poll());

            if (g.size() != s.size()) {
                medians.add(-1.0 * s.peek());
                System.out.println(s.peek());
            }
            else {
                medians.add((g.peek() - s.peek())
                        / 2);
                System.out.println(g.peek() + " " + s.peek());
            }

        }
        return medians;
    }

    public static void main(String[] args) {

        List<Integer> arr = Arrays.asList(1,2,3,4,5,6,7,8,9,10);
        runningMedian(arr);
    }
}
