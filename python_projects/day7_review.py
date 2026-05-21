"""
Day 7: Review & Practice - Mixed Problems from Days 1-6
Topics: Arrays, Strings, Stacks, Queues, Linked Lists, Trees
Focus: Pattern recognition, problem-solving strategies, implementation fluency
"""

from typing import List, Optional
from collections import deque, defaultdict


# ============================================================
# 1. ARRAYS & HASH MAP PATTERNS (Days 1-2)
# ============================================================

def two_sum(nums: List[int], target: int) -> List[int]:
    """
    LeetCode #1: Two Sum
    Given an array of integers and a target, return indices of two numbers that add to target.
    
    Time: O(n), Space: O(n)
    Pattern: Hash map for complement lookup
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
    LeetCode #15: 3Sum
    Find all unique triplets that sum to zero.
    
    Time: O(n²), Space: O(1) excluding output
    Pattern: Sort + two-pointer technique, skip duplicates
    """
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicates
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Two-pointer for remaining two numbers
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
    
    return result


def container_with_most_water(height: List[int]) -> int:
    """
    LeetCode #11: Container With Most Water
    Find two lines that form a container holding the most water.
    
    Time: O(n), Space: O(1)
    Pattern: Two-pointer from both ends, greedy approach
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate area
        h = min(height[left], height[right])
        w = right - left
        max_area = max(max_area, h * w)
        
        # Move pointer with shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    LeetCode #49: Group Anagrams
    Group strings that are anagrams of each other.
    
    Time: O(n * k log k) where k is max string length, Space: O(n * k)
    Pattern: Hash map with sorted string as key
    """
    anagram_map = defaultdict(list)
    
    for s in strs:
        # Sort string to create key
        key = ''.join(sorted(s))
        anagram_map[key].append(s)
    
    return list(anagram_map.values())


# ============================================================
# 2. STRING MANIPULATION PATTERNS (Day 3)
# ============================================================

def longest_substring_without_repeating(s: str) -> int:
    """
    LeetCode #3: Longest Substring Without Repeating Characters
    Find length of longest substring without repeating characters.
    
    Time: O(n), Space: O(min(n, m)) where m is charset size
    Pattern: Sliding window with hash set
    """
    seen = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        # Shrink window until no duplicate
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        
        # Update max length
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)
    
    return max_len


def longest_palindromic_substring(s: str) -> str:
    """
    LeetCode #5: Longest Palindromic Substring
    Find the longest palindromic substring.
    
    Time: O(n²), Space: O(1)
    Pattern: Expand around center
    """
    if not s:
        return ""
    
    start, end = 0, 0
    
    def expand_around_center(left: int, right: int) -> tuple:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1
    
    for i in range(len(s)):
        # Odd-length palindrome
        left1, right1 = expand_around_center(i, i)
        # Even-length palindrome
        left2, right2 = expand_around_center(i, i + 1)
        
        # Update longest
        if right1 - left1 > end - start:
            start, end = left1, right1
        if right2 - left2 > end - start:
            start, end = left2, right2
    
    return s[start:end + 1]


def str_str(haystack: str, needle: str) -> int:
    """
    LeetCode #28: Find the Index of the First Occurrence in a String
    Implement strStr().
    
    Time: O(n * m) naive, Space: O(1)
    Pattern: Sliding window matching
    """
    if not needle:
        return 0
    
    n, m = len(haystack), len(needle)
    
    for i in range(n - m + 1):
        if haystack[i:i + m] == needle:
            return i
    
    return -1


# ============================================================
# 3. STACK & QUEUE PATTERNS (Day 4)
# ============================================================

