package strings;
public class ReverseString {
    public static void main(String[] args) {
        String str = "Hi Sharath welcome to Persistent";

        System.out.println(reverseWord(str));
    }
    public static String reverseWord(String str){
        String words[]=str.split("\\s");
        String reverseWord="";
        for(String w:words){
            StringBuilder sb=new StringBuilder(w);
            sb.reverse();
            reverseWord+=sb.toString()+" ";
        }
        return reverseWord.trim();
    }
}
