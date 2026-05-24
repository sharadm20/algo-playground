package excercise;
public class CustomFunctionInterface {
        public static void main(String args[]) {
        CustomFunctionalInterface test2 = (int a, int b) -> a*b;
      
      System.out.println("multiply of x*y = " + test2.multiply(3,2));
    }
}
@FunctionalInterface
interface CustomFunctionalInterface {
   int multiply(int a, int b);
}