"""
Day 11: Dynamic Programming - Part 1
Python Implementations

Topics:
- Fibonacci Sequence
- Climbing Stairs
- House Robber
- Coin Change
- 0/1 Knapsack
- Unbounded Knapsack
- Target Sum
- Longest Common Subsequence
- Edit Distance
- Longest Palindromic Subsequence
"""


# =============================================================================
# 1. Fibonacci Sequence
# =============================================================================

def fibonacci_naive(n: int) -> int:
    """Naive recursive Fibonacci - O(2^n) time, O(n) space"""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memo(n: int) -> int:
    """Memoization (top-down) Fibonacci - O(n) time, O(n) space"""
    memo = {}
    
    def helper(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n not in memo:
            memo[n] = helper(n - 1) + helper(n - 2)
        return memo[n]
    
    return helper(n)


def fibonacci_tabulation(n: int) -> int:
    """Tabulation (bottom-up) Fibonacci - O(n) time, O(n) space"""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def fibonacci_optimized(n: int) -> int:
    """Space-optimized Fibonacci - O(n) time, O(1) space"""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    
    return prev1


# =============================================================================
# 2. Climbing Stairs
# =============================================================================

def climb_stairs(n: int) -> int:
    """
    Climbing Stairs - O(n) time, O(1) space
    
    You can climb 1 or 2 steps at a time.
    How many distinct ways to climb n steps?
    This is identical to Fibonacci!
    """
    if n <= 1:
        return 1
    
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    
    return prev1


# =============================================================================
# 3. House Robber
# =============================================================================

def house_robber(nums: list[int]) -> int:
    """
    House Robber - O(n) time, O(1) space
    
    Given an array of house values, find the maximum money you can rob
    without robbing adjacent houses.
    
    Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev2 = 0  # dp[i-2]
    prev1 = 0  # dp[i-1]
    
    for num in nums:
        curr = max(prev1, prev2 + num)
        prev2 = prev1
        prev1 = curr
    
    return prev1


# =============================================================================
# 4. Coin Change
# =============================================================================

def coin_change(coins: list[int], amount: int) -> int:
    """
    Coin Change (Minimum Coins) - O(amount * len(coins)) time, O(amount) space
    
    Given coins of different denominations and a total amount, find the minimum
    number of coins needed to make up that amount. Return -1 if impossible.
    
    Recurrence: dp[i] = min(dp[i], dp[i - coin] + 1) for each coin
    """
    # Initialize DP array with infinity (impossible value)
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins needed to make amount 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


# =============================================================================
# 5. 0/1 Knapsack Problem
# =============================================================================

def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """
    0/1 Knapsack - O(n * capacity) time, O(n * capacity) space
    
    Given n items with weights and values, find the maximum value you can get
    with a knapsack of capacity W. Each item can only be taken once.
    
    Recurrence: dp[i][w] = max(dp[i-1][w], dp[i-1][w-weight[i]] + value[i])
    """
    n = len(weights)
    # dp[i][w] = max value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Option 1: Don't include item i
            dp[i][w] = dp[i - 1][w]
            
            # Option 2: Include item i (if it fits)
            if w >= weights[i - 1]:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    
    return dp[n][capacity]


def knapsack_01_optimized(weights: list[int], values: list[int], capacity: int) -> int:
    """
    0/1 Knapsack with optimized space - O(n * capacity) time, O(capacity) space
    
    Uses 1D array by iterating backwards to avoid using updated values.
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Iterate backwards to avoid using updated values from current iteration
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]


# =============================================================================
# 6. Unbounded Knapsack
# =============================================================================

