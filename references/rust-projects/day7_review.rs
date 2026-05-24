// Day 7: Review & Practice - Mixed Problems from Days 1-6
// Topics: Arrays, Strings, Stacks, Queues, Linked Lists, Trees
// Focus: Pattern recognition, problem-solving strategies, implementation fluency

use std::collections::{HashMap, HashSet, VecDeque};
use std::cell::RefCell;
use std::rc::Rc;

// ============================================================
// 1. ARRAYS & HASH MAP PATTERNS (Days 1-2)
// ============================================================

/// LeetCode #1: Two Sum
/// Given an array of integers and a target, return indices of two numbers that add to target.
/// 
/// Time: O(n), Space: O(n)
/// Pattern: Hash map for complement lookup
fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
    let mut seen = HashMap::new();
    
    for (i, &num) in nums.iter().enumerate() {
        let complement = target - num;
        if let Some(&j) = seen.get(&complement) {
            return vec![j as i32, i as i32];
        }
        seen.insert(num, i);
    }
    
    vec![]
}

/// LeetCode #11: Container With Most Water
/// Find two lines that form a container holding the most water.
/// 
/// Time: O(n), Space: O(1)
/// Pattern: Two-pointer from both ends, greedy approach
fn container_with_most_water(height: Vec<i32>) -> i32 {
    let mut left = 0;
    let mut right = height.len() - 1;
    let mut max_area = 0;
    
    while left < right {
        let h = height[left].min(height[right]);
        let w = (right - left) as i32;
        max_area = max_area.max(h * w);
        
        if height[left] < height[right] {
            left += 1;
        } else {
            right -= 1;
        }
    }
    
    max_area
}

/// LeetCode #49: Group Anagrams
/// Group strings that are anagrams of each other.
/// 
/// Time: O(n * k log k) where k is max string length, Space: O(n * k)
/// Pattern: Hash map with sorted string as key
fn group_anagrams(strs: Vec<String>) -> Vec<Vec<String>> {
    let mut anagram_map: HashMap<String, Vec<String>> = HashMap::new();
    
    for s in strs {
        let mut key: Vec<char> = s.chars().collect();
        key.sort();
        let key_str: String = key.into_iter().collect();
        
        anagram_map.entry(key_str).or_insert_with(Vec::new).push(s);
    }
    
    anagram_map.into_values().collect()
}

// ============================================================
// 2. STRING MANIPULATION PATTERNS (Day 3)
// ============================================================

/// LeetCode #3: Longest Substring Without Repeating Characters
/// Find length of longest substring without repeating characters.
/// 
/// Time: O(n), Space: O(min(n, m)) where m is charset size
/// Pattern: Sliding window with hash set
fn longest_substring_without_repeating(s: String) -> i32 {
    let chars: Vec<char> = s.chars().collect();
    let mut seen = HashSet::new();
    let mut left = 0;
    let mut max_len = 0;
    
    for right in 0..chars.len() {
        while seen.contains(&chars[right]) {
            seen.remove(&chars[left]);
            left += 1;
        }
        
        seen.insert(chars[right]);
        max_len = max_len.max(right - left + 1);
    }
    
    max_len as i32
}

/// LeetCode #5: Longest Palindromic Substring
/// Find the longest palindromic substring.
/// 
/// Time: O(n²), Space: O(1)
/// Pattern: Expand around center
fn longest_palindromic_substring(s: String) -> String {
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len();
    
    if n == 0 {
        return String::new();
    }
    
    let mut start = 0;
    let mut end = 0;
    
    fn expand_around_center(chars: &[char], mut left: usize, mut right: usize) -> (usize, usize) {
        let n = chars.len();
        while left > 0 && right < n && chars[left] == chars[right] {
            if left == 0 {
                break;
            }
            left -= 1;
            right += 1;
        }
        
        if chars[left] != chars[right] {
            (left + 1, right - 1)
        } else {
            (left, right)
        }
    }
    
    for i in 0..n {
        // Odd-length palindrome
        let (l1, r1) = expand_around_center(&chars, i, i);
        // Even-length palindrome
        let (l2, r2) = if i + 1 < n {
            expand_around_center(&chars, i, i + 1)
        } else {
            (0, 0)
        };
        
        // Update longest
        if (r1 - l1) > (end - start) {
            start = l1;
            end = r1;
        }
        if (r2 - l2) > (end - start) {
            start = l2;
            end = r2;
        }
    }
    
    chars[start..=end].iter().collect()
}

