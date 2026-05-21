/// Day 12: Advanced Dynamic Programming - Part 2
/// Rust Implementations

use std::collections::HashMap;

// =============================================================================
// 1. Tree Diameter with DP
// =============================================================================

/// Tree Diameter - O(n) time, O(n) space
fn tree_diameter(tree: &[Vec<usize>]) -> usize {
    let mut diameter = 0;
    
    fn dfs(node: usize, parent: usize, tree: &[Vec<usize>], diameter: &mut usize) -> usize {
        let mut max_height1 = 0;
        let mut max_height2 = 0;
        
        for &child in &tree[node] {
            if child != parent {
                let height = dfs(child, node, tree, diameter);
                
                if height > max_height1 {
                    max_height2 = max_height1;
                    max_height1 = height;
                } else if height > max_height2 {
                    max_height2 = height;
                }
            }
        }
        
        *diameter = (*diameter).max(max_height1 + max_height2);
        max_height1 + 1
    }
    
    dfs(0, usize::MAX, tree, &mut diameter);
    diameter
}

// =============================================================================
// 2. Maximum Independent Set on Trees
// =============================================================================

/// Maximum Independent Set on Trees - O(n) time, O(n) space
fn max_independent_set_tree(tree: &[Vec<usize>]) -> usize {
    let n = tree.len();
    let mut dp = vec![[0, 0]; n];
    
    fn dfs(node: usize, parent: usize, tree: &[Vec<usize>], dp: &mut [[usize; 2]]) {
        dp[node][1] = 1;  // Include this node
        
        for &child in &tree[node] {
            if child != parent {
                dfs(child, node, tree, dp);
                // If node not included, children can be included or not
                dp[node][0] += dp[child][0].max(dp[child][1]);
                // If node included, children cannot be included
                dp[node][1] += dp[child][0];
            }
        }
    }
    
    dfs(0, usize::MAX, tree, &mut dp);
    dp[0][0].max(dp[0][1])
}

// =============================================================================
// 3. Traveling Salesman Problem (Bitmask DP)
// =============================================================================

/// TSP with Bitmask DP - O(n^2 * 2^n) time, O(n * 2^n) space
fn tsp(dist: &[Vec<i32>]) -> i32 {
    let n = dist.len();
    let inf = i32::MAX / 2;
    let num_states = 1 << n;
    
    // dp[mask][i] = min cost to visit all cities in mask, ending at i
    let mut dp = vec![vec![inf; n]; num_states];
    dp[1][0] = 0;  // Start at city 0
    
    for mask in 1..num_states {
        for i in 0..n {
            if dp[mask][i] == inf {
                continue;
            }
            
            // Try to visit next city j
            for j in 0..n {
                if mask & (1 << j) == 0 {  // If j not visited
                    let new_mask = mask | (1 << j);
                    dp[new_mask][j] = dp[new_mask][j].min(dp[mask][i] + dist[i][j]);
                }
            }
        }
    }
    
    // Return to start
    let full_mask = num_states - 1;
    (1..n).map(|i| dp[full_mask][i] + dist[i][0]).min().unwrap()
}

// =============================================================================
// 4. Assignment Problem (Bitmask DP)
// =============================================================================

/// Assignment Problem - O(n * 2^n) time, O(2^n) space
fn assignment_problem(cost: &[Vec<i32>]) -> i32 {
    let n = cost.len();
    let inf = i32::MAX / 2;
    let num_states = 1 << n;
    
    // dp[mask] = min cost to assign jobs in mask to first k workers
    let mut dp = vec![inf; num_states];
    dp[0] = 0;
    
    // Process masks by number of set bits (workers assigned so far)
    for worker in 0..n {
        // For each mask with 'worker' bits set
        for mask in 0..num_states {
            if mask.count_ones() as usize != worker {
                continue;
            }
            if dp[mask] == inf {
                continue;
            }
            
            // Try to assign job j to current worker
            for j in 0..n {
                if mask & (1 << j) == 0 {  // If job j not yet assigned
                    let new_mask = mask | (1 << j);
                    dp[new_mask] = dp[new_mask].min(dp[mask] + cost[worker][j]);
                }
            }
        }
    }
    
    dp[num_states - 1]
}

// =============================================================================
// 5. Digit DP - Count Numbers Without Digit 4
// =============================================================================

/// Count numbers from 0 to n without digit 4 - O(log(n)) time, O(log(n)) space
fn count_without_digit_4(n: i64) -> i64 {
    let digits: Vec<i32> = n.to_string()
        .chars()
        .map(|c| c.to_digit(10).unwrap() as i32)
        .collect();
    
    let mut memo = HashMap::new();
    
    fn dp(pos: usize, tight: bool, started: bool, 
          digits: &[i32], memo: &mut HashMap<(usize, bool, bool), i64>) -> i64 {
        if pos == digits.len() {
            return if started { 1 } else { 0 };
        }
        
        let state = (pos, tight, started);
        if let Some(&count) = memo.get(&state) {
            return count;
        }
        
        let limit = if tight { digits[pos] } else { 9 };
        let mut count = 0;
        
        for digit in 0..=limit {
            if digit == 4 {
                continue;
            }
            
            let new_tight = tight && (digit == limit);
            let new_started = started || (digit > 0);
            count += dp(pos + 1, new_tight, new_started, digits, memo);
        }
        
        memo.insert(state, count);
        count
    }
    
    dp(0, true, false, &digits, &mut memo) + 1  // +1 for number 0
}

