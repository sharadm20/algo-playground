/// Day 13: More Advanced Dynamic Programming
/// Rust Implementations
/// 
/// Topics: Interval DP, Game Theory DP, Probability DP, Advanced Patterns

// =============================================================================
// 1. Palindrome Partitioning (Minimum Cuts)
// =============================================================================

/// Minimum cuts to partition string into palindromes - O(n^2) time, O(n^2) space
fn min_palindrome_cuts(s: &str) -> usize {
    let chars: Vec<char> = s.chars().collect();
    let n = chars.len();
    if n <= 1 {
        return 0;
    }

    // Precompute palindrome table
    let mut is_pal = vec![vec![false; n]; n];

    // All single chars are palindromes
    for i in 0..n {
        is_pal[i][i] = true;
    }

    // Check for length 2
    for i in 0..n - 1 {
        is_pal[i][i + 1] = chars[i] == chars[i + 1];
    }

    // Check for length > 2
    for length in 3..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            is_pal[i][j] = chars[i] == chars[j] && is_pal[i + 1][j - 1];
        }
    }

    // DP for minimum cuts
    let mut cuts: Vec<usize> = (0..n).collect();

    for i in 1..n {
        if is_pal[0][i] {
            cuts[i] = 0;
        } else {
            for j in 0..i {
                if is_pal[j + 1][i] {
                    cuts[i] = cuts[i].min(cuts[j] + 1);
                }
            }
        }
    }

    cuts[n - 1]
}

// =============================================================================
// 2. Burst Balloons
// =============================================================================

/// Maximize coins from bursting balloons - O(n^3) time, O(n^2) space
fn max_coins_burst_balloons(nums: &[i32]) -> i32 {
    let mut nums_extended = vec![1];
    nums_extended.extend_from_slice(nums);
    nums_extended.push(1);
    
    let n = nums_extended.len();
    let mut dp = vec![vec![0; n]; n];

    // Fill for increasing lengths
    for length in 1..=n - 2 {
        for i in 1..=n - length - 1 {
            let j = i + length - 1;
            // Try each k as the LAST balloon to burst in [i, j]
            for k in i..=j {
                let coins = dp[i][k - 1] + dp[k + 1][j] + nums_extended[i - 1] * nums_extended[k] * nums_extended[j + 1];
                dp[i][j] = dp[i][j].max(coins);
            }
        }
    }

    dp[1][n - 2]
}

// =============================================================================
// 3. Stone Merge Problem
// =============================================================================

/// Minimum cost to merge all piles into one - O(n^3) time, O(n^2) space
fn min_stone_merge_cost(stones: &[usize]) -> usize {
    let n = stones.len();
    if n <= 1 {
        return 0;
    }

    // Precompute prefix sums
    let mut prefix_sum = vec![0; n + 1];
    for i in 0..n {
        prefix_sum[i + 1] = prefix_sum[i] + stones[i];
    }

    let range_sum = |i: usize, j: usize| -> usize {
        prefix_sum[j + 1] - prefix_sum[i]
    };

    // dp[i][j] = min cost to merge stones[i..j]
    let mut dp = vec![vec![0; n]; n];

    // Fill for increasing lengths
    for length in 2..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            dp[i][j] = usize::MAX;
            for k in i..j {
                let cost = dp[i][k] + dp[k + 1][j] + range_sum(i, j);
                dp[i][j] = dp[i][j].min(cost);
            }
        }
    }

    dp[0][n - 1]
}

// =============================================================================
// 4. Optimal Game Strategy
// =============================================================================

/// Maximum value Player 1 can get when both play optimally - O(n^2) time, O(n^2) space
fn optimal_game_strategy(values: &[i32]) -> i32 {
    let n = values.len();
    let mut dp = vec![vec![0; n]; n];

    // Base case: single element
    for i in 0..n {
        dp[i][i] = values[i];
    }

    // Fill for increasing lengths
    for length in 2..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            dp[i][j] = (values[i] - dp[i + 1][j]).max(values[j] - dp[i][j - 1]);
        }
    }

    // Player 1's score = (total + diff) / 2
    let total: i32 = values.iter().sum();
    let diff = dp[0][n - 1];
    (total + diff) / 2
}

