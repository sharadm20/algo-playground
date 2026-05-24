package excercise;

//find the max of two number without if else or direct comparator.
public class MaximumNumberHard {
    public static void main(String[] args) {
        int x = 10;
        int y = 37;
        int dif = x - y;
        int max = x -  (dif & (dif >> 31)); // bitwise right shift int of negative number will give -1.
        System.out.println(max);
       // System.out.println(10 -(-27 & (-27 >> 31)));
    }   
}