// =============================================================================
// 6. Digit DP - Count Numbers with Digit Sum K
// =============================================================================

/// Count numbers from 0 to n with digit sum k - O(log(n) * k) time, O(log(n) * k) space
fn count_with_digit_sum_k(n: i64, k: i32) -> i64 {
    let digits: Vec<i32> = n.to_string()
        .chars()
        .map(|c| c.to_digit(10).unwrap() as i32)
        .collect();
    
    let mut memo = HashMap::new();
    
    fn dp(pos: usize, tight: bool, sum_digits: i32, started: bool,
          k: i32, digits: &[i32], memo: &mut HashMap<(usize, bool, i32, bool), i64>) -> i64 {
        if sum_digits > k {
            return 0;
        }
        
        if pos == digits.len() {
            return if started && sum_digits == k { 1 } else { 0 };
        }
        
        let state = (pos, tight, sum_digits, started);
        if let Some(&count) = memo.get(&state) {
            return count;
        }
        
        let limit = if tight { digits[pos] } else { 9 };
        let mut count = 0;
        
        for digit in 0..=limit {
            let new_tight = tight && (digit == limit);
            let new_started = started || (digit > 0);
            count += dp(pos + 1, new_tight, sum_digits + digit, new_started, 
                       k, digits, memo);
        }
        
        memo.insert(state, count);
        count
    }
    
    dp(0, true, 0, false, k, &digits, &mut memo)
}

// =============================================================================
// 7. Matrix Chain Multiplication
// =============================================================================

/// Matrix Chain Order - O(n^3) time, O(n^2) space
fn matrix_chain_order(dimensions: &[usize]) -> usize {
    let n = dimensions.len() - 1;  // Number of matrices
    let mut dp = vec![vec![0; n]; n];
    
    // l is chain length
    for l in 2..=n {
        for i in 0..=n - l {
            let j = i + l - 1;
            dp[i][j] = usize::MAX;
            
            for k in i..j {
                let cost = dp[i][k] + dp[k + 1][j] + 
                          dimensions[i] * dimensions[k + 1] * dimensions[j + 1];
                dp[i][j] = dp[i][j].min(cost);
            }
        }
    }
    
    dp[0][n - 1]
}

// =============================================================================
// 8. Boolean Parenthesization
// =============================================================================

/// Boolean Parenthesization - O(n^3) time, O(n^2) space
fn boolean_parenthesization(symbols: &[char], operators: &[char]) -> usize {
    let n = symbols.len();
    
    // dpT[i][j] = ways to get True from symbols[i..j]
    // dpF[i][j] = ways to get False from symbols[i..j]
    let mut dpT = vec![vec![0; n]; n];
    let mut dpF = vec![vec![0; n]; n];
    
    // Base case: single symbols
    for i in 0..n {
        if symbols[i] == 'T' {
            dpT[i][i] = 1;
            dpF[i][i] = 0;
        } else {
            dpT[i][i] = 0;
            dpF[i][i] = 1;
        }
    }
    
    // Fill for increasing lengths
    for length in 2..=n {
        for i in 0..=n - length {
            let j = i + length - 1;
            dpT[i][j] = 0;
            dpF[i][j] = 0;
            
            for k in i..j {
                let op = operators[k];
                
                let total_left = dpT[i][k] + dpF[i][k];
                let total_right = dpT[k + 1][j] + dpF[k + 1][j];
                
                match op {
                    '&' => {
                        dpT[i][j] += dpT[i][k] * dpT[k + 1][j];
                        dpF[i][j] += total_left * total_right - dpT[i][k] * dpT[k + 1][j];
                    }
                    '|' => {
                        dpF[i][j] += dpF[i][k] * dpF[k + 1][j];
                        dpT[i][j] += total_left * total_right - dpF[i][k] * dpF[k + 1][j];
                    }
                    '^' => {
                        dpT[i][j] += dpT[i][k] * dpF[k + 1][j] + dpF[i][k] * dpT[k + 1][j];
                        dpF[i][j] += dpT[i][k] * dpT[k + 1][j] + dpF[i][k] * dpF[k + 1][j];
                    }
                    _ => {}
                }
            }
        }
    }
    
    dpT[0][n - 1]
}

