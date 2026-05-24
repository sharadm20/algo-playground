public class ExcelSheetColumnNumber {
    public static void main(String[] args) {
        String s = "ZY";
        System.out.println(titleToNumber(s));
    }
    public static int titleToNumber(String str) {
        int len = str.length() - 1;
        //int sum = 0;
        int val = 0;
        int j = 0;
        int i = len;
        if(len == 0) return (int)str.charAt(0) - 64 ;
        while(i>=0  && j<=len){
           val += (int) (Math.pow(26,j) * ((int)str.charAt(i) - 64));
            //System.out.println("value:"+val);
           i--;
           j++;
        }
        return val;
    }
}
