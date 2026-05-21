/*
 * Day 14: DP Review & Practice
 * Topics: Mixed DP problems, pattern recognition, optimization techniques
 * Covers: 1D DP, 2D DP, Interval DP, Tree DP, Bitmask DP, Game Theory DP, Probability DP
 */

// ============================================================================
// PATTERN 1: 1D DP - Fibonacci Variants
// ============================================================================

fn climb_stairs(n: usize) -> usize {
    /*
     * Climbing Stairs - O(n) time, O(1) space
     * Pattern: 1D DP with space optimization
     */
    if n <= 2 {
        return n;
    }
    let (mut prev2, mut prev1) = (1, 2);
    for _ in 3..=n {
        let curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    prev1
}

fn house_robber(nums: &[i32]) -> i32 {
    /*
     * House Robber - O(n) time, O(1) space
     * Pattern: 1D DP - max amount without robbing adjacent houses
     */
    if nums.is_empty() {
        return 0;
    }
    let (mut prev2, mut prev1) = (0, nums[0]);
    for i in 1..nums.len() {
        let curr = prev1.max(prev2 + nums[i]);
        prev2 = prev1;
        prev1 = curr;
    }
    prev1
}

fn coin_change(coins: &[i32], amount: usize) -> i32 {
    /*
     * Coin Change - O(amount * len(coins)) time, O(amount) space
     * Pattern: 1D DP - minimum coins to make up amount
     */
    let mut dp = vec![i32::MAX; amount + 1];
    dp[0] = 0;

    for i in 1..=amount {
        for &coin in coins {
            if i >= coin as usize && dp[i - coin as usize] != i32::MAX {
                dp[i] = dp[i].min(dp[i - coin as usize] + 1);
            }
        }
    }

    if dp[amount] == i32::MAX { -1 } else { dp[amount] }
}

// ============================================================================
// PATTERN 2: 2D DP - LCS, Edit Distance, Knapsack
// ============================================================================

fn longest_common_subsequence(text1: &str, text2: &str) -> usize {
    /*
     * Longest Common Subsequence - O(m*n) time, O(m*n) space
     * Pattern: 2D DP
     */
    let s1: Vec<char> = text1.chars().collect();
    let s2: Vec<char> = text2.chars().collect();
    let m = s1.len();
    let n = s2.len();

    let mut dp = vec![vec![0; n + 1]; m + 1];

    for i in 1..=m {
        for j in 1..=n {
            if s1[i - 1] == s2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = dp[i - 1][j].max(dp[i][j - 1]);
            }
        }
    }

    dp[m][n]
}

fn edit_distance(word1: &str, word2: &str) -> usize {
    /*
     * Edit Distance - O(m*n) time, O(m*n) space
     * Pattern: 2D DP - minimum operations to convert word1 to word2
     */
    let s1: Vec<char> = word1.chars().collect();
    let s2: Vec<char> = word2.chars().collect();
    let m = s1.len();
    let n = s2.len();

    let mut dp = vec![vec![0; n + 1]; m + 1];

    for i in 0..=m {
        dp[i][0] = i;
    }
    for j in 0..=n {
        dp[0][j] = j;
    }

    for i in 1..=m {
        for j in 1..=n {
            if s1[i - 1] == s2[j - 1] {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = 1 + dp[i - 1][j].min(dp[i][j - 1].min(dp[i - 1][j - 1]));
            }
        }
    }

    dp[m][n]
}

fn knapsack_01(weights: &[usize], values: &[usize], capacity: usize) -> usize {
    /*
     * 0/1 Knapsack - O(n*capacity) time, O(capacity) space
     * Pattern: 2D DP with space optimization
     */
    let mut dp = vec![0; capacity + 1];

    for i in 0..weights.len() {
        for w in (weights[i]..=capacity).rev() {
            dp[w] = dp[w].max(dp[w - weights[i]] + values[i]);
        }
    }

    dp[capacity]
}

fn target_sum(nums: &[i32], target: i32) -> usize {
    /*
     * Target Sum - O(n*sum) time, O(sum) space
     * Pattern: 2D DP - count ways to assign +/- to reach target
     */
    let total: i32 = nums.iter().sum();
    if target.abs() > total || (total + target) % 2 != 0 {
        return 0;
    }

    let subset_sum = ((total + target) / 2) as usize;
    let mut dp = vec![0; subset_sum + 1];
    dp[0] = 1;

    for &num in nums {
        for s in (num as usize..=subset_sum).rev() {
            dp[s] += dp[s - num as usize];
        }
    }

    dp[subset_sum]
}

// ============================================================================
// PATTERN 3: Interval DP - Palindrome Partitioning, Burst Balloons
// ============================================================================

