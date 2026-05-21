"""
Day 17: Binary Search Review & Practice
Python Implementations - Mixed Practice Problems
"""


# =============================================================================
# 1. Search in a 2D Matrix
# =============================================================================

def search_matrix(matrix, target):
    """
    Search for target in a 2D matrix where:
    - Each row is sorted left to right
    - First element of each row > last element of previous row
    Time: O(log(m*n)), Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        row, col = mid // n, mid % n
        val = matrix[row][col]
        
        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# =============================================================================
# 2. Find Kth Smallest Element in Two Sorted Arrays
# =============================================================================

def find_kth_sorted_arrays(nums1, nums2, k):
    """
    Find kth smallest element in merged sorted arrays.
    Time: O(log k), Space: O(1)
    """
    def helper(nums1, i, nums2, j, k):
        # If we've exhausted one array
        if i >= len(nums1):
            return nums2[j + k - 1]
        if j >= len(nums2):
            return nums1[i + k - 1]
        if k == 1:
            return min(nums1[i], nums2[j])
        
        # Get mid elements from both arrays
        mid1 = nums1[i + k // 2 - 1] if i + k // 2 - 1 < len(nums1) else float('inf')
        mid2 = nums2[j + k // 2 - 1] if j + k // 2 - 1 < len(nums2) else float('inf')
        
        # Discard the smaller half
        if mid1 < mid2:
            return helper(nums1, i + k // 2, nums2, j, k - k // 2)
        else:
            return helper(nums1, i, nums2, j + k // 2, k - k // 2)
    
    if k < 1 or k > len(nums1) + len(nums2):
        return -1
    
    return helper(nums1, 0, nums2, 0, k)


# =============================================================================
# 3. Square Root (Integer)
# =============================================================================

def my_sqrt(x):
    """
    Compute integer square root of x.
    Time: O(log x), Space: O(1)
    """
    if x < 2:
        return x
    
    left, right = 1, x // 2
    while left <= right:
        mid = left + (right - left) // 2
        if mid * mid == x:
            return mid
        elif mid * mid < x:
            left = mid + 1
        else:
            right = mid - 1
    
    return right


# =============================================================================
# 4. Smallest Missing Positive Integer
# =============================================================================

def first_missing_positive(nums):
    """
    Find smallest missing positive integer in sorted array.
    Time: O(log n), Space: O(1)
    """
    nums.sort()  # Assuming already sorted for binary search approach
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == mid + 1:
            left = mid + 1
        else:
            right = mid - 1
    
    return left + 1


# =============================================================================
# 5. Find Minimum in Rotated Sorted Array II (with duplicates)
# =============================================================================

def find_min_rotated_duplicates(nums):
    """
    Find minimum in rotated sorted array with duplicates.
    Time: O(log n) average, O(n) worst case, Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[right]:
            left = mid + 1
        elif nums[mid] < nums[right]:
            right = mid
        else:
            # nums[mid] == nums[right], can't determine which half
            # Reduce search space by 1
            right -= 1
    
    return nums[left]


# =============================================================================
# 6. Search in Rotated Sorted Array II (with duplicates)
# =============================================================================

