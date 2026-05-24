"""
Day 15: Heaps, Tries, & Bit Manipulation
Topics: Priority queues, prefix trees, bitwise operations
"""

import heapq
from typing import List, Dict, Optional
from collections import Counter


# ============================================================================
# PATTERN 1: Heaps & Priority Queues
# ============================================================================

class TrieNode:
    """Node for Trie data structure."""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    """Trie (Prefix Tree) implementation."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Search for a complete word in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Check if any word in trie starts with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """
    Top K Frequent Elements - O(n log k) time, O(n) space
    Pattern: Min-heap to track top k frequent elements
    """
    # Count frequency
    freq = Counter(nums)
    
    # Use min-heap of size k
    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    # Extract elements
    return [num for count, num in heap]


def kth_largest(nums: List[int], k: int) -> int:
    """
    Kth Largest Element in Array - O(n log k) time, O(k) space
    Pattern: Min-heap to maintain k largest elements
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]


def merge_k_sorted_lists(lists: List[List[int]]) -> List[int]:
    """
    Merge K Sorted Lists - O(n log k) time, O(n) space
    Pattern: Min-heap to merge k sorted arrays
    """
    if not lists:
        return []
    
    heap = []
    # Push first element of each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    
    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        # Push next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result


def find_median_from_stream():
    """
    Find Median from Data Stream - O(log n) insert, O(1) find median
    Pattern: Two heaps (max-heap for lower half, min-heap for upper half)
    Returns a closure with add_num and find_median methods
    """
    max_heap = []  # Lower half (negated for max-heap)
    min_heap = []  # Upper half
    
    def add_num(num: int) -> None:
        # Add to max-heap (lower half)
        heapq.heappush(max_heap, -num)
        
        # Balance: max of lower <= min of upper
        if max_heap and min_heap and (-max_heap[0] > min_heap[0]):
            val = -heapq.heappop(max_heap)
            heapq.heappush(min_heap, val)
        
        # Balance sizes
        if len(max_heap) > len(min_heap) + 1:
            val = -heapq.heappop(max_heap)
            heapq.heappush(min_heap, val)
        elif len(min_heap) > len(max_heap) + 1:
            val = heapq.heappop(min_heap)
            heapq.heappush(max_heap, -val)
    
    def find_median() -> float:
        if len(max_heap) > len(min_heap):
            return -max_heap[0]
        elif len(min_heap) > len(max_heap):
            return min_heap[0]
        else:
            return (-max_heap[0] + min_heap[0]) / 2
    
    return add_num, find_median


# ============================================================================
# PATTERN 2: Trie Applications
# ============================================================================

def word_search_on_board(board: List[List[str]], words: List[str]) -> List[str]:
    """
    Word Search II - O(m*n*4^L) time where L is max word length
    Pattern: Trie + DFS on board
    """
    if not board or not board[0]:
        return []
    
    # Build trie from words
    trie = Trie()
    word_set = set(words)
    for word in words:
        trie.insert(word)
    
    result = []
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c, node, path):
        char = board[r][c]
        if char not in node.children:
            return
        
        node = node.children[char]
        path.append(char)
        
        # Check if we found a word
        if node.is_end_of_word:
            word = ''.join(path)
            if word not in result:
                result.append(word)
        
        # Mark as visited
        board[r][c] = '#'
        
        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, node, path)
        
        # Backtrack
        board[r][c] = char
        path.pop()
    
    # Start DFS from each cell
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, trie.root, [])
    
    return result


def longest_common_prefix(strs: List[str]) -> str:
    """
    Longest Common Prefix using Trie - O(S) time where S is sum of all characters
    Pattern: Trie traversal to find shared prefix
    """
    if not strs:
        return ""
    
    trie = Trie()
    for word in strs:
        trie.insert(word)
    
    # Traverse trie to find common prefix
    prefix = []
    node = trie.root
    
    while len(node.children) == 1 and not node.is_end_of_word:
        char = list(node.children.keys())[0]
        prefix.append(char)
        node = node.children[char]
    
    return ''.join(prefix)


def autocomplete(trie: Trie, prefix: str) -> List[str]:
    """
    Autocomplete - Find all words with given prefix
    Pattern: Trie DFS from prefix node
    """
    # Navigate to prefix node
    node = trie.root
    for char in prefix:
        if char not in node.children:
            return []
        node = node.children[char]
    
    # DFS to collect all words with this prefix
    result = []
    
    def dfs(current_node, current_word):
        if current_node.is_end_of_word:
            result.append(current_word)
        
        for char, child_node in current_node.children.items():
            dfs(child_node, current_word + char)
    
    dfs(node, prefix)
    return result


# ============================================================================
# PATTERN 3: Bit Manipulation
# ============================================================================

