//! Day 4: Stack & Queue Data Structures
//! =====================================
//! Topics Covered:
//! 1. Stack Operations and Applications
//! 2. Queue Operations and Applications
//! 3. Monotonic Stack Patterns
//! 4. BFS (Breadth-First Search) Applications
//!
//! Each section includes:
//! - Concept explanation
//! - Implementation template
//! - Practice problems with solutions

use std::collections::{HashMap, VecDeque};

// ============================================================================
// 1. STACK OPERATIONS AND APPLICATIONS
// ============================================================================

/// Stack implementation using Vec
///
/// Operations:
/// - push(x): Add element to top - O(1)
/// - pop(): Remove top element - O(1)
/// - peek(): View top element - O(1)
/// - is_empty(): Check if empty - O(1)
///
/// Applications:
/// - Function call stack
/// - Undo mechanisms
/// - Expression evaluation
/// - Backtracking algorithms
#[derive(Debug)]
struct Stack<T> {
    data: Vec<T>,
}

impl<T> Stack<T> {
    fn new() -> Self {
        Stack { data: Vec::new() }
    }

    fn push(&mut self, x: T) {
        self.data.push(x);
    }

    fn pop(&mut self) -> Option<T> {
        self.data.pop()
    }

    fn peek(&self) -> Option<&T> {
        self.data.last()
    }

    fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    fn size(&self) -> usize {
        self.data.len()
    }
}

/// MinStack: Stack that supports push, pop, top, and retrieving minimum in O(1)
///
/// Approach: Use two stacks
/// - Main stack stores all values
/// - Min stack tracks minimum at each level
#[derive(Debug)]
struct MinStack {
    stack: Vec<i32>,
    min_stack: Vec<i32>,
}

impl MinStack {
    fn new() -> Self {
        MinStack {
            stack: Vec::new(),
            min_stack: Vec::new(),
        }
    }

    fn push(&mut self, val: i32) {
        self.stack.push(val);
        if self.min_stack.is_empty() || val <= *self.min_stack.last().unwrap() {
            self.min_stack.push(val);
        }
    }

    fn pop(&mut self) -> Option<i32> {
        if let Some(val) = self.stack.pop() {
            if self.min_stack.last() == Some(&val) {
                self.min_stack.pop();
            }
            Some(val)
        } else {
            None
        }
    }

    fn top(&self) -> Option<i32> {
        self.stack.last().copied()
    }

    fn get_min(&self) -> Option<i32> {
        self.min_stack.last().copied()
    }
}

/// Valid Parentheses
///
/// Problem: Given a string containing just '(', ')', '{', '}', '[' and ']',
/// determine if the input string is valid.
///
/// Example:
///     "()" → true
///     "()[]{}" → true
///     "(]" → false
///     "([)]" → false
///     "{[]}" → true
///
/// Approach: Stack-based validation
/// - Push opening brackets onto stack
/// - For closing brackets, check if matches top of stack
/// - String is valid if stack is empty at end
fn is_valid(s: &str) -> bool {
    let mut stack: Vec<char> = Vec::new();
    let bracket_map: HashMap<char, char> = [
        (')', '('),
        ('}', '{'),
        (']', '['),
    ].iter().cloned().collect();

    for c in s.chars() {
        if let Some(&opening) = bracket_map.get(&c) {
            // Closing bracket
            if stack.pop() != Some(opening) {
                return false;
            }
        } else {
            // Opening bracket
            stack.push(c);
        }
    }

    stack.is_empty()
}

