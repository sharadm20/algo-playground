//! Day 3: String Manipulation and Algorithms
//! ==========================================
//! Topics Covered:
//! 1. Palindrome Patterns
//! 2. String Matching Algorithms
//! 3. Sliding Window on Strings
//! 4. Trie (Prefix Tree) Structures
//!
//! Each section includes:
//! - Concept explanation
//! - Implementation template
//! - Practice problems with solutions

// ============================================================================
// 1. PALINDROME PATTERNS
// ============================================================================

/// Palindrome patterns:
///
/// Pattern 1: Expand Around Center
/// - Used for: Finding palindromic substrings
/// - Time: O(n²), Space: O(1)
///
/// Pattern 2: Two-Pointer Validation
/// - Used for: Checking if string is palindrome
/// - Time: O(n), Space: O(1)
///
/// Pattern 3: Dynamic Programming
/// - Used for: Counting all palindromic substrings
/// - Time: O(n²), Space: O(n²)

/// Problem: Check if a string is a palindrome (ignoring case and non-alphanumeric).
///
/// Example: s = "A man, a plan, a canal: Panama" → True
///          s = "race a car" → False
///
/// Approach: Two-pointer validation
/// - Left starts at beginning, right at end
/// - Skip non-alphanumeric characters
/// - Compare characters (case-insensitive)
fn is_palindrome(s: &str) -> bool {
    let chars: Vec<char> = s.chars().collect();
    let mut left = 0;
    let mut right = chars.len().saturating_sub(1);

    while left < right {
        // Skip non-alphanumeric from left
        while left < right && !chars[left].is_alphanumeric() {
            left += 1;
        }
        // Skip non-alphanumeric from right
        while left < right && !chars[right].is_alphanumeric() {
            right = right.saturating_sub(1);
        }

        if chars[left].to_ascii_lowercase() != chars[right].to_ascii_lowercase() {
            return false;
        }

        left += 1;
        if right > 0 {
            right -= 1;
        }
    }

    true
}

/// Problem: Find the longest palindromic substring.
///
/// Example: s = "babad" → "bab" or "aba"
///          s = "cbbd" → "bb"
///
/// Approach: Expand around center
/// - Each character (and gap) can be center of palindrome
/// - Expand outward while characters match
/// - Track longest palindrome found
fn longest_palindromic_substring(s: &str) -> String {
    if s.is_empty() {
        return String::new();
    }

    let chars: Vec<char> = s.chars().collect();
    let mut start = 0;
    let mut end = 0;

    fn expand_around_center(chars: &[char], mut left: i32, mut right: i32) -> (i32, i32) {
        while left >= 0 && right < chars.len() as i32 && chars[left as usize] == chars[right as usize] {
            left -= 1;
            right += 1;
        }
        (left + 1, right - 1)
    }

    for i in 0..chars.len() {
        // Odd-length palindrome (single character center)
        let (left1, right1) = expand_around_center(&chars, i as i32, i as i32);
        // Even-length palindrome (two character center)
        let (left2, right2) = expand_around_center(&chars, i as i32, (i + 1) as i32);

        // Update longest
        if right1 - left1 > end as i32 - start as i32 {
            start = left1 as usize;
            end = right1 as usize;
        }
        if right2 - left2 > end as i32 - start as i32 {
            start = left2 as usize;
            end = right2 as usize;
        }
    }

    chars[start..=end].iter().collect()
}

/// Problem: Count all palindromic substrings.
///
/// Example: s = "abc" → 3 ("a", "b", "c")
///          s = "aaa" → 6 ("a", "a", "a", "aa", "aa", "aaa")
///
/// Approach: Expand around center, count each valid expansion
fn count_palindromic_substrings(s: &str) -> usize {
    let chars: Vec<char> = s.chars().collect();
    let mut count = 0;

    fn expand_and_count(chars: &[char], mut left: i32, mut right: i32) -> usize {
        let mut palindrome_count = 0;
        while left >= 0 && right < chars.len() as i32 && chars[left as usize] == chars[right as usize] {
            palindrome_count += 1;
            left -= 1;
            right += 1;
        }
        palindrome_count
    }

    for i in 0..chars.len() {
        // Odd-length palindromes
        count += expand_and_count(&chars, i as i32, i as i32);
        // Even-length palindromes
        count += expand_and_count(&chars, i as i32, (i + 1) as i32);
    }

    count
}