def single_number(nums: List[int]) -> int:
    """
    Single Number - O(n) time, O(1) space
    Pattern: XOR cancels duplicates: n ^ n = 0, n ^ 0 = n
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def number_of_1_bits(n: int) -> int:
    """
    Number of 1 Bits (Hamming Weight) - O(log n) time, O(1) space
    Pattern: n & (n-1) clears the lowest set bit
    """
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def counting_bits(n: int) -> List[int]:
    """
    Counting Bits - O(n) time, O(n) space
    Pattern: DP with bit manipulation
    bits[i] = bits[i >> 1] + (i & 1)
    """
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits


def is_power_of_two(n: int) -> bool:
    """
    Power of Two - O(1) time, O(1) space
    Pattern: n & (n-1) clears lowest set bit, powers of 2 have only 1 bit set
    """
    return n > 0 and (n & (n - 1)) == 0


def reverse_bits(n: int) -> int:
    """
    Reverse Bits - O(1) time (32 iterations), O(1) space
    Pattern: Bit extraction and reconstruction
    """
    result = 0
    for i in range(32):
        bit = (n >> i) & 1
        result |= (bit << (31 - i))
    return result


def sum_of_two_integers(a: int, b: int) -> int:
    """
    Sum of Two Integers - O(1) time, O(1) space
    Pattern: Addition using XOR (sum without carry) and AND (carry)
    """
    # 32-bit mask
    MASK = 0xFFFFFFFF
    MAX_INT = 0x7FFFFFFF
    
    while b != 0:
        # Sum without carry
        sum_without_carry = (a ^ b) & MASK
        # Carry
        carry = ((a & b) << 1) & MASK
        
        a = sum_without_carry
        b = carry
    
    # Handle negative numbers
    return a if a <= MAX_INT else ~(a ^ MASK)


def get_bit(num: int, i: int) -> int:
    """Get the ith bit of num."""
    return (num >> i) & 1


def set_bit(num: int, i: int) -> int:
    """Set the ith bit of num to 1."""
    return num | (1 << i)


def clear_bit(num: int, i: int) -> int:
    """Clear the ith bit of num."""
    return num & ~(1 << i)


def toggle_bit(num: int, i: int) -> int:
    """Toggle the ith bit of num."""
    return num ^ (1 << i)


# ============================================================================
# TESTS
# ============================================================================

def test_top_k_frequent():
    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert top_k_frequent([1], 1) == [1]
    assert sorted(top_k_frequent([4, 1, -1, 2, -1, 2, 3], 2)) == [-1, 2]
    print("✓ test_top_k_frequent passed")


def test_kth_largest():
    assert kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    print("✓ test_kth_largest passed")


def test_merge_k_sorted_lists():
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    assert merge_k_sorted_lists(lists) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert merge_k_sorted_lists([]) == []
    assert merge_k_sorted_lists([[]]) == []
    print("✓ test_merge_k_sorted_lists passed")


def test_find_median_from_stream():
    add_num, find_median = find_median_from_stream()
    add_num(1)
    add_num(2)
    assert find_median() == 1.5
    add_num(3)
    assert find_median() == 2.0
    add_num(4)
    assert find_median() == 2.5
    print("✓ test_find_median_from_stream passed")


def test_trie_operations():
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") == True
    assert trie.search("app") == False
    assert trie.starts_with("app") == True
    trie.insert("app")
    assert trie.search("app") == True
    print("✓ test_trie_operations passed")


def test_longest_common_prefix():
    assert longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert longest_common_prefix(["dog", "racecar", "car"]) == ""
    assert longest_common_prefix(["interspecies", "interstellar", "interstate"]) == "inters"
    print("✓ test_longest_common_prefix passed")


def test_single_number():
    assert single_number([2, 2, 1]) == 1
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert single_number([1]) == 1
    print("✓ test_single_number passed")


def test_number_of_1_bits():
    assert number_of_1_bits(11) == 3  # 1011 in binary
    assert number_of_1_bits(128) == 1  # 10000000
    assert number_of_1_bits(0) == 0
    print("✓ test_number_of_1_bits passed")


def test_counting_bits():
    assert counting_bits(5) == [0, 1, 1, 2, 1, 2]
    assert counting_bits(0) == [0]
    assert counting_bits(2) == [0, 1, 1]
    print("✓ test_counting_bits passed")


def test_is_power_of_two():
    assert is_power_of_two(1) == True
    assert is_power_of_two(16) == True
    assert is_power_of_two(3) == False
    assert is_power_of_two(0) == False
    print("✓ test_is_power_of_two passed")


def test_reverse_bits():
    assert reverse_bits(1) == 2147483648  # 1 reversed in 32 bits
    assert reverse_bits(43261596) == 964176192
    print("✓ test_reverse_bits passed")


def test_sum_of_two_integers():
    assert sum_of_two_integers(1, 2) == 3
    assert sum_of_two_integers(-2, 3) == 1
    assert sum_of_two_integers(0, 0) == 0
    print("✓ test_sum_of_two_integers passed")


def test_bit_operations():
    assert get_bit(5, 0) == 1  # 101
    assert get_bit(5, 1) == 0
    assert get_bit(5, 2) == 1
    assert set_bit(5, 1) == 7  # 101 -> 111
    assert clear_bit(5, 2) == 1  # 101 -> 001
    assert toggle_bit(5, 1) == 7  # 101 -> 111
    print("✓ test_bit_operations passed")


if __name__ == "__main__":
    print("Running Day 15 Tests...")
    print("=" * 60)
    
    test_top_k_frequent()
    test_kth_largest()
    test_merge_k_sorted_lists()
    test_find_median_from_stream()
    test_trie_operations()
    test_longest_common_prefix()
    test_single_number()
    test_number_of_1_bits()
    test_counting_bits()
    test_is_power_of_two()
    test_reverse_bits()
    test_sum_of_two_integers()
    test_bit_operations()
    
    print("=" * 60)
    print("All 13 tests passed!")
