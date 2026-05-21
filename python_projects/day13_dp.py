"""
Day 13: More Advanced Dynamic Programming
Python Implementations

Topics: Interval DP, Game Theory DP, Probability DP, Advanced Patterns
"""


# =============================================================================
# 1. Palindrome Partitioning (Minimum Cuts)
# =============================================================================

def min_palindrome_cuts(s: str) -> int:
    """
    Minimum cuts to partition string into palindromes.
    Time: O(n^2), Space: O(n^2)
    """
    n = len(s)
    if n <= 1:
        return 0

    # Precompute palindrome table
    is_pal = [[False] * n for _ in range(n)]

    # All single chars are palindromes
    for i in range(n):
        is_pal[i][i] = True

    # Check for length 2
    for i in range(n - 1):
        is_pal[i][i + 1] = (s[i] == s[i + 1])

    # Check for length > 2
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_pal[i][j] = (s[i] == s[j] and is_pal[i + 1][j - 1])

    # DP for minimum cuts
    # cuts[i] = min cuts for s[0..i]
    cuts = list(range(n))  # Worst case: cut after each character

    for i in range(1, n):
        if is_pal[0][i]:
            cuts[i] = 0
        else:
            for j in range(i):
                if is_pal[j + 1][i]:
                    cuts[i] = min(cuts[i], cuts[j] + 1)

    return cuts[n - 1]


# =============================================================================
# 2. Burst Balloons
# =============================================================================

def max_coins_burst_balloons(nums: list[int]) -> int:
    """
    Maximize coins from bursting balloons.
    Time: O(n^3), Space: O(n^2)
    """
    # Add boundary balloons with value 1
    nums = [1] + nums + [1]
    n = len(nums)

    # dp[i][j] = max coins from bursting balloons in range [i, j]
    dp = [[0] * n for _ in range(n)]

    # Fill for increasing lengths
    for length in range(1, n - 1):  # length of range (excluding boundaries)
        for i in range(1, n - length):
            j = i + length - 1
            # Try each k as the LAST balloon to burst in [i, j]
            for k in range(i, j + 1):
                coins = (dp[i][k - 1] if k > i else 0) + \
                        (dp[k + 1][j] if k < j else 0) + \
                        nums[i - 1] * nums[k] * nums[j + 1]
                dp[i][j] = max(dp[i][j], coins)

    return dp[1][n - 2]


# =============================================================================
# 3. Stone Merge Problem
# =============================================================================

def min_stone_merge_cost(stones: list[int]) -> int:
    """
    Minimum cost to merge all piles into one.
    Time: O(n^3), Space: O(n^2)
    """
    n = len(stones)
    if n <= 1:
        return 0

    # Precompute prefix sums for fast range sum
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + stones[i]

    def range_sum(i, j):
        return prefix_sum[j + 1] - prefix_sum[i]

    # dp[i][j] = min cost to merge stones[i..j]
    dp = [[0] * n for _ in range(n)]

    # Fill for increasing lengths
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + range_sum(i, j)
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]


# =============================================================================
# 4. Optimal Game Strategy (Predict the Winner)
# =============================================================================

def optimal_game_strategy(values: list[int]) -> int:
    """
    Maximum value Player 1 can get when both play optimally.
    Time: O(n^2), Space: O(n^2)
    """
    n = len(values)

    # dp[i][j] = max score difference (current player - opponent) for range [i, j]
    dp = [[0] * n for _ in range(n)]

    # Base case: single element
    for i in range(n):
        dp[i][i] = values[i]

    # Fill for increasing lengths
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Pick left or right, opponent will play optimally
            dp[i][j] = max(values[i] - dp[i + 1][j],
                          values[j] - dp[i][j - 1])

    # Player 1's score = (total + diff) / 2
    total = sum(values)
    diff = dp[0][n - 1]
    return (total + diff) // 2