/// LeetCode #28: Find the Index of the First Occurrence in a String
/// Implement strStr().
/// 
/// Time: O(n * m) naive, Space: O(1)
/// Pattern: Sliding window matching
fn str_str(haystack: String, needle: String) -> i32 {
    if needle.is_empty() {
        return 0;
    }
    
    let n = haystack.len();
    let m = needle.len();
    
    if m > n {
        return -1;
    }
    
    for i in 0..=(n - m) {
        if &haystack[i..i + m] == needle.as_str() {
            return i as i32;
        }
    }
    
    -1
}

// ============================================================
// 3. STACK PATTERNS (Day 4)
// ============================================================

/// LeetCode #155: Min Stack
/// Design a stack that supports push, pop, top, and retrieving minimum in O(1).
/// 
/// Time: O(1) for all operations, Space: O(n)
/// Pattern: Two stacks - main stack and min stack
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
    
    fn pop(&mut self) {
        if let Some(val) = self.stack.pop() {
            if self.min_stack.last() == Some(&val) {
                self.min_stack.pop();
            }
        }
    }
    
    fn top(&self) -> Option<i32> {
        self.stack.last().copied()
    }
    
    fn get_min(&self) -> Option<i32> {
        self.min_stack.last().copied()
    }
}

/// LeetCode #150: Evaluate Reverse Polish Notation
/// Evaluate arithmetic expression in RPN.
/// 
/// Time: O(n), Space: O(n)
/// Pattern: Stack-based evaluation
fn eval_rpn(tokens: Vec<String>) -> i32 {
    let mut stack = Vec::new();
    
    for token in tokens {
        match token.as_str() {
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
                stack.push(a / b);  // Integer division truncates toward zero
            }
            _ => {
                stack.push(token.parse().unwrap());
            }
        }
    }
    
    stack[0]
}

/// LeetCode #739: Daily Temperatures
/// For each day, find how many days until warmer temperature.
/// 
/// Time: O(n), Space: O(n)
/// Pattern: Monotonic decreasing stack
fn daily_temperatures(temperatures: Vec<i32>) -> Vec<i32> {
    let n = temperatures.len();
    let mut result = vec![0; n];
    let mut stack: Vec<usize> = Vec::new();  // Store indices
    
    for i in 0..n {
        while !stack.is_empty() && temperatures[i] > temperatures[*stack.last().unwrap()] {
            let idx = stack.pop().unwrap();
            result[idx] = (i - idx) as i32;
        }
        stack.push(i);
    }
    
    result
}

// ============================================================
// 4. LINKED LIST PATTERNS (Day 5)
// ============================================================

// Definition for singly-linked list.
#[derive(PartialEq, Eq, Clone, Debug)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    #[inline]
    fn new(val: i32) -> Self {
        ListNode { next: None, val }
    }
}

/// LeetCode #876: Middle of the Linked List
/// Find the middle node of a linked list.
/// 
/// Time: O(n), Space: O(1)
/// Pattern: Fast-slow pointers
fn middle_node(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut slow = &head;
    let mut fast = &head;
    
    while let Some(ref node) = fast {
        if let Some(ref next) = node.next {
            fast = &next.next;
            slow = &slow.as_ref().unwrap().next;
        } else {
            break;
        }
    }
    
    slow.cloned()
}

