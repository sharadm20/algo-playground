package strings;
public class StringPalindrome {
    public static void main(String[] args) {
        String s = "A man, a plan, a canal: Panama";
        System.out.println(isPalindrome(s));
    }
    static public boolean isPalindrome(String s) {
        s = s.toLowerCase().replaceAll("[^a-z0-9]", "");
        return isPalin(s, 0, s.length() - 1);
    }
    static public boolean isPalin(String s, int start, int end)
    {
        if(start >= end)
        {
            return true;
        }
        if(s.charAt(start) != s.charAt(end))
        {
            return false;
        }
        return isPalin(s, ++start, --end);
    }
}
