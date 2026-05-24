import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

public class LambdaExample {
    /***
     * Square of numbers present in a list
     */
    public void runExample() {
        List<Integer> numbers = Arrays.asList(1, 2, 3,4,5);
        Function<Integer, Integer> squareRT = x -> x * x;
       // Double squareRT = (num) -> (Math.sqrt(num));
        List<Integer> doubles = numbers.stream().map(squareRT).collect(Collectors.toList());
        System.out.println(doubles);
    }
}
