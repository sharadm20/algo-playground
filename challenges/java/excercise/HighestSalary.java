package excercise;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class HighestSalary {
    public static void main(String[] args) {
           List<Employee> employees = Arrays.asList(
                new Employee("Alice", "HR", 70000),
                new Employee("Bob", "IT", 90000),
                new Employee("Charlie", "HR", 80000),
                new Employee("David", "IT", 100000),
                new Employee("Eve", "Finance", 95000)
        );

        // Group by department and find the highest salary employee in each department
        Map<String, String> highestPaidByDept = employees.stream()
        .collect(Collectors.groupingBy(
                Employee::getDepartment,
                Collectors.collectingAndThen(
                    Collectors.maxBy(Comparator.comparingDouble(Employee::getSalary)),
                    opt -> opt.map(Employee::getName).orElse("No employee")
                )
            ));

        Map<String, Long> groupByDept= employees.stream()
        .collect(Collectors.groupingBy(
            Employee::getDepartment,
            Collectors.counting()) 
        );

        // Print the results
        highestPaidByDept.forEach((department, employee) -> 
            System.out.println("Department: " + department + ", Highest Paid Employee: " + employee)
        );

        groupByDept.forEach((dept, count)->System.out.println("department: " + dept + ", count: "+ count));
    }
    static Map<Character, Integer> countCharacter(String str){
        Map<Character, Integer> res = new HashMap<Character, Integer>();
        String s = str.toLowerCase().trim();
       // loop the string either through stream or for loop
       for(int i = 0; i< s.length(); i++){
           Character c = s.charAt(i);
            res.put(c,res.getOrDefault(c, 0) + 1);
       }
       // filter the stream with only valid chars (not including space and symbols)
       //if char is in map increase the count or add char in map and set count as 1
        return res;
    }
    
    static Map<String, Long> countByStream(String str){
        return Arrays.stream(str.split("")).map(String::toLowerCase).collect(Collectors.groupingBy(s -> s, HashMap::new, Collectors.counting()));
        //return result;
    }
}

class Employee {
    private String name;
    private String department;
    private int salary;

    // Constructor, getters, and toString()
    public Employee(String name, String department, int salary) {
        this.name = name;
        this.department = department;
        this.salary = salary;
    }

    public String getName() {
        return name;
    }

    public String getDepartment() {
        return department;
    }

    public int getSalary() {
        return salary;
    }

    @Override
    public String toString() {
        return "Employee{" +
                "name='" + name + '\'' +
                ", department='" + department + '\'' +
                ", salary=" + salary +
                '}';
    }
}

