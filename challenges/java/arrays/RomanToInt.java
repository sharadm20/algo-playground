package arrays;
import java.util.*;
public class RomanToInt {
    public static void main(String[] args) {
        String s1="III",s2="LVIII",s3="MCMXCIV";
        System.out.println(romanToInt(s1));
        System.out.println(romanToInt(s2));
        System.out.println(romanToInt(s3));
    }
    public static int romanToInt(String s){
        HashMap<Character, Integer> convert= new HashMap<>(7);
        convert.put('I', 1);
        convert.put('V', 5);
        convert.put('X', 10);
        convert.put('L', 50);
        convert.put('C', 100);
        convert.put('D', 500);
        convert.put('M', 1000);

        int sum=0,prev = 0, next=0;
        for(int i=s.length() - 1; i>=0; i--){
            next = convert.get(s.charAt(i));
            if(prev>next) sum -= next;
            else sum += next;
            prev = next;
        }
        return sum;
    }
    public String longestCommonPrefix(String[] strs) {
        if(strs.length == 0)
            return "";
        String prefix = strs[0];
        for(int i = 1; i<strs.length ; i++){
            while(strs[i].indexOf(prefix)!=0){
                prefix = prefix.substring(0,prefix.length()-1);
            }
        }
        return prefix;
    }

}