/// Problem: Check if string can be palindrome with at most one deletion.
///
/// Example: s = "abca" → True (delete 'c')
///          s = "abc" → False
///
/// Approach: Two-pointer with fallback
fn valid_palindrome_with_one_deletion(s: &str) -> bool {
    let chars: Vec<char> = s.chars().collect();

    fn is_palindrome_range(chars: &[char], mut left: usize, mut right: usize) -> bool {
        while left < right {
            if chars[left] != chars[right] {
                return false;
            }
            left += 1;
            right = right.saturating_sub(1);
        }
        true
    }

    let mut left = 0;
    let mut right = chars.len().saturating_sub(1);

    while left < right {
        if chars[left] != chars[right] {
            // Try deleting left character OR right character
            return is_palindrome_range(&chars, left + 1, right)
                || is_palindrome_range(&chars, left, right.saturating_sub(1));
        }
        left += 1;
        if right > 0 {
            right -= 1;
        }
    }

    true
}

// ============================================================================
// 2. STRING MATCHING ALGORITHMS
// ============================================================================

/// String Matching patterns:
///
/// Pattern 1: Naive String Matching
/// - Used for: Simple substring search
/// - Time: O(n*m), Space: O(1)
///
/// Pattern 2: Rabin-Karp Algorithm
/// - Used for: Multiple pattern matching
/// - Time: O(n+m) average, Space: O(1)
///
/// Pattern 3: KMP (Knuth-Morris-Pratt)
/// - Used for: Efficient single pattern matching
/// - Time: O(n+m), Space: O(m)

/// Problem: Find all occurrences of pattern in text.
///
/// Example: text = "ababcabcab", pattern = "ab" → [0, 2, 5, 8]
///
/// Approach: Naive string matching
fn naive_string_search(text: &str, pattern: &str) -> Vec<usize> {
    if pattern.is_empty() || text.is_empty() {
        return vec![];
    }

    let mut result = Vec::new();
    let text_chars: Vec<char> = text.chars().collect();
    let pattern_chars: Vec<char> = pattern.chars().collect();
    let n = text_chars.len();
    let m = pattern_chars.len();

    for i in 0..=n - m {
        if text_chars[i..i + m] == pattern_chars[..] {
            result.push(i);
        }
    }

    result
}

/// Problem: Find all occurrences of pattern in text using rolling hash.
///
/// Example: text = "ababcabcab", pattern = "ab" → [0, 2, 5, 8]
///
/// Approach: Rabin-Karp algorithm
fn rabin_karp(text: &str, pattern: &str) -> Vec<usize> {
    if pattern.is_empty() || text.is_empty() {
        return vec![];
    }

    let mut result = Vec::new();
    let text_chars: Vec<char> = text.chars().collect();
    let pattern_chars: Vec<char> = pattern.chars().collect();
    let n = text_chars.len();
    let m = pattern_chars.len();

    let prime = 101u64;
    let base = 256u64;

    // Compute h = base^(m-1) % prime
    let mut h = 1u64;
    for _ in 0..m - 1 {
        h = (h * base) % prime;
    }

    // Compute hash of pattern and first window
    let mut pattern_hash = 0u64;
    let mut text_hash = 0u64;

    for i in 0..m {
        pattern_hash = (base * pattern_hash + pattern_chars[i] as u64) % prime;
        text_hash = (base * text_hash + text_chars[i] as u64) % prime;
    }

    // Slide pattern over text
    for i in 0..=n - m {
        // Check if hashes match
        if pattern_hash == text_hash {
            // Verify character-by-character
            if text_chars[i..i + m] == pattern_chars[..] {
                result.push(i);
            }
        }

        // Compute hash for next window
        if i < n - m {
            text_hash = (base * (text_hash + prime - (text_chars[i] as u64 * h) % prime)
                + text_chars[i + m] as u64)
                % prime;
        }
    }

    result
}

/// Problem: Find all occurrences of pattern in text using KMP.
///
/// Example: text = "ababcabcab", pattern = "ab" → [0, 2, 5, 8]
///
/// Approach: KMP algorithm with LPS array
fn kmp_search(text: &str, pattern: &str) -> Vec<usize> {
    if pattern.is_empty() || text.is_empty() {
        return vec![];
    }

    let mut result = Vec::new();
    let text_chars: Vec<char> = text.chars().collect();
    let pattern_chars: Vec<char> = pattern.chars().collect();
    let n = text_chars.len();
    let m = pattern_chars.len();

    // Build LPS array
    fn compute_lps(pattern: &[char]) -> Vec<usize> {
        let m = pattern.len();
        let mut lps = vec![0; m];
        let mut length = 0;
        let mut i = 1;

        while i < m {
            if pattern[i] == pattern[length] {
                length += 1;
                lps[i] = length;
                i += 1;
            } else if length != 0 {
                length = lps[length - 1];
            } else {
                lps[i] = 0;
                i += 1;
            }
        }

        lps
    }

    let lps = compute_lps(&pattern_chars);

    // Search using LPS array
    let mut i = 0; // index for text
    let mut j = 0; // index for pattern

    while i < n {
        if pattern_chars[j] == text_chars[i] {
            i += 1;
            j += 1;

            if j == m {
                result.push(i - j);
                j = lps[j - 1];
            }
        } else if j != 0 {
            j = lps[j - 1];
        } else {
            i += 1;
        }
    }

    result
}