/// Evaluate Reverse Polish Notation
///
/// Problem: Evaluate the value of an arithmetic expression in Reverse Polish Notation.
/// Valid operators: +, -, *, /
///
/// Example:
///     ["2", "1", "+", "3", "*"] → 9  // ((2 + 1) * 3)
///     ["4", "13", "5", "/", "+"] → 6  // (4 + (13 / 5))
///
/// Approach: Stack-based evaluation
/// - Push numbers onto stack
/// - When operator encountered, pop two operands, compute, push result
fn eval_rpn(tokens: Vec<&str>) -> i32 {
    let mut stack: Vec<i32> = Vec::new();

    for token in tokens {
        match token {
            "+" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a + b);
            }
            "-" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a - b);
            }
            "*" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a * b);
            }
            "/" => {
                let b = stack.pop().unwrap();
                let a = stack.pop().unwrap();
                stack.push(a / b); // Integer division truncates toward zero
            }
            _ => {
                stack.push(token.parse::<i32>().unwrap());
            }
        }
    }

    stack[0]
}

// ============================================================================
// 2. QUEUE OPERATIONS AND APPLICATIONS
// ============================================================================

/// Queue implementation using VecDeque
///
/// Operations:
/// - enqueue(x): Add element to rear - O(1)
/// - dequeue(): Remove front element - O(1)
/// - front(): View front element - O(1)
/// - is_empty(): Check if empty - O(1)
///
/// Applications:
/// - BFS traversal
/// - Level-order traversal
/// - Task scheduling
/// - Buffer management
#[derive(Debug)]
struct Queue<T> {
    data: VecDeque<T>,
}

impl<T> Queue<T> {
    fn new() -> Self {
        Queue {
            data: VecDeque::new(),
        }
    }

    fn enqueue(&mut self, x: T) {
        self.data.push_back(x);
    }

    fn dequeue(&mut self) -> Option<T> {
        self.data.pop_front()
    }

    fn front(&self) -> Option<&T> {
        self.data.front()
    }

    fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    fn size(&self) -> usize {
        self.data.len()
    }
}

/// MyCircularQueue: Circular queue (ring buffer) with fixed size k
///
/// Approach: Vec with two pointers
/// - Use Vec of size k
/// - Front pointer points to first element
/// - Rear pointer points to next available slot
/// - Track count to distinguish full vs empty
#[derive(Debug)]
struct MyCircularQueue {
    queue: Vec<i32>,
    front: usize,
    rear: usize,
    count: usize,
    capacity: usize,
}

impl MyCircularQueue {
    fn new(k: i32) -> Self {
        let capacity = k as usize;
        MyCircularQueue {
            queue: vec![0; capacity],
            front: 0,
            rear: 0,
            count: 0,
            capacity,
        }
    }

    fn en_queue(&mut self, value: i32) -> bool {
        if self.is_full() {
            return false;
        }
        self.queue[self.rear] = value;
        self.rear = (self.rear + 1) % self.capacity;
        self.count += 1;
        true
    }

    fn de_queue(&mut self) -> bool {
        if self.is_empty() {
            return false;
        }
        self.front = (self.front + 1) % self.capacity;
        self.count -= 1;
        true
    }

    fn front(&self) -> i32 {
        if self.is_empty() {
            -1
        } else {
            self.queue[self.front]
        }
    }

    fn rear(&self) -> i32 {
        if self.is_empty() {
            -1
        } else {
            self.queue[(self.rear + self.capacity - 1) % self.capacity]
        }
    }

    fn is_empty(&self) -> bool {
        self.count == 0
    }

    fn is_full(&self) -> bool {
        self.count == self.capacity
    }
}

// ============================================================================
// 3. MONOTONIC STACK PATTERNS
// ============================================================================

/// Monotonic Stack patterns:
///
/// Pattern 1: Next Greater Element
/// - Used for: Finding next greater/smaller element
/// - Time: O(n), Space: O(n)
///
/// Pattern 2: Daily Temperatures
/// - Used for: Finding distance to next greater element
/// - Time: O(n), Space: O(n)
///
/// Pattern 3: Largest Rectangle in Histogram
/// - Used for: Finding maximum area
/// - Time: O(n), Space: O(n)

