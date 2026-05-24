const queries = [
  {
    id: 'filter-basic',
    category: 'Filtering & Conditionals',
    difficulty: 'beginner',
    title: 'Find Customers with High Purchase Amounts',
    description: 'Filter customers who made purchases above a threshold',
    domain: 'ecommerce',
    sqlQuery: `-- Find customers with total purchases > $1000
SELECT customer_id, customer_name, total_purchases
FROM customers
WHERE total_purchases > 1000
ORDER BY total_purchases DESC;`,
    javaStreamCode: `// Java Stream API equivalent
List<Customer> highValueCustomers = customers.stream()
    .filter(c -> c.getTotalPurchases() > 1000)
    .sorted(Comparator.comparingDouble(Customer::getTotalPurchases).reversed())
    .collect(Collectors.toList());`,
    explanation: 'Both approaches filter records/objects based on a condition and sort the results in descending order.',
    output: 'customer_id | customer_name    | total_purchases\n1           | Alice Johnson    | 2500.00\n3           | Bob Smith        | 1800.00\n5           | Carol Williams   | 1200.00',
  },
  {
    id: 'filter-multiple',
    category: 'Filtering & Conditionals',
    difficulty: 'intermediate',
    title: 'Multi-Condition Filter with OR/AND Logic',
    description: 'Find employees matching complex criteria',
    domain: 'hr',
    sqlQuery: `-- Find employees in Engineering or Sales with salary > 50000 AND 3+ years
SELECT employee_id, name, department, salary, years_of_service
FROM employees
WHERE (department = 'Engineering' OR department = 'Sales')
  AND salary > 50000
  AND years_of_service >= 3
ORDER BY salary DESC;`,
    javaStreamCode: `// Java Stream API equivalent
List<Employee> result = employees.stream()
    .filter(e -> (e.getDepartment().equals("Engineering")
               || e.getDepartment().equals("Sales"))
               && e.getSalary() > 50000
               && e.getYearsOfService() >= 3)
    .sorted(Comparator.comparingDouble(Employee::getSalary).reversed())
    .collect(Collectors.toList());`,
    explanation: 'Both SQL WHERE clauses and Java Stream filters can combine multiple conditions using AND/OR logic.',
    output: 'employee_id | name         | department   | salary   | years_of_service\n3           | Bob Smith    | Engineering  | 95000.00 | 5\n5           | Diana Prince | Sales        | 72000.00 | 4',
  },
  {
    id: 'nth-highest',
    category: 'Nth Most/Least Queries',
    difficulty: 'intermediate',
    title: 'Find the 3rd Highest Salary',
    description: 'Retrieve the employee with the 3rd highest salary',
    domain: 'hr',
    sqlQuery: `-- Find the employee with the 3rd highest salary
SELECT employee_id, name, salary
FROM employees e1
WHERE 3 = (SELECT COUNT(DISTINCT salary)
           FROM employees e2
           WHERE e2.salary >= e1.salary)
ORDER BY salary DESC;`,
    javaStreamCode: `// Java Stream API equivalent
Optional<Employee> thirdHighest = employees.stream()
    .sorted(Comparator.comparingDouble(Employee::getSalary).reversed())
    .skip(2)
    .findFirst();`,
    explanation: 'The SQL subquery counts distinct salaries greater than or equal to the current row. The Java approach sorts descending, skips the first 2, and takes the next.',
    output: 'employee_id | name        | salary\n3           | Bob Smith   | 95000.00',
  },
  {
    id: 'nth-lowest',
    category: 'Nth Most/Least Queries',
    difficulty: 'intermediate',
    title: 'Find the 2nd Lowest Price Product',
    description: 'Retrieve the product with the 2nd lowest price',
    domain: 'ecommerce',
    sqlQuery: `-- Find the product with the 2nd lowest price
SELECT product_id, product_name, price
FROM products p1
WHERE 2 = (SELECT COUNT(DISTINCT price)
           FROM products p2
           WHERE p2.price <= p1.price)
ORDER BY price ASC;`,
    javaStreamCode: `// Java Stream API equivalent
Optional<Product> secondLowest = products.stream()
    .sorted(Comparator.comparingDouble(Product::getPrice))
    .skip(1)
    .findFirst();`,
    explanation: 'Same pattern as nth-highest but sorted ascending and skipping 1 instead of 2.',
    output: 'product_id | product_name | price\n2          | Wireless Mouse | 29.99',
  },
  {
    id: 'group-count',
    category: 'Grouping & Aggregation',
    difficulty: 'beginner',
    title: 'Count Orders per Customer',
    description: 'Count how many orders each customer has placed',
    domain: 'ecommerce',
    sqlQuery: `-- Count orders per customer
SELECT c.customer_id, c.customer_name, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY order_count DESC;`,
    javaStreamCode: `// Java Stream API equivalent
Map<String, Long> orderCounts = orders.stream()
    .collect(Collectors.groupingBy(
        o -> o.getCustomer().getCustomerName(),
        Collectors.counting()
    ));`,
    explanation: 'SQL GROUP BY with COUNT maps to Java Collectors.groupingBy with Collectors.counting().',
    output: 'customer_id | customer_name    | order_count\n1           | Alice Johnson    | 3\n5           | Carol Williams   | 2\n3           | Bob Smith        | 1',
  },
  {
    id: 'group-date',
    category: 'Grouping & Aggregation',
    difficulty: 'intermediate',
    title: 'Monthly Revenue Analysis',
    description: 'Calculate total revenue per month',
    domain: 'ecommerce',
    sqlQuery: `-- Monthly revenue from orders
SELECT DATE_TRUNC('month', order_date) AS month, SUM(total_amount) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;`,
    javaStreamCode: `// Java Stream API equivalent
Map<YearMonth, Double> monthlyRevenue = orders.stream()
    .collect(Collectors.groupingBy(
        o -> YearMonth.from(o.getOrderDate().toInstant()
            .atZone(ZoneId.systemDefault()).toLocalDate()),
        Collectors.summingDouble(Order::getTotalAmount)
    ));`,
    explanation: 'SQL DATE_TRUNC with GROUP BY maps to groupingBy with a date extraction function.',
    output: 'month       | revenue\n2024-01-01  | 5400.00\n2024-02-01  | 3200.00',
  },
  {
    id: 'window-rank',
    category: 'Window Functions',
    difficulty: 'advanced',
    title: 'Rank Students by Grade per Subject',
    description: 'Rank students within each subject by their grade',
    domain: 'student',
    sqlQuery: `-- Rank students by grade within each subject
SELECT student_id, student_name, subject, grade,
       RANK() OVER (PARTITION BY subject ORDER BY grade DESC) AS rank
FROM student_grades
ORDER BY subject, rank;`,
    javaStreamCode: `// Java Stream API equivalent
Map<String, List<StudentGrade>> ranked = studentGrades.stream()
    .sorted(Comparator.comparingDouble(StudentGrade::getGrade).reversed())
    .collect(Collectors.groupingBy(
        StudentGrade::getSubject,
        LinkedHashMap::new,
        Collectors.toList()
    ));`,
    explanation: 'SQL window functions partition data into groups before applying ranking. Java groups by subject and sorts within each group.',
    output: 'student_id | student_name | subject     | grade | rank\n1          | Alice        | Math        | 95    | 1\n3          | Bob          | Math        | 82    | 2\n2          | Alice        | Science     | 88    | 1',
  },
  {
    id: 'window-moving-avg',
    category: 'Window Functions',
    difficulty: 'advanced',
    title: 'Calculate 3-Day Moving Average',
    description: 'Compute rolling 3-day average of daily sales',
    domain: 'ecommerce',
    sqlQuery: `-- 3-day moving average of daily sales
SELECT sale_date, daily_sales,
       AVG(daily_sales) OVER (ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3d
FROM daily_sales
ORDER BY sale_date;`,
    javaStreamCode: `// Java Stream API equivalent not directly expressible
// Use a simple loop or IntStream to compute sliding window averages
List<Double> movingAvgs = IntStream.range(0, sales.size())
    .mapToObj(i -> {
        int start = Math.max(0, i - 2);
        return sales.subList(start, i + 1).stream()
            .mapToDouble(DailySales::getDailySales)
            .average().orElse(0);
    })
    .collect(Collectors.toList());`,
    explanation: 'Window functions with frame specifications (ROWS BETWEEN) are powerful in SQL. Java Stream API has no built-in sliding window, so we use indexed access.',
    output: 'sale_date  | daily_sales | moving_avg_3d\n2024-01-01 | 100.00      | 100.00\n2024-01-02 | 150.00      | 125.00\n2024-01-03 | 200.00      | 150.00',
  },
  {
    id: 'join-inner',
    category: 'Joins & Relationships',
    difficulty: 'intermediate',
    title: 'Find Users with Their Posts',
    description: 'Join users and posts to show user activity',
    domain: 'social-media',
    sqlQuery: `-- List users with their post titles
SELECT u.username, p.title AS post_title, p.created_at
FROM users u
INNER JOIN posts p ON u.user_id = p.user_id
ORDER BY u.username, p.created_at DESC;`,
    javaStreamCode: `// Java Stream API equivalent
List<UserPost> userPosts = users.stream()
    .flatMap(u -> u.getPosts().stream()
        .map(p -> new UserPost(u.getUsername(), p.getTitle(), p.getCreatedAt())))
    .sorted(Comparator.comparing(UserPost::getUsername)
        .thenComparing(Comparator.comparing(UserPost::getCreatedAt).reversed()))
    .collect(Collectors.toList());`,
    explanation: 'SQL JOINs connect related tables on foreign keys. Java flatMap streams through each user and their posts to create a combined view.',
    output: 'username | post_title              | created_at\nalice    | Getting Started with SQL | 2024-01-15\nbob      | Advanced Streams        | 2024-02-20',
  },
  {
    id: 'join-self',
    category: 'Joins & Relationships',
    difficulty: 'advanced',
    title: 'Find Employees Earning More Than Their Manager',
    description: 'Self-join to compare employee salaries with their managers',
    domain: 'hr',
    sqlQuery: `-- Employees earning more than their manager
SELECT e1.name AS employee, e1.salary AS emp_salary,
       e2.name AS manager, e2.salary AS mgr_salary
FROM employees e1
INNER JOIN employees e2 ON e1.manager_id = e2.employee_id
WHERE e1.salary > e2.salary
ORDER BY e1.salary DESC;`,
    javaStreamCode: `// Java Stream API equivalent
List<SalaryComparison> result = employees.stream()
    .filter(e -> e.getManager() != null)
    .filter(e -> e.getSalary() > e.getManager().getSalary())
    .map(e -> new SalaryComparison(e.getName(), e.getSalary(),
        e.getManager().getName(), e.getManager().getSalary()))
    .sorted(Comparator.comparingDouble(SalaryComparison::getEmpSalary).reversed())
    .collect(Collectors.toList());`,
    explanation: 'Self-joins compare rows within the same table. Java filters on the manager relationship defined in the Employee model.',
    output: 'employee | emp_salary | manager | mgr_salary\nBob      | 95000.00   | Alice   | 85000.00',
  },
  {
    id: 'subquery-exists',
    category: 'Subqueries & EXISTS',
    difficulty: 'advanced',
    title: 'Find Customers Who Ordered a Specific Product',
    description: 'Use EXISTS to find customers who ordered Wireless Mouse',
    domain: 'ecommerce',
    sqlQuery: `-- Customers who ordered Wireless Mouse
SELECT c.customer_id, c.customer_name, c.email
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
    WHERE o.customer_id = c.customer_id
      AND p.product_name = 'Wireless Mouse'
)
ORDER BY c.customer_name;`,
    javaStreamCode: `// Java Stream API equivalent
Set<String> qualifyingProductIds = products.stream()
    .filter(p -> p.getProductName().equals("Wireless Mouse"))
    .map(Product::getProductId)
    .collect(Collectors.toSet());

List<Customer> result = orders.stream()
    .filter(o -> o.getOrderItems().stream()
        .anyMatch(oi -> qualifyingProductIds.contains(oi.getProductId())))
    .map(Order::getCustomer)
    .distinct()
    .sorted(Comparator.comparing(Customer::getCustomerName))
    .collect(Collectors.toList());`,
    explanation: 'SQL EXISTS checks for the presence of related records. Java uses anyMatch() on nested streams for the same logic.',
    output: 'customer_id | customer_name | email\n1           | Alice Johnson | alice@email.com\n5           | Carol Williams| carol@email.com',
  },
  {
    id: 'pivot-case',
    category: 'Pivot & Conditional Logic',
    difficulty: 'advanced',
    title: 'Department Salary Distribution',
    description: 'Pivot salary data to show salary ranges per department',
    domain: 'hr',
    sqlQuery: `-- Salary distribution by department
SELECT department,
       COUNT(*) AS total_employees,
       SUM(CASE WHEN salary < 50000 THEN 1 ELSE 0 END) AS low,
       SUM(CASE WHEN salary BETWEEN 50000 AND 80000 THEN 1 ELSE 0 END) AS mid,
       SUM(CASE WHEN salary > 80000 THEN 1 ELSE 0 END) AS high
FROM employees
GROUP BY department
ORDER BY department;`,
    javaStreamCode: `// Java Stream API equivalent
Map<String, DepartmentStats> distribution = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.collectingAndThen(Collectors.toList(), list -> {
            long low = list.stream().filter(e -> e.getSalary() < 50000).count();
            long mid = list.stream().filter(e -> e.getSalary() >= 50000 && e.getSalary() <= 80000).count();
            long high = list.stream().filter(e -> e.getSalary() > 80000).count();
            return new DepartmentStats(list.size(), low, mid, high);
        })
    ));`,
    explanation: 'SQL CASE expressions inside aggregate functions pivot data into multiple columns. Java groups by department and computes counts using filters.',
    output: 'department    | total_employees | low | mid | high\nEngineering   | 3               | 0   | 1   | 2\nSales         | 2               | 0   | 2   | 0',
  },
  {
    id: 'cte-hierarchy',
    category: 'CTEs & Hierarchical Queries',
    difficulty: 'advanced',
    title: 'Employee Reporting Hierarchy',
    description: 'Build an org chart showing reporting relationships',
    domain: 'hr',
    sqlQuery: `-- Recursive CTE for employee hierarchy
WITH RECURSIVE org_chart AS (
    SELECT employee_id, name, manager_id, 0 AS level, name AS path
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.name, e.manager_id,
           oc.level + 1, oc.path || ' -> ' || e.name
    FROM employees e
    INNER JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT employee_id, name, level, path
FROM org_chart
ORDER BY path;`,
    javaStreamCode: `// Java Stream API equivalent
// Build hierarchy tree from flat employee list
Map<Integer, List<Employee>> byManager = employees.stream()
    .filter(e -> e.getManagerId() != null)
    .collect(Collectors.groupingBy(Employee::getManagerId));

List<HierarchyNode> buildHierarchy(Employee mgr, int level) {
    List<HierarchyNode> result = new ArrayList<>();
    result.add(new HierarchyNode(mgr, level));
    List<Employee> reports = byManager.getOrDefault(mgr.getEmployeeId(), List.of());
    for (Employee report : reports) {
        result.addAll(buildHierarchy(report, level + 1));
    }
    return result;
}

List<HierarchyNode> orgChart = employees.stream()
    .filter(e -> e.getManagerId() == null)
    .flatMap(e -> buildHierarchy(e, 0).stream())
    .collect(Collectors.toList());`,
    explanation: 'Recursive CTEs traverse hierarchical data in SQL. Java requires a recursive helper method since Stream API has no built-in recursion.',
    output: 'employee_id | name       | level | path\n1           | Alice      | 0     | Alice\n3           | Bob        | 1     | Alice -> Bob\n2           | Charlie    | 1     | Alice -> Charlie',
  },
  {
    id: 'deduplicate',
    category: 'Nth Most/Least Queries',
    difficulty: 'intermediate',
    title: 'Remove Duplicate Posts Keeping Latest',
    description: 'Find duplicate posts and keep only the most recent',
    domain: 'social-media',
    sqlQuery: `-- Find duplicate posts by same user with same title, keep latest
WITH ranked_posts AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY user_id, title ORDER BY created_at DESC
    ) AS rn
    FROM posts
)
SELECT post_id, user_id, title, created_at
FROM ranked_posts
WHERE rn = 1
ORDER BY user_id, created_at DESC;`,
    javaStreamCode: `// Java Stream API equivalent
Collection<Post> uniquePosts = posts.stream()
    .collect(Collectors.toMap(
        p -> p.getUser().getUserId() + "-" + p.getTitle(),
        Function.identity(),
        (a, b) -> a.getCreatedAt().compareTo(b.getCreatedAt()) > 0 ? a : b
    ))
    .values();`,
    explanation: 'SQL uses ROW_NUMBER() with PARTITION BY to identify duplicates. Java uses toMap with a merge function to keep the latest.',
    output: 'post_id | user_id | title              | created_at\n3       | 1       | Getting Started    | 2024-01-20\n4       | 2       | Advanced Streams   | 2024-02-25',
  },
  {
    id: 'percentile',
    category: 'Window Functions',
    difficulty: 'advanced',
    title: 'Find Top 10% Performers',
    description: 'Identify students in the top 10% by grade',
    domain: 'student',
    sqlQuery: `-- Top 10% of students by grade
WITH ranked AS (
    SELECT *, NTILE(10) OVER (ORDER BY grade DESC) AS decile
    FROM student_grades
)
SELECT student_id, student_name, subject, grade
FROM ranked
WHERE decile = 1
ORDER BY grade DESC;`,
    javaStreamCode: `// Java Stream API equivalent
int topPercent = 10;
List<StudentGrade> sorted = studentGrades.stream()
    .sorted(Comparator.comparingDouble(StudentGrade::getGrade).reversed())
    .collect(Collectors.toList());
int cutoff = (int) Math.ceil(sorted.size() * topPercent / 100.0);
List<StudentGrade> topPerformers = sorted.subList(0, cutoff);`,
    explanation: 'SQL NTILE(10) divides rows into 10 buckets. Java sorts, calculates the cutoff index, and takes the top portion.',
    output: 'student_id | student_name | subject | grade\n1          | Alice        | Math    | 95',
  },
  {
    id: 'string-agg',
    category: 'Grouping & Aggregation',
    difficulty: 'intermediate',
    title: 'Concatenate Skills per Employee',
    description: 'List each employee with their comma-separated skills',
    domain: 'hr',
    sqlQuery: `-- Concatenate skills per employee
SELECT e.employee_id, e.name,
       STRING_AGG(s.skill_name, ', ' ORDER BY s.skill_name) AS skills
FROM employees e
LEFT JOIN employee_skills es ON e.employee_id = es.employee_id
LEFT JOIN skills s ON es.skill_id = s.skill_id
GROUP BY e.employee_id, e.name
ORDER BY e.name;`,
    javaStreamCode: `// Java Stream API equivalent
Map<String, String> empSkills = employees.stream()
    .collect(Collectors.toMap(
        Employee::getName,
        e -> e.getSkills().stream()
            .map(Skill::getSkillName)
            .sorted()
            .collect(Collectors.joining(", "))
    ));`,
    explanation: 'SQL STRING_AGG concatenates grouped values. Java uses Collectors.joining() after sorting within each group.',
    output: 'employee_id | name       | skills\n1           | Alice      | Java, Python, SQL\n3           | Bob        | JavaScript, TypeScript',
  },
  {
    id: 'having-complex',
    category: 'Grouping & Aggregation',
    difficulty: 'advanced',
    title: 'Find Departments with High Avg Salary',
    description: 'Filter groups based on aggregate conditions',
    domain: 'hr',
    sqlQuery: `-- Departments with average salary > 70000
SELECT department, AVG(salary) AS avg_salary, COUNT(*) AS emp_count
FROM employees
GROUP BY department
HAVING AVG(salary) > 70000
ORDER BY avg_salary DESC;`,
    javaStreamCode: `// Java Stream API equivalent
Map<String, DepartmentStats> highAvgDepts = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.averagingDouble(Employee::getSalary)
    ))
    .entrySet().stream()
    .filter(e -> e.getValue() > 70000)
    .collect(Collectors.toMap(
        Map.Entry::getKey,
        Map.Entry::getValue
    ));`,
    explanation: 'SQL HAVING filters after GROUP BY. Java groups first, then filters the resulting map entries.',
    output: 'department    | avg_salary | emp_count\nEngineering   | 81666.67   | 3',
  },
  {
    id: 'cross-join',
    category: 'Joins & Relationships',
    difficulty: 'intermediate',
    title: 'Generate All Product-Category Combinations',
    description: 'Create a complete product-category matrix',
    domain: 'ecommerce',
    sqlQuery: `-- All product-category combinations
SELECT p.product_name, p.category, pr.promotion_code,
       pr.discount_percent
FROM products p
CROSS JOIN promotions pr
WHERE pr.active = TRUE
ORDER BY p.product_name, pr.promotion_code;`,
    javaStreamCode: `// Java Stream API equivalent
List<ProductPromotion> combinations = products.stream()
    .flatMap(p -> promotions.stream()
        .filter(pr -> pr.isActive())
        .map(pr -> new ProductPromotion(
            p.getProductName(), p.getCategory(),
            pr.getPromotionCode(), pr.getDiscountPercent()
        )))
    .sorted(Comparator.comparing(ProductPromotion::getProductName)
        .thenComparing(ProductPromotion::getPromotionCode))
    .collect(Collectors.toList());`,
    explanation: 'CROSS JOIN produces every combination of rows from two tables. Java flatMap on the outer stream produces every pairing.',
    output: 'product_name    | category    | promotion_code | discount_percent\nLaptop          | Electronics | SUMMER24       | 15\nLaptop          | Electronics | WINTER24       | 10\nMouse           | Accessories | SUMMER24       | 15',
  },
];

