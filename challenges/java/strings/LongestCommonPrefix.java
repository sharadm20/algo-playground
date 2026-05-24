package strings;

public class LongestCommonPrefix {
    public static void main(String[] args) {
        String[] strs = {"dog", "racecar", "car"};
        String[] strs1 = {"flower","flow","flight"};
        System.out.println(findLongestCommonPrefix(strs)+ " : " + findLongestCommonPrefix(strs1));
    }
    static String findLongestCommonPrefix(String[] strs){
    String prefix=strs[0];
    for(int index=1;index<strs.length;index++){
        while(strs[index].indexOf(prefix)!=0){ //this  will check if prefix starting index is 0, will be true only if prefix is present
            prefix=prefix.substring(0,prefix.length()-1);// prefix will keep getting shorten by 1 till it matches 
        }
    } 
    return prefix;
    } 
}
