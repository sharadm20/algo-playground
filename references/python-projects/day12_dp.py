"""
Day 12: Advanced Dynamic Programming - Part 2
Python Implementations

Topics:
- DP on Trees
- Bitmask DP (Traveling Salesman Problem)
- Digit DP
- Matrix Chain Multiplication
- DP Optimization Techniques
"""


# =============================================================================
# 1. Tree Diameter with DP
# =============================================================================

def tree_diameter(tree):
    """
    Find the diameter of a tree using DP.
    tree: adjacency list representation (list of lists)
    Returns the diameter (longest path between any two nodes)
    
    Time: O(n), Space: O(n)
    """
    n = len(tree)
    diameter = [0]
    
    def dfs(node, parent=-1):
        max_height1 = 0  # Top two heights
        max_height2 = 0
        
        for child in tree[node]:
            if child != parent:
                height = dfs(child, node)
                
                # Update top two heights
                if height > max_height1:
                    max_height2 = max_height1
                    max_height1 = height
                elif height > max_height2:
                    max_height2 = height
        
        # Diameter through this node = sum of two longest paths
        diameter[0] = max(diameter[0], max_height1 + max_height2)
        
        return max_height1 + 1
    
    dfs(0)  # Root at node 0
    return diameter[0]


# =============================================================================
# 2. Maximum Independent Set on Trees
# =============================================================================

def max_independent_set_tree(tree):
    """
    Find maximum independent set on a tree using DP.
    tree: adjacency list representation
    Returns (size, dp_table) where dp_table[node][0/1]
    0 = node not included, 1 = node included
    
    Time: O(n), Space: O(n)
    """
    n = len(tree)
    # dp[node][0] = max set when node NOT included
    # dp[node][1] = max set when node IS included
    dp = [[0, 0] for _ in range(n)]
    
    def dfs(node, parent=-1):
        dp[node][1] = 1  # Include this node
        
        for child in tree[node]:
            if child != parent:
                dfs(child, node)
                # If node not included, children can be included or not
                dp[node][0] += max(dp[child][0], dp[child][1])
                # If node included, children cannot be included
                dp[node][1] += dp[child][0]
    
    dfs(0)
    return max(dp[0][0], dp[0][1])


# =============================================================================
# 3. Traveling Salesman Problem (Bitmask DP)
# =============================================================================

def tsp(dist):
    """
    Solve TSP using bitmask DP.
    dist: n x n distance matrix
    Returns minimum cost of TSP tour
    
    Time: O(n^2 * 2^n), Space: O(n * 2^n)
    """
    n = len(dist)
    INF = float('inf')
    
    # dp[mask][i] = min cost to visit all cities in mask, ending at i
    num_states = 1 << n
    dp = [[INF] * n for _ in range(num_states)]
    dp[1][0] = 0  # Start at city 0
    
    for mask in range(1, num_states):
        for i in range(n):
            if dp[mask][i] == INF:
                continue
            
            # Try to visit next city j
            for j in range(n):
                if not (mask & (1 << j)):  # If j not visited
                    new_mask = mask | (1 << j)
                    dp[new_mask][j] = min(dp[new_mask][j], 
                                         dp[mask][i] + dist[i][j])
    
    # Return to start
    full_mask = num_states - 1
    return min(dp[full_mask][i] + dist[i][0] for i in range(1, n))


# =============================================================================
# 4. Assignment Problem (Bitmask DP)
# =============================================================================

def assignment_problem(cost):
    """
    Solve assignment problem using bitmask DP.
    cost: n x n cost matrix where cost[i][j] = cost of assigning worker i to job j
    Returns minimum total cost
    
    Time: O(n * 2^n), Space: O(2^n)
    """
    n = len(cost)
    INF = float('inf')
    num_states = 1 << n
    
    # dp[mask] = min cost to assign jobs in mask to first k workers
    dp = [INF] * num_states
    dp[0] = 0
    
    # Process masks by number of set bits (workers assigned so far)
    for worker in range(n):
        # For each mask with 'worker' bits set
        for mask in range(num_states):
            if bin(mask).count('1') != worker:
                continue
            if dp[mask] == INF:
                continue
            
            # Try to assign job j to current worker
            for j in range(n):
                if not (mask & (1 << j)):  # If job j not yet assigned
                    new_mask = mask | (1 << j)
                    dp[new_mask] = min(dp[new_mask], dp[mask] + cost[worker][j])
    
    return dp[num_states - 1]


# =============================================================================
# 5. Digit DP - Count Numbers Without Digit 4
# =============================================================================

