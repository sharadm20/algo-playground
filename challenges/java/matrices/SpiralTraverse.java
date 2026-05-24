package matrices;


import java.util.ArrayList;
import java.util.List;

public class SpiralTraverse {
    public enum Direction {
      Up, Down, Left, Right
    }
    List<Integer> spiralTraversal(int [][] matrix){
        List<Integer> result = new ArrayList<>();
        int m = matrix.length;
        int n = matrix[0].length;
        Direction direction = Direction.Up;
        int row=0, col=0, round=0;
        for(int i = 0; i <(m*n); i++){
             result.add(matrix[row][col]);
            switch (direction){
                case Up: if(row == round + 1){ //Note: round + 1 as 0th row was already traversed at begining
                    col++;
                    round++;
                    direction = Direction.Right;
                }else{
                    row--;
                }
                case Right: if(col + 1 == n - round){
                    row++;
                    direction = Direction.Down;
                }
                else {
                    col++;
                }
                case Down: if(row + 1 == m - round){
                    col--;
                    direction = Direction.Left;
                }
                else {
                    row++;
                }
                case Left: if(col == round){
                    row --;
                    direction = Direction.Up;
                }else{
                    col--;
                }
            }
        }
        return result;
    }
}
