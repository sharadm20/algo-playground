// Day 10: Comprehensive Review & Practice
// Topics: Mixed problem sets, pattern recognition, complexity analysis

use std::collections::{HashMap, HashSet, VecDeque, BinaryHeap};
use std::cmp::Reverse;

// ============================================================================
// PATTERN 1: Arrays & Hashing - Two Sum
// ============================================================================
fn two_sum(nums: &[i32], target: i32) -> Vec<usize> {
    let mut seen = HashMap::new();
    for (i, &num) in nums.iter().enumerate() {
        let complement = target - num;
        if let Some(&prev_idx) = seen.get(&complement) {
            return vec![prev_idx, i];
        }
        seen.insert(num, i);
    }
    vec![]
}

fn three_sum(mut nums: Vec<i32>) -> Vec<Vec<i32>> {
    nums.sort();
    let mut result = Vec::new();
    let n = nums.len();
    
    for i in 0..n.saturating_sub(2) {
        if i > 0 && nums[i] == nums[i - 1] {
            continue;
        }
        
        let mut left = i + 1;
        let mut right = n - 1;
        
        while left < right {
            let total = nums[i] + nums[left] + nums[right];
            
            if total == 0 {
                result.push(vec![nums[i], nums[left], nums[right]]);
                while left < right && nums[left] == nums[left + 1] {
                    left += 1;
                }
                while left < right && nums[right] == nums[right - 1] {
                    right -= 1;
                }
                left += 1;
                right -= 1;
            } else if total < 0 {
                left += 1;
            } else {
                right -= 1;
            }
        }
    }
    
    result
}

fn max_area(height: &[i32]) -> i32 {
    let mut left = 0;
    let mut right = height.len() - 1;
    let mut max_area = 0;
    
    while left < right {
        let width = (right - left) as i32;
        let h = height[left].min(height[right]);
        max_area = max_area.max(width * h);
        
        if height[left] < height[right] {
            left += 1;
        } else {
            right -= 1;
        }
    }
    
    max_area
}

fn group_anagrams(strs: &[String]) -> Vec<Vec<String>> {
    let mut anagram_groups: HashMap<String, Vec<String>> = HashMap::new();
    
    for s in strs {
        let mut key = s.clone();
        let mut chars: Vec<char> = key.chars().collect();
        chars.sort_unstable();
        key = chars.into_iter().collect();
        anagram_groups.entry(key).or_insert_with(Vec::new).push(s.clone());
    }
    
    anagram_groups.into_values().collect()
}

// ============================================================================
// PATTERN 2: String Manipulation
// ============================================================================
fn length_of_longest_substring(s: &str) -> usize {
    let chars: Vec<char> = s.chars().collect();
    let mut char_set = HashSet::new();
    let mut left = 0;
    let mut max_length = 0;
    
    for right in 0..chars.len() {
        while char_set.contains(&chars[right]) {
            char_set.remove(&chars[left]);
            left += 1;
        }
        char_set.insert(chars[right]);
        max_length = max_length.max(right - left + 1);
    }
    
    max_length
}

fn count_palindromic_substrings(s: &str) -> usize {
    let chars: Vec<char> = s.chars().collect();
    let mut count = 0;
    
    fn expand(chars: &[char], left: usize, right: usize, count: &mut usize) {
        let mut l = left;
        let mut r = right;
        while l < chars.len() && r < chars.len() && chars[l] == chars[r] {
            *count += 1;
            if l == 0 { break; }
            l -= 1;
            r += 1;
        }
    }
    
    for i in 0..chars.len() {
        expand(&chars, i, i, &mut count);
        if i + 1 < chars.len() {
            expand(&chars, i, i + 1, &mut count);
        }
    }
    
    count
}

fn str_str(haystack: &str, needle: &str) -> i32 {
    if needle.is_empty() {
        return 0;
    }
    if needle.len() > haystack.len() {
        return -1;
    }
    
    for i in 0..=(haystack.len() - needle.len()) {
        if &haystack[i..i + needle.len()] == needle {
            return i as i32;
        }
    }
    
    -1
}