def search_rotated_duplicates(nums, target):
    """
    Search in rotated sorted array with duplicates.
    Time: O(log n) average, O(n) worst case, Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return True
        
        # Handle duplicates
        if nums[left] == nums[mid] and nums[mid] == nums[right]:
            left += 1
            right -= 1
        elif nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return False


# =============================================================================
# 7. H-Index II
# =============================================================================

def h_index(citations):
    """
    Calculate h-index for sorted citations array.
    Time: O(log n), Space: O(1)
    """
    n = len(citations)
    left, right = 0, n - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        h = n - mid
        
        if citations[mid] == h:
            return h
        elif citations[mid] < h:
            left = mid + 1
        else:
            right = mid - 1
    
    return n - left


# =============================================================================
# 8. Find Peak Element II (2D Grid)
# =============================================================================

def find_peak_grid(mat):
    """
    Find peak element in 2D grid (greater than all adjacent neighbors).
    Time: O(n * log m), Space: O(1)
    """
    if not mat or not mat[0]:
        return [-1, -1]
    
    m, n = len(mat), len(mat[0])
    left, right = 0, n - 1
    
    while left <= right:
        mid_col = left + (right - left) // 2
        
        # Find row with maximum value in this column
        max_row = 0
        for i in range(m):
            if mat[i][mid_col] > mat[max_row][mid_col]:
                max_row = i
        
        # Check left and right neighbors
        left_neighbor = mat[max_row][mid_col - 1] if mid_col > 0 else -1
        right_neighbor = mat[max_row][mid_col + 1] if mid_col < n - 1 else -1
        
        if mat[max_row][mid_col] > left_neighbor and \
           mat[max_row][mid_col] > right_neighbor:
            return [max_row, mid_col]
        elif mid_col > 0 and left_neighbor > mat[max_row][mid_col]:
            right = mid_col - 1
        else:
            left = mid_col + 1
    
    return [-1, -1]


# =============================================================================
# 9. Minimize Max Distance to Gas Station
# =============================================================================

def minmax_gas_stations(stations, k):
    """
    Add k gas stations to minimize maximum distance between adjacent stations.
    Time: O(n * log(range/precision)), Space: O(1)
    """
    def possible(dist):
        count = 0
        for i in range(len(stations) - 1):
            count += int((stations[i+1] - stations[i]) / dist)
        return count <= k
    
    left, right = 0.0, float(max(stations[i+1] - stations[i] 
                                  for i in range(len(stations)-1)))
    
    # Binary search with precision
    for _ in range(100):  # Sufficient iterations for precision
        mid = left + (right - left) / 2
        if mid == 0:
            left = mid
            continue
        if possible(mid):
            right = mid
        else:
            left = mid
    
    return right


# =============================================================================
# 10. Find the Smallest Divisor Given a Threshold
# =============================================================================

def smallest_divisor(nums, threshold):
    """
    Find smallest divisor such that sum of divisions <= threshold.
    Time: O(n * log(max(nums))), Space: O(1)
    """
    def check(divisor):
        total = 0
        for num in nums:
            total += (num + divisor - 1) // divisor  # ceil division
        return total <= threshold
    
    left, right = 1, max(nums)
    while left < right:
        mid = left + (right - left) // 2
        if check(mid):
            right = mid
        else:
            left = mid + 1
    
    return left


# =============================================================================
# 11. Median of Two Sorted Arrays
# =============================================================================

def find_median_sorted_arrays(nums1, nums2):
    """
    Find median of two sorted arrays.
    Time: O(log(min(m, n))), Space: O(1)
    """
    if len(nums1) > len(nums2):
        return find_median_sorted_arrays(nums2, nums1)
    
    m, n = len(nums1), len(nums2)
    left, right = 0, m
    total = m + n
    
    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (total + 1) // 2 - partition1
        
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1-1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2-1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found correct partition
            if total % 2 == 0:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2
            else:
                return max(max_left1, max_left2)
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1
    
    return 0.0


# =============================================================================
# 12. Count of Smaller Numbers After Self
# =============================================================================

def count_smaller(nums):
    """
    For each element, count number of smaller elements to its right.
    Using binary search with insertion (alternative to merge sort approach).
    Time: O(n^2) worst case, Space: O(n)
    """
    sorted_list = []
    result = []
    
    for num in reversed(nums):
        # Binary search for insertion point
        left, right = 0, len(sorted_list)
        while left < right:
            mid = left + (right - left) // 2
            if sorted_list[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        # All elements before left are smaller
        result.append(left)
        sorted_list.insert(left, num)
    
    return result[::-1]


# =============================================================================
# TESTS
# =============================================================================

def test_search_matrix():
    matrix = [
        [1, 3, 5, 7],
        [10, 11, 16, 20],
        [23, 30, 34, 60]
    ]
    assert search_matrix(matrix, 3) == True
    assert search_matrix(matrix, 13) == False
    assert search_matrix(matrix, 60) == True
    assert search_matrix(matrix, 1) == True
    assert search_matrix([], 5) == False
    print("✓ test_search_matrix passed")


def test_find_kth_sorted_arrays():
    nums1 = [1, 3, 5]
    nums2 = [2, 4, 6]
    assert find_kth_sorted_arrays(nums1, nums2, 1) == 1  # 1st smallest
    assert find_kth_sorted_arrays(nums1, nums2, 3) == 3  # 3rd smallest
    assert find_kth_sorted_arrays(nums1, nums2, 6) == 6  # 6th smallest
    assert find_kth_sorted_arrays([], [1, 2, 3], 2) == 2
    print("✓ test_find_kth_sorted_arrays passed")


def test_my_sqrt():
    assert my_sqrt(4) == 2
    assert my_sqrt(8) == 2
    assert my_sqrt(0) == 0
    assert my_sqrt(1) == 1
    assert my_sqrt(16) == 4
    assert my_sqrt(25) == 5
    print("✓ test_my_sqrt passed")


def test_first_missing_positive():
    assert first_missing_positive([1, 2, 3, 5, 6]) == 4
    assert first_missing_positive([1, 2, 3, 4, 5]) == 6
    assert first_missing_positive([2, 3, 4, 5]) == 1
    assert first_missing_positive([]) == 1
    print("✓ test_first_missing_positive passed")


def test_find_min_rotated_duplicates():
    assert find_min_rotated_duplicates([3, 3, 1, 3]) == 1
    assert find_min_rotated_duplicates([2, 2, 2, 0, 1]) == 0
    assert find_min_rotated_duplicates([1, 1, 1, 1]) == 1
    assert find_min_rotated_duplicates([1]) == 1
    print("✓ test_find_min_rotated_duplicates passed")


def test_search_rotated_duplicates():
    assert search_rotated_duplicates([2, 5, 6, 0, 0, 1, 2], 0) == True
    assert search_rotated_duplicates([2, 5, 6, 0, 0, 1, 2], 3) == False
    assert search_rotated_duplicates([1, 1, 1, 1, 1], 1) == True
    assert search_rotated_duplicates([1, 0, 1, 1, 1], 0) == True
    print("✓ test_search_rotated_duplicates passed")


def test_h_index():
    assert h_index([0, 1, 3, 5, 6]) == 3
    assert h_index([1, 2, 100]) == 2
    assert h_index([0]) == 0
    assert h_index([100]) == 1
    print("✓ test_h_index passed")


def test_find_peak_grid():
    mat = [
        [1, 4],
        [3, 2]
    ]
    result = find_peak_grid(mat)
    assert result in [[0, 1], [1, 0]]  # 4 or 3
    
    mat2 = [
        [10, 20, 15],
        [21, 30, 14],
        [7, 16, 32]
    ]
    result2 = find_peak_grid(mat2)
    assert mat2[result2[0]][result2[1]] in [30, 32, 21]  # Any peak
    print("✓ test_find_peak_grid passed")


def test_smallest_divisor():
    assert smallest_divisor([1, 2, 5, 9], 6) == 5
    assert smallest_divisor([44, 22, 33, 11, 1], 5) == 44
    assert smallest_divisor([2, 3, 5, 7, 11], 11) == 3
    assert smallest_divisor([1, 1, 1], 3) == 1
    print("✓ test_smallest_divisor passed")


def test_find_median_sorted_arrays():
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5
    assert find_median_sorted_arrays([0, 0], [0, 0]) == 0.0
    assert find_median_sorted_arrays([], [1]) == 1.0
    assert find_median_sorted_arrays([2], []) == 2.0
    print("✓ test_find_median_sorted_arrays passed")


def test_count_smaller():
    assert count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert count_smaller([-1]) == [0]
    assert count_smaller([-1, -1]) == [0, 0]
    assert count_smaller([1, 2, 3, 4]) == [0, 0, 0, 0]
    assert count_smaller([4, 3, 2, 1]) == [3, 2, 1, 0]
    print("✓ test_count_smaller passed")


if __name__ == "__main__":
    test_search_matrix()
    test_find_kth_sorted_arrays()
    test_my_sqrt()
    test_first_missing_positive()
    test_find_min_rotated_duplicates()
    test_search_rotated_duplicates()
    test_h_index()
    test_find_peak_grid()
    test_smallest_divisor()
    test_find_median_sorted_arrays()
    test_count_smaller()

    print("\n" + "=" * 50)
    print("All Day 17 tests passed! ✓")
    print("=" * 50)
