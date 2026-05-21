/// Day 15: Heaps, Tries, & Bit Manipulation
/// Topics: Priority queues, prefix trees, bitwise operations

use std::collections::{BinaryHeap, HashMap};
use std::cmp::Reverse;

// ============================================================================
// PATTERN 1: Heaps & Priority Queues
// ============================================================================

/// Top K Frequent Elements - O(n log k) time, O(n) space
/// Pattern: Min-heap to track top k frequent elements
fn top_k_frequent(nums: Vec<i32>, k: i32) -> Vec<i32> {
    let mut freq_map = HashMap::new();
    for num in &nums {
        *freq_map.entry(*num).or_insert(0) += 1;
    }
    
    // Min-heap (using Reverse for min-heap behavior)
    let mut heap: BinaryHeap<Reverse<(i32, i32)>> = BinaryHeap::new();
    
    for (num, count) in freq_map {
        heap.push(Reverse((count, num)));
        if heap.len() > k as usize {
            heap.pop();
        }
    }
    
    heap.into_iter().map(|Reverse((_, num))| num).collect()
}

/// Kth Largest Element in Array - O(n log k) time, O(k) space
/// Pattern: Min-heap to maintain k largest elements
fn kth_largest(nums: Vec<i32>, k: i32) -> i32 {
    let mut heap: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    
    for num in nums {
        heap.push(Reverse(num));
        if heap.len() > k as usize {
            heap.pop();
        }
    }
    
    heap.into_iter().next().map(|Reverse(v)| v).unwrap()
}

/// Merge K Sorted Lists - O(n log k) time, O(n) space
/// Pattern: Min-heap to merge k sorted arrays
fn merge_k_sorted_lists(lists: Vec<Vec<i32>>) -> Vec<i32> {
    if lists.is_empty() {
        return vec![];
    }
    
    // Min-heap: (value, list_index, element_index)
    let mut heap: BinaryHeap<Reverse<(i32, usize, usize)>> = BinaryHeap::new();
    
    // Push first element of each list
    for (i, lst) in lists.iter().enumerate() {
        if !lst.is_empty() {
            heap.push(Reverse((lst[0], i, 0)));
        }
    }
    
    let mut result = Vec::new();
    
    while let Some(Reverse((val, list_idx, elem_idx))) = heap.pop() {
        result.push(val);
        
        // Push next element from same list
        if elem_idx + 1 < lists[list_idx].len() {
            let next_val = lists[list_idx][elem_idx + 1];
            heap.push(Reverse((next_val, list_idx, elem_idx + 1)));
        }
    }
    
    result
}

// ============================================================================
// PATTERN 2: Trie (Prefix Tree)
// ============================================================================

#[derive(Debug, Clone)]
struct TrieNode {
    children: HashMap<char, TrieNode>,
    is_end_of_word: bool,
}

impl TrieNode {
    fn new() -> Self {
        TrieNode {
            children: HashMap::new(),
            is_end_of_word: false,
        }
    }
}

#[derive(Debug, Clone)]
struct Trie {
    root: TrieNode,
}

impl Trie {
    fn new() -> Self {
        Trie {
            root: TrieNode::new(),
        }
    }
    
    /// Insert a word into the trie
    fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;
        for ch in word.chars() {
            node = node.children.entry(ch).or_insert_with(TrieNode::new);
        }
        node.is_end_of_word = true;
    }
    
    /// Search for a complete word in the trie
    fn search(&self, word: &str) -> bool {
        let mut node = &self.root;
        for ch in word.chars() {
            if let Some(child) = node.children.get(&ch) {
                node = child;
            } else {
                return false;
            }
        }
        node.is_end_of_word
    }
    
    /// Check if any word in trie starts with the given prefix
    fn starts_with(&self, prefix: &str) -> bool {
        let mut node = &self.root;
        for ch in prefix.chars() {
            if let Some(child) = node.children.get(&ch) {
                node = child;
            } else {
                return false;
            }
        }
        true
    }
    
    /// Get all words with given prefix
    fn autocomplete(&self, prefix: &str) -> Vec<String> {
        let mut node = &self.root;
        for ch in prefix.chars() {
            if let Some(child) = node.children.get(&ch) {
                node = child;
            } else {
                return vec![];
            }
        }
        
        let mut result = Vec::new();
        Self::dfs(node, prefix.to_string(), &mut result);
        result
    }
    
    fn dfs(node: &TrieNode, current_word: String, result: &mut Vec<String>) {
        if node.is_end_of_word {
            result.push(current_word.clone());
        }
        
        for (ch, child_node) in &node.children {
            let mut new_word = current_word.clone();
            new_word.push(*ch);
            Self::dfs(child_node, new_word, result);
        }
    }
}

/// Longest Common Prefix using Trie - O(S) time where S is sum of all characters
/// Pattern: Trie traversal to find shared prefix
fn longest_common_prefix(strs: Vec<String>) -> String {
    if strs.is_empty() {
        return String::new();
    }
    
    let mut trie = Trie::new();
    for word in &strs {
        trie.insert(word);
    }
    
    let mut prefix = String::new();
    let mut node = &trie.root;
    
    while node.children.len() == 1 && !node.is_end_of_word {
        if let (ch, child_node) = node.children.iter().next().unwrap() {
            prefix.push(*ch);
            node = child_node;
        } else {
            break;
        }
    }
    
    prefix
}

// ============================================================================
// PATTERN 3: Bit Manipulation
// ============================================================================

/// Single Number - O(n) time, O(1) space
/// Pattern: XOR cancels duplicates: n ^ n = 0, n ^ 0 = n
fn single_number(nums: Vec<i32>) -> i32 {
    let mut result = 0;
    for num in nums {
        result ^= num;
    }
    result
}

