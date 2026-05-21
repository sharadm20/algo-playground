"""
Day 4: Stack & Queue Data Structures
=====================================
Topics Covered:
1. Stack Operations and Applications
2. Queue Operations and Applications
3. Monotonic Stack Patterns
4. BFS (Breadth-First Search) Applications

Each section includes:
- Concept explanation
- Implementation template
- Practice problems with solutions
"""

# ============================================================================
# 1. STACK OPERATIONS AND APPLICATIONS
# ============================================================================

class StackUsingArray:
    """
    Stack implementation using array (list in Python).

    Operations:
    - push(x): Add element to top - O(1)
    - pop(): Remove top element - O(1)
    - peek(): View top element - O(1)
    - is_empty(): Check if empty - O(1)

    Applications:
    - Function call stack
    - Undo mechanisms
    - Expression evaluation
    - Backtracking algorithms
    """

    def __init__(self):
        self.stack = []

    def push(self, x: int) -> None:
        """Push element onto stack."""
        self.stack.append(x)

    def pop(self) -> int:
        """Remove and return top element."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.stack.pop()

    def peek(self) -> int:
        """Return top element without removing."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.stack[-1]

    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.stack) == 0

    def size(self) -> int:
        """Return stack size."""
        return len(self.stack)


class MinStack:
    """
    Problem: Design a stack that supports push, pop, top, and retrieving
    the minimum element in constant time.

    Example:
        minStack = MinStack()
        minStack.push(-2)
        minStack.push(0)
        minStack.push(-3)
        minStack.getMin()  # Returns -3
        minStack.pop()
        minStack.top()     # Returns 0
        minStack.getMin()  # Returns -2

    Approach: Use two stacks
    - Main stack stores all values
    - Min stack tracks minimum at each level
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        """Push element onto stack."""
        self.stack.append(val)
        # Push to min_stack if it's smaller or equal to current min
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> int:
        """Remove and return top element."""
        if not self.stack:
            raise IndexError("Pop from empty stack")
        val = self.stack.pop()
        # Pop from min_stack if it matches
        if self.min_stack and self.min_stack[-1] == val:
            self.min_stack.pop()
        return val

    def top(self) -> int:
        """Return top element."""
        if not self.stack:
            raise IndexError("Top from empty stack")
        return self.stack[-1]

    def get_min(self) -> int:
        """Return minimum element."""
        if not self.min_stack:
            raise IndexError("GetMin from empty stack")
        return self.min_stack[-1]


class ValidParentheses:
    """
    Problem: Given a string containing just '(', ')', '{', '}', '[' and ']',
    determine if the input string is valid.

    Example:
        "()" → True
        "()[]{}" → True
        "(]" → False
        "([)]" → False
        "{[]}" → True

    Approach: Stack-based validation
    - Push opening brackets onto stack
    - For closing brackets, check if matches top of stack
    - String is valid if stack is empty at end
    """

    @staticmethod
    def is_valid(s: str) -> bool:
        """Check if parentheses string is valid."""
        # Map closing to opening brackets
        bracket_map = {')': '(', '}': '{', ']': '['}
        stack = []

        for char in s:
            if char in bracket_map:
                # Pop from stack if matching, else use dummy
                top_element = stack.pop() if stack else '#'
                if bracket_map[char] != top_element:
                    return False
            else:
                # Push opening bracket
                stack.append(char)

        # Valid if stack is empty
        return not stack


class EvaluateReversePolishNotation:
    """
    Problem: Evaluate the value of an arithmetic expression in Reverse Polish Notation.
    Valid operators: +, -, *, /

    Example:
        ["2", "1", "+", "3", "*"] → 9  # ((2 + 1) * 3)
        ["4", "13", "5", "/", "+"] → 6  # (4 + (13 / 5))

    Approach: Stack-based evaluation
    - Push numbers onto stack
    - When operator encountered, pop two operands, compute, push result
    """

    @staticmethod
    def eval_rpn(tokens: list[str]) -> int:
        """Evaluate Reverse Polish Notation expression."""
        stack = []
        operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: int(a / b),  # Truncate toward zero
        }

        for token in tokens:
            if token in operators:
                # Pop two operands (note: order matters for - and /)
                b = stack.pop()
                a = stack.pop()
                # Apply operator and push result
                result = operators[token](a, b)
                stack.append(result)
            else:
                # Push number
                stack.append(int(token))

        return stack[0]


# ============================================================================
# 2. QUEUE OPERATIONS AND APPLICATIONS
# ============================================================================

class QueueUsingDeque:
    """
    Queue implementation using deque (double-ended queue).

    Operations:
    - enqueue(x): Add element to rear - O(1)
    - dequeue(): Remove front element - O(1)
    - front(): View front element - O(1)
    - is_empty(): Check if empty - O(1)

    Applications:
    - BFS traversal
    - Level-order traversal
    - Task scheduling
    - Buffer management
    """

    def __init__(self):
        from collections import deque
        self.queue = deque()

    def enqueue(self, x: int) -> None:
        """Add element to rear of queue."""
        self.queue.append(x)

    def dequeue(self) -> int:
        """Remove and return front element."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.queue.popleft()

    def front(self) -> int:
        """Return front element without removing."""
        if self.is_empty():
            raise IndexError("Front from empty queue")
        return self.queue[0]

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.queue) == 0

    def size(self) -> int:
        """Return queue size."""
        return len(self.queue)


