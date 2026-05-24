"""
Day 16: Binary Search & Advanced Searching
Python Implementations
"""


# =============================================================================
# 1. Standard Binary Search
# =============================================================================

def binary_search(arr, target):
    """
    Standard binary search to find exact match.
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# =============================================================================
# 2. Lower Bound (First Occurrence)
# =============================================================================

def lower_bound(arr, target):
    """
    Find first index where target appears (or insertion point).
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr)
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left


# =============================================================================
# 3. Upper Bound (Last Occurrence)
# =============================================================================

def upper_bound(arr, target):
    """
    Find last index where target appears.
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr)
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left - 1


# =============================================================================
# 4. Search Insert Position
# =============================================================================

def search_insert(arr, target):
    """
    Find index to insert target while maintaining sorted order.
    Same as lower_bound.
    Time: O(log n), Space: O(1)
    """
    return lower_bound(arr, target)


# =============================================================================
# 5. Search in Rotated Sorted Array
# =============================================================================

def search_rotated(arr, target):
    """
    Search in a rotated sorted array.
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        
        # Check if left half is sorted
        if arr[left] <= arr[mid]:
            # Left half is sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


# =============================================================================
# 6. Find Peak Element
# =============================================================================

def find_peak_element(arr):
    """
    Find a peak element (greater than neighbors).
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < arr[mid + 1]:
            # Peak is on the right
            left = mid + 1
        else:
            # Peak is on the left (could be mid)
            right = mid
    return left


# =============================================================================
# 7. Find Minimum in Rotated Sorted Array
# =============================================================================

def find_min_rotated(arr):
    """
    Find minimum element in rotated sorted array.
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] > arr[right]:
            # Minimum is in right half
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            right = mid
    return arr[left]


# =============================================================================
# 8. Single Element in Sorted Array
# =============================================================================

