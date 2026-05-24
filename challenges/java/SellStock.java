public class SellStock {
    public static void main(String[] args) {
        int [] prices1 = {7,1,5,3,6,4};
        int [] prices2 = {7,6,3,4,1};
        System.out.println(maxProfit(prices1));
        System.out.println(maxProfit(prices2));
    }
    public static int maxProfit(int[] prices) {
        int profit = 0;
        int lowest = prices[0];
        for(int i =0; i < prices.length; i++){
            lowest = Math.min(lowest, prices[i]);
            profit = Math.max(profit, (prices[i]-lowest));

        }
        return profit;
    }
}