// ============================================================================
// PATTERN 3: Stack & Queue
// ============================================================================
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
            if Some(&val) == self.min_stack.last() {
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
                stack.push(a / b);
            }
            _ => {
                stack.push(token.parse().unwrap());
            }
        }
    }
    
    stack[0]
}

fn daily_temperatures(temperatures: &[i32]) -> Vec<i32> {
    let mut result = vec![0; temperatures.len()];
    let mut stack: Vec<usize> = Vec::new();
    
    for (i, &temp) in temperatures.iter().enumerate() {
        while let Some(&prev_idx) = stack.last() {
            if temperatures[prev_idx] < temp {
                stack.pop();
                result[prev_idx] = (i - prev_idx) as i32;
            } else {
                break;
            }
        }
        stack.push(i);
    }
    
    result
}

// ============================================================================
// PATTERN 4: Linked List
// ============================================================================
#[derive(PartialEq, Eq, Clone, Debug)]
struct ListNode {
    val: i32,
    next: Option<Box<ListNode>>,
}

impl ListNode {
    fn new(val: i32) -> Self {
        ListNode { val, next: None }
    }
}

fn merge_two_lists(
    l1: Option<Box<ListNode>>,
    l2: Option<Box<ListNode>>,
) -> Option<Box<ListNode>> {
    match (l1, l2) {
        (None, None) => None,
        (Some(node), None) | (None, Some(node)) => Some(node),
        (Some(mut n1), Some(mut n2)) => {
            if n1.val < n2.val {
                n1.next = merge_two_lists(n1.next, Some(n2));
                Some(n1)
            } else {
                n2.next = merge_two_lists(Some(n1), n2.next);
                Some(n2)
            }
        }
    }
}

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

// ============================================================================
// PATTERN 5: Trees
// ============================================================================
#[derive(Debug, PartialEq, Eq, Clone)]
struct TreeNode {
    val: i32,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

impl TreeNode {
    fn new(val: i32) -> Self {
        TreeNode { val, left: None, right: None }
    }
}

fn max_depth(root: Option<Box<TreeNode>>) -> i32 {
    match root {
        None => 0,
        Some(node) => 1 + max_depth(node.left).max(max_depth(node.right)),
    }
}

fn is_valid_bst(root: Option<Box<TreeNode>>) -> bool {
    fn validate(node: Option<&Box<TreeNode>>, low: i64, high: i64) -> bool {
        match node {
            None => true,
            Some(n) => {
                let val = n.val as i64;
                val > low && val < high
                    && validate(n.left.as_ref(), low, val)
                    && validate(n.right.as_ref(), val, high)
            }
        }
    }
    
    validate(root.as_ref(), i64::MIN, i64::MAX)
}

// ============================================================================
// PATTERN 6: Graphs
// ============================================================================
fn graph_bfs(graph: &HashMap<usize, Vec<usize>>, start: usize) -> Vec<usize> {
    let mut visited = HashSet::new();
    let mut result = Vec::new();
    let mut queue = VecDeque::new();
    
    queue.push_back(start);
    visited.insert(start);
    
    while let Some(node) = queue.pop_front() {
        result.push(node);
        
        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if visited.insert(neighbor) {
                    queue.push_back(neighbor);
                }
            }
        }
    }
    
    result
}

fn dijkstra(graph: &HashMap<usize, Vec<(usize, i32)>>, start: usize) -> HashMap<usize, i32> {
    let mut distances = HashMap::new();
    
    for &node in graph.keys() {
        distances.insert(node, i32::MAX);
    }
    distances.insert(start, 0);
    
    let mut pq = BinaryHeap::new();
    pq.push(Reverse((0, start)));
    
    while let Some(Reverse((dist, node))) = pq.pop() {
        if dist > distances[&node] {
            continue;
        }
        
        if let Some(neighbors) = graph.get(&node) {
            for &(neighbor, weight) in neighbors {
                let new_dist = dist + weight;
                if new_dist < distances[&neighbor] {
                    distances.insert(neighbor, new_dist);
                    pq.push(Reverse((new_dist, neighbor)));
                }
            }
        }
    }
    
    distances
}