const domainSchemas = {
  ecommerce: {
    domain: 'ecommerce',
    label: '🛒 E-commerce',
    ddl: `CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(100),
  email VARCHAR(100),
  total_purchases DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(100),
  price DECIMAL(10,2),
  category VARCHAR(50),
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_id INT REFERENCES customers(customer_id),
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_amount DECIMAL(10,2)
);

CREATE TABLE order_items (
  order_item_id INT PRIMARY KEY,
  order_id INT REFERENCES orders(order_id),
  product_id INT REFERENCES products(product_id),
  quantity INT,
  unit_price DECIMAL(10,2)
);

CREATE TABLE promotions (
  promotion_code VARCHAR(20) PRIMARY KEY,
  discount_percent DECIMAL(5,2),
  active BOOLEAN DEFAULT TRUE,
  valid_from DATE,
  valid_until DATE
);

CREATE TABLE daily_sales (
  sale_date DATE PRIMARY KEY,
  daily_sales DECIMAL(10,2)
);`,
    sampleData: `INSERT INTO customers VALUES
  (1, 'Alice Johnson', 'alice@email.com', 2500.00, '2023-06-15'),
  (2, 'Charlie Brown', 'charlie@email.com', 500.00, '2023-08-20'),
  (3, 'Bob Smith', 'bob@email.com', 1800.00, '2023-07-01'),
  (4, 'Diana Prince', 'diana@email.com', 300.00, '2024-01-10'),
  (5, 'Carol Williams', 'carol@email.com', 1200.00, '2023-09-05');

INSERT INTO products VALUES
  (1, 'Laptop', 999.99, 'Electronics', TRUE, '2024-01-01'),
  (2, 'Wireless Mouse', 29.99, 'Accessories', TRUE, '2024-01-01'),
  (3, 'Monitor', 399.99, 'Electronics', TRUE, '2024-01-01'),
  (4, 'Keyboard', 79.99, 'Accessories', TRUE, '2024-01-10'),
  (5, 'Headphones', 149.99, 'Electronics', TRUE, '2024-01-15');

INSERT INTO orders VALUES
  (1, 1, '2024-01-15', 1200.00),
  (2, 1, '2024-02-20', 800.00),
  (3, 3, '2024-01-25', 950.00),
  (4, 5, '2024-03-01', 750.00),
  (5, 1, '2024-03-15', 250.00),
  (6, 5, '2024-03-20', 450.00);

INSERT INTO order_items VALUES
  (1, 1, 1, 1, 999.99),
  (2, 2, 2, 2, 29.99),
  (3, 3, 3, 1, 399.99),
  (4, 4, 4, 1, 79.99),
  (5, 5, 2, 1, 29.99),
  (6, 6, 5, 1, 149.99);

INSERT INTO promotions VALUES
  ('SUMMER24', 15.00, TRUE, '2024-06-01', '2024-08-31'),
  ('WINTER24', 10.00, TRUE, '2024-12-01', '2024-12-31');

INSERT INTO daily_sales VALUES
  ('2024-01-01', 100.00),
  ('2024-01-02', 150.00),
  ('2024-01-03', 200.00);`,
    javaModels: `public class Customer {
    private int customerId;
    private String customerName;
    private String email;
    private double totalPurchases;
    private LocalDateTime createdAt;
    private List<Order> orders = new ArrayList<>();
    // constructor, getters, setters, toString()
}

public class Product {
    private int productId;
    private String productName;
    private double price;
    private String category;
    private boolean active;
    private LocalDateTime createdAt;
    // constructor, getters, setters, toString()
}

public class Order {
    private int orderId;
    private Customer customer;
    private LocalDateTime orderDate;
    private double totalAmount;
    private List<OrderItem> orderItems = new ArrayList<>();
    // constructor, getters, setters, toString()
}

public class OrderItem {
    private int orderItemId;
    private Order order;
    private Product product;
    private int quantity;
    private double unitPrice;
    // constructor, getters, setters, toString()
}

public class Promotion {
    private String promotionCode;
    private double discountPercent;
    private boolean active;
    private LocalDate validFrom;
    private LocalDate validUntil;
    // constructor, getters, setters, toString()
}

public class DailySales {
    private LocalDate saleDate;
    private double dailySales;
    // constructor, getters, setters, toString()
}

// DTOs
public class ProductPromotion {
    private String productName;
    private String category;
    private String promotionCode;
    private double discountPercent;
    // constructor, getters, toString()
}`,
  },
  hr: {
    domain: 'hr',
    label: '🏢 HR',
    ddl: `CREATE TABLE employees (
  employee_id INT PRIMARY KEY,
  name VARCHAR(100),
  department VARCHAR(50),
  salary DECIMAL(10,2),
  years_of_service INT,
  manager_id INT REFERENCES employees(employee_id),
  hire_date DATE
);

CREATE TABLE skills (
  skill_id INT PRIMARY KEY,
  skill_name VARCHAR(50)
);

CREATE TABLE employee_skills (
  employee_id INT REFERENCES employees(employee_id),
  skill_id INT REFERENCES skills(skill_id),
  PRIMARY KEY (employee_id, skill_id)
);`,
    sampleData: `INSERT INTO employees VALUES
  (1, 'Alice Johnson', 'Engineering', 85000.00, 8, NULL, '2016-03-15'),
  (2, 'Charlie Brown', 'Sales', 62000.00, 3, 1, '2021-06-01'),
  (3, 'Bob Smith', 'Engineering', 95000.00, 5, 1, '2019-01-20'),
  (4, 'Diana Prince', 'Sales', 72000.00, 4, 1, '2020-02-15'),
  (5, 'Eve Davis', 'Engineering', 65000.00, 2, 3, '2022-08-01');

INSERT INTO skills VALUES
  (1, 'Java'), (2, 'Python'), (3, 'SQL'),
  (4, 'JavaScript'), (5, 'TypeScript');

INSERT INTO employee_skills VALUES
  (1, 1), (1, 2), (1, 3),
  (3, 4), (3, 5),
  (5, 1), (5, 3);`,
    javaModels: `public class Employee {
    private int employeeId;
    private String name;
    private String department;
    private double salary;
    private int yearsOfService;
    private int managerId;
    private Employee manager;
    private LocalDate hireDate;
    private List<Skill> skills = new ArrayList<>();
    // constructor, getters, setters, toString()
}

public class Skill {
    private int skillId;
    private String skillName;
    // constructor, getters, setters, toString()
}

public class EmployeeSkill {
    private int employeeId;
    private int skillId;
    // constructor, getters, setters, toString()
}

// DTOs
public class SalaryComparison {
    private String employee;
    private double empSalary;
    private String manager;
    private double mgrSalary;
    // constructor, getters, toString()
}

public class DepartmentStats {
    private long totalEmployees;
    private long low;
    private long mid;
    private long high;
    // constructor, getters, toString()
}

public class HierarchyNode {
    private Employee employee;
    private int level;
    private List<HierarchyNode> children = new ArrayList<>();
    // constructor, getters, toString()
}`,
  },
  'social-media': {
    domain: 'social-media',
    label: '📱 Social Media',
    ddl: `CREATE TABLE users (
  user_id INT PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  email VARCHAR(100),
  status VARCHAR(20),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
  post_id INT PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  title VARCHAR(200),
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
  comment_id INT PRIMARY KEY,
  post_id INT REFERENCES posts(post_id),
  user_id INT REFERENCES users(user_id),
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);`,
    sampleData: `INSERT INTO users VALUES
  (1, 'alice', 'alice@social.com', 'active', '2024-01-01'),
  (2, 'bob', 'bob@social.com', 'active', '2024-01-05');

INSERT INTO posts VALUES
  (1, 1, 'Getting Started with SQL', 'SQL is amazing...', '2024-01-15'),
  (2, 2, 'Advanced Streams', 'Java streams are powerful...', '2024-02-20'),
  (3, 1, 'Getting Started with SQL', 'Duplicate post...', '2024-01-20'),
  (4, 2, 'Advanced Streams', 'Another on same topic...', '2024-02-25');

INSERT INTO comments VALUES
  (1, 1, 2, 'Great post!', '2024-01-16'),
  (2, 2, 1, 'Thanks for sharing', '2024-02-21');`,
    javaModels: `public class User {
    private int userId;
    private String username;
    private String email;
    private String status;
    private LocalDateTime createdAt;
    private List<Post> posts = new ArrayList<>();
    // constructor, getters, setters, toString()
}

public class Post {
    private int postId;
    private User user;
    private String title;
    private String content;
    private LocalDateTime createdAt;
    private List<Comment> comments = new ArrayList<>();
    // constructor, getters, setters, toString()
}

public class Comment {
    private int commentId;
    private Post post;
    private User user;
    private String content;
    private LocalDateTime createdAt;
    // constructor, getters, setters, toString()
}`,
  },
  student: {
    domain: 'student',
    label: '🎓 Student',
    ddl: `CREATE TABLE student_grades (
  student_id INT,
  student_name VARCHAR(100),
  subject VARCHAR(50),
  grade DECIMAL(5,2),
  semester VARCHAR(20),
  PRIMARY KEY (student_id, subject)
);`,
    sampleData: `INSERT INTO student_grades VALUES
  (1, 'Alice', 'Math', 95.00, '2024-S1'),
  (1, 'Alice', 'Science', 88.00, '2024-S1'),
  (2, 'Bob', 'Math', 82.00, '2024-S1'),
  (2, 'Bob', 'Science', 75.00, '2024-S1'),
  (3, 'Charlie', 'Math', 70.00, '2024-S1'),
  (3, 'Charlie', 'Science', 85.00, '2024-S1');`,
    javaModels: `public class StudentGrade {
    private int studentId;
    private String studentName;
    private String subject;
    private double grade;
    private String semester;
    // constructor, getters, setters, toString()
}

// DTOs
public class StudentGradeWithRank {
    private StudentGrade grade;
    private int rank;
    // constructor, getters, toString()
}

public class StudentPercentile {
    private StudentGrade grade;
    private int percentile;
    // constructor, getters, toString()
}`,
  },
};

const categories = [...new Set(queries.map(q => q.category))].sort();
const domains = Object.keys(domainSchemas);
const difficulties = ['beginner', 'intermediate', 'advanced'];

const domainLabels = {
  ecommerce: '🛒 E-commerce',
  hr: '🏢 HR',
  'social-media': '📱 Social Media',
  student: '🎓 Student',
};

const difficultyColors = {
  beginner: { bg: '#d4edda', color: '#155724' },
  intermediate: { bg: '#fff3cd', color: '#856404' },
  advanced: { bg: '#f8d7da', color: '#721c24' },
};

export { queries, domainSchemas, categories, domains, difficulties, domainLabels, difficultyColors };