class MinStack:
    """
    LeetCode #155: Min Stack
    Design a stack that supports push, pop, top, and retrieving minimum in O(1).
    
    Time: O(1) for all operations, Space: O(n)
    Pattern: Two stacks - main stack and min stack
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
            if self.min_stack and self.min_stack[-1] == val:
                self.min_stack.pop()
    
    def top(self) -> int:
        return self.stack[-1] if self.stack else None
    
    def get_min(self) -> int:
        return self.min_stack[-1] if self.min_stack else None


def eval_rpn(tokens: List[str]) -> int:
    """
    LeetCode #150: Evaluate Reverse Polish Notation
    Evaluate arithmetic expression in RPN.
    
    Time: O(n), Space: O(n)
    Pattern: Stack-based evaluation
    """
    stack = []
    operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b),  # Truncate toward zero
    }
    
    for token in tokens:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            result = operators[token](a, b)
            stack.append(result)
        else:
            stack.append(int(token))
    
    return stack[0]


def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    LeetCode #739: Daily Temperatures
    For each day, find how many days until warmer temperature.
    
    Time: O(n), Space: O(n)
    Pattern: Monotonic decreasing stack
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Store indices
    
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    
    return result


def num_islands(grid: List[List[str]]) -> int:
    """
    LeetCode #200: Number of Islands
    Count number of islands in 2D grid.
    
    Time: O(m * n), Space: O(m * n) in worst case
    Pattern: BFS/DFS for connected components
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def bfs(r: int, c: int) -> None:
        queue = deque([(r, c)])
        grid[r][c] = '0'  # Mark as visited
        
        while queue:
            row, col = queue.popleft()
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'
                    queue.append((nr, nc))
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                count += 1
                bfs(i, j)
    
    return count


# ============================================================
# 4. LINKED LIST PATTERNS (Day 5)
# ============================================================

class ListNode:
    """Node for a singly linked list."""
    
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    LeetCode #876: Middle of the Linked List
    Find the middle node of a linked list.
    
    Time: O(n), Space: O(1)
    Pattern: Fast-slow pointers
    """
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow


def has_cycle(head: Optional[ListNode]) -> bool:
    """
    LeetCode #141: Linked List Cycle
    Determine if linked list has a cycle.
    
    Time: O(n), Space: O(1)
    Pattern: Floyd's cycle detection (tortoise and hare)
    """
    if not head or not head.next:
        return False
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False


def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    LeetCode #142: Linked List Cycle II
    Find the starting node of a cycle.
    
    Time: O(n), Space: O(1)
    Pattern: Floyd's + reset one pointer to head
    """
    if not head or not head.next:
        return None
    
    slow = head
    fast = head
    
    # Detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            # Find cycle start
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    
    return None


def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    LeetCode #21: Merge Two Sorted Lists
    Merge two sorted linked lists into one sorted list.
    
    Time: O(n + m), Space: O(1)
    Pattern: Dummy node + iterative merge
    """
    dummy = ListNode()
    curr = dummy
    
    while list1 and list2:
        if list1.val < list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next
    
    curr.next = list1 if list1 else list2
    
    return dummy.next


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    LeetCode #206: Reverse Linked List
    Reverse a linked list iteratively.
    
    Time: O(n), Space: O(1)
    Pattern: Three-pointer reversal
    """
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    return prev


def is_palindrome(head: Optional[ListNode]) -> bool:
    """
    LeetCode #234: Palindrome Linked List
    Check if linked list is a palindrome.
    
    Time: O(n), Space: O(1)
    Pattern: Find middle + reverse second half + compare
    """
    if not head or not head.next:
        return True
    
    # Find middle
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    curr = slow
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    # Compare
    first = head
    second = prev
    while second:
        if first.val != second.val:
            return False
        first = first.next
        second = second.next
    
    return True


# ============================================================
# 5. TREE PATTERNS (Day 6)
# ============================================================

class TreeNode:
    """Node for a binary tree."""
    
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    LeetCode #102: Binary Tree Level Order Traversal
    Return level-order traversal of binary tree.
    
    Time: O(n), Space: O(w) where w is max width
    Pattern: BFS with queue
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(current_level)
    
    return result