def can_first_player_win(values: list[int]) -> bool:
    """
    Can Player 1 win (get >= half of total)?
    Time: O(n^2), Space: O(n^2)
    """
    n = len(values)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = values[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(values[i] - dp[i + 1][j],
                          values[j] - dp[i][j - 1])

    return dp[0][n - 1] >= 0


# =============================================================================
# 5. Nim Game
# =============================================================================

def can_win_nim(n: int, max_removal: int = 3) -> bool:
    """
    Can first player win Nim game? (remove 1 to max_removal stones)
    Time: O(1), Space: O(1)
    """
    return n % (max_removal + 1) != 0


# =============================================================================
# 6. Coin Game (Pick from Ends with Optimal Play)
# =============================================================================

def coin_game_max_value(coins: list[int]) -> int:
    """
    Maximum value first player can guarantee getting.
    Time: O(n^2), Space: O(n^2)
    """
    n = len(coins)
    if n == 0:
        return 0

    # dp[i][j] = max value current player can get from coins[i..j]
    dp = [[0] * n for _ in range(n)]

    # Base case: single coin
    for i in range(n):
        dp[i][i] = coins[i]

    # Base case: two coins
    for i in range(n - 1):
        dp[i][i + 1] = max(coins[i], coins[i + 1])

    # Fill for length >= 3
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # If pick coins[i], opponent picks optimally from [i+1, j]
            # We get min of what's left after opponent
            pick_left = coins[i] + min(
                dp[i + 2][j] if i + 2 <= j else 0,
                dp[i + 1][j - 1] if i + 1 <= j - 1 else 0
            )
            # If pick coins[j]
            pick_right = coins[j] + min(
                dp[i + 1][j - 1] if i + 1 <= j - 1 else 0,
                dp[i][j - 2] if i <= j - 2 else 0
            )
            dp[i][j] = max(pick_left, pick_right)

    return dp[0][n - 1]


# =============================================================================
# 7. Expected Rolls to Get Specific Face (Dice Problem)
# =============================================================================

def expected_rolls_for_face(face_prob: float) -> float:
    """
    Expected number of rolls to get a specific face.
    E = 1/p
    Time: O(1), Space: O(1)
    """
    return 1.0 / face_prob


def expected_rolls_for_all_faces(num_faces: int = 6) -> float:
    """
    Expected rolls to see all faces at least once (Coupon Collector).
    E = n * H(n) = n * (1 + 1/2 + 1/3 + ... + 1/n)
    Time: O(n), Space: O(1)
    """
    harmonic = sum(1.0 / i for i in range(1, num_faces + 1))
    return num_faces * harmonic


# =============================================================================
# 8. Random Walk Expected Steps
# =============================================================================

def random_walk_expected_steps(target: int) -> int:
    """
    Expected steps to reach target from 0 in 1D random walk (+1 or -1 each step).
    Answer: target^2
    Time: O(1), Space: O(1)
    """
    return target * target


# =============================================================================
# 9. Grid Path Counting (Simple Broken Profile)
# =============================================================================

def grid_unique_paths(m: int, n: int) -> int:
    """
    Number of unique paths from top-left to bottom-right (right/down moves only).
    Time: O(m*n), Space: O(n) with space optimization
    """
    # Use 1D DP array
    dp = [1] * n

    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]

    return dp[n - 1]


def grid_unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    """
    Unique paths with obstacles (0 = empty, 1 = obstacle).
    Time: O(m*n), Space: O(n)
    """
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    dp = [0] * n
    dp[0] = 1 if grid[0][0] == 0 else 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]

    return dp[n - 1]


# =============================================================================
# Tests
# =============================================================================

def test_min_palindrome_cuts():
    assert min_palindrome_cuts("aab") == 1, "Test 1 failed"
    assert min_palindrome_cuts("a") == 0, "Test 2 failed"
    assert min_palindrome_cuts("ab") == 1, "Test 3 failed"
    assert min_palindrome_cuts("aba") == 0, "Test 4 failed"
    assert min_palindrome_cuts("abcba") == 0, "Test 5 failed"
    print("✓ test_min_palindrome_cuts passed")