def single_non_duplicate(arr):
    """
    Find the single element that appears once (all others appear twice).
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        mid = left + (right - left) // 2
        
        # Determine if we should look at pairs starting from mid or mid-1
        if mid % 2 == 0:
            pair_first, pair_second = mid, mid + 1
        else:
            pair_first, pair_second = mid - 1, mid
        
        # Check if pair is intact
        if arr[pair_first] == arr[pair_second]:
            # Single element is on the right
            left = pair_second + 1
        else:
            # Single element is on the left (could be pair_first)
            right = pair_first
    return arr[left]


# =============================================================================
# 9. Koko Eating Bananas (Binary Search on Answer)
# =============================================================================

def min_eating_speed(piles, h):
    """
    Find minimum eating speed k to finish all bananas within h hours.
    Time: O(n * log(max_pile)), Space: O(1)
    """
    def can_finish(k):
        hours = 0
        for pile in piles:
            hours += (pile + k - 1) // k  # ceil(pile / k)
        return hours <= h
    
    left, right = 1, max(piles)
    while left < right:
        mid = left + (right - left) // 2
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    return left


# =============================================================================
# 10. Capacity to Ship Packages within D Days
# =============================================================================

def ship_within_days(weights, days):
    """
    Find minimum ship capacity to ship all packages within d days.
    Time: O(n * log(sum_weights)), Space: O(1)
    """
    def can_ship(capacity):
        days_needed = 1
        current_load = 0
        for weight in weights:
            if current_load + weight > capacity:
                days_needed += 1
                current_load = 0
            current_load += weight
        return days_needed <= days
    
    left, right = max(weights), sum(weights)
    while left < right:
        mid = left + (right - left) // 2
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1
    return left


# =============================================================================
# 11. Split Array Largest Sum
# =============================================================================

def split_array(nums, m):
    """
    Split array into m subarrays to minimize the largest sum.
    Time: O(n * log(sum_nums)), Space: O(1)
    """
    def can_split(max_sum):
        subarrays = 1
        current_sum = 0
        for num in nums:
            if current_sum + num > max_sum:
                subarrays += 1
                current_sum = num
            else:
                current_sum += num
        return subarrays <= m
    
    left, right = max(nums), sum(nums)
    while left < right:
        mid = left + (right - left) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    return left


# =============================================================================
# 12. Find First and Last Position of Element
# =============================================================================

def search_range(arr, target):
    """
    Find first and last position of target in sorted array.
    Time: O(log n), Space: O(1)
    """
    def find_bound(is_first):
        left, right = 0, len(arr) - 1
        bound = -1
        while left <= right:
            mid = left + (right - left) // 2
            if arr[mid] == target:
                bound = mid
                if is_first:
                    right = mid - 1
                else:
                    left = mid + 1
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return bound
    
    first = find_bound(True)
    if first == -1:
        return [-1, -1]
    last = find_bound(False)
    return [first, last]


# =============================================================================
# TESTS
# =============================================================================

def test_binary_search():
    assert binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 5) == 4
    assert binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 1) == 0
    assert binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 9) == 8
    assert binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 10) == -1
    assert binary_search([], 5) == -1
    assert binary_search([5], 5) == 0
    assert binary_search([5], 3) == -1
    print("✓ test_binary_search passed")


def test_lower_bound():
    assert lower_bound([1, 2, 2, 2, 3, 4, 5], 2) == 1
    assert lower_bound([1, 2, 2, 2, 3, 4, 5], 1) == 0
    assert lower_bound([1, 2, 2, 2, 3, 4, 5], 5) == 6
    assert lower_bound([1, 2, 2, 2, 3, 4, 5], 6) == 7
    assert lower_bound([1, 2, 2, 2, 3, 4, 5], 0) == 0
    assert lower_bound([], 5) == 0
    print("✓ test_lower_bound passed")


def test_upper_bound():
    assert upper_bound([1, 2, 2, 2, 3, 4, 5], 2) == 3
    assert upper_bound([1, 2, 2, 2, 3, 4, 5], 1) == 0
    assert upper_bound([1, 2, 2, 2, 3, 4, 5], 5) == 6
    # When target > all elements, returns last index
    assert upper_bound([1, 2, 2, 2, 3, 4, 5], 6) == 6
    # When target < all elements, returns -1
    assert upper_bound([1, 2, 2, 2, 3, 4, 5], 0) == -1
    print("✓ test_upper_bound passed")


def test_search_insert():
    assert search_insert([1, 3, 5, 6], 5) == 2
    assert search_insert([1, 3, 5, 6], 2) == 1
    assert search_insert([1, 3, 5, 6], 7) == 4
    assert search_insert([1, 3, 5, 6], 0) == 0
    assert search_insert([], 5) == 0
    print("✓ test_search_insert passed")


def test_search_rotated():
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 6) == 2
    assert search_rotated([1], 0) == -1
    assert search_rotated([1], 1) == 0
    assert search_rotated([3, 1], 1) == 1
    print("✓ test_search_rotated passed")


def test_find_peak_element():
    assert find_peak_element([1, 2, 3, 1]) == 2  # 3 is peak
    assert find_peak_element([1, 2, 1, 3, 5, 6, 4]) in [1, 5]  # 2 or 6
    assert find_peak_element([1]) == 0
    assert find_peak_element([2, 1]) == 0
    assert find_peak_element([1, 2]) == 1
    print("✓ test_find_peak_element passed")


def test_find_min_rotated():
    assert find_min_rotated([3, 4, 5, 1, 2]) == 1
    assert find_min_rotated([4, 5, 6, 7, 0, 1, 2]) == 0
    assert find_min_rotated([11, 13, 15, 17]) == 11
    assert find_min_rotated([1]) == 1
    assert find_min_rotated([2, 1]) == 1
    print("✓ test_find_min_rotated passed")


def test_single_non_duplicate():
    assert single_non_duplicate([1, 1, 2, 3, 3, 4, 4, 8, 8]) == 2
    assert single_non_duplicate([3, 3, 7, 7, 10, 11, 11]) == 10
    assert single_non_duplicate([1]) == 1
    assert single_non_duplicate([1, 1, 2]) == 2
    assert single_non_duplicate([1, 2, 2]) == 1
    print("✓ test_single_non_duplicate passed")


def test_min_eating_speed():
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
    assert min_eating_speed([1, 1, 1, 1], 4) == 1
    assert min_eating_speed([312884470], 312884469) == 2
    print("✓ test_min_eating_speed passed")


def test_ship_within_days():
    assert ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert ship_within_days([3, 2, 2, 4, 1, 4], 3) == 6
    assert ship_within_days([1, 2, 3, 1, 1], 4) == 3
    assert ship_within_days([10], 1) == 10
    assert ship_within_days([1, 2, 3], 3) == 3
    print("✓ test_ship_within_days passed")


def test_split_array():
    assert split_array([7, 2, 5, 10, 8], 2) == 18
    assert split_array([1, 2, 3, 4, 5], 2) == 9
    assert split_array([1, 4, 4], 3) == 4
    assert split_array([1, 1, 1, 1], 4) == 1
    assert split_array([10], 1) == 10
    print("✓ test_split_array passed")


def test_search_range():
    assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert search_range([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert search_range([], 0) == [-1, -1]
    assert search_range([1], 1) == [0, 0]
    assert search_range([1, 1, 1, 1], 1) == [0, 3]
    print("✓ test_search_range passed")


if __name__ == "__main__":
    test_binary_search()
    test_lower_bound()
    test_upper_bound()
    test_search_insert()
    test_search_rotated()
    test_find_peak_element()
    test_find_min_rotated()
    test_single_non_duplicate()
    test_min_eating_speed()
    test_ship_within_days()
    test_split_array()
    test_search_range()
    
    print("\n" + "=" * 50)
    print("All Day 16 tests passed! ✓")
    print("=" * 50)
