package strings;

// two pointer, dynamic programming
public class Substring {
    public static void main(String[] args) {
      String s1 = "ahb", t1 = "ahbgdc",s = "axc", t = "ahbgdc";
      System.out.println(isSubsequence(s, t) + " ," + isSubsequence(s1, t1));

    }
   
    public static boolean isSubsequence(String s, String t) {
        if (s.length() ==0) return true;
        char[] c = s.toCharArray();
        int sp = 0;
        for( char tc : t.toCharArray()){
            if(c[sp] == tc) sp++;
            if(sp == s.length()) return true;
        }
        return sp==s.length();
    }

}