/// Next Greater Element
///
/// Problem: Find the next greater element for each element.
///
/// Example: nums = [2, 1, 2, 4, 3] → [4, 2, 4, -1, -1]
///
/// Approach: Monotonic decreasing stack
/// - Stack stores indices of elements waiting for greater element
/// - When current > stack top, we found next greater for stack top
fn next_greater_element(nums: &[i32]) -> Vec<i32> {
    let n = nums.len();
    let mut result = vec![-1; n];
    let mut stack: Vec<usize> = Vec::new();

    for i in 0..n {
        while let Some(&idx) = stack.last() {
            if nums[i] > nums[idx] {
                stack.pop();
                result[idx] = nums[i];
            } else {
                break;
            }
        }
        stack.push(i);
    }

    result
}

/// Daily Temperatures
///
/// Problem: For each day, find how many days until warmer temperature.
///
/// Example: temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
///          → [1, 1, 4, 2, 1, 1, 0, 0]
///
/// Approach: Monotonic decreasing stack
/// - Stack stores indices of days waiting for warmer temperature
/// - When current temp > stack top, calculate waiting days
fn daily_temperatures(temperatures: &[i32]) -> Vec<i32> {
    let n = temperatures.len();
    let mut result = vec![0; n];
    let mut stack: Vec<usize> = Vec::new();

    for i in 0..n {
        while let Some(&idx) = stack.last() {
            if temperatures[i] > temperatures[idx] {
                stack.pop();
                result[idx] = (i - idx) as i32;
            } else {
                break;
            }
        }
        stack.push(i);
    }

    result
}

/// Largest Rectangle in Histogram
///
/// Problem: Find largest rectangle in histogram.
///
/// Example: heights = [2, 1, 5, 6, 2, 3] → 10
///
/// Approach: Monotonic increasing stack
/// - Stack stores indices of bars in increasing height order
/// - When current < stack top, pop and calculate area with popped height
/// - Width = current index - new stack top index - 1
fn largest_rectangle_in_histogram(heights: &[i32]) -> i32 {
    let mut stack: Vec<usize> = Vec::new();
    let mut max_area = 0;
    let n = heights.len();

    for i in 0..=n {
        let h = if i < n { heights[i] } else { 0 };

        while let Some(&idx) = stack.last() {
            if h < heights[idx] {
                stack.pop();
                let height = heights[idx];
                let width = if stack.is_empty() { i } else { i - stack.last().unwrap() - 1 };
                max_area = max_area.max(height * width as i32);
            } else {
                break;
            }
        }
        stack.push(i);
    }

    max_area
}

/// Maximal Rectangle
///
/// Problem: Find largest rectangle containing only 1's in binary matrix.
///
/// Example: matrix = [["1","0","1","0","0"],
///                    ["1","0","1","1","1"],
///                    ["1","1","1","1","1"],
///                    ["1","0","0","1","0"]]
///          → 6
///
/// Approach: Build histograms row by row
/// - For each row, build histogram of consecutive 1's above
/// - Apply largest rectangle in histogram for each row
fn maximal_rectangle(matrix: &[Vec<char>]) -> i32 {
    if matrix.is_empty() || matrix[0].is_empty() {
        return 0;
    }

    let cols = matrix[0].len();
    let mut heights = vec![0; cols];
    let mut max_area = 0;

    for row in matrix {
        for j in 0..cols {
            if row[j] == '1' {
                heights[j] += 1;
            } else {
                heights[j] = 0;
            }
        }
        max_area = max_area.max(largest_rectangle_in_histogram(&heights));
    }

    max_area
}

// ============================================================================
// 4. BFS (BREADTH-FIRST SEARCH) APPLICATIONS
// ============================================================================

/// BFS patterns:
///
/// Pattern 1: Level-Order Traversal
/// - Used for: Tree level processing
/// - Time: O(n), Space: O(w) where w is max width
///
/// Pattern 2: Shortest Path in Unweighted Graph
/// - Used for: Finding minimum steps
/// - Time: O(V + E), Space: O(V)
///
/// Pattern 3: Multi-Source BFS
/// - Used for: Distance from nearest source
/// - Time: O(m*n), Space: O(m*n)

