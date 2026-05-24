public class MaxContainer {
    public static void main(String[] args) {
        int [] height = {1,8,6,2,5,4,8,3,7};
        System.out.println(maxArea(height));
    }
    public static int maxArea(int[] height) {
        int area = 0;
        int pt1 = 0, pt2= height.length - 1;
        while(pt1<pt2){
            area = Math.max(area,calcArea(pt1,pt2,height[pt1], height[pt2]));
            if(height[pt1]<height[pt2]) pt1++;
            else pt2--;
        }

        return area;

    }
    public static int calcArea(int i, int j, int ha, int hb){
        int base = j-i;
        int height = Math.min(ha, hb);
        return base*height;
    }
}
