/// Day 11: Dynamic Programming - Part 1
/// Rust Implementations

// =============================================================================
// 1. Fibonacci Sequence
// =============================================================================

/// Space-optimized Fibonacci - O(n) time, O(1) space
fn fibonacci_optimized(n: u64) -> u64 {
    if n == 0 {
        return 0;
    }
    if n == 1 {
        return 1;
    }
    
    let (mut prev2, mut prev1) = (0u64, 1u64);
    for _ in 2..=n {
        let curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    prev1
}

// =============================================================================
// 2. Climbing Stairs
// =============================================================================

/// Climbing Stairs - O(n) time, O(1) space
fn climb_stairs(n: u32) -> u32 {
    if n <= 1 {
        return 1;
    }
    
    let (mut prev2, mut prev1) = (1u32, 1u32);
    for _ in 2..=n {
        let curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    prev1
}

// =============================================================================
// 3. House Robber
// =============================================================================

/// House Robber - O(n) time, O(1) space
fn house_robber(nums: &[i32]) -> i32 {
    if nums.is_empty() {
        return 0;
    }
    if nums.len() == 1 {
        return nums[0];
    }
    
    let (mut prev2, mut prev1) = (0i32, 0i32);
    for &num in nums {
        let curr = prev1.max(prev2 + num);
        prev2 = prev1;
        prev1 = curr;
    }
    prev1
}

// =============================================================================
// 4. Coin Change
// =============================================================================

/// Coin Change (Minimum Coins) - O(amount * len(coins)) time, O(amount) space
fn coin_change(coins: &[i32], amount: i32) -> i32 {
    let amount = amount as usize;
    let mut dp = vec![i32::MAX; amount + 1];
    dp[0] = 0;
    
    for &coin in coins {
        let coin = coin as usize;
        for i in coin..=amount {
            if dp[i - coin] != i32::MAX {
                dp[i] = dp[i].min(dp[i - coin] + 1);
            }
        }
    }
    
    if dp[amount] == i32::MAX {
        -1
    } else {
        dp[amount] as i32
    }
}

// =============================================================================
// 5. 0/1 Knapsack Problem
// =============================================================================

/// 0/1 Knapsack with optimized space - O(n * capacity) time, O(capacity) space
fn knapsack_01(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    let capacity = capacity as usize;
    let mut dp = vec![0i32; capacity + 1];
    
    for i in 0..weights.len() {
        let weight = weights[i] as usize;
        let value = values[i];
        // Iterate backwards to avoid using updated values from current iteration
        for w in (weight..=capacity).rev() {
            dp[w] = dp[w].max(dp[w - weight] + value);
        }
    }
    
    dp[capacity]
}

// =============================================================================
// 6. Unbounded Knapsack
// =============================================================================

/// Unbounded Knapsack - O(n * capacity) time, O(capacity) space
fn knapsack_unbounded(weights: &[i32], values: &[i32], capacity: i32) -> i32 {
    let capacity = capacity as usize;
    let mut dp = vec![0i32; capacity + 1];
    
    for i in 0..weights.len() {
        let weight = weights[i] as usize;
        let value = values[i];
        // Iterate forwards (can reuse same item multiple times)
        for w in weight..=capacity {
            dp[w] = dp[w].max(dp[w - weight] + value);
        }
    }
    
    dp[capacity]
}

// =============================================================================
// 7. Target Sum
// =============================================================================

/// Target Sum - O(n * sum) time, O(sum) space
fn find_target_sum_ways(nums: &[i32], target: i32) -> i32 {
    let total_sum: i32 = nums.iter().sum();
    
    // Check if solution is possible
    if target.abs() > total_sum || (total_sum + target) % 2 != 0 {
        return 0;
    }
    
    let subset_sum = ((total_sum + target) / 2) as usize;
    
    // Now solve subset sum problem
    let mut dp = vec![0i32; subset_sum + 1];
    dp[0] = 1; // One way to make sum 0 (take nothing)
    
    for &num in nums {
        let num = num as usize;
        for w in (num..=subset_sum).rev() {
            dp[w] += dp[w - num];
        }
    }
    
    dp[subset_sum]
}

// =============================================================================
// 8. Longest Common Subsequence (LCS)
// =============================================================================

/// Longest Common Subsequence - O(m * n) time, O(m * n) space
fn longest_common_subsequence(s1: &str, s2: &str) -> i32 {
    let s1: Vec<char> = s1.chars().collect();
    let s2: Vec<char> = s2.chars().collect();
    let m = s1.len();
    let n = s2.len();
    
    // dp[i][j] = LCS length for s1[0..i-1] and s2[0..j-1]
    let mut dp = vec![vec![0i32; n + 1]; m + 1];
    
    for i in 1..=m {
        for j in 1..=n {
            if s1[i - 1] == s2[j - 1] {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = dp[i - 1][j].max(dp[i][j - 1]);
            }
        }
    }
    
    dp[m][n]
}

// =============================================================================
// 9. Edit Distance (Levenshtein Distance)
// =============================================================================

/// Edit Distance - O(m * n) time, O(m * n) space
fn edit_distance(word1: &str, word2: &str) -> i32 {
    let word1: Vec<char> = word1.chars().collect();
    let word2: Vec<char> = word2.chars().collect();
    let m = word1.len();
    let n = word2.len();
    
    // dp[i][j] = edit distance for word1[0..i-1] and word2[0..j-1]
    let mut dp = vec![vec![0i32; n + 1]; m + 1];
    
    // Base cases
    for i in 0..=m {
        dp[i][0] = i as i32;
    }
    for j in 0..=n {
        dp[0][j] = j as i32;
    }
    
    for i in 1..=m {
        for j in 1..=n {
            if word1[i - 1] == word2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1]; // No operation needed
            } else {
                dp[i][j] = 1 + dp[i - 1][j]      // Delete
                    .min(dp[i][j - 1])              // Insert
                    .min(dp[i - 1][j - 1]);         // Replace
            }
        }
    }
    
    dp[m][n]
}