/// Binary tree node for tree problems
#[derive(Debug, Clone)]
struct TreeNode {
    val: i32,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

impl TreeNode {
    fn new(val: i32) -> Self {
        TreeNode {
            val,
            left: None,
            right: None,
        }
    }
}

/// Level Order Traversal
///
/// Problem: Return level-order traversal of binary tree.
///
/// Example:     3
///             / \
///            9  20
///              /  \
///             15   7
///          → [[3], [9, 20], [15, 7]]
///
/// Approach: Queue-based level processing
/// - Add root to queue
/// - Process all nodes at current level before next
/// - Track level size to know when level ends
fn level_order_traversal(root: Option<Box<TreeNode>>) -> Vec<Vec<i32>> {
    let mut result: Vec<Vec<i32>> = Vec::new();
    let mut queue: VecDeque<Box<TreeNode>> = VecDeque::new();

    if let Some(root_node) = root {
        queue.push_back(root_node);
    }

    while !queue.is_empty() {
        let level_size = queue.len();
        let mut current_level: Vec<i32> = Vec::new();

        for _ in 0..level_size {
            if let Some(node) = queue.pop_front() {
                current_level.push(node.val);

                if let Some(left) = node.left {
                    queue.push_back(left);
                }
                if let Some(right) = node.right {
                    queue.push_back(right);
                }
            }
        }

        result.push(current_level);
    }

    result
}

/// Number of Islands
///
/// Problem: Count number of islands in 2D grid ('1' = land, '0' = water).
///
/// Example: grid = [["1","1","0","0","0"],
///                  ["1","1","0","0","0"],
///                  ["0","0","1","0","0"],
///                  ["0","0","0","1","1"]]
///          → 3
///
/// Approach: BFS to mark connected components
/// - Iterate through grid, when find '1', increment count
/// - Use BFS to mark entire island as visited
fn num_islands(grid: &mut Vec<Vec<char>>) -> i32 {
    if grid.is_empty() || grid[0].is_empty() {
        return 0;
    }

    let rows = grid.len();
    let cols = grid[0].len();
    let mut count = 0;

    fn bfs(grid: &mut Vec<Vec<char>>, start_row: usize, start_col: usize) {
        let rows = grid.len();
        let cols = grid[0].len();
        let mut queue: VecDeque<(usize, usize)> = VecDeque::new();

        grid[start_row][start_col] = '0';
        queue.push_back((start_row, start_col));

        let directions = [(1, 0), (-1, 0), (0, 1), (0, -1)];

        while let Some((row, col)) = queue.pop_front() {
            for (dr, dc) in directions {
                let nr = row as i32 + dr;
                let nc = col as i32 + dc;

                if nr >= 0 && nr < rows as i32 && nc >= 0 && nc < cols as i32 {
                    let (nr, nc) = (nr as usize, nc as usize);
                    if grid[nr][nc] == '1' {
                        grid[nr][nc] = '0';
                        queue.push_back((nr, nc));
                    }
                }
            }
        }
    }

    for i in 0..rows {
        for j in 0..cols {
            if grid[i][j] == '1' {
                count += 1;
                bfs(grid, i, j);
            }
        }
    }

    count
}

/// Shortest Path in Binary Matrix
///
/// Problem: Find shortest clear path from top-left to bottom-right.
/// Can move in 8 directions. Return -1 if no path.
///
/// Example: grid = [[0,0,0],
///                  [1,1,0],
///                  [1,1,0]]
///          → 4
///
/// Approach: BFS for shortest path in unweighted grid
/// - Start from (0, 0), explore 8 directions
/// - Track distance, return when reach (n-1, n-1)
fn shortest_path_binary_matrix(grid: &mut Vec<Vec<i32>>) -> i32 {
    let n = grid.len();

    if n == 0 || grid[0][0] != 0 || grid[n - 1][n - 1] != 0 {
        return -1;
    }

    if n == 1 {
        return 1;
    }

    let mut queue: VecDeque<(usize, usize, i32)> = VecDeque::new();
    queue.push_back((0, 0, 1));
    grid[0][0] = 1;

    let directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)];

    while let Some((row, col, dist)) = queue.pop_front() {
        for (dr, dc) in directions {
            let nr = row as i32 + dr;
            let nc = col as i32 + dc;

            if nr == n as i32 - 1 && nc == n as i32 - 1 {
                return dist + 1;
            }

            if nr >= 0 && nr < n as i32 && nc >= 0 && nc < n as i32 {
                let (nr, nc) = (nr as usize, nc as usize);
                if grid[nr][nc] == 0 {
                    grid[nr][nc] = 1;
                    queue.push_back((nr, nc, dist + 1));
                }
            }
        }
    }

    -1
}

