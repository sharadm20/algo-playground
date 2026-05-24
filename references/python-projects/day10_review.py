"""
Day 10: Comprehensive Review & Practice
Topics: Mixed problem sets, pattern recognition, complexity analysis, problem decomposition
"""

from collections import defaultdict, deque, Counter
import heapq
from typing import List, Dict, Set, Tuple, Optional


# ============================================================================
# PATTERN 1: Arrays & Hashing - Two Sum
# ============================================================================
def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Two Sum - O(n) time, O(n) space
    Pattern: Hash map complement lookup
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


def three_sum(nums: List[int]) -> List[List[int]]:
    """
    3Sum - O(n^2) time, O(1) extra space (excluding output)
    Pattern: Sorting + Two pointers
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result


def max_area(height: List[int]) -> int:
    """
    Container With Most Water - O(n) time, O(1) space
    Pattern: Two pointers (opposite ends)
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_area = max(max_area, width * h)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Group Anagrams - O(n * k * log(k)) time, O(n * k) space
    Pattern: Hash map with sorted key
    """
    anagram_groups = defaultdict(list)
    
    for s in strs:
        key = ''.join(sorted(s))
        anagram_groups[key].append(s)
    
    return list(anagram_groups.values())


# ============================================================================
# PATTERN 2: String Manipulation
# ============================================================================
def length_of_longest_substring(s: str) -> int:
    """
    Longest Substring Without Repeating - O(n) time, O(min(n, m)) space
    Pattern: Sliding window with hash set
    """
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length


def count_palindromic_substrings(s: str) -> int:
    """
    Count Palindromic Substrings - O(n^2) time, O(1) space
    Pattern: Expand around center
    """
    count = 0
    
    def expand_around_center(left: int, right: int):
        nonlocal count
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
    
    for i in range(len(s)):
        expand_around_center(i, i)
        expand_around_center(i, i + 1)
    
    return count


def str_str(haystack: str, needle: str) -> int:
    """
    Implement strStr() - O(n * m) naive, O(n + m) with KMP
    Pattern: String matching
    """
    if not needle:
        return 0
    if len(needle) > len(haystack):
        return -1
    
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i + len(needle)] == needle:
            return i
    
    return -1


# ============================================================================
# PATTERN 3: Stack & Queue
# ============================================================================
class MinStack:
    """
    Min Stack - O(1) time for all operations, O(n) space
    Pattern: Auxiliary stack for minimum tracking
    """
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        if self.stack:
            val = self.stack.pop()
            if val == self.min_stack[-1]:
                self.min_stack.pop()
    
    def top(self) -> int:
        return self.stack[-1] if self.stack else None
    
    def get_min(self) -> int:
        return self.min_stack[-1] if self.min_stack else None


def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluate Reverse Polish Notation - O(n) time, O(n) space
    Pattern: Stack for expression evaluation
    """
    stack = []
    
    for token in tokens:
        if token in {'+', '-', '*', '/'}:
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    
    return stack[0]


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    Daily Temperatures - O(n) time, O(n) space
    Pattern: Monotonic decreasing stack
    """
    result = [0] * len(temperatures)
    stack = []
    
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx
        stack.append(i)
    
    return result


def num_islands(grid: List[List[str]]) -> int:
    """
    Number of Islands - O(m * n) time, O(min(m, n)) space
    Pattern: BFS/DFS on grid
    """
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def bfs(r: int, c: int):
        queue = deque([(r, c)])
        grid[r][c] = '0'
        
        while queue:
            curr_r, curr_c = queue.popleft()
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_r, new_c = curr_r + dr, curr_c + dc
                
                if (0 <= new_r < rows and 0 <= new_c < cols and 
                    grid[new_r][new_c] == '1'):
                    grid[new_r][new_c] = '0'
                    queue.append((new_r, new_c))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                bfs(r, c)
    
    return count


# ============================================================================
# PATTERN 4: Linked List
# ============================================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Merge Two Sorted Lists - O(n + m) time, O(1) space
    Pattern: Iterative merging with dummy node
    """
    dummy = ListNode()
    curr = dummy
    
    while l1 and l2:
        if l1.val < l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    
    curr.next = l1 if l1 else l2
    return dummy.next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse Linked List - O(n) time, O(1) space
    Pattern: Three-pointer iteration
    """
    prev = None
    curr = head
    
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    
    return prev


def is_palindrome(head: Optional[ListNode]) -> bool:
    """
    Palindrome Linked List - O(n) time, O(1) space
    Pattern: Fast-slow pointers + reversal
    """
    if not head or not head.next:
        return True
    
    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    while slow:
        next_node = slow.next
        slow.next = prev
        prev = slow
        slow = next_node
    
    # Compare halves
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    
    return True


# ============================================================================
# PATTERN 5: Trees
# ============================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Binary Tree Level Order Traversal - O(n) time, O(n) space
    Pattern: BFS with queue
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result


def max_depth(root: Optional[TreeNode]) -> int:
    """
    Maximum Depth of Binary Tree - O(n) time, O(h) space
    Pattern: DFS recursion
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Validate BST - O(n) time, O(h) space
    Pattern: DFS with range validation
    """
    def validate(node: Optional[TreeNode], low: float, high: float) -> bool:
        if not node:
            return True
        
        if not (low < node.val < high):
            return False
        
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))
    
    return validate(root, float('-inf'), float('inf'))


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    Diameter of Binary Tree - O(n) time, O(h) space
    Pattern: DFS with global max tracking
    """
    diameter = [0]
    
    def depth(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        
        left_depth = depth(node.left)
        right_depth = depth(node.right)
        
        diameter[0] = max(diameter[0], left_depth + right_depth)
        
        return 1 + max(left_depth, right_depth)
    
    depth(root)
    return diameter[0]


def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    Balanced Binary Tree - O(n) time, O(h) space
    Pattern: DFS with balance checking
    """
    def check_balance(node: Optional[TreeNode]) -> Tuple[int, bool]:
        if not node:
            return 0, True
        
        left_height, left_balanced = check_balance(node.left)
        right_height, right_balanced = check_balance(node.right)
        
        balanced = (left_balanced and right_balanced and
                   abs(left_height - right_height) <= 1)
        
        return 1 + max(left_height, right_height), balanced
    
    _, result = check_balance(root)
    return result


# ============================================================================
# PATTERN 6: Graphs
# ============================================================================
def graph_bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    BFS on Graph - O(V + E) time, O(V) space
    Pattern: Queue-based traversal
    """
    visited = set()
    result = []
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result


def topological_sort(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    Topological Sort (Kahn's Algorithm) - O(V + E) time, O(V + E) space
    Pattern: BFS with in-degree tracking
    """
    in_degree = [0] * num_courses
    graph = defaultdict(list)
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == num_courses else []


def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    """
    Dijkstra's Algorithm - O((V + E) * log(V)) time, O(V + E) space
    Pattern: Priority queue for shortest path
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_dist > distances[curr_node]:
            continue
        
        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances


# ============================================================================
# TESTING
# ============================================================================
def test_all():
    print("=" * 80)
    print("Day 10: Comprehensive Review & Practice - Running Tests")
    print("=" * 80)
    
    # Test Two Sum
    print("\n1. Two Sum")
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    print("   ✓ Two Sum tests passed")
    
    # Test 3Sum
    print("\n2. 3Sum")
    result = three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted(result) == sorted([[-1, -1, 2], [-1, 0, 1]])
    print("   ✓ 3Sum tests passed")
    
    # Test Max Area
    print("\n3. Container With Most Water")
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    print("   ✓ Max Area tests passed")
    
    # Test Group Anagrams
    print("\n4. Group Anagrams")
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert len(result) == 3
    print("   ✓ Group Anagrams tests passed")
    
    # Test Longest Substring
    print("\n5. Longest Substring Without Repeating")
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    print("   ✓ Longest Substring tests passed")
    
    # Test Palindromic Substrings
    print("\n6. Count Palindromic Substrings")
    assert count_palindromic_substrings("abc") == 3
    assert count_palindromic_substrings("aaa") == 6
    print("   ✓ Palindromic Substrings tests passed")
    
    # Test Min Stack
    print("\n7. Min Stack")
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    assert min_stack.get_min() == -3
    min_stack.pop()
    assert min_stack.top() == 0
    assert min_stack.get_min() == -2
    print("   ✓ Min Stack tests passed")
    
    # Test Number of Islands
    print("\n8. Number of Islands")
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    assert num_islands(grid1) == 1
    
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    assert num_islands(grid2) == 3
    print("   ✓ Number of Islands tests passed")
    
    # Test Level Order
    print("\n9. Level Order Traversal")
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20, TreeNode(15), TreeNode(7))
    assert level_order(root) == [[3], [9, 20], [15, 7]]
    print("   ✓ Level Order tests passed")
    
    # Test Max Depth
    print("\n10. Max Depth")
    assert max_depth(root) == 3
    print("   ✓ Max Depth tests passed")
    
    # Test Valid BST
    print("\n11. Validate BST")
    bst_root = TreeNode(2)
    bst_root.left = TreeNode(1)
    bst_root.right = TreeNode(3)
    assert is_valid_bst(bst_root) == True
    print("   ✓ Validate BST tests passed")
    
    # Test BFS on Graph
    print("\n12. Graph BFS")
    graph = {
        0: [1, 2],
        1: [2],
        2: [0, 3],
        3: [3]
    }
    bfs_result = graph_bfs(graph, 2)
    assert bfs_result == [2, 0, 3, 1]
    print("   ✓ Graph BFS tests passed")
    
    # Test Topological Sort
    print("\n13. Topological Sort")
    result = topological_sort(6, [[3, 0], [3, 1], [4, 1], [4, 2], [5, 3], [5, 4]])
    assert len(result) == 6
    print("   ✓ Topological Sort tests passed")
    
    # Test Dijkstra
    print("\n14. Dijkstra's Algorithm")
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }
    distances = dijkstra(graph, 0)
    assert distances[0] == 0
    assert distances[1] == 3
    assert distances[2] == 1
    assert distances[3] == 4
    print("   ✓ Dijkstra's tests passed")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\nKey Patterns Reviewed:")
    print("  1. Arrays & Hashing: Two Sum, 3Sum, Container, Group Anagrams")
    print("  2. String Manipulation: Longest Substring, Palindromic, strStr")
    print("  3. Stack & Queue: Min Stack, Eval RPN, Daily Temperatures, Islands")
    print("  4. Linked List: Merge, Reverse, Palindrome")
    print("  5. Trees: Level Order, Max Depth, BST, Diameter, Balanced")
    print("  6. Graphs: BFS, Topological Sort, Dijkstra")
    print("\nReady for advanced problem solving!")


if __name__ == "__main__":
    test_all()