// =============================================================================
// 10. Longest Palindromic Subsequence
// =============================================================================

/// Longest Palindromic Subsequence - O(n^2) time, O(n^2) space
fn longest_palindromic_subsequence(s: &str) -> i32 {
    let s: Vec<char> = s.chars().collect();
    let n = s.len();
    
    if n == 0 {
        return 0;
    }
    
    // dp[i][j] = LPS length for s[i..j]
    let mut dp = vec![vec![0i32; n]; n];
    
    // Base case: single characters are palindromes of length 1
    for i in 0..n {
        dp[i][i] = 1;
    }
    
    // Fill for substrings of length 2 to n
    for length in 2..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            if s[i] == s[j] {
                dp[i][j] = 2 + dp[i + 1][j - 1];
            } else {
                dp[i][j] = dp[i + 1][j].max(dp[i][j - 1]);
            }
        }
    }
    
    dp[0][n - 1]
}

// =============================================================================
// Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fibonacci() {
        let test_cases = vec![
            (0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (10, 55), (15, 610)
        ];
        
        for (n, expected) in test_cases {
            assert_eq!(fibonacci_optimized(n), expected, "Failed for n={}", n);
        }
    }

    #[test]
    fn test_climb_stairs() {
        let test_cases = vec![
            (0, 1), (1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (10, 89)
        ];
        
        for (n, expected) in test_cases {
            assert_eq!(climb_stairs(n), expected, "Failed for n={}", n);
        }
    }

    #[test]
    fn test_house_robber() {
        assert_eq!(house_robber(&[1, 2, 3, 1]), 4);
        assert_eq!(house_robber(&[2, 7, 9, 3, 1]), 12);
        assert_eq!(house_robber(&[]), 0);
        assert_eq!(house_robber(&[5]), 5);
        assert_eq!(house_robber(&[2, 1, 1, 2]), 4);
        assert_eq!(house_robber(&[10, 2, 2, 10, 2, 10]), 30);
    }

    #[test]
    fn test_coin_change() {
        assert_eq!(coin_change(&[1, 2, 5], 11), 3);
        assert_eq!(coin_change(&[2], 3), -1);
        assert_eq!(coin_change(&[1], 0), 0);
        assert_eq!(coin_change(&[1, 2, 5], 100), 20);
    }

    #[test]
    fn test_knapsack_01() {
        let weights = vec![1, 3, 4, 5];
        let values = vec![1, 4, 5, 7];
        let capacity = 7;
        assert_eq!(knapsack_01(&weights, &values, capacity), 9);
    }

    #[test]
    fn test_knapsack_unbounded() {
        let weights = vec![1, 3, 4, 5];
        let values = vec![1, 4, 5, 7];
        let capacity = 7;
        assert_eq!(knapsack_unbounded(&weights, &values, capacity), 9);
    }

    #[test]
    fn test_target_sum() {
        assert_eq!(find_target_sum_ways(&[1, 1, 1, 1, 1], 3), 5);
        assert_eq!(find_target_sum_ways(&[1], 1), 1);
        assert_eq!(find_target_sum_ways(&[1], 2), 0);
        assert_eq!(find_target_sum_ways(&[1, 2, 3, 4, 5], 3), 3);
    }

    #[test]
    fn test_lcs() {
        assert_eq!(longest_common_subsequence("abcde", "ace"), 3);
        assert_eq!(longest_common_subsequence("abc", "abc"), 3);
        assert_eq!(longest_common_subsequence("abc", "def"), 0);
        assert_eq!(longest_common_subsequence("", ""), 0);
    }

    #[test]
    fn test_edit_distance() {
        assert_eq!(edit_distance("horse", "ros"), 3);
        assert_eq!(edit_distance("intention", "execution"), 5);
        assert_eq!(edit_distance("", "abc"), 3);
        assert_eq!(edit_distance("abc", ""), 3);
        assert_eq!(edit_distance("abc", "abc"), 0);
        assert_eq!(edit_distance("sunday", "saturday"), 3);
    }

    #[test]
    fn test_longest_palindromic_subsequence() {
        assert_eq!(longest_palindromic_subsequence("bbbab"), 4);
        assert_eq!(longest_palindromic_subsequence("cbbd"), 2);
        assert_eq!(longest_palindromic_subsequence("a"), 1);
        assert_eq!(longest_palindromic_subsequence(""), 0);
        assert_eq!(longest_palindromic_subsequence("abcd"), 1);
        assert_eq!(longest_palindromic_subsequence("racexyzca"), 5);
    }
}
