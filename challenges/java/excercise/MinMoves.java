package excercise;
public class MinMoves {
    public static int minMoves(int n, String[] blocks) {
        if (n == 0) {
            return 0;
        }

        int steps = 1; // Start with 1 step since there's at least one block
        for (int i = 1; i < n; i++) {
            if (!blocks[i].equals(blocks[i - 1])) {
                steps++;
            }
        }

        return steps;
    }

    public static void main(String[] args) {
        // Sample Input 1
        int n1 = 4;
        String[] blocks1 = {"white", "red", "white", "red"};
        System.out.println("Minimum steps required: " + minMoves(n1, blocks1));  // Output: 3

        // Sample Input 2
        int n2 = 4;
        String[] blocks2 = {"red", "white", "white", "red"};
        System.out.println("Minimum steps required: " + minMoves(n2, blocks2));  // Output: 2
    }
}