/// Rotting Oranges
///
/// Problem: Find minimum minutes until no fresh oranges left.
/// 0 = empty, 1 = fresh, 2 = rotten. Return -1 if impossible.
///
/// Example: grid = [[2,1,1],
///                  [1,1,0],
///                  [0,1,1]]
///          → 4
///
/// Approach: Multi-source BFS
/// - Add all rotten oranges to queue initially
/// - Process level by level, each level = 1 minute
/// - Count fresh oranges, decrement as they rot
fn rotting_oranges(grid: &mut Vec<Vec<i32>>) -> i32 {
    if grid.is_empty() || grid[0].is_empty() {
        return 0;
    }

    let rows = grid.len();
    let cols = grid[0].len();
    let mut queue: VecDeque<(usize, usize)> = VecDeque::new();
    let mut fresh_count = 0;

    // Initialize: count fresh, add rotten to queue
    for i in 0..rows {
        for j in 0..cols {
            if grid[i][j] == 2 {
                queue.push_back((i, j));
            } else if grid[i][j] == 1 {
                fresh_count += 1;
            }
        }
    }

    if fresh_count == 0 {
        return 0;
    }

    let mut minutes = 0;
    let directions = [(1, 0), (-1, 0), (0, 1), (0, -1)];

    while !queue.is_empty() && fresh_count > 0 {
        let level_size = queue.len();
        minutes += 1;

        for _ in 0..level_size {
            let (row, col) = queue.pop_front().unwrap();

            for (dr, dc) in directions {
                let nr = row as i32 + dr;
                let nc = col as i32 + dc;

                if nr >= 0 && nr < rows as i32 && nc >= 0 && nc < cols as i32 {
                    let (nr, nc) = (nr as usize, nc as usize);
                    if grid[nr][nc] == 1 {
                        grid[nr][nc] = 2;
                        fresh_count -= 1;
                        queue.push_back((nr, nc));
                    }
                }
            }
        }
    }

    if fresh_count == 0 {
        minutes
    } else {
        -1
    }
}