class MyCircularQueue:
    """
    Problem: Design a circular queue (ring buffer) with fixed size k.

    Example:
        cq = MyCircularQueue(3)
        cq.en_queue(1)  # True
        cq.en_queue(2)  # True
        cq.en_queue(3)  # True
        cq.en_queue(4)  # False (full)
        cq.rear()       # 3
        cq.is_full()    # True
        cq.de_queue()   # True
        cq.en_queue(4)  # True
        cq.rear()       # 4

    Approach: Array with two pointers
    - Use array of size k
    - Front pointer points to first element
    - Rear pointer points to next available slot
    - Track count to distinguish full vs empty
    """

    def __init__(self, k: int):
        """Initialize circular queue with capacity k."""
        self.capacity = k
        self.queue = [0] * k
        self.front_idx = 0
        self.rear_idx = 0
        self.count = 0

    def en_queue(self, value: int) -> bool:
        """Insert element into queue."""
        if self.is_full():
            return False
        self.queue[self.rear_idx] = value
        self.rear_idx = (self.rear_idx + 1) % self.capacity
        self.count += 1
        return True

    def de_queue(self) -> bool:
        """Delete element from queue."""
        if self.is_empty():
            return False
        self.front_idx = (self.front_idx + 1) % self.capacity
        self.count -= 1
        return True

    def front(self) -> int:
        """Get front item."""
        if self.is_empty():
            return -1
        return self.queue[self.front_idx]

    def rear(self) -> int:
        """Get last item."""
        if self.is_empty():
            return -1
        return self.queue[(self.rear_idx - 1) % self.capacity]

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.count == 0

    def is_full(self) -> bool:
        """Check if queue is full."""
        return self.count == self.capacity


# ============================================================================
# 3. MONOTONIC STACK PATTERNS
# ============================================================================

