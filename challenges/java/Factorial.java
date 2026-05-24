public class Factorial {
    public static void main(String[] args) {
        int k =4;
       // int [] memo = new int[k+1];
       // System.out.println(factorial(k,memo));
        System.out.println(factByDP(k));
    }
    //Memoization
    static public int factorial(int k, int[] memo){
        if(k==0) return 1;
        if(memo[k]!= 0) return memo[k];
        memo[k] = k * factorial(k-1, memo);
        return memo[k];
    }
    //Tabulation
    static public int factByDP(int k){
        if(k==0 || k==1) return 1;
        int[] memo = new int[k+1];
        memo[0] =1;
        //memo[1] = 1;
        for(int j =1; j<=k;j++){
            memo[j] = j* memo[j-1];
        }
        return memo[k];
    }
}
