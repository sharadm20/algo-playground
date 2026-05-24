package arrays;
import java.util.List;
import java.util.ArrayList;

public class SummaryRange {
    public static void main(String args[]) {
        int[] nums ={0,1,2,4,5,7};
    
        System.out.println(getRanges(nums));
      }

      public static List<String> getRanges(int[] nums){
          List<String> ranges = new ArrayList<>();
          int n = nums.length;
          int start = 0;
          for(int end = 1; end<=n; end++){
              if(end==n || nums[end]!=nums[end-1]+1){
                  if(start == end-1) ranges.add(String.valueOf(nums[start]));
                  else{ ranges.add(nums[start] + "->" + nums[end-1]);}
                  start = end;
              }
          }
          return ranges;
      }
}