class MonotonicStackPatterns:
    """
    Monotonic Stack patterns:

    Pattern 1: Next Greater Element
    - Used for: Finding next greater/smaller element
    - Time: O(n), Space: O(n)

    Pattern 2: Daily Temperatures
    - Used for: Finding distance to next greater element
    - Time: O(n), Space: O(n)

    Pattern 3: Largest Rectangle in Histogram
    - Used for: Finding maximum area
    - Time: O(n), Space: O(n)
    """

    @staticmethod
    def next_greater_element(nums: list[int]) -> list[int]:
        """
        Problem: Find the next greater element for each element.

        Example: nums = [2, 1, 2, 4, 3] → [4, 2, 4, -1, -1]

        Approach: Monotonic decreasing stack
        - Stack stores indices of elements waiting for greater element
        - When current > stack top, we found next greater for stack top
        """
        n = len(nums)
        result = [-1] * n
        stack = []  # Store indices

        for i in range(n):
            # While current element is greater than stack top
            while stack and nums[i] > nums[stack[-1]]:
                idx = stack.pop()
                result[idx] = nums[i]
            stack.append(i)

        return result

    @staticmethod
    def daily_temperatures(temperatures: list[int]) -> list[int]:
        """
        Problem: For each day, find how many days until warmer temperature.

        Example: temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
                 → [1, 1, 4, 2, 1, 1, 0, 0]

        Approach: Monotonic decreasing stack
        - Stack stores indices of days waiting for warmer temperature
        - When current temp > stack top, calculate waiting days
        """
        n = len(temperatures)
        result = [0] * n
        stack = []  # Store indices

        for i in range(n):
            # While current temperature is warmer than stack top
            while stack and temperatures[i] > temperatures[stack[-1]]:
                idx = stack.pop()
                result[idx] = i - idx
            stack.append(i)

        return result

    @staticmethod
    def largest_rectangle_in_histogram(heights: list[int]) -> int:
        """
        Problem: Find largest rectangle in histogram.

        Example: heights = [2, 1, 5, 6, 2, 3] → 10

        Approach: Monotonic increasing stack
        - Stack stores indices of bars in increasing height order
        - When current < stack top, pop and calculate area with popped height
        - Width = current index - new stack top index - 1
        """
        stack = []
        max_area = 0
        n = len(heights)

        for i in range(n + 1):
            # Use 0 height at end to pop remaining bars
            h = heights[i] if i < n else 0

            while stack and h < heights[stack[-1]]:
                height = heights[stack.pop()]
                # Width extends from after previous bar to current
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)

            stack.append(i)

        return max_area

    @staticmethod
    def maximal_rectangle(matrix: list[list[str]]) -> int:
        """
        Problem: Find largest rectangle containing only 1's in binary matrix.

        Example: matrix = [["1","0","1","0","0"],
                          ["1","0","1","1","1"],
                          ["1","1","1","1","1"],
                          ["1","0","0","1","0"]]
                 → 6

        Approach: Build histograms row by row
        - For each row, build histogram of consecutive 1's above
        - Apply largest rectangle in histogram for each row
        """
        if not matrix or not matrix[0]:
            return 0

        cols = len(matrix[0])
        heights = [0] * cols
        max_area = 0

        for row in matrix:
            # Update heights
            for j in range(cols):
                if row[j] == '1':
                    heights[j] += 1
                else:
                    heights[j] = 0

            # Calculate max area for current histogram
            max_area = max(max_area, MonotonicStackPatterns.largest_rectangle_in_histogram(heights))

        return max_area


# ============================================================================
# 4. BFS (BREADTH-FIRST SEARCH) APPLICATIONS
# ============================================================================

