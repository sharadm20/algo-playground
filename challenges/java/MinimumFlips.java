/***
 * Approach: The given problem can be solved by using a Greedy Algorithm based on the observations that the resultant monotonically increasing string after any number of flips will be of the form (‘x’*p + ‘y’*q), where p and q are the count of 0s and 1s respectively in the modified string. The idea is to traverse the given string S and for each index, i modify the substring S[0, i) to 0s and substring S[i, N) to 1s and find the minimum flips required accordingly. Follow the steps below to solve the problem:
 *
 * Find the count of Xs in the given string S and store it in a variable countX.
 * Initialize variable, say minFlips(res) as (N – countX) that stores the minimum number of flips required.
 * Initialize variable, say countY as 0 that stores the count of Ys in the string while traversing the string.
 * Traverse the given string S and perform the following steps:
 * If the character S[i] is X, then decrement the value of countX by 1.
 * Otherwise, update the value of minFlips as the minimum of minFlips and (countX + countY) and increment the value of countY by 1.
 * After completing the above steps, print the value of minFlips(res) as the result.
 */
public class MinimumFlips {
    public static void main(String[] args) {
        String s = "xyxxxyxyy";
        System.out.println(numberOfFlips(s));
    }
    public static int numberOfFlips(String s){

        int countX = count(s,'x');
        int countY= 0;
        int res = s.length() - countX;
        for(int i=0; i<s.length();i++){
            if(s.charAt(i) =='x') {
                countX -= 1;
            }
            else if(s.charAt(i) =='y') {
                res = Math.min(res, countX+countY);
                System.out.println(res);
                countY++;
            }
        }
        return res;
    }
    private static int count(String s, char c) {
        int ans = 0;
        for (char i : s.toCharArray())
            if (c == i)
                ans++;
        return ans;
    }

}