/// Problem: Find first occurrence of needle in haystack.
/// Returns -1 if not found.
///
/// Example: haystack = "sadbutsad", needle = "sad" → 0
///          haystack = "leetcode", needle = "leeto" → -1
fn implement_strstr(haystack: &str, needle: &str) -> i32 {
    if needle.is_empty() {
        return 0;
    }
    if needle.len() > haystack.len() {
        return -1;
    }

    let haystack_chars: Vec<char> = haystack.chars().collect();
    let needle_chars: Vec<char> = needle.chars().collect();
    let n = haystack_chars.len();
    let m = needle_chars.len();

    for i in 0..=n - m {
        if haystack_chars[i..i + m] == needle_chars[..] {
            return i as i32;
        }
    }

    -1
}

// ============================================================================
// 3. SLIDING WINDOW ON STRINGS
// ============================================================================

/// String Sliding Window patterns:
///
/// Pattern 1: Character Frequency Window
/// - Used for: Anagram finding, permutation checking
/// - Time: O(n), Space: O(1) (fixed alphabet)
///
/// Pattern 2: Unique Character Window
/// - Used for: Longest substring without repeating
/// - Time: O(n), Space: O(min(n, alphabet_size))
///
/// Pattern 3: Replacement Window
/// - Used for: Character replacement problems
/// - Time: O(n), Space: O(1)

use std::collections::{HashMap, HashSet};

/// Problem: Find all starting indices of p's anagrams in s.
///
/// Example: s = "cbaebabacd", p = "abc" → [0, 6]
///
/// Approach: Sliding window with frequency map
fn find_all_anagrams(s: &str, p: &str) -> Vec<usize> {
    if p.len() > s.len() {
        return vec![];
    }

    let mut result = Vec::new();
    let s_chars: Vec<char> = s.chars().collect();
    let p_chars: Vec<char> = p.chars().collect();

    let mut p_count: HashMap<char, usize> = HashMap::new();
    let mut window_count: HashMap<char, usize> = HashMap::new();

    for &c in &p_chars {
        *p_count.entry(c).or_insert(0) += 1;
    }

    // Initialize first window
    for &c in &s_chars[..p.len()] {
        *window_count.entry(c).or_insert(0) += 1;
    }

    if window_count == p_count {
        result.push(0);
    }

    // Slide window
    for i in p.len()..s_chars.len() {
        // Add new character
        *window_count.entry(s_chars[i]).or_insert(0) += 1;
        // Remove old character
        let old_char = s_chars[i - p.len()];
        if let Some(count) = window_count.get_mut(&old_char) {
            *count -= 1;
            if *count == 0 {
                window_count.remove(&old_char);
            }
        }

        if window_count == p_count {
            result.push(i - p.len() + 1);
        }
    }

    result
}

/// Problem: Check if s2 contains a permutation of s1.
///
/// Example: s1 = "ab", s2 = "eidbaooo" → True ("ba")
///          s1 = "ab", s2 = "eidboaoo" → False
///
/// Approach: Sliding window with frequency comparison
fn permutation_in_string(s1: &str, s2: &str) -> bool {
    if s1.len() > s2.len() {
        return false;
    }

    let s1_chars: Vec<char> = s1.chars().collect();
    let s2_chars: Vec<char> = s2.chars().collect();

    let mut s1_count: HashMap<char, usize> = HashMap::new();
    let mut window_count: HashMap<char, usize> = HashMap::new();

    for &c in &s1_chars {
        *s1_count.entry(c).or_insert(0) += 1;
    }

    // Initialize first window
    for &c in &s2_chars[..s1.len()] {
        *window_count.entry(c).or_insert(0) += 1;
    }

    if window_count == s1_count {
        return true;
    }

    // Slide window
    for i in s1.len()..s2_chars.len() {
        // Add new character
        *window_count.entry(s2_chars[i]).or_insert(0) += 1;
        // Remove old character
        let old_char = s2_chars[i - s1.len()];
        if let Some(count) = window_count.get_mut(&old_char) {
            *count -= 1;
            if *count == 0 {
                window_count.remove(&old_char);
            }
        }

        if window_count == s1_count {
            return true;
        }
    }

    false
}