/// LeetCode #21: Merge Two Sorted Lists
/// Merge two sorted linked lists into one sorted list.
/// 
/// Time: O(n + m), Space: O(1)
/// Pattern: Dummy node + iterative merge
fn merge_two_lists(
    l1: Option<Box<ListNode>>,
    l2: Option<Box<ListNode>>,
) -> Option<Box<ListNode>> {
    let mut dummy = Box::new(ListNode::new(0));
    let mut curr = &mut dummy;
    let mut list1 = l1;
    let mut list2 = l2;
    
    while list1.is_some() && list2.is_some() {
        let val1 = list1.as_ref().unwrap().val;
        let val2 = list2.as_ref().unwrap().val;
        
        if val1 < val2 {
            curr.next = list1.take();
            list1 = curr.next.as_mut().unwrap().next.take();
        } else {
            curr.next = list2.take();
            list2 = curr.next.as_mut().unwrap().next.take();
        }
        curr = curr.next.as_mut().unwrap();
    }
    
    curr.next = list1.or(list2);
    dummy.next
}

/// LeetCode #206: Reverse Linked List
/// Reverse a linked list iteratively.
/// 
/// Time: O(n), Space: O(1)
/// Pattern: Iterative reversal
fn reverse_list(head: Option<Box<ListNode>>) -> Option<Box<ListNode>> {
    let mut prev = None;
    let mut curr = head;
    
    while let Some(mut node) = curr {
        curr = node.next.take();
        node.next = prev;
        prev = Some(node);
    }
    
    prev
}

// ============================================================
// 5. TREE PATTERNS (Day 6)
// ============================================================

// Definition for a binary tree node.
#[derive(Debug, PartialEq, Eq)]
pub struct TreeNode {
    pub val: i32,
    pub left: Option<Rc<RefCell<TreeNode>>>,
    pub right: Option<Rc<RefCell<TreeNode>>>,
}

impl TreeNode {
    #[inline]
    pub fn new(val: i32) -> Self {
        TreeNode {
            val,
            left: None,
            right: None,
        }
    }
}

/// LeetCode #102: Binary Tree Level Order Traversal
/// Return level-order traversal of binary tree.
/// 
/// Time: O(n), Space: O(w) where w is max width
/// Pattern: BFS with queue
fn level_order(root: Option<Rc<RefCell<TreeNode>>>) -> Vec<Vec<i32>> {
    let mut result = Vec::new();
    
    if let Some(node) = root {
        let mut queue = VecDeque::new();
        queue.push_back(node);
        
        while !queue.is_empty() {
            let level_size = queue.len();
            let mut current_level = Vec::new();
            
            for _ in 0..level_size {
                if let Some(node) = queue.pop_front() {
                    let borrowed = node.borrow();
                    current_level.push(borrowed.val);
                    
                    if let Some(left) = borrowed.left.clone() {
                        queue.push_back(left);
                    }
                    if let Some(right) = borrowed.right.clone() {
                        queue.push_back(right);
                    }
                }
            }
            
            result.push(current_level);
        }
    }
    
    result
}

/// LeetCode #104: Maximum Depth of Binary Tree
/// Calculate the maximum depth of binary tree.
/// 
/// Time: O(n), Space: O(h)
/// Pattern: DFS with recursion
fn max_depth(root: Option<Rc<RefCell<TreeNode>>>) -> i32 {
    if let Some(node) = root {
        let borrowed = node.borrow();
        1 + max_depth(borrowed.left.clone()).max(max_depth(borrowed.right.clone()))
    } else {
        0
    }
}

/// LeetCode #98: Validate Binary Search Tree
/// Validate if a binary tree is a valid BST.
/// 
/// Time: O(n), Space: O(h)
/// Pattern: DFS with range validation
fn is_valid_bst(root: Option<Rc<RefCell<TreeNode>>>) -> bool {
    fn validate(node: Option<Rc<RefCell<TreeNode>>>, low: i64, high: i64) -> bool {
        if let Some(n) = node {
            let borrowed = n.borrow();
            let val = borrowed.val as i64;
            
            if val <= low || val >= high {
                return false;
            }
            
            validate(borrowed.left.clone(), low, val) &&
            validate(borrowed.right.clone(), val, high)
        } else {
            true
        }
    }
    
    validate(root, i64::MIN, i64::MAX)
}