/// Number of 1 Bits (Hamming Weight) - O(log n) time, O(1) space
/// Pattern: n & (n-1) clears the lowest set bit
fn number_of_1_bits(mut n: i32) -> i32 {
    let mut count = 0;
    while n != 0 {
        n &= n - 1;
        count += 1;
    }
    count
}

/// Counting Bits - O(n) time, O(n) space
/// Pattern: DP with bit manipulation
/// bits[i] = bits[i >> 1] + (i & 1)
fn counting_bits(n: i32) -> Vec<i32> {
    let mut bits = vec![0; (n + 1) as usize];
    for i in 1..=n as usize {
        bits[i] = bits[i >> 1] + (i as i32 & 1);
    }
    bits
}

/// Power of Two - O(1) time, O(1) space
/// Pattern: n & (n-1) clears lowest set bit, powers of 2 have only 1 bit set
fn is_power_of_two(n: i32) -> bool {
    n > 0 && (n & (n - 1)) == 0
}

/// Reverse Bits - O(1) time (32 iterations), O(1) space
/// Pattern: Bit extraction and reconstruction
fn reverse_bits(mut n: u32) -> u32 {
    let mut result: u32 = 0;
    for i in 0..32 {
        let bit = (n >> i) & 1;
        result |= bit << (31 - i);
    }
    result
}

/// Get the ith bit of num
fn get_bit(num: i32, i: i32) -> i32 {
    (num >> i) & 1
}

/// Set the ith bit of num to 1
fn set_bit(num: i32, i: i32) -> i32 {
    num | (1 << i)
}

/// Clear the ith bit of num
fn clear_bit(num: i32, i: i32) -> i32 {
    num & !(1 << i)
}

/// Toggle the ith bit of num
fn toggle_bit(num: i32, i: i32) -> i32 {
    num ^ (1 << i)
}

// ============================================================================
// TESTS
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_top_k_frequent() {
        let mut result = top_k_frequent(vec![1, 1, 1, 2, 2, 3], 2);
        result.sort();
        assert_eq!(result, vec![1, 2]);
        
        assert_eq!(top_k_frequent(vec![1], 1), vec![1]);
        
        let mut result2 = top_k_frequent(vec![4, 1, -1, 2, -1, 2, 3], 2);
        result2.sort();
        assert_eq!(result2, vec![-1, 2]);
    }

    #[test]
    fn test_kth_largest() {
        assert_eq!(kth_largest(vec![3, 2, 1, 5, 6, 4], 2), 5);
        assert_eq!(kth_largest(vec![3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4);
    }

    #[test]
    fn test_merge_k_sorted_lists() {
        let lists = vec![vec![1, 4, 5], vec![1, 3, 4], vec![2, 6]];
        assert_eq!(merge_k_sorted_lists(lists), vec![1, 1, 2, 3, 4, 4, 5, 6]);
        
        assert_eq!(merge_k_sorted_lists(vec![]), vec![] as Vec<i32>);
    }

    #[test]
    fn test_trie_operations() {
        let mut trie = Trie::new();
        trie.insert("apple");
        
        assert_eq!(trie.search("apple"), true);
        assert_eq!(trie.search("app"), false);
        assert_eq!(trie.starts_with("app"), true);
        
        trie.insert("app");
        assert_eq!(trie.search("app"), true);
    }

    #[test]
    fn test_longest_common_prefix() {
        assert_eq!(
            longest_common_prefix(vec!["flower".to_string(), "flow".to_string(), "flight".to_string()]),
            "fl"
        );
        assert_eq!(
            longest_common_prefix(vec!["dog".to_string(), "racecar".to_string(), "car".to_string()]),
            ""
        );
        assert_eq!(
            longest_common_prefix(vec![
                "interspecies".to_string(),
                "interstellar".to_string(),
                "interstate".to_string()
            ]),
            "inters"
        );
    }

    #[test]
    fn test_single_number() {
        assert_eq!(single_number(vec![2, 2, 1]), 1);
        assert_eq!(single_number(vec![4, 1, 2, 1, 2]), 4);
        assert_eq!(single_number(vec![1]), 1);
    }

    #[test]
    fn test_number_of_1_bits() {
        assert_eq!(number_of_1_bits(11), 3); // 1011 in binary
        assert_eq!(number_of_1_bits(128), 1); // 10000000
        assert_eq!(number_of_1_bits(0), 0);
    }

    #[test]
    fn test_counting_bits() {
        assert_eq!(counting_bits(5), vec![0, 1, 1, 2, 1, 2]);
        assert_eq!(counting_bits(0), vec![0]);
        assert_eq!(counting_bits(2), vec![0, 1, 1]);
    }

    #[test]
    fn test_is_power_of_two() {
        assert_eq!(is_power_of_two(1), true);
        assert_eq!(is_power_of_two(16), true);
        assert_eq!(is_power_of_two(3), false);
        assert_eq!(is_power_of_two(0), false);
    }

    #[test]
    fn test_reverse_bits() {
        assert_eq!(reverse_bits(1), 2147483648);
        assert_eq!(reverse_bits(43261596), 964176192);
    }

    #[test]
    fn test_bit_operations() {
        assert_eq!(get_bit(5, 0), 1); // 101
        assert_eq!(get_bit(5, 1), 0);
        assert_eq!(get_bit(5, 2), 1);
        assert_eq!(set_bit(5, 1), 7); // 101 -> 111
        assert_eq!(clear_bit(5, 2), 1); // 101 -> 001
        assert_eq!(toggle_bit(5, 1), 7); // 101 -> 111
    }
}

fn main() {
    println!("Day 15: Heaps, Tries, & Bit Manipulation");
    println!("Run 'cargo test' to execute all tests.");
}