/// Problem: Find minimum window in s containing all characters of t.
///
/// Example: s = "ADOBECODEBANC", t = "ABC" → "BANC"
///
/// Approach: Dynamic sliding window with frequency map
fn minimum_window_substring(s: &str, t: &str) -> String {
    if s.is_empty() || t.is_empty() {
        return String::new();
    }

    let s_chars: Vec<char> = s.chars().collect();

    let mut need: HashMap<char, usize> = HashMap::new();
    for c in t.chars() {
        *need.entry(c).or_insert(0) += 1;
    }
    let required = need.len();

    let mut formed = 0;
    let mut window_counts: HashMap<char, usize> = HashMap::new();

    let mut left = 0;
    let mut min_length = usize::MAX;
    let mut result = (0, 0);

    for right in 0..s_chars.len() {
        let char = s_chars[right];
        *window_counts.entry(char).or_insert(0) += 1;

        // Check if this character satisfies requirement
        if let Some(&needed_count) = need.get(&char) {
            if let Some(&window_count) = window_counts.get(&char) {
                if window_count == needed_count {
                    formed += 1;
                }
            }
        }

        // Contract window while valid
        while formed == required {
            // Update minimum
            if right - left + 1 < min_length {
                min_length = right - left + 1;
                result = (left, right);
            }

            // Remove left character
            *window_counts.get_mut(&s_chars[left]).unwrap() -= 1;
            if let Some(&needed_count) = need.get(&s_chars[left]) {
                if let Some(&window_count) = window_counts.get(&s_chars[left]) {
                    if window_count < needed_count {
                        formed -= 1;
                    }
                }
            }
            left += 1;
        }
    }

    if min_length == usize::MAX {
        String::new()
    } else {
        s_chars[result.0..=result.1].iter().collect()
    }
}

/// Problem: Longest substring with at most k character replacements.
///
/// Example: s = "AABABBA", k = 1 → 4
///          s = "ABAB", k = 2 → 4
///
/// Approach: Sliding window with max frequency tracking
fn longest_substring_with_k_replacements(s: &str, k: usize) -> usize {
    let s_chars: Vec<char> = s.chars().collect();
    let mut char_count: HashMap<char, usize> = HashMap::new();
    let mut left = 0;
    let mut max_freq = 0;
    let mut max_length = 0;

    for right in 0..s_chars.len() {
        *char_count.entry(s_chars[right]).or_insert(0) += 1;
        max_freq = max_freq.max(*char_count.get(&s_chars[right]).unwrap());

        // Contract if invalid: need more than k replacements
        while (right - left + 1) - max_freq > k {
            *char_count.get_mut(&s_chars[left]).unwrap() -= 1;
            left += 1;
        }

        max_length = max_length.max(right - left + 1);
    }

    max_length
}

// ============================================================================
// 4. TRIE (PREFIX TREE) STRUCTURES
// ============================================================================

/// Trie Node implementation
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

/// Trie (Prefix Tree) implementation
///
/// Use cases:
/// - Autocomplete systems
/// - Spell checkers
/// - IP routing
/// - Word search games
///
/// Time Complexity:
/// - Insert: O(m) where m is word length
/// - Search: O(m)
/// - StartsWith: O(m)
///
/// Space Complexity: O(n * m) where n is number of words
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

        for char in word.chars() {
            node = node.children.entry(char).or_insert_with(TrieNode::new);
        }

        node.is_end_of_word = true;
    }

    /// Search for a complete word in the trie
    fn search(&self, word: &str) -> bool {
        if let Some(node) = self.find_node(word) {
            node.is_end_of_word
        } else {
            false
        }
    }

    /// Check if any word in trie starts with given prefix
    fn starts_with(&self, prefix: &str) -> bool {
        self.find_node(prefix).is_some()
    }

    /// Find the node at the end of prefix path
    fn find_node(&self, prefix: &str) -> Option<&TrieNode> {
        let mut node = &self.root;

        for char in prefix.chars() {
            if let Some(child) = node.children.get(&char) {
                node = child;
            } else {
                return None;
            }
        }

        Some(node)
    }

    /// Find all words in trie that start with given prefix
    fn find_all_words_with_prefix(&self, prefix: &str) -> Vec<String> {
        if let Some(node) = self.find_node(prefix) {
            let mut result = Vec::new();
            Self::dfs(node, prefix.to_string(), &mut result);
            result
        } else {
            vec![]
        }
    }

    /// DFS to collect all words from a node
    fn dfs(node: &TrieNode, current_word: String, result: &mut Vec<String>) {
        if node.is_end_of_word {
            result.push(current_word.clone());
        }

        for (char, child_node) in &node.children {
            let mut new_word = current_word.clone();
            new_word.push(*char);
            Self::dfs(child_node, new_word, result);
        }
    }
}