def max_depth(root: Optional[TreeNode]) -> int:
    """
    LeetCode #104: Maximum Depth of Binary Tree
    Calculate the maximum depth of binary tree.
    
    Time: O(n), Space: O(h)
    Pattern: DFS with recursion
    """
    if not root:
        return 0
    
    return 1 + max(max_depth(root.left), max_depth(root.right))


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    LeetCode #98: Validate Binary Search Tree
    Validate if a binary tree is a valid BST.
    
    Time: O(n), Space: O(h)
    Pattern: DFS with range validation
    """
    def validate(node, low=float('-inf'), high=float('inf')) -> bool:
        if not node:
            return True
        
        if node.val <= low or node.val >= high:
            return False
        
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))
    
    return validate(root)


def lowest_common_ancestor_bst(root: Optional[TreeNode], 
                                p: Optional[TreeNode], 
                                q: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    LeetCode #235: Lowest Common Ancestor of a BST
    Find LCA in a BST using BST property.
    
    Time: O(h), Space: O(h)
    Pattern: BST property optimization
    """
    if not root:
        return None
    
    # Both smaller, go left
    if p.val < root.val and q.val < root.val:
        return lowest_common_ancestor_bst(root.left, p, q)
    
    # Both larger, go right
    if p.val > root.val and q.val > root.val:
        return lowest_common_ancestor_bst(root.right, p, q)
    
    # Split point, current is LCA
    return root


def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    LeetCode #543: Diameter of Binary Tree
    Calculate the diameter (longest path between any two nodes).
    
    Time: O(n), Space: O(h)
    Pattern: DFS with height and diameter tracking
    """
    diameter = [0]
    
    def height(node):
        if not node:
            return 0
        
        left_h = height(node.left)
        right_h = height(node.right)
        
        # Update diameter
        diameter[0] = max(diameter[0], left_h + right_h)
        
        return 1 + max(left_h, right_h)
    
    height(root)
    return diameter[0]


def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    LeetCode #110: Balanced Binary Tree
    Check if binary tree is height-balanced.
    
    Time: O(n), Space: O(h)
    Pattern: DFS with balance checking
    """
    def check(node):
        if not node:
            return (True, 0)
        
        left_balanced, left_h = check(node.left)
        right_balanced, right_h = check(node.right)
        
        is_bal = (left_balanced and right_balanced and 
                  abs(left_h - right_h) <= 1)
        
        return (is_bal, 1 + max(left_h, right_h))
    
    return check(root)[0]


def build_tree(values: List[Optional[int]], index: int = 0) -> Optional[TreeNode]:
    """Build a binary tree from a list of values (level-order)."""
    if index >= len(values) or values[index] is None:
        return None
    
    root = TreeNode(values[index])
    root.left = build_tree(values, 2 * index + 1)
    root.right = build_tree(values, 2 * index + 2)
    
    return root


# ============================================================
# TESTING
# ============================================================

def test_arrays_and_hashing():
    """Test array and hash map patterns."""
    print("=" * 60)
    print("Testing Arrays & Hashing Patterns")
    print("=" * 60)
    
    # Two Sum
    result = two_sum([2, 7, 11, 15], 9)
    print(f"✓ Two Sum: {result} (expected [0, 1])")
    assert result == [0, 1]
    
    # Three Sum
    result = three_sum([-1, 0, 1, 2, -1, -4])
    print(f"✓ 3Sum: {result}")
    assert len(result) == 2
    
    # Container With Most Water
    result = container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7])
    print(f"✓ Container: {result} (expected 49)")
    assert result == 49
    
    # Group Anagrams
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    print(f"✓ Group Anagrams: {len(result)} groups (expected 3)")
    assert len(result) == 3
    
    print("✓ All Arrays & Hashing tests passed\n")


def test_string_manipulation():
    """Test string manipulation patterns."""
    print("=" * 60)
    print("Testing String Manipulation Patterns")
    print("=" * 60)
    
    # Longest Substring Without Repeating
    result = longest_substring_without_repeating("abcabcbb")
    print(f"✓ Longest Substring: {result} (expected 3)")
    assert result == 3
    
    # Longest Palindromic Substring
    result = longest_palindromic_substring("babad")
    print(f"✓ Longest Palindrome: '{result}' (expected 'bab' or 'aba')")
    assert result in ["bab", "aba"]
    
    # strStr
    result = str_str("hello", "ll")
    print(f"✓ strStr: {result} (expected 2)")
    assert result == 2
    
    print("✓ All String Manipulation tests passed\n")