// ============================================================================
// TESTS
// ============================================================================
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_two_sum() {
        assert_eq!(two_sum(&[2, 7, 11, 15], 9), vec![0, 1]);
        assert_eq!(two_sum(&[3, 2, 4], 6), vec![1, 2]);
    }

    #[test]
    fn test_three_sum() {
        let result = three_sum(vec![-1, 0, 1, 2, -1, -4]);
        assert_eq!(result.len(), 2);
    }

    #[test]
    fn test_max_area() {
        assert_eq!(max_area(&[1, 8, 6, 2, 5, 4, 8, 3, 7]), 49);
    }

    #[test]
    fn test_group_anagrams() {
        let strs = vec!["eat".to_string(), "tea".to_string(), "tan".to_string(),
                        "ate".to_string(), "nat".to_string(), "bat".to_string()];
        let result = group_anagrams(&strs);
        assert_eq!(result.len(), 3);
    }

    #[test]
    fn test_length_of_longest_substring() {
        assert_eq!(length_of_longest_substring("abcabcbb"), 3);
        assert_eq!(length_of_longest_substring("bbbbb"), 1);
    }

    #[test]
    fn test_str_str() {
        assert_eq!(str_str("hello", "ll"), 2);
        assert_eq!(str_str("aaaaa", "bba"), -1);
        assert_eq!(str_str("", ""), 0);
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
    fn test_daily_temperatures() {
        let temps = vec![73, 74, 75, 71, 69, 72, 76, 73];
        let result = daily_temperatures(&temps);
        assert_eq!(result, vec![1, 1, 4, 2, 1, 1, 0, 0]);
    }

    #[test]
    fn test_reverse_list() {
        let mut head = Some(Box::new(ListNode::new(1)));
        head.as_mut().unwrap().next = Some(Box::new(ListNode::new(2)));
        head.as_mut().unwrap().next.as_mut().unwrap().next = Some(Box::new(ListNode::new(3)));
        
        let reversed = reverse_list(head);
        assert_eq!(reversed.as_ref().unwrap().val, 3);
        assert_eq!(reversed.as_ref().unwrap().next.as_ref().unwrap().val, 2);
    }

    #[test]
    fn test_max_depth() {
        let root = Some(Box::new(TreeNode {
            val: 3,
            left: Some(Box::new(TreeNode::new(9))),
            right: Some(Box::new(TreeNode {
                val: 20,
                left: Some(Box::new(TreeNode::new(15))),
                right: Some(Box::new(TreeNode::new(7))),
            })),
        }));
        
        assert_eq!(max_depth(root), 3);
    }

    #[test]
    fn test_is_valid_bst() {
        let root = Some(Box::new(TreeNode {
            val: 2,
            left: Some(Box::new(TreeNode::new(1))),
            right: Some(Box::new(TreeNode::new(3))),
        }));
        
        assert!(is_valid_bst(root));
    }

    #[test]
    fn test_graph_bfs() {
        let mut graph = HashMap::new();
        graph.insert(0, vec![1, 2]);
        graph.insert(1, vec![2]);
        graph.insert(2, vec![0, 3]);
        graph.insert(3, vec![3]);
        
        let result = graph_bfs(&graph, 2);
        assert_eq!(result.len(), 4);
    }

    #[test]
    fn test_dijkstra() {
        let mut graph = HashMap::new();
        graph.insert(0, vec![(1, 4), (2, 1)]);
        graph.insert(1, vec![(3, 1)]);
        graph.insert(2, vec![(1, 2), (3, 5)]);
        graph.insert(3, vec![]);
        
        let distances = dijkstra(&graph, 0);
        assert_eq!(distances[&0], 0);
        assert_eq!(distances[&1], 3);
        assert_eq!(distances[&2], 1);
        assert_eq!(distances[&3], 4);
    }
}