/// Applications of Trie data structure
struct TrieApplications;

impl TrieApplications {
    /// Problem: Find all words from a list that can be formed on the board.
    /// Words can be formed by connecting adjacent cells (horizontally or vertically).
    ///
    /// Example: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    ///          words = ["oath","pea","oath","rain"]
    ///          → ["oath", "rain"]
    ///
    /// Approach: Trie + Backtracking
    fn word_search_on_board(board: Vec<Vec<char>>, words: Vec<&str>) -> Vec<String> {
        if board.is_empty() || board[0].is_empty() {
            return vec![];
        }

        // Build trie
        let mut trie = Trie::new();
        for word in words {
            trie.insert(word);
        }

        let mut result: HashSet<String> = HashSet::new();
        let rows = board.len();
        let cols = board[0].len();

        fn dfs(
            board: &mut Vec<Vec<char>>,
            row: i32,
            col: i32,
            node: &TrieNode,
            path: String,
            result: &mut HashSet<String>,
        ) {
            let rows = board.len() as i32;
            let cols = board[0].len() as i32;

            // Check bounds and if cell visited
            if row < 0 || row >= rows || col < 0 || col >= cols {
                return;
            }
            if board[row as usize][col as usize] == '#' {
                return;
            }

            let char = board[row as usize][col as usize];
            let node = match node.children.get(&char) {
                Some(n) => n,
                None => return,
            };

            let mut new_path = path.clone();
            new_path.push(char);

            // Check if word found
            if node.is_end_of_word {
                result.insert(new_path.clone());
            }

            // Mark as visited
            let temp = board[row as usize][col as usize];
            board[row as usize][col as usize] = '#';

            // Explore neighbors
            dfs(board, row + 1, col, node, new_path.clone(), result);
            dfs(board, row - 1, col, node, new_path.clone(), result);
            dfs(board, row, col + 1, node, new_path.clone(), result);
            dfs(board, row, col - 1, node, new_path, result);

            // Backtrack
            board[row as usize][col as usize] = temp;
        }

        let mut board = board;
        for i in 0..rows {
            for j in 0..cols {
                dfs(&mut board, i as i32, j as i32, &trie.root, String::new(), &mut result);
            }
        }

        result.into_iter().collect()
    }
}

// ============================================================================
// 5. STRING MANIPULATION PATTERNS
// ============================================================================

/// String Manipulation patterns:
///
/// Pattern 1: In-Place Reversal
/// - Used for: Reverse words, reverse string
/// - Time: O(n), Space: O(1) or O(n) depending on mutability
///
/// Pattern 2: String Compression
/// - Used for: Run-length encoding
/// - Time: O(n), Space: O(1) excluding output
///
/// Pattern 3: String Tokenization
/// - Used for: Parsing, splitting
/// - Time: O(n), Space: O(n)

/// Problem: Reverse string in-place (as character vector).
///
/// Example: s = ["h","e","l","l","o"] → ["o","l","l","e","h"]
///
/// Approach: Two-pointer swap
fn reverse_string(s: &mut Vec<char>) {
    let mut left = 0;
    let mut right = s.len().saturating_sub(1);

    while left < right {
        s.swap(left, right);
        left += 1;
        if right > 0 {
            right -= 1;
        }
    }
}

/// Problem: Reverse the order of words in a string.
///
/// Example: s = "the sky is blue" → "blue is sky the"
///          s = "  hello world  " → "world hello"
///
/// Approach: Split, reverse, join
fn reverse_words_in_string(s: &str) -> String {
    let mut words: Vec<&str> = s.split_whitespace().collect();
    words.reverse();
    words.join(" ")
}

/// Problem: Check if s can be rotated to become goal.
///
/// Example: s = "abcde", goal = "cdeab" → True
///          s = "abcde", goal = "abced" → False
///
/// Approach: String concatenation trick
fn rotate_string(s: &str, goal: &str) -> bool {
    s.len() == goal.len() && goal.is_empty() || (s.len() > 0 && (s.to_string() + s).contains(goal))
}