// ============================================================================
// TESTS
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_parentheses() {
        assert_eq!(is_valid("()"), true);
        assert_eq!(is_valid("()[]{}"), true);
        assert_eq!(is_valid("(]"), false);
        assert_eq!(is_valid("([)]"), false);
        assert_eq!(is_valid("{[]}"), true);
        assert_eq!(is_valid(""), true);
    }

    #[test]
    fn test_min_stack() {
        let mut min_stack = MinStack::new();
        min_stack.push(-2);
        min_stack.push(0);
        min_stack.push(-3);
        assert_eq!(min_stack.get_min(), Some(-3));
        min_stack.pop();
        assert_eq!(min_stack.top(), Some(0));
        assert_eq!(min_stack.get_min(), Some(-2));
    }

    #[test]
    fn test_eval_rpn() {
        assert_eq!(eval_rpn(vec!["2", "1", "+", "3", "*"]), 9);
        assert_eq!(eval_rpn(vec!["4", "13", "5", "/", "+"]), 6);
        assert_eq!(eval_rpn(vec!["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]), 22);
    }

    #[test]
    fn test_next_greater_element() {
        assert_eq!(next_greater_element(&[2, 1, 2, 4, 3]), vec![4, 2, 4, -1, -1]);
        assert_eq!(next_greater_element(&[1, 2, 3, 4, 5]), vec![2, 3, 4, 5, -1]);
        assert_eq!(next_greater_element(&[5, 4, 3, 2, 1]), vec![-1, -1, -1, -1, -1]);
    }

    #[test]
    fn test_daily_temperatures() {
        assert_eq!(daily_temperatures(&[73, 74, 75, 71, 69, 72, 76, 73]), vec![1, 1, 4, 2, 1, 1, 0, 0]);
        assert_eq!(daily_temperatures(&[30, 40, 50, 60]), vec![1, 1, 1, 0]);
        assert_eq!(daily_temperatures(&[30, 60, 90]), vec![1, 1, 0]);
    }

    #[test]
    fn test_largest_rectangle_in_histogram() {
        assert_eq!(largest_rectangle_in_histogram(&[2, 1, 5, 6, 2, 3]), 10);
        assert_eq!(largest_rectangle_in_histogram(&[2, 4]), 4);
        assert_eq!(largest_rectangle_in_histogram(&[1]), 1);
    }

    #[test]
    fn test_num_islands() {
        let mut grid1 = vec![
            vec!['1', '1', '0', '0', '0'],
            vec!['1', '1', '0', '0', '0'],
            vec!['0', '0', '1', '0', '0'],
            vec!['0', '0', '0', '1', '1'],
        ];
        assert_eq!(num_islands(&mut grid1), 3);

        let mut grid2 = vec![
            vec!['1', '1', '1'],
            vec!['0', '1', '0'],
            vec!['1', '1', '1'],
        ];
        assert_eq!(num_islands(&mut grid2), 1);
    }

    #[test]
    fn test_rotting_oranges() {
        let mut grid1 = vec![
            vec![2, 1, 1],
            vec![1, 1, 0],
            vec![0, 1, 1],
        ];
        assert_eq!(rotting_oranges(&mut grid1), 4);

        let mut grid2 = vec![
            vec![2, 1, 1],
            vec![0, 1, 1],
            vec![1, 0, 1],
        ];
        assert_eq!(rotting_oranges(&mut grid2), -1);
    }

    #[test]
    fn test_circular_queue() {
        let mut cq = MyCircularQueue::new(3);
        assert_eq!(cq.en_queue(1), true);
        assert_eq!(cq.en_queue(2), true);
        assert_eq!(cq.en_queue(3), true);
        assert_eq!(cq.en_queue(4), false);
        assert_eq!(cq.rear(), 3);
        assert_eq!(cq.is_full(), true);
        assert_eq!(cq.de_queue(), true);
        assert_eq!(cq.en_queue(4), true);
        assert_eq!(cq.rear(), 4);
    }

    #[test]
    fn test_shortest_path_binary_matrix() {
        let mut grid1 = vec![
            vec![0, 0, 0],
            vec![1, 1, 0],
            vec![1, 1, 0],
        ];
        assert_eq!(shortest_path_binary_matrix(&mut grid1), 4);

        let mut grid2 = vec![
            vec![0, 1],
            vec![1, 0],
        ];
        assert_eq!(shortest_path_binary_matrix(&mut grid2), 2);

        let mut grid3 = vec![
            vec![1, 0, 0],
            vec![1, 1, 0],
            vec![1, 1, 0],
        ];
        assert_eq!(shortest_path_binary_matrix(&mut grid3), -1);
    }
}

fn main() {
    println!("Day 4: Stack & Queue");
    println!("====================");
    println!("Run 'cargo test' to execute all tests.");
    println!();
    println!("Example tests available:");
    println!("  - test_valid_parentheses");
    println!("  - test_min_stack");
    println!("  - test_eval_rpn");
    println!("  - test_next_greater_element");
    println!("  - test_daily_temperatures");
    println!("  - test_largest_rectangle_in_histogram");
    println!("  - test_num_islands");
    println!("  - test_rotting_oranges");
    println!("  - test_circular_queue");
    println!("  - test_shortest_path_binary_matrix");
}