fn min_palindrome_cuts(s: &str) -> usize {
    /*
     * Palindrome Partitioning II - O(n^2) time, O(n^2) space
     * Pattern: Interval DP - minimum cuts to partition into palindromes
     */
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len();
    if n <= 1 {
        return 0;
    }

    let mut is_pal = vec![vec![false; n]; n];
    let mut dp = vec![0; n];

    for i in 0..n {
        let mut min_cuts = i;
        for j in 0..=i {
            if chars[i] == chars[j] && (i - j <= 2 || is_pal[j + 1][i - 1]) {
                is_pal[j][i] = true;
                if j == 0 {
                    min_cuts = 0;
                } else {
                    min_cuts = min_cuts.min(dp[j - 1] + 1);
                }
            }
        }
        dp[i] = min_cuts;
    }

    dp[n - 1]
}

fn burst_balloons(nums: &[i32]) -> i32 {
    /*
     * Burst Balloons - O(n^3) time, O(n^2) space
     * Pattern: Interval DP
     */
    let mut balloons = vec![1];
    balloons.extend_from_slice(nums);
    balloons.push(1);

    let n = balloons.len();
    let mut dp = vec![vec![0; n]; n];

    for length in 2..n {
        for i in 0..(n - length) {
            let j = i + length;
            for k in (i + 1)..j {
                let coins = balloons[i] * balloons[k] * balloons[j];
                dp[i][j] = dp[i][j].max(dp[i][k] + coins + dp[k][j]);
            }
        }
    }

    dp[0][n - 1]
}

// ============================================================================
// PATTERN 4: Tree DP - Diameter, Max Independent Set
// ============================================================================

#[derive(Debug, Clone)]
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

fn tree_diameter(root: &Option<Box<TreeNode>>) -> usize {
    /*
     * Tree Diameter - O(n) time, O(h) space
     * Pattern: Tree DP - longest path between any two nodes
     */
    fn depth(node: &Option<Box<TreeNode>>) -> (usize, usize) {
        /* Returns (depth, diameter_through_node) */
        if let Some(n) = node {
            let (left_depth, _) = depth(&n.left);
            let (right_depth, _) = depth(&n.right);

            let diameter = left_depth + right_depth;
            (1 + left_depth.max(right_depth), diameter)
        } else {
            (0, 0)
        }
    }

    fn max_diameter(node: &Option<Box<TreeNode>>) -> usize {
        if let Some(n) = node {
            let (_, d1) = max_diameter_helper(&n);
            let d2 = max_diameter(&n.left);
            let d3 = max_diameter(&n.right);
            d1.max(d2).max(d3)
        } else {
            0
        }
    }

    fn max_diameter_helper(node: &TreeNode) -> (usize, usize) {
        /* Returns (depth, max_diameter_in_subtree) */
        match (&node.left, &node.right) {
            (None, None) => (0, 0),
            (Some(left), None) => {
                let (ld, lm) = max_diameter_helper(left);
                (ld + 1, lm.max(ld))
            }
            (None, Some(right)) => {
                let (rd, rm) = max_diameter_helper(right);
                (rd + 1, rm.max(rd))
            }
            (Some(left), Some(right)) => {
                let (ld, lm) = max_diameter_helper(left);
                let (rd, rm) = max_diameter_helper(right);
                let depth = 1 + ld.max(rd);
                let diameter_through = ld + rd;
                let max_diam = diameter_through.max(lm).max(rm);
                (depth, max_diam)
            }
        }
    }

    max_diameter(root)
}

fn max_independent_set_tree(root: &Option<Box<TreeNode>>) -> i32 {
    /*
     * Maximum Independent Set on Tree - O(n) time, O(h) space
     * Pattern: Tree DP - max nodes with no two adjacent
     * Returns (include_root, exclude_root)
     */
    fn dfs(node: &Option<Box<TreeNode>>) -> (i32, i32) {
        if let Some(n) = node {
            let (left_inc, left_exc) = dfs(&n.left);
            let (right_inc, right_exc) = dfs(&n.right);

            let include = n.val + left_exc + right_exc;
            let exclude = left_inc.max(left_exc) + right_inc.max(right_exc);

            (include, exclude)
        } else {
            (0, 0)
        }
    }

    let (inc, exc) = dfs(root);
    inc.max(exc)
}

// ============================================================================
// PATTERN 5: Game Theory DP - Optimal Strategy
// ============================================================================

fn optimal_game_strategy(coins: &[i32]) -> i32 {
    /*
     * Optimal Strategy Game - O(n^2) time, O(n^2) space
     * Pattern: Game Theory DP (Minimax)
     * Two players pick from ends, maximize your score assuming opponent plays optimally
     */
    let n = coins.len();
    let mut dp = vec![vec![0; n]; n];

    for i in 0..n {
        dp[i][i] = coins[i];
    }

    for length in 2..=n {
        for i in 0..(n - length + 1) {
            let j = i + length - 1;
            let pick_left = coins[i] + dp[i + 2].get(j).unwrap_or(&0).min(
                dp.get(i + 1).and_then(|row| row.get(j - 1)).unwrap_or(&0)
            );
            let pick_right = coins[j] + dp.get(i + 1).and_then(|row| row.get(j - 1)).unwrap_or(&0).min(
                dp.get(i).and_then(|row| row.get(j - 2)).unwrap_or(&0)
            );
            dp[i][j] = pick_left.max(pick_right);
        }
    }

    dp[0][n - 1]
}