/// Problem: Compress character array using run-length encoding.
/// Returns new length, modifies array in-place.
///
/// Example: chars = ["a","a","b","b","c","c","c"]
///          → length = 6, chars = ["a","2","b","2","c","3"]
///
/// Approach: Two-pointer compression
fn string_compression(chars: &mut Vec<char>) -> usize {
    let mut write = 0;
    let mut read = 0;

    while read < chars.len() {
        let char = chars[read];
        let mut count = 0;

        // Count consecutive identical characters
        while read < chars.len() && chars[read] == char {
            read += 1;
            count += 1;
        }

        // Write character
        chars[write] = char;
        write += 1;

        // Write count if > 1
        if count > 1 {
            for digit in count.to_string().chars() {
                chars[write] = digit;
                write += 1;
            }
        }
    }

    write
}

/// Problem: Group anagrams together.
///
/// Example: ["eat","tea","tan","ate","nat","bat"]
///          → [["eat","tea","ate"],["tan","nat"],["bat"]]
///
/// Approach: Hash map with sorted key
fn group_anagrams(strs: Vec<&str>) -> Vec<Vec<String>> {
    let mut groups: HashMap<String, Vec<String>> = HashMap::new();

    for s in strs {
        let mut key: Vec<char> = s.chars().collect();
        key.sort_unstable();
        let key: String = key.into_iter().collect();

        groups.entry(key).or_insert_with(Vec::new).push(s.to_string());
    }

    groups.into_values().collect()
}

// ============================================================================
// PRACTICE PROBLEMS FOR HOMEWORK
// ============================================================================

/// Homework Problems - Try solving these on your own!
///
/// EASY:
/// 1. Valid Palindrome
/// 2. Reverse String
/// 3. Valid Anagram
/// 4. First Unique Character in String
///
/// MEDIUM:
/// 5. Longest Palindromic Substring
/// 6. Group Anagrams
/// 7. Find All Anagrams in a String
/// 8. Minimum Window Substring
/// 9. Longest Substring Without Repeating Characters
///
/// HARD:
/// 10. Regular Expression Matching
/// 11. Edit Distance
/// 12. Word Search II

struct PracticeProblems;

impl PracticeProblems {
    /// Problem: Find index of first non-repeating character.
    ///
    /// Example: s = "leetcode" → 0 ('l')
    ///          s = "loveleetcode" → 2 ('v')
    ///          s = "aabb" → -1
    ///
    /// Approach: Two-pass with frequency map
    fn first_unique_character(s: &str) -> i32 {
        let chars: Vec<char> = s.chars().collect();
        let mut char_count: HashMap<char, usize> = HashMap::new();

        for &c in &chars {
            *char_count.entry(c).or_insert(0) += 1;
        }

        for (i, &c) in chars.iter().enumerate() {
            if let Some(&count) = char_count.get(&c) {
                if count == 1 {
                    return i as i32;
                }
            }
        }

        -1
    }

    /// Problem: Check if t is an anagram of s.
    ///
    /// Example: s = "anagram", t = "nagaram" → True
    ///          s = "rat", t = "car" → False
    ///
    /// Approach: Character frequency comparison
    fn valid_anagram(s: &str, t: &str) -> bool {
        let mut char_count: HashMap<char, i32> = HashMap::new();

        for c in s.chars() {
            *char_count.entry(c).or_insert(0) += 1;
        }

        for c in t.chars() {
            *char_count.entry(c).or_insert(0) -= 1;
        }

        char_count.values().all(|&count| count == 0)
    }

