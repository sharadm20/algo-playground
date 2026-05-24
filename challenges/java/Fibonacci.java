import java.util.Arrays;

public class Fibonacci {
    static  int []memo = new int [1000];
    public static void main(String[] args) {
        System.out.println("Fibonacci by recursion:" + fib(6));
        System.out.println("Fibonacci by Dynamic proggramming:" + fibByDynamic(6));
        System.out.println("Fib by memo" +fibByMemoization(6));
    }
    static int fib(int n){
        if(n<=1) return n;
        return fib(n-1) + fib(n-2);
    }
    static int fibByDynamic(int n){
        int[] f= new int[n+1];
        f[0] =0;
        f[1] =1;
        for(int i = 2; i<=n; i++){
            f[i] = f[i-1] + f[i-2];
        }
        System.out.println(Arrays.toString(f));
        return f[n];
    }
    static int fibByMemoization(int n){
        if(n<=1) return n;
        if (memo[n]!=0) return memo[n];
        memo[n] = fibByMemoization(n-1) + fibByMemoization(n-2);
        return memo[n];
    }
}