def test_burst_balloons():
    assert max_coins_burst_balloons([3, 1, 5, 8]) == 167, "Test 1 failed"
    assert max_coins_burst_balloons([1, 5]) == 10, "Test 2 failed"
    assert max_coins_burst_balloons([10]) == 10, "Test 3 failed"
    print("✓ test_burst_balloons passed")


def test_stone_merge():
    assert min_stone_merge_cost([1, 2, 3, 4, 5]) == 33, "Test 1 failed"
    assert min_stone_merge_cost([1, 2, 3]) == 9, "Test 2 failed"
    assert min_stone_merge_cost([5]) == 0, "Test 3 failed"
    print("✓ test_stone_merge passed")


def test_optimal_game_strategy():
    assert optimal_game_strategy([8, 15, 3, 7]) == 22, "Test 1 failed"
    assert optimal_game_strategy([1, 2, 3, 4]) == 6, "Test 2 failed"
    assert optimal_game_strategy([5, 3, 7, 10]) == 15, "Test 3 failed"
    print("✓ test_optimal_game_strategy passed")


def test_can_first_player_win():
    assert can_first_player_win([1, 2, 3]) == True, "Test 1 failed"
    assert can_first_player_win([1, 1]) == True, "Test 2 failed"
    print("✓ test_can_first_player_win passed")


def test_nim_game():
    assert can_win_nim(4) == False, "Test 1 failed"  # Multiple of 4
    assert can_win_nim(1) == True, "Test 2 failed"
    assert can_win_nim(5) == True, "Test 3 failed"
    assert can_win_nim(8) == False, "Test 4 failed"
    print("✓ test_nim_game passed")


def test_coin_game():
    assert coin_game_max_value([5, 3, 7, 10]) == 15, "Test 1 failed"
    assert coin_game_max_value([8, 15, 3, 7]) == 22, "Test 2 failed"
    assert coin_game_max_value([1, 2]) == 2, "Test 3 failed"
    print("✓ test_coin_game passed")


def test_expected_rolls():
    # Expected rolls for specific face on 6-sided die
    assert abs(expected_rolls_for_face(1/6) - 6.0) < 0.01, "Test 1 failed"
    # Coupon collector for 6 faces
    expected_6 = expected_rolls_for_all_faces(6)
    assert 14.0 < expected_6 < 15.0, f"Test 2 failed: got {expected_6}"
    print("✓ test_expected_rolls passed")


def test_random_walk():
    assert random_walk_expected_steps(1) == 1, "Test 1 failed"
    assert random_walk_expected_steps(2) == 4, "Test 2 failed"
    assert random_walk_expected_steps(3) == 9, "Test 3 failed"
    assert random_walk_expected_steps(5) == 25, "Test 4 failed"
    print("✓ test_random_walk passed")


def test_grid_paths():
    assert grid_unique_paths(3, 7) == 28, "Test 1 failed"
    assert grid_unique_paths(3, 2) == 3, "Test 2 failed"
    assert grid_unique_paths(1, 1) == 1, "Test 3 failed"

    # With obstacles
    grid1 = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert grid_unique_paths_with_obstacles(grid1) == 2, "Test 4 failed"

    grid2 = [[0, 1], [0, 0]]
    assert grid_unique_paths_with_obstacles(grid2) == 1, "Test 5 failed"
    print("✓ test_grid_paths passed")


if __name__ == "__main__":
    print("Running Day 13: More Advanced Dynamic Programming Tests\n")

    test_min_palindrome_cuts()
    test_burst_balloons()
    test_stone_merge()
    test_optimal_game_strategy()
    test_can_first_player_win()
    test_nim_game()
    test_coin_game()
    test_expected_rolls()
    test_random_walk()
    test_grid_paths()

    print("\n✅ All Day 13 tests passed!")