    /// Problem: Find length of longest substring without repeating characters.
    ///
    /// Example: s = "abcabcbb" → 3 ("abc")
    ///          s = "bbbbb" → 1 ("b")
    ///          s = "pwwkew" → 3 ("wke")
    ///
    /// Approach: Sliding window with hash set
    fn longest_substring_no_repeat(s: &str) -> usize {
        let chars: Vec<char> = s.chars().collect();
        let mut char_set: HashSet<char> = HashSet::new();
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

    /// Problem: Implement regular expression matching with '.' and '*'.
    /// '.' matches any single character
    /// '*' matches zero or more of preceding element
    ///
    /// Example: s = "aa", p = "a*" → True
    ///          s = "ab", p = ".*" → True
    ///
    /// Approach: Dynamic programming
    fn regular_expression_matching(s: &str, p: &str) -> bool {
        let s_chars: Vec<char> = s.chars().collect();
        let p_chars: Vec<char> = p.chars().collect();
        let m = s_chars.len();
        let n = p_chars.len();

        // dp[i][j] = s[:i] matches p[:j]
        let mut dp = vec![vec![false; n + 1]; m + 1];
        dp[0][0] = true;

        // Handle patterns like a*, a*b*, a*b*c* matching empty string
        for j in 2..=n {
            if p_chars[j - 1] == '*' {
                dp[0][j] = dp[0][j - 2];
            }
        }

        for i in 1..=m {
            for j in 1..=n {
                if p_chars[j - 1] == '.' || p_chars[j - 1] == s_chars[i - 1] {
                    dp[i][j] = dp[i - 1][j - 1];
                } else if p_chars[j - 1] == '*' {
                    // Zero occurrences of preceding char
                    dp[i][j] = dp[i][j - 2];
                    // One or more if preceding char matches
                    if p_chars[j - 2] == '.' || p_chars[j - 2] == s_chars[i - 1] {
                        dp[i][j] = dp[i][j] || dp[i - 1][j];
                    }
                }
            }
        }

        dp[m][n]
    }

    /// Problem: Minimum operations to convert word1 to word2.
    /// Operations: insert, delete, replace
    ///
    /// Example: word1 = "horse", word2 = "ros" → 3
    ///
    /// Approach: Dynamic programming
    fn edit_distance(word1: &str, word2: &str) -> i32 {
        let word1_chars: Vec<char> = word1.chars().collect();
        let word2_chars: Vec<char> = word2.chars().collect();
        let m = word1_chars.len();
        let n = word2_chars.len();

        // dp[i][j] = min operations for word1[:i] -> word2[:j]
        let mut dp = vec![vec![0; n + 1]; m + 1];

        // Base cases
        for i in 0..=m {
            dp[i][0] = i;
        }
        for j in 0..=n {
            dp[0][j] = j;
        }

        for i in 1..=m {
            for j in 1..=n {
                if word1_chars[i - 1] == word2_chars[j - 1] {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + dp[i][j - 1].min(dp[i - 1][j]).min(dp[i - 1][j - 1]);
                }
            }
        }

        dp[m][n] as i32
    }
}

// ============================================================================
// TEST CASEES
// ============================================================================

fn run_tests() {
    println!("{}", "=".repeat(60));
    println!("DAY 3: STRING MANIPULATION - TEST CASES");
    println!("{}", "=".repeat(60));

    // Palindrome Tests
    println!("\n1. PALINDROME PATTERNS");
    println!("{}", "-".repeat(40));

    // Is Palindrome
    let result = is_palindrome("A man, a plan, a canal: Panama");
    println!("Is Palindrome 'A man, a plan...': {}", result);
    assert!(result);

    let result = is_palindrome("race a car");
    println!("Is Palindrome 'race a car': {}", result);
    assert!(!result);

    // Longest Palindromic Substring
    let longest = longest_palindromic_substring("babad");
    println!("Longest Palindrome in 'babad': {}", longest);
    assert!(longest == "bab" || longest == "aba");

    let longest = longest_palindromic_substring("cbbd");
    println!("Longest Palindrome in 'cbbd': {}", longest);
    assert_eq!(longest, "bb");

    // Count Palindromic Substrings
    let count = count_palindromic_substrings("abc");
    println!("Count Palindromes in 'abc': {}", count);
    assert_eq!(count, 3);

    let count = count_palindromic_substrings("aaa");
    println!("Count Palindromes in 'aaa': {}", count);
    assert_eq!(count, 6);

    // String Matching Tests
    println!("\n2. STRING MATCHING ALGORITHMS");
    println!("{}", "-".repeat(40));

    // Naive Search
    let indices = naive_string_search("ababcabcab", "ab");
    println!("Naive Search 'ab' in 'ababcabcab': {:?}", indices);
    assert_eq!(indices, vec![0, 2, 5, 8]);

    // Rabin-Karp
    let indices = rabin_karp("ababcabcab", "ab");
    println!("Rabin-Karp 'ab' in 'ababcabcab': {:?}", indices);
    assert_eq!(indices, vec![0, 2, 5, 8]);

    // KMP Search
    let indices = kmp_search("ababcabcab", "ab");
    println!("KMP Search 'ab' in 'ababcabcab': {:?}", indices);
    assert_eq!(indices, vec![0, 2, 5, 8]);

    // Implement strStr
    let pos = implement_strstr("sadbutsad", "sad");
    println!("strStr('sadbutsad', 'sad'): {}", pos);
    assert_eq!(pos, 0);

    let pos = implement_strstr("leetcode", "leeto");
    println!("strStr('leetcode', 'leeto'): {}", pos);
    assert_eq!(pos, -1);

    // Sliding Window Tests
    println!("\n3. SLIDING WINDOW ON STRINGS");
    println!("{}", "-".repeat(40));

    // Find All Anagrams
    let anagrams = find_all_anagrams("cbaebabacd", "abc");
    println!("Find Anagrams of 'abc' in 'cbaebabacd': {:?}", anagrams);
    assert_eq!(anagrams, vec![0, 6]);

    // Permutation in String
    let has_perm = permutation_in_string("ab", "eidbaooo");
    println!("Permutation of 'ab' in 'eidbaooo': {}", has_perm);
    assert!(has_perm);

    // Minimum Window Substring
    let window = minimum_window_substring("ADOBECODEBANC", "ABC");
    println!("Min Window 'ABC' in 'ADOBECODEBANC': {}", window);
    assert_eq!(window, "BANC");

    // Longest Substring with K Replacements
    let longest = longest_substring_with_k_replacements("AABABBA", 1);
    println!("Longest Substring (k=1) in 'AABABBA': {}", longest);
    assert_eq!(longest, 4);

    // Trie Tests
    println!("\n4. TRIE STRUCTURES");
    println!("{}", "-".repeat(40));

    let mut trie = Trie::new();
    trie.insert("apple");
    trie.insert("application");
    trie.insert("app");

    let search_result = trie.search("apple");
    println!("Trie Search 'apple': {}", search_result);
    assert!(search_result);

    let search_result = trie.search("app");
    println!("Trie Search 'app': {}", search_result);
    assert!(search_result);

    let prefix_result = trie.starts_with("app");
    println!("Trie StartsWith 'app': {}", prefix_result);
    assert!(prefix_result);

    let prefix_result = trie.starts_with("appl");
    println!("Trie StartsWith 'appl': {}", prefix_result);
    assert!(prefix_result);

    let words = trie.find_all_words_with_prefix("app");
    println!("Trie Words with prefix 'app': {:?}", words);
    assert!(words.contains(&"apple".to_string()));
    assert!(words.contains(&"application".to_string()));
    assert!(words.contains(&"app".to_string()));

    // String Manipulation Tests
    println!("\n5. STRING MANIPULATION");
    println!("{}", "-".repeat(40));

    // Reverse String
    let mut chars = vec!['h', 'e', 'l', 'l', 'o'];
    reverse_string(&mut chars);
    println!("Reverse String 'hello': {:?}", chars);
    assert_eq!(chars, vec!['o', 'l', 'l', 'e', 'h']);

    // Reverse Words
    let reversed_words = reverse_words_in_string("  hello world  ");
    println!("Reverse Words '  hello world  ': '{}'", reversed_words);
    assert_eq!(reversed_words, "world hello");

    // Rotate String
    let is_rotation = rotate_string("abcde", "cdeab");
    println!("Rotate String 'abcde' -> 'cdeab': {}", is_rotation);
    assert!(is_rotation);

    // String Compression
    let mut chars = vec!['a', 'a', 'b', 'b', 'c', 'c', 'c'];
    let length = string_compression(&mut chars);
    println!("String Compression: length={}, chars={:?}", length, &chars[..length]);
    assert_eq!(length, 6);
    assert_eq!(&chars[..length], &['a', '2', 'b', '2', 'c', '3']);

    // Group Anagrams
    let groups = group_anagrams(vec!["eat", "tea", "tan", "ate", "nat", "bat"]);
    println!("Group Anagrams: {:?}", groups);
    assert_eq!(groups.len(), 3);

    // Practice Problems Tests
    println!("\n6. PRACTICE PROBLEMS");
    println!("{}", "-".repeat(40));

    // First Unique Character
    let idx = PracticeProblems::first_unique_character("leetcode");
    println!("First Unique in 'leetcode': index {}", idx);
    assert_eq!(idx, 0);

    let idx = PracticeProblems::first_unique_character("aabb");
    println!("First Unique in 'aabb': index {}", idx);
    assert_eq!(idx, -1);

    // Valid Anagram
    let is_anagram = PracticeProblems::valid_anagram("anagram", "nagaram");
    println!("Valid Anagram 'anagram' & 'nagaram': {}", is_anagram);
    assert!(is_anagram);

    // Longest Substring No Repeat
    let longest = PracticeProblems::longest_substring_no_repeat("abcabcbb");
    println!("Longest No Repeat 'abcabcbb': {}", longest);
    assert_eq!(longest, 3);

    // Edit Distance
    let distance = PracticeProblems::edit_distance("horse", "ros");
    println!("Edit Distance 'horse' -> 'ros': {}", distance);
    assert_eq!(distance, 3);

    let distance = PracticeProblems::edit_distance("intention", "execution");
    println!("Edit Distance 'intention' -> 'execution': {}", distance);
    assert_eq!(distance, 5);

    println!("\n{}", "=".repeat(60));
    println!("ALL TESTS PASSED!");
    println!("{}", "=".repeat(60));
}

fn main() {
    run_tests();
}