class BFSApplications:
    """
    BFS patterns:

    Pattern 1: Level-Order Traversal
    - Used for: Tree level processing
    - Time: O(n), Space: O(w) where w is max width

    Pattern 2: Shortest Path in Unweighted Graph
    - Used for: Finding minimum steps
    - Time: O(V + E), Space: O(V)

    Pattern 3: Multi-Source BFS
    - Used for: Distance from nearest source
    - Time: O(m*n), Space: O(m*n)
    """

    @staticmethod
    def level_order_traversal(root) -> list[list[int]]:
        """
        Problem: Return level-order traversal of binary tree.

        Example:     3
                    / \\
                   9  20
                     /  \\
                    15   7
                 → [[3], [9, 20], [15, 7]]

        Approach: Queue-based level processing
        - Add root to queue
        - Process all nodes at current level before next
        - Track level size to know when level ends
        """
        from collections import deque

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

    @staticmethod
    def num_islands(grid: list[list[str]]) -> int:
        """
        Problem: Count number of islands in 2D grid ('1' = land, '0' = water).

        Example: grid = [["1","1","0","0","0"],
                        ["1","1","0","0","0"],
                        ["0","0","1","0","0"],
                        ["0","0","0","1","1"]]
                 → 3

        Approach: BFS/DFS to mark connected components
        - Iterate through grid, when find '1', increment count
        - Use BFS to mark entire island as visited
        """
        from collections import deque

        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        count = 0

        def bfs(r: int, c: int) -> None:
            """Mark entire island using BFS."""
            queue = deque([(r, c)])
            grid[r][c] = '0'  # Mark as visited

            while queue:
                row, col = queue.popleft()

                # Check all 4 directions
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                        grid[nr][nc] = '0'  # Mark as visited
                        queue.append((nr, nc))

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == '1':
                    count += 1
                    bfs(i, j)

        return count

    @staticmethod
    def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
        """
        Problem: Find shortest clear path from top-left to bottom-right.
        Can move in 8 directions. Return -1 if no path.

        Example: grid = [[0,0,0],
                        [1,1,0],
                        [1,1,0]]
                 → 4

        Approach: BFS for shortest path in unweighted grid
        - Start from (0, 0), explore 8 directions
        - Track distance, return when reach (n-1, n-1)
        """
        from collections import deque

        if not grid or not grid[0]:
            return -1

        n = len(grid)

        # Check if start or end is blocked
        if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return -1

        # Special case: single cell
        if n == 1:
            return 1

        # BFS
        queue = deque([(0, 0, 1)])  # (row, col, distance)
        grid[0][0] = 1  # Mark as visited

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]

        while queue:
            row, col, dist = queue.popleft()

            # Explore 8 directions
            for dr, dc in directions:
                nr, nc = row + dr, col + dc

                # Check if reached destination
                if nr == n - 1 and nc == n - 1:
                    return dist + 1

                # Check bounds and if cell is clear
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1  # Mark as visited
                    queue.append((nr, nc, dist + 1))

        return -1

    @staticmethod
    def rotting_oranges(grid: list[list[int]]) -> int:
        """
        Problem: Find minimum minutes until no fresh oranges left.
        0 = empty, 1 = fresh, 2 = rotten. Return -1 if impossible.

        Example: grid = [[2,1,1],
                        [1,1,0],
                        [0,1,1]]
                 → 4

        Approach: Multi-source BFS
        - Add all rotten oranges to queue initially
        - Process level by level, each level = 1 minute
        - Count fresh oranges, decrement as they rot
        """
        from collections import deque

        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        queue = deque()
        fresh_count = 0

        # Initialize: count fresh, add rotten to queue
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 2:
                    queue.append((i, j))
                elif grid[i][j] == 1:
                    fresh_count += 1

        # No fresh oranges initially
        if fresh_count == 0:
            return 0

        minutes = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue and fresh_count > 0:
            # Process all oranges at current minute
            for _ in range(len(queue)):
                row, col = queue.popleft()

                # Rot adjacent fresh oranges
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2  # Make rotten
                        fresh_count -= 1
                        queue.append((nr, nc))

            minutes += 1

        return minutes if fresh_count == 0 else -1

    @staticmethod
    def word_ladder(begin_word: str, end_word: str, word_list: list[str]) -> int:
        """
        Problem: Find shortest transformation sequence from begin_word to end_word.
        Only one letter can be changed at a time, each transformed word must exist in word_list.

        Example: begin_word = "hit", end_word = "cog",
                 word_list = ["hot","dot","dog","lot","log","cog"]
                 → 5  (hit -> hot -> dot -> dog -> cog)

        Approach: BFS on word transformation graph
        - Each word is a node, edges connect words differing by one letter
        - BFS finds shortest path
        """
        from collections import deque, defaultdict

        if end_word not in word_list:
            return 0

        # Build adjacency list using generic intermediate states
        # e.g., "hot" -> {"*ot": ["hot"], "h*t": ["hot"], "ho*": ["hot"]}
        all_combo_dict = defaultdict(list)
        for word in word_list:
            for i in range(len(word)):
                generic_form = word[:i] + "*" + word[i + 1:]
                all_combo_dict[generic_form].append(word)

        # BFS
        queue = deque([(begin_word, 1)])
        visited = {begin_word}

        while queue:
            current_word, level = queue.popleft()

            # Try all possible generic forms
            for i in range(len(current_word)):
                generic_form = current_word[:i] + "*" + current_word[i + 1:]

                for neighbor in all_combo_dict[generic_form]:
                    if neighbor == end_word:
                        return level + 1

                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, level + 1))

        return 0


# ============================================================================
# TreeNode class for tree problems
# ============================================================================