/// Can Player 1 win (get >= half of total)? - O(n^2) time, O(n^2) space
fn can_first_player_win(values: &[i32]) -> bool {
    let n = values.len();
    let mut dp = vec![vec![0; n]; n];

    for i in 0..n {
        dp[i][i] = values[i];
    }

    for length in 2..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            dp[i][j] = (values[i] - dp[i + 1][j]).max(values[j] - dp[i][j - 1]);
        }
    }

    dp[0][n - 1] >= 0
}

// =============================================================================
// 5. Nim Game
// =============================================================================

/// Can first player win Nim game? - O(1) time, O(1) space
fn can_win_nim(n: i32, max_removal: i32) -> bool {
    n % (max_removal + 1) != 0
}

// =============================================================================
// 6. Coin Game (Pick from Ends)
// =============================================================================

/// Maximum value first player can guarantee getting - O(n^2) time, O(n^2) space
fn coin_game_max_value(coins: &[i32]) -> i32 {
    let n = coins.len();
    if n == 0 {
        return 0;
    }

    let mut dp = vec![vec![0; n]; n];

    // Base case: single coin
    for i in 0..n {
        dp[i][i] = coins[i];
    }

    // Base case: two coins
    for i in 0..n - 1 {
        dp[i][i + 1] = coins[i].max(coins[i + 1]);
    }

    // Fill for length >= 3
    for length in 3..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            let pick_left = coins[i] + 
                (if i + 2 <= j { dp[i + 2][j] } else { 0 })
                    .min(if i + 1 <= j - 1 { dp[i + 1][j - 1] } else { 0 });
            let pick_right = coins[j] + 
                (if i + 1 <= j - 1 { dp[i + 1][j - 1] } else { 0 })
                    .min(if i <= j - 2 { dp[i][j - 2] } else { 0 });
            dp[i][j] = pick_left.max(pick_right);
        }
    }

    dp[0][n - 1]
}

// =============================================================================
// 7. Expected Rolls (Dice Problem)
// =============================================================================

/// Expected number of rolls to get a specific face - O(1) time, O(1) space
fn expected_rolls_for_face(face_prob: f64) -> f64 {
    1.0 / face_prob
}

/// Expected rolls to see all faces (Coupon Collector) - O(n) time, O(1) space
fn expected_rolls_for_all_faces(num_faces: usize) -> f64 {
    let harmonic: f64 = (1..=num_faces).map(|i| 1.0 / i as f64).sum();
    num_faces as f64 * harmonic
}

// =============================================================================
// 8. Random Walk Expected Steps
// =============================================================================

/// Expected steps to reach target from 0 in 1D random walk - O(1) time, O(1) space
fn random_walk_expected_steps(target: i32) -> i32 {
    target * target
}

// =============================================================================
// 9. Grid Path Counting
// =============================================================================

/// Unique paths from top-left to bottom-right - O(m*n) time, O(n) space
fn grid_unique_paths(m: usize, n: usize) -> usize {
    let mut dp = vec![1; n];

    for _ in 1..m {
        for j in 1..n {
            dp[j] += dp[j - 1];
        }
    }

    dp[n - 1]
}

/// Unique paths with obstacles - O(m*n) time, O(n) space
fn grid_unique_paths_with_obstacles(grid: &[Vec<i32>]) -> usize {
    if grid.is_empty() || grid[0].is_empty() {
        return 0;
    }

    let m = grid.len();
    let n = grid[0].len();
    let mut dp = vec![0; n];
    dp[0] = if grid[0][0] == 0 { 1 } else { 0 };

    for i in 0..m {
        for j in 0..n {
            if grid[i][j] == 1 {
                dp[j] = 0;
            } else if j > 0 {
                dp[j] += dp[j - 1];
            }
        }
    }

    dp[n - 1]
}

