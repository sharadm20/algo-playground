"""
Day 18: Segment Trees & Binary Indexed Trees

This module implements Segment Trees and Binary Indexed Trees (Fenwick Trees)
for efficient range queries and point updates.
"""

class SegmentTree:
    """
    Segment Tree implementation for range sum queries and point updates.
    
    Attributes:
        n (int): Number of elements in the original array
        size (int): Size of the segment tree (next power of 2 >= n)
        tree (list): Array representation of the segment tree
    """
    
    def __init__(self, data):
        """
        Initialize the segment tree with the given data.
        
        Args:
            data (list): Input array of numbers
        """
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)
        
        # Build the tree
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    
    def update(self, index, value):
        """
        Update the value at the given index.
        
        Args:
            index (int): Index to update
            value (int): New value
        """
        index += self.size
        self.tree[index] = value
        index >>= 1
        
        while index >= 1:
            new_val = self.tree[2 * index] + self.tree[2 * index + 1]
            if self.tree[index] == new_val:
                break
            self.tree[index] = new_val
            index >>= 1
    
    def query_range(self, l, r):
        """
        Query the sum of elements in the range [l, r].
        
        Args:
            l (int): Left index of the range
            r (int): Right index of the range
            
        Returns:
            int: Sum of elements in the range [l, r]
        """
        res = 0
        l += self.size
        r += self.size
        
        while l <= r:
            if l % 2 == 1:
                res += self.tree[l]
                l += 1
            if r % 2 == 0:
                res += self.tree[r]
                r -= 1
            l >>= 1
            r >>= 1
        
        return res


class FenwickTree:
    """
    Binary Indexed Tree (Fenwick Tree) implementation for prefix sum queries and point updates.
    
    Attributes:
        size (int): Size of the tree
        tree (list): Array representation of the Fenwick tree
    """
    
    def __init__(self, size):
        """
        Initialize the Fenwick tree with the given size.
        
        Args:
            size (int): Size of the tree
        """
        self.size = size
        self.tree = [0] * (self.size + 1)
    
    def update(self, index, delta):
        """
        Update the value at the given index by adding delta.
        
        Args:
            index (int): Index to update (1-based)
            delta (int): Value to add
        """
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index
    
    def query(self, index):
        """
        Query the prefix sum up to the given index.
        
        Args:
            index (int): Index to query (1-based)
            
        Returns:
            int: Prefix sum up to the given index
        """
        res = 0
        while index > 0:
            res += self.tree[index]
            index -= index & -index
        return res


def test_segment_tree():
    """Test the SegmentTree implementation."""
    print("Testing SegmentTree...")
    data = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(data)
    
    # Test range queries
    assert st.query_range(0, 5) == sum(data), "Full range query failed"
    assert st.query_range(1, 3) == 15, "Range query [1,3] failed"
    assert st.query_range(2, 4) == 21, "Range query [2,4] failed"
    
    # Test updates
    st.update(2, 10)  # Change 5 to 10
    assert st.query_range(0, 5) == 41, "Update failed"
    assert st.query_range(2, 2) == 10, "Point query failed"
    
    print("SegmentTree tests passed!")


def test_fenwick_tree():
    """Test the FenwickTree implementation."""
    print("Testing FenwickTree...")
    ft = FenwickTree(6)
    
    # Test updates and queries
    ft.update(1, 1)
    ft.update(2, 3)
    ft.update(3, 5)
    ft.update(4, 7)
    ft.update(5, 9)
    ft.update(6, 11)
    
    assert ft.query(1) == 1, "Prefix sum at 1 failed"
    assert ft.query(3) == 9, "Prefix sum at 3 failed"
    assert ft.query(6) == 36, "Prefix sum at 6 failed"
    
    # Test range query using prefix sums
    range_sum = ft.query(6) - ft.query(2)
    assert range_sum == 32, "Range sum [3,6] failed"
    
    print("FenwickTree tests passed!")


def test_inversion_count():
    """Test inversion count using Fenwick Tree."""
    print("Testing Inversion Count...")
    
    def count_inversions(arr):
        """Count the number of inversions in the array."""
        # Coordinate compression
        sorted_arr = sorted(arr)
        rank = {v: i + 1 for i, v in enumerate(sorted_arr)}
        
        ft = FenwickTree(len(arr))
        inversions = 0
        
        # Traverse from right to left
        for i in range(len(arr) - 1, -1, -1):
            current_rank = rank[arr[i]]
            inversions += ft.query(current_rank - 1)
            ft.update(current_rank, 1)
        
        return inversions
    
    # Test cases
    assert count_inversions([2, 4, 1, 3, 5]) == 3, "Inversion count test 1 failed"
    assert count_inversions([5, 4, 3, 2, 1]) == 10, "Inversion count test 2 failed"
    assert count_inversions([1, 2, 3, 4, 5]) == 0, "Inversion count test 3 failed"
    
    print("Inversion Count tests passed!")


if __name__ == "__main__":
    test_segment_tree()
    test_fenwick_tree()
    test_inversion_count()
    print("All tests passed successfully!")