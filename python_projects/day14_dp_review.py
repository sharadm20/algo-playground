"""
Day 14: DP Review & Practice
Topics: Mixed DP problems, pattern recognition, optimization techniques
Covers: 1D DP, 2D DP, Interval DP, Tree DP, Bitmask DP, Game Theory DP, Probability DP
"""

from typing import List, Tuple, Optional, Dict
from collections import defaultdict


# ============================================================================
# PATTERN 1: 1D DP - Fibonacci Variants
# ============================================================================
def climb_stairs(n: int) -> int:
    """
    Climbing Stairs - O(n) time, O(1) space
    Pattern: 1D DP with space optimization
    Each step you can climb 1 or 2 stairs.
    """
    if n <= 2:
        return n

    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr

    return prev1


def house_robber(nums: List[int]) -> int:
    """
    House Robber - O(n) time, O(1) space
    Pattern: 1D DP - max amount without robbing adjacent houses.
    dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2, prev1 = 0, nums[0]
    for i in range(1, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = curr

    return prev1


def coin_change(coins: List[int], amount: int) -> int:
    """
    Coin Change - O(amount * len(coins)) time, O(amount) space
    Pattern: 1D DP - minimum coins to make up amount.
    dp[i] = min(dp[i - coin] + 1) for all coins
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


# ============================================================================
# PATTERN 2: 2D DP - LCS, Edit Distance, Knapsack
# ============================================================================
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Longest Common Subsequence - O(m*n) time, O(m*n) space
    Pattern: 2D DP
    dp[i][j] = LCS of text1[:i] and text2[:j]
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def edit_distance(word1: str, word2: str) -> int:
    """
    Edit Distance - O(m*n) time, O(m*n) space
    Pattern: 2D DP - minimum operations to convert word1 to word2.
    Operations: insert, delete, replace
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # delete
                                   dp[i][j - 1],      # insert
                                   dp[i - 1][j - 1])  # replace

    return dp[m][n]


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack - O(n*capacity) time, O(capacity) space
    Pattern: 2D DP with space optimization
    dp[w] = max value with capacity w
    """
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


def target_sum(nums: List[int], target: int) -> int:
    """
    Target Sum - O(n*sum) time, O(sum) space
    Pattern: 2D DP - count ways to assign +/- to reach target.
    Transform: count subsets with sum = (total + target) / 2
    """
    total = sum(nums)
    if abs(target) > total or (total + target) % 2 != 0:
        return 0

    subset_sum = (total + target) // 2
    dp = [0] * (subset_sum + 1)
    dp[0] = 1

    for num in nums:
        for s in range(subset_sum, num - 1, -1):
            dp[s] += dp[s - num]

    return dp[subset_sum]


# ============================================================================
# PATTERN 3: Interval DP - Palindrome Partitioning, Burst Balloons
# ============================================================================
def min_palindrome_cuts(s: str) -> int:
    """
    Palindrome Partitioning II - O(n^2) time, O(n^2) space
    Pattern: Interval DP - minimum cuts to partition into palindromes.
    """
    n = len(s)
    if n <= 1:
        return 0

    # is_pal[i][j] = True if s[i:j+1] is palindrome
    is_pal = [[False] * n for _ in range(n)]
    # dp[i] = min cuts for s[0:i+1]
    dp = [0] * n

    for i in range(n):
        min_cuts = i  # worst case: cut each character
        for j in range(i + 1):
            if s[i] == s[j] and (i - j <= 2 or is_pal[j + 1][i - 1]):
                is_pal[j][i] = True
                if j == 0:
                    min_cuts = 0
                else:
                    min_cuts = min(min_cuts, dp[j - 1] + 1)
        dp[i] = min_cuts

    return dp[n - 1]


def burst_balloons(nums: List[int]) -> int:
    """
    Burst Balloons - O(n^3) time, O(n^2) space
    Pattern: Interval DP
    Add virtual balloons at ends, dp[i][j] = max coins from bursting balloons in (i, j)
    """
    # Add virtual balloons with value 1 at both ends
    balloons = [1] + nums + [1]
    n = len(balloons)

    # dp[i][j] = max coins from bursting balloons in range (i, j) exclusive
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):  # length of interval
        for i in range(n - length):
            j = i + length
            # Try bursting each balloon k in (i, j) last
            for k in range(i + 1, j):
                coins = balloons[i] * balloons[k] * balloons[j]
                dp[i][j] = max(dp[i][j], dp[i][k] + coins + dp[k][j])

    return dp[0][n - 1]