// =============================================================================
// Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_min_palindrome_cuts() {
        assert_eq!(min_palindrome_cuts("aab"), 1, "Test 1 failed");
        assert_eq!(min_palindrome_cuts("a"), 0, "Test 2 failed");
        assert_eq!(min_palindrome_cuts("ab"), 1, "Test 3 failed");
        assert_eq!(min_palindrome_cuts("aba"), 0, "Test 4 failed");
        assert_eq!(min_palindrome_cuts("abcba"), 0, "Test 5 failed");
    }

    #[test]
    fn test_burst_balloons() {
        assert_eq!(max_coins_burst_balloons(&[3, 1, 5, 8]), 167, "Test 1 failed");
        assert_eq!(max_coins_burst_balloons(&[1, 5]), 10, "Test 2 failed");
        assert_eq!(max_coins_burst_balloons(&[10]), 10, "Test 3 failed");
    }

    #[test]
    fn test_stone_merge() {
        assert_eq!(min_stone_merge_cost(&[1, 2, 3, 4, 5]), 33, "Test 1 failed");
        assert_eq!(min_stone_merge_cost(&[1, 2, 3]), 9, "Test 2 failed");
        assert_eq!(min_stone_merge_cost(&[5]), 0, "Test 3 failed");
    }

    #[test]
    fn test_optimal_game_strategy() {
        assert_eq!(optimal_game_strategy(&[8, 15, 3, 7]), 22, "Test 1 failed");
        assert_eq!(optimal_game_strategy(&[1, 2, 3, 4]), 6, "Test 2 failed");
        assert_eq!(optimal_game_strategy(&[5, 3, 7, 10]), 15, "Test 3 failed");
    }

    #[test]
    fn test_can_first_player_win() {
        assert_eq!(can_first_player_win(&[1, 2, 3]), true, "Test 1 failed");
        assert_eq!(can_first_player_win(&[1, 1]), true, "Test 2 failed");
    }

    #[test]
    fn test_nim_game() {
        assert_eq!(can_win_nim(4, 3), false, "Test 1 failed");
        assert_eq!(can_win_nim(1, 3), true, "Test 2 failed");
        assert_eq!(can_win_nim(5, 3), true, "Test 3 failed");
        assert_eq!(can_win_nim(8, 3), false, "Test 4 failed");
    }

    #[test]
    fn test_coin_game() {
        assert_eq!(coin_game_max_value(&[5, 3, 7, 10]), 15, "Test 1 failed");
        assert_eq!(coin_game_max_value(&[8, 15, 3, 7]), 22, "Test 2 failed");
        assert_eq!(coin_game_max_value(&[1, 2]), 2, "Test 3 failed");
    }

    #[test]
    fn test_expected_rolls() {
        assert!((expected_rolls_for_face(1.0/6.0) - 6.0).abs() < 0.01, "Test 1 failed");
        let expected_6 = expected_rolls_for_all_faces(6);
        assert!(14.0 < expected_6 && expected_6 < 15.0, "Test 2 failed: got {}", expected_6);
    }

    #[test]
    fn test_random_walk() {
        assert_eq!(random_walk_expected_steps(1), 1, "Test 1 failed");
        assert_eq!(random_walk_expected_steps(2), 4, "Test 2 failed");
        assert_eq!(random_walk_expected_steps(3), 9, "Test 3 failed");
        assert_eq!(random_walk_expected_steps(5), 25, "Test 4 failed");
    }

    #[test]
    fn test_grid_paths() {
        assert_eq!(grid_unique_paths(3, 7), 28, "Test 1 failed");
        assert_eq!(grid_unique_paths(3, 2), 3, "Test 2 failed");
        assert_eq!(grid_unique_paths(1, 1), 1, "Test 3 failed");

        let grid1 = vec![vec![0, 0, 0], vec![0, 1, 0], vec![0, 0, 0]];
        assert_eq!(grid_unique_paths_with_obstacles(&grid1), 2, "Test 4 failed");

        let grid2 = vec![vec![0, 1], vec![0, 0]];
        assert_eq!(grid_unique_paths_with_obstacles(&grid2), 1, "Test 5 failed");
    }
}