// =============================================================================
// Tests
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tree_diameter() {
        // Test 1: Simple tree
        //       0
        //      / \
        //     1   2
        //    / \
        //   3   4
        let tree1 = vec![vec![1, 2], vec![3, 4], vec![], vec![], vec![]];
        assert_eq!(tree_diameter(&tree1), 3, "Test 1 failed");
        
        // Test 2: Linear tree (path)
        // 0 - 1 - 2 - 3 - 4
        let tree2 = vec![vec![1], vec![0, 2], vec![1, 3], vec![2, 4], vec![3]];
        assert_eq!(tree_diameter(&tree2), 4, "Test 2 failed");
        
        // Test 3: Star tree
        //     0
        //   / | \
        //  1  2  3
        let tree3 = vec![vec![1, 2, 3], vec![0], vec![0], vec![0]];
        assert_eq!(tree_diameter(&tree3), 2, "Test 3 failed");
    }

    #[test]
    fn test_max_independent_set() {
        // Test 1: Simple tree
        let tree1 = vec![vec![1, 2], vec![3, 4], vec![], vec![], vec![]];
        assert_eq!(max_independent_set_tree(&tree1), 3, "Test 1 failed");
        
        // Test 2: Linear tree
        let tree2 = vec![vec![1], vec![0, 2], vec![1, 3], vec![2, 4], vec![3]];
        assert_eq!(max_independent_set_tree(&tree2), 3, "Test 2 failed");
        
        // Test 3: Star tree
        let tree3 = vec![vec![1, 2, 3], vec![0], vec![0], vec![0]];
        assert_eq!(max_independent_set_tree(&tree3), 3, "Test 3 failed");
    }

    #[test]
    fn test_tsp() {
        // Test 1: 4 cities
        let dist1 = vec![
            vec![0, 10, 15, 20],
            vec![10, 0, 35, 25],
            vec![15, 35, 0, 30],
            vec![20, 25, 30, 0]
        ];
        assert_eq!(tsp(&dist1), 80, "Test 1 failed");
        
        // Test 2: 3 cities (triangle)
        let dist2 = vec![
            vec![0, 10, 20],
            vec![10, 0, 15],
            vec![20, 15, 0]
        ];
        assert_eq!(tsp(&dist2), 45, "Test 2 failed");
    }

    #[test]
    fn test_assignment_problem() {
        // Test 1: 3 workers, 3 jobs
        let cost1 = vec![
            vec![10, 2, 6],
            vec![5, 7, 3],
            vec![6, 8, 9]
        ];
        assert_eq!(assignment_problem(&cost1), 11, "Test 1 failed");  // 2 + 3 + 6
        
        // Test 2: 2 workers, 2 jobs
        let cost2 = vec![
            vec![1, 2],
            vec![2, 1]
        ];
        assert_eq!(assignment_problem(&cost2), 2, "Test 2 failed");
    }

    #[test]
    fn test_count_without_digit_4() {
        assert_eq!(count_without_digit_4(10), 10, "Test 1 failed");  // 0-10 except 4
        assert_eq!(count_without_digit_4(100), 82, "Test 2 failed");
        assert_eq!(count_without_digit_4(4), 4, "Test 3 failed");  // 0,1,2,3
        assert_eq!(count_without_digit_4(14), 13, "Test 4 failed");  // 0-14 except 4,14
    }

    #[test]
    fn test_count_with_digit_sum_k() {
        assert_eq!(count_with_digit_sum_k(20, 5), 2, "Test 1 failed");  // 5, 14
        assert_eq!(count_with_digit_sum_k(100, 1), 3, "Test 2 failed");  // 1, 10, 100
        assert_eq!(count_with_digit_sum_k(10, 10), 0, "Test 3 failed");
    }

    #[test]
    fn test_matrix_chain_order() {
        // Test 1: A1(10x30), A2(30x5), A3(5x60)
        let dims1 = vec![10, 30, 5, 60];
        assert_eq!(matrix_chain_order(&dims1), 4500, "Test 1 failed");
        
        // Test 2: A1(5x10), A2(10x3), A3(3x12), A4(12x5)
        let dims2 = vec![5, 10, 3, 12, 5];
        assert_eq!(matrix_chain_order(&dims2), 405, "Test 2 failed");
        
        // Test 3: Two matrices only
        let dims3 = vec![10, 20, 30];
        assert_eq!(matrix_chain_order(&dims3), 6000, "Test 3 failed");
    }

    #[test]
    fn test_boolean_parenthesization() {
        // Test 1: T | T & F
        let symbols1 = vec!['T', 'T', 'F'];
        let ops1 = vec!['|', '&'];
        assert_eq!(boolean_parenthesization(&symbols1, &ops1), 1, "Test 1 failed");
        
        // Test 2: T ^ T ^ T
        let symbols2 = vec!['T', 'T', 'T'];
        let ops2 = vec!['^', '^'];
        assert_eq!(boolean_parenthesization(&symbols2, &ops2), 2, "Test 2 failed");  // Both ways give True
        
        // Test 3: T | T | T
        let symbols3 = vec!['T', 'T', 'T'];
        let ops3 = vec!['|', '|'];
        assert_eq!(boolean_parenthesization(&symbols3, &ops3), 2, "Test 3 failed");
    }
}