def count_without_digit_4(n):
    """
    Count numbers from 0 to n that don't contain digit 4.
    
    Time: O(log(n)), Space: O(log(n))
    """
    digits = [int(d) for d in str(n)]
    memo = {}
    
    def dp(pos, tight, started):
        if pos == len(digits):
            return 1 if started else 0
        
        state = (pos, tight, started)
        if state in memo:
            return memo[state]
        
        limit = digits[pos] if tight else 9
        count = 0
        
        for digit in range(limit + 1):
            if digit == 4:
                continue
            
            new_tight = tight and (digit == limit)
            new_started = started or (digit > 0)
            count += dp(pos + 1, new_tight, new_started)
        
        memo[state] = count
        return count
    
    return dp(0, True, False) + 1  # +1 for number 0


# =============================================================================
# 6. Digit DP - Count Numbers with Digit Sum K
# =============================================================================

def count_with_digit_sum_k(n, k):
    """
    Count numbers from 0 to n where sum of digits equals k.
    
    Time: O(log(n) * k), Space: O(log(n) * k)
    """
    digits = [int(d) for d in str(n)]
    memo = {}
    
    def dp(pos, tight, sum_digits, started):
        if sum_digits > k:
            return 0
        
        if pos == len(digits):
            return 1 if started and sum_digits == k else 0
        
        state = (pos, tight, sum_digits, started)
        if state in memo:
            return memo[state]
        
        limit = digits[pos] if tight else 9
        count = 0
        
        for digit in range(limit + 1):
            new_tight = tight and (digit == limit)
            new_started = started or (digit > 0)
            count += dp(pos + 1, new_tight, sum_digits + digit, new_started)
        
        memo[state] = count
        return count
    
    return dp(0, True, 0, False)


# =============================================================================
# 7. Matrix Chain Multiplication
# =============================================================================

def matrix_chain_order(dimensions):
    """
    Find minimum number of scalar multiplications for matrix chain.
    dimensions: array where matrix i has dimensions dimensions[i] x dimensions[i+1]
    
    Time: O(n^3), Space: O(n^2)
    """
    n = len(dimensions) - 1  # Number of matrices
    dp = [[0] * n for _ in range(n)]
    
    # l is chain length
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float('inf')
            
            for k in range(i, j):
                cost = (dp[i][k] + dp[k + 1][j] + 
                       dimensions[i] * dimensions[k + 1] * dimensions[j + 1])
                dp[i][j] = min(dp[i][j], cost)
    
    return dp[0][n - 1]


# =============================================================================
# 8. Boolean Parenthesization
# =============================================================================

def boolean_parenthesization(symbols, operators):
    """
    Count ways to parenthesize boolean expression to evaluate to True.
    symbols: list of 'T' or 'F'
    operators: list of '&', '|', '^'
    
    Time: O(n^3), Space: O(n^2)
    """
    n = len(symbols)
    
    # dpT[i][j] = ways to get True from symbols[i..j]
    # dpF[i][j] = ways to get False from symbols[i..j]
    dpT = [[0] * n for _ in range(n)]
    dpF = [[0] * n for _ in range(n)]
    
    # Base case: single symbols
    for i in range(n):
        if symbols[i] == 'T':
            dpT[i][i] = 1
            dpF[i][i] = 0
        else:
            dpT[i][i] = 0
            dpF[i][i] = 1
    
    # Fill for increasing lengths
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dpT[i][j] = 0
            dpF[i][j] = 0
            
            for k in range(i, j):
                # Split at operator k
                op = operators[k]
                
                # Total ways for left and right subexpressions
                total_left = dpT[i][k] + dpF[i][k]
                total_right = dpT[k + 1][j] + dpF[k + 1][j]
                
                if op == '&':
                    # True only if both are True
                    dpT[i][j] += dpT[i][k] * dpT[k + 1][j]
                    # False otherwise
                    dpF[i][j] += total_left * total_right - dpT[i][k] * dpT[k + 1][j]
                elif op == '|':
                    # False only if both are False
                    dpF[i][j] += dpF[i][k] * dpF[k + 1][j]
                    # True otherwise
                    dpT[i][j] += total_left * total_right - dpF[i][k] * dpF[k + 1][j]
                elif op == '^':
                    # True if one is True and other is False
                    dpT[i][j] += dpT[i][k] * dpF[k + 1][j] + dpF[i][k] * dpT[k + 1][j]
                    # False if both are same
                    dpF[i][j] += dpT[i][k] * dpT[k + 1][j] + dpF[i][k] * dpF[k + 1][j]
    
    return dpT[0][n - 1]


# =============================================================================
# Tests
# =============================================================================

def test_tree_diameter():
    """Test tree diameter calculation"""
    # Test 1: Simple tree
    #       0
    #      / \
    #     1   2
    #    / \
    #   3   4
    tree1 = [[1, 2], [3, 4], [], [], []]
    assert tree_diameter(tree1) == 3, "Test 1 failed"
    
    # Test 2: Linear tree (path)
    # 0 - 1 - 2 - 3 - 4
    tree2 = [[1], [0, 2], [1, 3], [2, 4], [3]]
    assert tree_diameter(tree2) == 4, "Test 2 failed"
    
    # Test 3: Star tree
    #     0
    #   / | \
    #  1  2  3
    tree3 = [[1, 2, 3], [0], [0], [0]]
    assert tree_diameter(tree3) == 2, "Test 3 failed"
    
    print("✓ All tree diameter tests passed")