# ============================================================================
# PATTERN 4: Tree DP - Diameter, Max Independent Set
# ============================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tree_diameter(root: Optional[TreeNode]) -> int:
    """
    Tree Diameter - O(n) time, O(h) space
    Pattern: Tree DP - longest path between any two nodes.
    """
    diameter = [0]

    def depth(node: Optional[TreeNode]) -> int:
        if not node:
            return 0

        left_depth = depth(node.left)
        right_depth = depth(node.right)

        # Update diameter through this node
        diameter[0] = max(diameter[0], left_depth + right_depth)

        return 1 + max(left_depth, right_depth)

    depth(root)
    return diameter[0]


def max_independent_set_tree(root: Optional[TreeNode]) -> int:
    """
    Maximum Independent Set on Tree - O(n) time, O(h) space
    Pattern: Tree DP - max nodes with no two adjacent.
    Returns (include_root, exclude_root)
    """
    def dfs(node: Optional[TreeNode]) -> Tuple[int, int]:
        if not node:
            return 0, 0

        left_inc, left_exc = dfs(node.left)
        right_inc, right_exc = dfs(node.right)

        # Include this node: children must be excluded
        include = node.val + left_exc + right_exc
        # Exclude this node: children can be included or excluded
        exclude = max(left_inc, left_exc) + max(right_inc, right_exc)

        return include, exclude

    return max(dfs(root))


# ============================================================================
# PATTERN 5: Bitmask DP - TSP, Subset Sum
# ============================================================================
def tsp_held_karp(dist: List[List[int]]) -> int:
    """
    Traveling Salesman Problem (Held-Karp) - O(n^2 * 2^n) time, O(n * 2^n) space
    Pattern: Bitmask DP
    dp[mask][i] = min cost visiting cities in mask, ending at city i
    """
    n = len(dist)
    if n == 0:
        return 0

    # dp[mask][i] = min cost
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at city 0

    for mask in range(1, 1 << n):
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            if dp[mask][i] == float('inf'):
                continue

            # Try going to next city j
            for j in range(n):
                if mask & (1 << j):
                    continue
                new_mask = mask | (1 << j)
                dp[new_mask][j] = min(dp[new_mask][j],
                                      dp[mask][i] + dist[i][j])

    # Return to start (city 0)
    full_mask = (1 << n) - 1
    result = float('inf')
    for i in range(1, n):
        result = min(result, dp[full_mask][i] + dist[i][0])

    return result if result != float('inf') else 0


def subset_sum_bitmask(nums: List[int], target: int) -> bool:
    """
    Subset Sum with Bitmask - O(2^n) time, O(2^n) space
    Pattern: Bitmask DP - check if any subset sums to target.
    """
    n = len(nums)
    dp = {0: True}  # sum -> reachable

    for num in nums:
        new_sums = {}
        for s in dp:
            new_sum = s + num
            if new_sum == target:
                return True
            if new_sum <= target:
                new_sums[new_sum] = True
        dp.update(new_sums)

    return target in dp


