package matrices;

import java.util.*;

/*
 * Find the min distance of 0 between two cell
 * in a matrices of mxn size, where each adjacent cell has 1 unit distance
 * for example Input: [[0,0,0],[0,1,0],[1,1,1]] Output: [[0,0,0],[0,1,0],[1,2,1]]
 */
public class MinDistance {

    //Method for checing validity
public boolean isValid(int i, int j, int n, int m){
    if(i < 0 || i >= n || j < 0 || j >= m){
        return false;
    }
    return true;
}
static void runner(){
    List<List<Integer>> matrix = new ArrayList<>();
    matrix.add(Arrays.asList(0,0,0));
    matrix.add(Arrays.asList(0,1,0));
    matrix.add(Arrays.asList(1,1,1));
    minDistance(matrix);
}

class Pair{
    int row;
    int col;
    Pair(int row, int col){
        this.row = row;
        this.col = col;
    }
}

private static List<List<Integer>> minDistance(List<List<Integer>> mat) {    
    int m = mat.size();
    int n = mat.get(0).size();
    List<List<Integer>> dist = new ArrayList<>();
    Queue<int[]> queue = new LinkedList<>();

    // Initialize the distance matrix and queue
    for (int i = 0; i < m; i++) {
        List<Integer> row = new ArrayList<>();
        for (int j = 0; j < n; j++) {
            if (mat.get(i).get(j) == 0) {
                row.add(0);
                queue.offer(new int[]{i, j});
            } else {
                row.add(Integer.MAX_VALUE);
            }
        }
        dist.add(row);
    }

    // Directions for moving up, down, left, and right
    int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    // BFS to update distances
    while (!queue.isEmpty()) {
        int[] cell = queue.poll();
        int x = cell[0], y = cell[1];

        for (int[] dir : directions) {
            int newX = x + dir[0];
            int newY = y + dir[1];

            if (newX >= 0 && newX < m && newY >= 0 && newY < n) {
                if (dist.get(newX).get(newY) > dist.get(x).get(y) + 1) {
                    dist.get(newX).set(newY, dist.get(x).get(y) + 1);
                    queue.offer(new int[]{newX, newY});
                }
            }
        }
    }

    return dist;
}

}