def knapsack_unbounded(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Unbounded Knapsack - O(n * capacity) time, O(capacity) space
    
    Same as 0/1 knapsack, but you can take unlimited copies of each item.
    
    Recurrence: dp[w] = max(dp[w], dp[w-weight[i]] + value[i])
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Iterate forwards (can reuse same item multiple times)
        for w in range(weights[i], capacity + 1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]


# =============================================================================
# 7. Target Sum
# =============================================================================

def find_target_sum_ways(nums: list[int], target: int) -> int:
    """
    Target Sum - O(n * sum) time, O(sum) space
    
    Given an array of numbers and a target, find the number of ways to assign
    + or - signs to make the sum equal to target.
    
    Transformation: Convert to subset sum problem
    Find subset with sum = (sum(nums) + target) / 2
    """
    total_sum = sum(nums)
    
    # Check if solution is possible
    if abs(target) > total_sum or (total_sum + target) % 2 != 0:
        return 0
    
    subset_sum = (total_sum + target) // 2
    
    # Now solve subset sum problem
    dp = [0] * (subset_sum + 1)
    dp[0] = 1  # One way to make sum 0 (take nothing)
    
    for num in nums:
        for w in range(subset_sum, num - 1, -1):
            dp[w] += dp[w - num]
    
    return dp[subset_sum]


# =============================================================================
# 8. Longest Common Subsequence (LCS)
# =============================================================================

def longest_common_subsequence(s1: str, s2: str) -> int:
    """
    Longest Common Subsequence - O(m * n) time, O(m * n) space
    
    Find the length of the longest subsequence common to two strings.
    
    Recurrence:
    - If s1[i] == s2[j]: dp[i][j] = 1 + dp[i-1][j-1]
    - Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    """
    m, n = len(s1), len(s2)
    
    # dp[i][j] = LCS length for s1[0..i-1] and s2[0..j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def longest_common_subsequence_optimized(s1: str, s2: str) -> int:
    """
    LCS with optimized space - O(m * n) time, O(min(m, n)) space
    """
    # Ensure s2 is the shorter string for space optimization
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = 1 + prev[j - 1]
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr[:]
    
    return prev[n]


# =============================================================================
# 9. Edit Distance (Levenshtein Distance)
# =============================================================================

def edit_distance(word1: str, word2: str) -> int:
    """
    Edit Distance - O(m * n) time, O(m * n) space
    
    Find the minimum number of operations (insert, delete, replace)
    to convert one string to another.
    
    Recurrence:
    - If word1[i] == word2[j]: dp[i][j] = dp[i-1][j-1]
    - Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    """
    m, n = len(word1), len(word2)
    
    # dp[i][j] = edit distance for word1[0..i-1] and word2[0..j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from word1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters to word1
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
    
    return dp[m][n]


# =============================================================================
# 10. Longest Palindromic Subsequence
# =============================================================================

def longest_palindromic_subsequence(s: str) -> int:
    """
    Longest Palindromic Subsequence - O(n^2) time, O(n^2) space
    
    Find the length of the longest palindromic subsequence in a string.
    
    Approach: Reverse string and find LCS with original
    """
    def lcs(s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        return dp[m][n]
    
    return lcs(s, s[::-1])


def longest_palindromic_subsequence_direct(s: str) -> int:
    """
    Longest Palindromic Subsequence - O(n^2) time, O(n^2) space
    
    Direct DP approach without using LCS.
    
    Recurrence:
    - If s[i] == s[j]: dp[i][j] = 2 + dp[i+1][j-1]
    - Else: dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    """
    n = len(s)
    if n == 0:
        return 0
    
    # dp[i][j] = LPS length for s[i..j]
    dp = [[0] * n for _ in range(n)]
    
    # Base case: single characters are palindromes of length 1
    for i in range(n):
        dp[i][i] = 1
    
    # Fill for substrings of length 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + dp[i + 1][j - 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]


# =============================================================================
# Test Functions
# =============================================================================

def test_fibonacci():
    """Test Fibonacci implementations"""
    print("\n=== Testing Fibonacci ===")
    
    # Test cases: (input, expected)
    test_cases = [
        (0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (10, 55), (15, 610)
    ]
    
    for n, expected in test_cases:
        assert fibonacci_memo(n) == expected, f"Failed for n={n}"
        assert fibonacci_tabulation(n) == expected, f"Failed for n={n}"
        assert fibonacci_optimized(n) == expected, f"Failed for n={n}"
    
    print("All Fibonacci tests passed!")


def test_climb_stairs():
    """Test climbing stairs implementation"""
    print("\n=== Testing Climbing Stairs ===")
    
    test_cases = [
        (0, 1), (1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (10, 89)
    ]
    
    for n, expected in test_cases:
        result = climb_stairs(n)
        assert result == expected, f"Failed for n={n}: expected {expected}, got {result}"
    
    print("All climbing stairs tests passed!")


def test_house_robber():
    """Test house robber implementation"""
    print("\n=== Testing House Robber ===")
    
    test_cases = [
        ([1, 2, 3, 1], 4),
        ([2, 7, 9, 3, 1], 12),
        ([], 0),
        ([5], 5),
        ([2, 1, 1, 2], 4),
        ([10, 2, 2, 10, 2, 10], 30)
    ]
    
    for nums, expected in test_cases:
        result = house_robber(nums)
        assert result == expected, f"Failed for {nums}: expected {expected}, got {result}"
    
    print("All house robber tests passed!")


def test_coin_change():
    """Test coin change implementation"""
    print("\n=== Testing Coin Change ===")
    
    test_cases = [
        ([1, 2, 5], 11, 3),  # 11 = 5 + 5 + 1
        ([2], 3, -1),         # Impossible
        ([1], 0, 0),          # Base case
        ([1, 2, 5], 100, 20), # 100 = 20 * 5
        ([186, 419, 83, 408], 6249, 20)
    ]
    
    for coins, amount, expected in test_cases:
        result = coin_change(coins, amount)
        assert result == expected, f"Failed for coins={coins}, amount={amount}: expected {expected}, got {result}"
    
    print("All coin change tests passed!")


def test_knapsack_01():
    """Test 0/1 knapsack implementation"""
    print("\n=== Testing 0/1 Knapsack ===")
    
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    
    result1 = knapsack_01(weights, values, capacity)
    result2 = knapsack_01_optimized(weights, values, capacity)
    expected = 9  # Take items with weights 3 and 4 (values 4 + 5)
    
    assert result1 == expected, f"Failed: expected {expected}, got {result1}"
    assert result2 == expected, f"Failed: expected {expected}, got {result2}"
    
    print("All 0/1 knapsack tests passed!")


def test_knapsack_unbounded():
    """Test unbounded knapsack implementation"""
    print("\n=== Testing Unbounded Knapsack ===")
    
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    
    result = knapsack_unbounded(weights, values, capacity)
    # With unbounded knapsack, we can take item with weight 3 (value 4) twice + weight 1 (value 1) = 9
    # Or take item with weight 4 (value 5) + weight 3 (value 4) = 9
    # Best: item with weight 3 (value 4) taken twice + 1 of weight 1 = 4+4+1 = 9
    expected = 9
    
    assert result == expected, f"Failed: expected {expected}, got {result}"
    
    print("All unbounded knapsack tests passed!")


def test_target_sum():
    """Test target sum implementation"""
    print("\n=== Testing Target Sum ===")
    
    test_cases = [
        ([1, 1, 1, 1, 1], 3, 5),
        ([1], 1, 1),
        ([1], 2, 0),
        ([1, 2, 3, 4, 5], 3, 3)
    ]
    
    for nums, target, expected in test_cases:
        result = find_target_sum_ways(nums, target)
        assert result == expected, f"Failed for nums={nums}, target={target}: expected {expected}, got {result}"
    
    print("All target sum tests passed!")


def test_lcs():
    """Test longest common subsequence implementation"""
    print("\n=== Testing Longest Common Subsequence ===")
    
    test_cases = [
        ("abcde", "ace", 3),
        ("abc", "abc", 3),
        ("abc", "def", 0),
        ("bsbininm", "jmjkbkjkv", 1),
        ("", "", 0)
    ]
    
    for s1, s2, expected in test_cases:
        result1 = longest_common_subsequence(s1, s2)
        result2 = longest_common_subsequence_optimized(s1, s2)
        assert result1 == expected, f"Failed for '{s1}', '{s2}': expected {expected}, got {result1}"
        assert result2 == expected, f"Failed optimized for '{s1}', '{s2}': expected {expected}, got {result2}"
    
    print("All LCS tests passed!")


def test_edit_distance():
    """Test edit distance implementation"""
    print("\n=== Testing Edit Distance ===")
    
    test_cases = [
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("", "abc", 3),
        ("abc", "", 3),
        ("abc", "abc", 0),
        ("sunday", "saturday", 3)
    ]
    
    for word1, word2, expected in test_cases:
        result = edit_distance(word1, word2)
        assert result == expected, f"Failed for '{word1}' -> '{word2}': expected {expected}, got {result}"
    
    print("All edit distance tests passed!")


def test_longest_palindromic_subsequence():
    """Test longest palindromic subsequence implementation"""
    print("\n=== Testing Longest Palindromic Subsequence ===")
    
    test_cases = [
        ("bbbab", 4),  # "bbbb"
        ("cbbd", 2),   # "bb"
        ("a", 1),
        ("", 0),
        ("abcd", 1),
        ("racexyzca", 5)  # "racecar" or similar
    ]
    
    for s, expected in test_cases:
        result1 = longest_palindromic_subsequence(s)
        result2 = longest_palindromic_subsequence_direct(s)
        assert result1 == expected, f"Failed for '{s}': expected {expected}, got {result1}"
        assert result2 == expected, f"Failed direct for '{s}': expected {expected}, got {result2}"
    
    print("All longest palindromic subsequence tests passed!")


# =============================================================================
# Main - Run All Tests
# =============================================================================

if __name__ == "__main__":
    print("Running Day 11: Dynamic Programming - Part 1 Tests")
    print("=" * 60)
    
    test_fibonacci()
    test_climb_stairs()
    test_house_robber()
    test_coin_change()
    test_knapsack_01()
    test_knapsack_unbounded()
    test_target_sum()
    test_lcs()
    test_edit_distance()
    test_longest_palindromic_subsequence()
    
    print("\n" + "=" * 60)
    print("All Day 11 tests passed successfully!")
    print("=" * 60)