class TreeNode:
    """Binary tree node."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
# TEST CASES
# ============================================================================

def run_tests():
    """Run all test cases."""
    print("=" * 60)
    print("Day 4: Stack & Queue - Test Cases")
    print("=" * 60)

    # Test 1: Valid Parentheses
    print("\n1. Valid Parentheses")
    test_cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
    ]
    for s, expected in test_cases:
        result = ValidParentheses.is_valid(s)
        status = "✓" if result == expected else "✗"
        print(f"  {status} is_valid('{s}') = {result} (expected {expected})")

    # Test 2: Min Stack
    print("\n2. Min Stack")
    min_stack = MinStack()
    min_stack.push(-2)
    min_stack.push(0)
    min_stack.push(-3)
    print(f"  getMin() = {min_stack.get_min()} (expected -3) {'✓' if min_stack.get_min() == -3 else '✗'}")
    min_stack.pop()
    print(f"  top() = {min_stack.top()} (expected 0) {'✓' if min_stack.top() == 0 else '✗'}")
    print(f"  getMin() = {min_stack.get_min()} (expected -2) {'✓' if min_stack.get_min() == -2 else '✗'}")

    # Test 3: Evaluate Reverse Polish Notation
    print("\n3. Evaluate Reverse Polish Notation")
    test_cases = [
        (["2", "1", "+", "3", "*"], 9),
        (["4", "13", "5", "/", "+"], 6),
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
    ]
    for tokens, expected in test_cases:
        result = EvaluateReversePolishNotation.eval_rpn(tokens)
        status = "✓" if result == expected else "✗"
        print(f"  {status} eval_rpn({tokens}) = {result} (expected {expected})")

    # Test 4: Next Greater Element
    print("\n4. Next Greater Element")
    test_cases = [
        ([2, 1, 2, 4, 3], [4, 2, 4, -1, -1]),
        ([1, 2, 3, 4, 5], [2, 3, 4, 5, -1]),
        ([5, 4, 3, 2, 1], [-1, -1, -1, -1, -1]),
    ]
    for nums, expected in test_cases:
        result = MonotonicStackPatterns.next_greater_element(nums)
        status = "✓" if result == expected else "✗"
        print(f"  {status} next_greater({nums}) = {result} (expected {expected})")

    # Test 5: Daily Temperatures
    print("\n5. Daily Temperatures")
    test_cases = [
        ([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
        ([30, 40, 50, 60], [1, 1, 1, 0]),
        ([30, 60, 90], [1, 1, 0]),
    ]
    for temps, expected in test_cases:
        result = MonotonicStackPatterns.daily_temperatures(temps)
        status = "✓" if result == expected else "✗"
        print(f"  {status} daily_temps({temps}) = {result} (expected {expected})")

    # Test 6: Largest Rectangle in Histogram
    print("\n6. Largest Rectangle in Histogram")
    test_cases = [
        ([2, 1, 5, 6, 2, 3], 10),
        ([2, 4], 4),
        ([1], 1),
    ]
    for heights, expected in test_cases:
        result = MonotonicStackPatterns.largest_rectangle_in_histogram(heights)
        status = "✓" if result == expected else "✗"
        print(f"  {status} largest_rectangle({heights}) = {result} (expected {expected})")

    # Test 7: Number of Islands
    print("\n7. Number of Islands")
    grid1 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    result = BFSApplications.num_islands([row[:] for row in grid1])
    print(f"  {'✓' if result == 3 else '✗'} num_islands(grid1) = {result} (expected 3)")

    grid2 = [
        ["1", "1", "1"],
        ["0", "1", "0"],
        ["1", "1", "1"],
    ]
    result = BFSApplications.num_islands([row[:] for row in grid2])
    print(f"  {'✓' if result == 1 else '✗'} num_islands(grid2) = {result} (expected 1)")

    # Test 8: Rotting Oranges
    print("\n8. Rotting Oranges")
    grid1 = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1],
    ]
    result = BFSApplications.rotting_oranges([row[:] for row in grid1])
    print(f"  {'✓' if result == 4 else '✗'} rotting_oranges(grid1) = {result} (expected 4)")

    grid2 = [
        [2, 1, 1],
        [0, 1, 1],
        [1, 0, 1],
    ]
    result = BFSApplications.rotting_oranges([row[:] for row in grid2])
    print(f"  {'✓' if result == -1 else '✗'} rotting_oranges(grid2) = {result} (expected -1)")

    # Test 9: Circular Queue
    print("\n9. Circular Queue")
    cq = MyCircularQueue(3)
    print(f"  {'✓' if cq.en_queue(1) else '✗'} en_queue(1) = True")
    print(f"  {'✓' if cq.en_queue(2) else '✗'} en_queue(2) = True")
    print(f"  {'✓' if cq.en_queue(3) else '✗'} en_queue(3) = True")
    print(f"  {'✓' if not cq.en_queue(4) else '✗'} en_queue(4) = False (full)")
    print(f"  {'✓' if cq.rear() == 3 else '✗'} rear() = {cq.rear()} (expected 3)")
    print(f"  {'✓' if cq.is_full() else '✗'} is_full() = True")
    print(f"  {'✓' if cq.de_queue() else '✗'} de_queue() = True")
    print(f"  {'✓' if cq.en_queue(4) else '✗'} en_queue(4) = True")
    print(f"  {'✓' if cq.rear() == 4 else '✗'} rear() = {cq.rear()} (expected 4)")

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