fn coin_game(coins: &[i32]) -> i32 {
    /*
     * Coin Game - O(n^2) time, O(n^2) space
     * Pattern: Game Theory DP - max difference (player1 - player2) with optimal play
     */
    let n = coins.len();
    let mut dp = vec![vec![0; n]; n];

    for i in 0..n {
        dp[i][i] = coins[i];
    }

    for length in 2..=n {
        for i in 0..(n - length + 1) {
            let j = i + length - 1;
            dp[i][j] = (coins[i] - dp[i + 1][j]).max(coins[j] - dp[i][j - 1]);
        }
    }

    dp[0][n - 1]
}

// ============================================================================
// PATTERN 6: Probability DP - Expected Values
// ============================================================================

fn expected_dice_rolls(target: usize) -> f64 {
    /*
     * Expected Number of Dice Rolls to Reach Target - O(target) time, O(target) space
     * Pattern: Probability DP
     * E[x] = 1 + (E[x-1] + E[x-2] + ... + E[x-6]) / 6
     */
    if target == 0 {
        return 0.0;
    }

    let mut dp = vec![0.0; target + 1];

    for i in 1..=target {
        dp[i] = 1.0;
        for j in 1..=6 {
            if i >= j {
                dp[i] += dp[i - j] / 6.0;
            }
        }
    }

    dp[target]
}

// ============================================================================
// TESTING
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_climb_stairs() {
        assert_eq!(climb_stairs(2), 2);
        assert_eq!(climb_stairs(3), 3);
        assert_eq!(climb_stairs(5), 8);
    }

    #[test]
    fn test_house_robber() {
        assert_eq!(house_robber(&[1, 2, 3, 1]), 4);
        assert_eq!(house_robber(&[2, 7, 9, 3, 1]), 12);
    }

    #[test]
    fn test_coin_change() {
        assert_eq!(coin_change(&[1, 2, 5], 11), 3);
        assert_eq!(coin_change(&[2], 3), -1);
    }

    #[test]
    fn test_longest_common_subsequence() {
        assert_eq!(longest_common_subsequence("abcde", "ace"), 3);
        assert_eq!(longest_common_subsequence("abc", "abc"), 3);
        assert_eq!(longest_common_subsequence("abc", "def"), 0);
    }

    #[test]
    fn test_edit_distance() {
        assert_eq!(edit_distance("horse", "ros"), 3);
        assert_eq!(edit_distance("intention", "execution"), 5);
    }

    #[test]
    fn test_knapsack_01() {
        assert_eq!(knapsack_01(&[1, 3, 4, 5], &[1, 4, 5, 7], 7), 9);
    }

    #[test]
    fn test_target_sum() {
        assert_eq!(target_sum(&[1, 1, 1, 1, 1], 3), 5);
    }

    #[test]
    fn test_min_palindrome_cuts() {
        assert_eq!(min_palindrome_cuts("aab"), 1);
        assert_eq!(min_palindrome_cuts("a"), 0);
    }

    #[test]
    fn test_burst_balloons() {
        assert_eq!(burst_balloons(&[3, 1, 5, 8]), 167);
    }

    #[test]
    fn test_tree_diameter() {
        let mut root = TreeNode::new(1);
        let mut left = TreeNode::new(2);
        let right = TreeNode::new(3);
        left.left = Some(Box::new(TreeNode::new(4)));
        left.right = Some(Box::new(TreeNode::new(5)));
        root.left = Some(Box::new(left));
        root.right = Some(Box::new(right));

        assert_eq!(tree_diameter(&Some(Box::new(root))), 3);
    }

    #[test]
    fn test_max_independent_set() {
        let mut root = TreeNode::new(1);
        let mut left = TreeNode::new(2);
        let right = TreeNode::new(3);
        left.left = Some(Box::new(TreeNode::new(4)));
        left.right = Some(Box::new(TreeNode::new(5)));
        root.left = Some(Box::new(left));
        root.right = Some(Box::new(right));

        assert_eq!(max_independent_set_tree(&Some(Box::new(root))), 12);
    }

    #[test]
    fn test_optimal_game_strategy() {
        assert_eq!(optimal_game_strategy(&[8, 15, 3, 7]), 22);
    }

    #[test]
    fn test_expected_dice_rolls() {
        let result = expected_dice_rolls(10);
        assert!(result > 0.0, "Expected value should be positive");
    }
}