# ============================================================================
# PATTERN 6: Game Theory DP - Optimal Strategy
# ============================================================================
def optimal_game_strategy(coins: List[int]) -> int:
    """
    Optimal Strategy Game - O(n^2) time, O(n^2) space
    Pattern: Game Theory DP (Minimax)
    Two players pick from ends, maximize your score assuming opponent plays optimally.
    Returns maximum value first player can get.
    """
    n = len(coins)
    # dp[i][j] = max value current player can get from coins[i:j+1]
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = coins[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Pick left: opponent will minimize your future gains
            pick_left = coins[i] + min(dp[i + 2][j] if i + 2 <= j else 0,
                                       dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)
            # Pick right: opponent will minimize your future gains
            pick_right = coins[j] + min(dp[i + 1][j - 1] if i + 1 <= j - 1 else 0,
                                        dp[i][j - 2] if i <= j - 2 else 0)
            dp[i][j] = max(pick_left, pick_right)

    return dp[0][n - 1]


def coin_game(coins: List[int]) -> int:
    """
    Coin Game - O(n^2) time, O(n^2) space
    Pattern: Game Theory DP - max difference (player1 - player2) with optimal play.
    """
    n = len(coins)
    # dp[i][j] = max difference current player can achieve from coins[i:j+1]
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = coins[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(coins[i] - dp[i + 1][j],
                          coins[j] - dp[i][j - 1])

    return dp[0][n - 1]


# ============================================================================
# PATTERN 7: Probability DP - Expected Values
# ============================================================================
def expected_dice_rolls(target: int) -> float:
    """
    Expected Number of Dice Rolls to Reach Target - O(target) time, O(target) space
    Pattern: Probability DP
    E[x] = 1 + (E[x-1] + E[x-2] + ... + E[x-6]) / 6
    """
    if target <= 0:
        return 0.0

    dp = [0.0] * (target + 1)

    for i in range(1, target + 1):
        dp[i] = 1.0
        for j in range(1, 7):
            if i - j >= 0:
                dp[i] += dp[i - j] / 6.0

    return dp[target]


def soup_servings(n: int) -> float:
    """
    Soup Servings - O(n^2) time, O(n^2) space (with scaling)
    Pattern: Probability DP
    Probability that soup A becomes empty first, plus half the probability both empty.
    Scales down for large n (approaches 1.0 for n > 4800).
    """
    if n > 4800:
        return 1.0

    # Scale down by 25
    n = (n + 24) // 25

    # Operations: (A, B) servings used
    operations = [(4, 0), (3, 1), (2, 2), (1, 3)]

    # dp[i][j] = probability A empty first + 0.5 * both empty from state (i, j)
    memo = {}

    def dfs(a: int, b: int) -> float:
        if a <= 0 and b <= 0:
            return 0.5
        if a <= 0:
            return 1.0
        if b <= 0:
            return 0.0
        if (a, b) in memo:
            return memo[(a, b)]

        memo[(a, b)] = sum(dfs(a - op_a, b - op_b)
                          for op_a, op_b in operations) / 4.0
        return memo[(a, b)]

    return dfs(n, n)


# ============================================================================
# TESTING
# ============================================================================
def test_all():
    print("=" * 80)
    print("Day 14: DP Review & Practice - Running Tests")
    print("=" * 80)

    # Test 1: Climbing Stairs
    print("\n1. Climbing Stairs (1D DP)")
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
    print("   ✓ Climbing Stairs tests passed")

    # Test 2: House Robber
    print("\n2. House Robber (1D DP)")
    assert house_robber([1, 2, 3, 1]) == 4
    assert house_robber([2, 7, 9, 3, 1]) == 12
    print("   ✓ House Robber tests passed")

    # Test 3: Coin Change
    print("\n3. Coin Change (1D DP)")
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    print("   ✓ Coin Change tests passed")

    # Test 4: Longest Common Subsequence
    print("\n4. Longest Common Subsequence (2D DP)")
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "abc") == 3
    assert longest_common_subsequence("abc", "def") == 0
    print("   ✓ LCS tests passed")

    # Test 5: Edit Distance
    print("\n5. Edit Distance (2D DP)")
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    print("   ✓ Edit Distance tests passed")

    # Test 6: 0/1 Knapsack
    print("\n6. 0/1 Knapsack (2D DP)")
    assert knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9
    print("   ✓ Knapsack tests passed")

    # Test 7: Target Sum
    print("\n7. Target Sum (2D DP)")
    assert target_sum([1, 1, 1, 1, 1], 3) == 5
    print("   ✓ Target Sum tests passed")

    # Test 8: Palindrome Partitioning
    print("\n8. Min Palindrome Cuts (Interval DP)")
    assert min_palindrome_cuts("aab") == 1
    assert min_palindrome_cuts("a") == 0
    print("   ✓ Palindrome Partitioning tests passed")

    # Test 9: Burst Balloons
    print("\n9. Burst Balloons (Interval DP)")
    assert burst_balloons([3, 1, 5, 8]) == 167
    print("   ✓ Burst Balloons tests passed")

    # Test 10: Tree Diameter
    print("\n10. Tree Diameter (Tree DP)")
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    assert tree_diameter(root) == 3
    print("   ✓ Tree Diameter tests passed")

    # Test 11: Max Independent Set
    print("\n11. Max Independent Set (Tree DP)")
    # Tree: root=1, left=2(right=4,left=5), right=3
    # Include 1+4+5=10, or 2+3=5, or 4+5+3=12
    assert max_independent_set_tree(root) == 12
    print("   ✓ Max Independent Set tests passed")

    # Test 12: Optimal Game Strategy
    print("\n12. Optimal Game Strategy (Game Theory DP)")
    assert optimal_game_strategy([8, 15, 3, 7]) == 22
    print("   ✓ Optimal Game Strategy tests passed")

    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\nDP Patterns Reviewed:")
    print("  1. 1D DP: Climbing Stairs, House Robber, Coin Change")
    print("  2. 2D DP: LCS, Edit Distance, Knapsack, Target Sum")
    print("  3. Interval DP: Palindrome Partitioning, Burst Balloons")
    print("  4. Tree DP: Diameter, Max Independent Set")
    print("  5. Bitmask DP: TSP, Subset Sum")
    print("  6. Game Theory DP: Optimal Strategy, Coin Game")
    print("  7. Probability DP: Expected Dice Rolls, Soup Servings")
    print("\nKey Takeaways:")
    print("  - Recognize optimal substructure and overlapping subproblems")
    print("  - Choose memoization vs tabulation based on problem structure")
    print("  - Optimize space when possible (rolling arrays, 1D compression)")
    print("  - Define state clearly, identify base cases, design transitions")


if __name__ == "__main__":
    test_all()