def test_stack_and_queue():
    """Test stack and queue patterns."""
    print("=" * 60)
    print("Testing Stack & Queue Patterns")
    print("=" * 60)
    
    # Min Stack
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    result = min_stack.get_min()
    print(f"✓ Min Stack get_min: {result} (expected -3)")
    assert result == -3
    
    min_stack.pop()
    result = min_stack.top()
    print(f"✓ Min Stack top: {result} (expected 0)")
    assert result == 0
    
    # Eval RPN
    result = eval_rpn(["2", "1", "+", "3", "*"])
    print(f"✓ Eval RPN: {result} (expected 9)")
    assert result == 9
    
    # Daily Temperatures
    result = daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
    print(f"✓ Daily Temperatures: {result}")
    assert result == [1, 1, 4, 2, 1, 1, 0, 0]
    
    # Number of Islands
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    result = num_islands([row[:] for row in grid])
    print(f"✓ Number of Islands: {result} (expected 3)")
    assert result == 3
    
    print("✓ All Stack & Queue tests passed\n")


def test_linked_list():
    """Test linked list patterns."""
    print("=" * 60)
    print("Testing Linked List Patterns")
    print("=" * 60)
    
    # Create list: 1 -> 2 -> 3 -> 4 -> 5
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    
    # Middle Node
    result = middle_node(head)
    print(f"✓ Middle Node: {result.val} (expected 3)")
    assert result.val == 3
    
    # Merge Two Sorted Lists
    list1 = ListNode(1, ListNode(3, ListNode(5)))
    list2 = ListNode(2, ListNode(4, ListNode(6)))
    merged = merge_two_lists(list1, list2)
    
    result = []
    curr = merged
    while curr:
        result.append(curr.val)
        curr = curr.next
    print(f"✓ Merge Lists: {result} (expected [1,2,3,4,5,6])")
    assert result == [1, 2, 3, 4, 5, 6]
    
    # Reverse List
    head2 = ListNode(1, ListNode(2, ListNode(3)))
    reversed_head = reverse_list(head2)
    result = []
    curr = reversed_head
    while curr:
        result.append(curr.val)
        curr = curr.next
    print(f"✓ Reverse List: {result} (expected [3,2,1])")
    assert result == [3, 2, 1]
    
    # Palindrome Linked List
    palindrome = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))
    result = is_palindrome(palindrome)
    print(f"✓ Is Palindrome: {result} (expected True)")
    assert result == True
    
    print("✓ All Linked List tests passed\n")


def test_trees():
    """Test tree patterns."""
    print("=" * 60)
    print("Testing Tree Patterns")
    print("=" * 60)
    
    # Build tree:
    #       3
    #      / \
    #     9  20
    #        / \
    #       15  7
    root = build_tree([3, 9, 20, None, None, 15, 7])
    
    # Level Order
    result = level_order(root)
    print(f"✓ Level Order: {result}")
    assert result == [[3], [9, 20], [15, 7]]
    
    # Max Depth
    result = max_depth(root)
    print(f"✓ Max Depth: {result} (expected 3)")
    assert result == 3
    
    # Validate BST
    bst = build_tree([2, 1, 3])
    result = is_valid_bst(bst)
    print(f"✓ Is Valid BST: {result} (expected True)")
    assert result == True
    
    # Diameter
    result = diameter_of_binary_tree(root)
    print(f"✓ Diameter: {result} (expected 3)")
    assert result == 3
    
    # Is Balanced
    result = is_balanced(root)
    print(f"✓ Is Balanced: {result} (expected True)")
    assert result == True
    
    print("✓ All Tree tests passed\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DAY 7: REVIEW & PRACTICE - COMPREHENSIVE TESTING")
    print("=" * 60 + "\n")
    
    test_arrays_and_hashing()
    test_string_manipulation()
    test_stack_and_queue()
    test_linked_list()
    test_trees()
    
    print("=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)
    print("\nDay 7 Review Complete!")
    print("Key patterns reviewed:")
    print("  • Hash map for complement lookup and frequency counting")
    print("  • Two-pointer techniques (opposite direction, fast-slow)")
    print("  • Sliding window with hash set")
    print("  • Stack-based evaluation and monotonic stack")
    print("  • BFS for connected components and level-order traversal")
    print("  • Linked list reversal and merging")
    print("  • Tree traversals and property validation")
    print("=" * 60)