/// LeetCode #543: Diameter of Binary Tree
/// Calculate the diameter (longest path between any two nodes).
/// 
/// Time: O(n), Space: O(h)
/// Pattern: DFS with height and diameter tracking
fn diameter_of_binary_tree(root: Option<Rc<RefCell<TreeNode>>>) -> i32 {
    use std::cell::Cell;
    
    fn height(node: Option<Rc<RefCell<TreeNode>>>, diameter: &Cell<i32>) -> i32 {
        if let Some(n) = node {
            let borrowed = n.borrow();
            let left_h = height(borrowed.left.clone(), diameter);
            let right_h = height(borrowed.right.clone(), diameter);
            
            // Update diameter
            diameter.set(diameter.get().max(left_h + right_h));
            
            1 + left_h.max(right_h)
        } else {
            0
        }
    }
    
    let diameter = Cell::new(0);
    height(root, &diameter);
    diameter.get()
}

// ============================================================
// TESTING
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_two_sum() {
        assert_eq!(two_sum(vec![2, 7, 11, 15], 9), vec![0, 1]);
        assert_eq!(two_sum(vec![3, 2, 4], 6), vec![1, 2]);
    }
    
    #[test]
    fn test_container_with_most_water() {
        assert_eq!(container_with_most_water(vec![1, 8, 6, 2, 5, 4, 8, 3, 7]), 49);
        assert_eq!(container_with_most_water(vec![1, 1]), 1);
    }
    
    #[test]
    fn test_group_anagrams() {
        let strs = vec![
            "eat".to_string(),
            "tea".to_string(),
            "tan".to_string(),
            "ate".to_string(),
            "nat".to_string(),
            "bat".to_string(),
        ];
        let result = group_anagrams(strs);
        assert_eq!(result.len(), 3);
    }
    
    #[test]
    fn test_longest_substring_without_repeating() {
        assert_eq!(longest_substring_without_repeating("abcabcbb".to_string()), 3);
        assert_eq!(longest_substring_without_repeating("bbbbb".to_string()), 1);
        assert_eq!(longest_substring_without_repeating("pwwkew".to_string()), 3);
    }
    
    #[test]
    fn test_longest_palindromic_substring() {
        let result = longest_palindromic_substring("babad".to_string());
        assert!(result == "bab" || result == "aba");
        
        let result = longest_palindromic_substring("cbbd".to_string());
        assert_eq!(result, "bb");
    }
    
    #[test]
    fn test_str_str() {
        assert_eq!(str_str("hello".to_string(), "ll".to_string()), 2);
        assert_eq!(str_str("aaaaa".to_string(), "bba".to_string()), -1);
        assert_eq!(str_str("".to_string(), "".to_string()), 0);
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
        assert_eq!(
            eval_rpn(vec!["2".to_string(), "1".to_string(), "+".to_string(), "3".to_string(), "*".to_string()]),
            9
        );
        assert_eq!(
            eval_rpn(vec!["4".to_string(), "13".to_string(), "5".to_string(), "/".to_string(), "+".to_string()]),
            6
        );
    }
    
    #[test]
    fn test_daily_temperatures() {
        assert_eq!(
            daily_temperatures(vec![73, 74, 75, 71, 69, 72, 76, 73]),
            vec![1, 1, 4, 2, 1, 1, 0, 0]
        );
    }
    
    #[test]
    fn test_merge_two_lists() {
        let l1 = Some(Box::new(ListNode {
            val: 1,
            next: Some(Box::new(ListNode {
                val: 3,
                next: Some(Box::new(ListNode::new(5))),
            })),
        }));
        
        let l2 = Some(Box::new(ListNode {
            val: 2,
            next: Some(Box::new(ListNode {
                val: 4,
                next: Some(Box::new(ListNode::new(6))),
            })),
        }));
        
        let merged = merge_two_lists(l1, l2);
        
        let result: Vec<i32> = {
            let mut vals = Vec::new();
            let mut curr = &merged;
            while let Some(node) = curr {
                vals.push(node.val);
                curr = &node.next;
            }
            vals
        };
        
        assert_eq!(result, vec![1, 2, 3, 4, 5, 6]);
    }
    
    #[test]
    fn test_reverse_list() {
        let head = Some(Box::new(ListNode {
            val: 1,
            next: Some(Box::new(ListNode {
                val: 2,
                next: Some(Box::new(ListNode::new(3))),
            })),
        }));
        
        let reversed = reverse_list(head);
        
        let result: Vec<i32> = {
            let mut vals = Vec::new();
            let mut curr = &reversed;
            while let Some(node) = curr {
                vals.push(node.val);
                curr = &node.next;
            }
            vals
        };
        
        assert_eq!(result, vec![3, 2, 1]);
    }
    
    #[test]
    fn test_level_order() {
        // Create tree:
        //       3
        //      / \
        //     9  20
        //        / \
        //       15  7
        let root = Rc::new(RefCell::new(TreeNode::new(3)));
        let node9 = Rc::new(RefCell::new(TreeNode::new(9)));
        let node20 = Rc::new(RefCell::new(TreeNode::new(20)));
        let node15 = Rc::new(RefCell::new(TreeNode::new(15)));
        let node7 = Rc::new(RefCell::new(TreeNode::new(7)));
        
        root.borrow_mut().left = Some(node9);
        root.borrow_mut().right = Some(node20);
        node20.borrow_mut().left = Some(node15);
        node20.borrow_mut().right = Some(node7);
        
        let result = level_order(Some(root));
        assert_eq!(result, vec![vec![3], vec![9, 20], vec![15, 7]]);
    }
    
    #[test]
    fn test_max_depth() {
        // Create tree:
        //       3
        //      / \
        //     9  20
        //        / \
        //       15  7
        let root = Rc::new(RefCell::new(TreeNode::new(3)));
        let node9 = Rc::new(RefCell::new(TreeNode::new(9)));
        let node20 = Rc::new(RefCell::new(TreeNode::new(20)));
        let node15 = Rc::new(RefCell::new(TreeNode::new(15)));
        let node7 = Rc::new(RefCell::new(TreeNode::new(7)));
        
        root.borrow_mut().left = Some(node9);
        root.borrow_mut().right = Some(node20);
        node20.borrow_mut().left = Some(node15);
        node20.borrow_mut().right = Some(node7);
        
        assert_eq!(max_depth(Some(root)), 3);
    }
    
    #[test]
    fn test_is_valid_bst() {
        // Create valid BST:
        //       2
        //      / \
        //     1   3
        let root = Rc::new(RefCell::new(TreeNode::new(2)));
        let node1 = Rc::new(RefCell::new(TreeNode::new(1)));
        let node3 = Rc::new(RefCell::new(TreeNode::new(3)));
        
        root.borrow_mut().left = Some(node1);
        root.borrow_mut().right = Some(node3);
        
        assert!(is_valid_bst(Some(root)));
    }
    
    #[test]
    fn test_diameter_of_binary_tree() {
        // Create tree:
        //       1
        //      / \
        //     2   3
        //    / \
        //   4   5
        let root = Rc::new(RefCell::new(TreeNode::new(1)));
        let node2 = Rc::new(RefCell::new(TreeNode::new(2)));
        let node3 = Rc::new(RefCell::new(TreeNode::new(3)));
        let node4 = Rc::new(RefCell::new(TreeNode::new(4)));
        let node5 = Rc::new(RefCell::new(TreeNode::new(5)));
        
        root.borrow_mut().left = Some(node2);
        root.borrow_mut().right = Some(node3);
        node2.borrow_mut().left = Some(node4);
        node2.borrow_mut().right = Some(node5);
        
        assert_eq!(diameter_of_binary_tree(Some(root)), 3);
    }
}

fn main() {
    println!("Day 7: Review & Practice - Rust Implementations");
    println!("Run 'cargo test' to verify all implementations");
}