def test_max_independent_set():
    """Test maximum independent set on trees"""
    # Test 1: Simple tree
    tree1 = [[1, 2], [3, 4], [], [], []]
    assert max_independent_set_tree(tree1) == 3, "Test 1 failed"
    
    # Test 2: Linear tree
    tree2 = [[1], [0, 2], [1, 3], [2, 4], [3]]
    assert max_independent_set_tree(tree2) == 3, "Test 2 failed"
    
    # Test 3: Star tree
    tree3 = [[1, 2, 3], [0], [0], [0]]
    assert max_independent_set_tree(tree3) == 3, "Test 3 failed"
    
    print("✓ All maximum independent set tests passed")


def test_tsp():
    """Test traveling salesman problem"""
    # Test 1: 4 cities
    dist1 = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    assert tsp(dist1) == 80, "Test 1 failed"
    
    # Test 2: 3 cities (triangle)
    dist2 = [
        [0, 10, 20],
        [10, 0, 15],
        [20, 15, 0]
    ]
    assert tsp(dist2) == 45, "Test 2 failed"
    
    print("✓ All TSP tests passed")


def test_assignment_problem():
    """Test assignment problem"""
    # Test 1: 3 workers, 3 jobs
    cost1 = [
        [10, 2, 6],
        [5, 7, 3],
        [6, 8, 9]
    ]
    assert assignment_problem(cost1) == 11, "Test 1 failed"  # 2 + 3 + 6
    
    # Test 2: 2 workers, 2 jobs
    cost2 = [
        [1, 2],
        [2, 1]
    ]
    assert assignment_problem(cost2) == 2, "Test 2 failed"
    
    print("✓ All assignment problem tests passed")


def test_count_without_digit_4():
    """Test counting numbers without digit 4"""
    assert count_without_digit_4(10) == 10, "Test 1 failed"  # 0-10 except 4
    assert count_without_digit_4(100) == 82, "Test 2 failed"
    assert count_without_digit_4(4) == 4, "Test 3 failed"  # 0,1,2,3
    assert count_without_digit_4(14) == 13, "Test 4 failed"  # 0-14 except 4,14
    
    print("✓ All count without digit 4 tests passed")


def test_count_with_digit_sum_k():
    """Test counting numbers with digit sum k"""
    assert count_with_digit_sum_k(20, 5) == 2, "Test 1 failed"  # 5, 14
    assert count_with_digit_sum_k(100, 1) == 3, "Test 2 failed"  # 1, 10, 100
    assert count_with_digit_sum_k(10, 10) == 0, "Test 3 failed"  # No number from 0-10 has digit sum 10
    
    print("✓ All count with digit sum k tests passed")


def test_matrix_chain_order():
    """Test matrix chain multiplication order"""
    # Test 1: A1(10x30), A2(30x5), A3(5x60)
    dims1 = [10, 30, 5, 60]
    assert matrix_chain_order(dims1) == 4500, "Test 1 failed"
    
    # Test 2: A1(5x10), A2(10x3), A3(3x12), A4(12x5)
    dims2 = [5, 10, 3, 12, 5]
    assert matrix_chain_order(dims2) == 405, "Test 2 failed"
    
    # Test 3: Two matrices only
    dims3 = [10, 20, 30]
    assert matrix_chain_order(dims3) == 6000, "Test 3 failed"
    
    print("✓ All matrix chain order tests passed")


def test_boolean_parenthesization():
    """Test boolean parenthesization"""
    # Test 1: T | T & F
    symbols1 = ['T', 'T', 'F']
    ops1 = ['|', '&']
    assert boolean_parenthesization(symbols1, ops1) == 1, "Test 1 failed"
    
    # Test 2: T ^ T ^ T
    symbols2 = ['T', 'T', 'T']
    ops2 = ['^', '^']
    assert boolean_parenthesization(symbols2, ops2) == 2, "Test 2 failed"  # Both ways give True
    
    # Test 3: T | T | T
    symbols3 = ['T', 'T', 'T']
    ops3 = ['|', '|']
    assert boolean_parenthesization(symbols3, ops3) == 2, "Test 3 failed"
    
    print("✓ All boolean parenthesization tests passed")


if __name__ == "__main__":
    print("Running Day 12: Advanced Dynamic Programming Tests\n")
    
    test_tree_diameter()
    test_max_independent_set()
    test_tsp()
    test_assignment_problem()
    test_count_without_digit_4()
    test_count_with_digit_sum_k()
    test_matrix_chain_order()
    test_boolean_parenthesization()
    
    print("\n✓ All tests passed successfully!")
