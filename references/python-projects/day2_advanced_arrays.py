"""
Day 2: Advanced Array Manipulation Techniques
==============================================
Topics Covered:
1. Two-Pointer Technique (Advanced)
2. Sliding Window Approach
3. Prefix Sums for Range Queries
4. Hash Map Applications

Each section includes:
- Concept explanation
- Implementation template
- Practice problems with solutions
"""

# ============================================================================
# 1. TWO-POINTER TECHNIQUE - ADVANCED PATTERNS
# ============================================================================

class TwoPointerPatterns:
    """
    Two-pointer technique variations:
    
    Pattern 1: Opposite Direction (Converging Pointers)
    - Used for: Sorted arrays, pair finding, palindrome checking
    - Time: O(n), Space: O(1)
    
    Pattern 2: Same Direction (Fast-Slow Pointers)
    - Used for: Removing duplicates, finding middle, cycle detection
    - Time: O(n), Space: O(1)
    
    Pattern 3: Three-Way Partitioning
    - Used for: Dutch National Flag, color sorting
    - Time: O(n), Space: O(1)
    """
    
    @staticmethod
    def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
        """
        Problem: Given a sorted array, find two numbers that add to target.
        Returns 1-indexed positions.
        
        Example: numbers = [2,7,11,15], target = 9 → [1,2]
        
        Approach: Opposite direction pointers
        - Left starts at beginning, right at end
        - Move pointers based on sum comparison
        """
        left, right = 0, len(numbers) - 1
        
        while left < right:
            current_sum = numbers[left] + numbers[right]
            
            if current_sum == target:
                return [left + 1, right + 1]  # 1-indexed
            elif current_sum < target:
                left += 1  # Need larger sum
            else:
                right -= 1  # Need smaller sum
        
        return [-1, -1]  # No solution
    
    @staticmethod
    def remove_duplicates_sorted(nums: list[int]) -> int:
        """
        Problem: Remove duplicates from sorted array in-place.
        Returns the new length.
        
        Example: nums = [0,0,1,1,2] → length = 3, nums = [0,1,2,_,_]
        
        Approach: Fast-slow pointers (same direction)
        - Slow pointer tracks position for next unique element
        - Fast pointer scans ahead
        """
        if not nums:
            return 0
        
        slow = 0  # Position of last unique element
        
        for fast in range(1, len(nums)):
            if nums[fast] != nums[slow]:
                slow += 1
                nums[slow] = nums[fast]
        
        return slow + 1  # Length is index + 1
    
    @staticmethod
    def sort_colors(nums: list[int]) -> None:
        """
        Problem: Sort array of 0s, 1s, and 2s in-place (Dutch National Flag).
        
        Example: nums = [2,0,2,1,1,0] → [0,0,1,1,2,2]
        
        Approach: Three-way partitioning
        - left: boundary for 0s
        - right: boundary for 2s
        - current: scanning pointer
        """
        left, right = 0, len(nums) - 1
        current = 0
        
        while current <= right:
            if nums[current] == 0:
                nums[left], nums[current] = nums[current], nums[left]
                left += 1
                current += 1
            elif nums[current] == 2:
                nums[right], nums[current] = nums[current], nums[right]
                right -= 1
                # Don't increment current - need to check swapped element
            else:  # nums[current] == 1
                current += 1
    
    @staticmethod
    def trap_rain_water(height: list[int]) -> int:
        """
        Problem: Calculate trapped rainwater between bars.
        
        Example: height = [0,1,0,2,1,0,1,3,2,1,2,1] → 6 units
        
        Approach: Two pointers from both ends
        - Track max height from left and right
        - Water at position = min(left_max, right_max) - height[i]
        """
        if not height:
            return 0
        
        left, right = 0, len(height) - 1
        left_max = right_max = 0
        water = 0
        
        while left < right:
            if height[left] < height[right]:
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water += left_max - height[left]
                left += 1
            else:
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water += right_max - height[right]
                right -= 1
        
        return water


# ============================================================================
# 2. SLIDING WINDOW TECHNIQUE
# ============================================================================

class SlidingWindowPatterns:
    """
    Sliding Window patterns:
    
    Pattern 1: Fixed Size Window
    - Used for: Subarray of length k, average calculations
    - Template: Process first k elements, then slide
    
    Pattern 2: Dynamic Size Window
    - Used for: Longest/shortest substring with constraints
    - Template: Expand right, contract left when condition violated
    
    Pattern 3: Variable Window with Hash Map
    - Used for: Character frequency constraints
    - Template: Track counts, maintain valid window
    """
    
    @staticmethod
    def max_subarray_sum_fixed(nums: list[int], k: int) -> int:
        """
        Problem: Find maximum sum of contiguous subarray of size k.
        
        Example: nums = [2,1,5,1,3,2], k = 3 → 9 (subarray [5,1,3])
        
        Approach: Fixed size sliding window
        - Calculate sum of first k elements
        - Slide window by adding new element, removing old
        """
        if len(nums) < k:
            return -1
        
        # Initialize window sum
        window_sum = sum(nums[:k])
        max_sum = window_sum
        
        # Slide window
        for i in range(k, len(nums)):
            window_sum += nums[i] - nums[i - k]
            max_sum = max(max_sum, window_sum)
        
        return max_sum
    
    @staticmethod
    def min_subarray_len(target: int, nums: list[int]) -> int:
        """
        Problem: Find minimum length subarray with sum >= target.
        
        Example: target = 7, nums = [2,3,1,2,4,3] → 2 (subarray [4,3])
        
        Approach: Dynamic size window
        - Expand right to increase sum
        - Contract left when sum >= target
        - Track minimum valid window size
        """
        left = 0
        current_sum = 0
        min_length = float('inf')
        
        for right in range(len(nums)):
            current_sum += nums[right]  # Expand window
            
            # Contract while condition is satisfied
            while current_sum >= target:
                min_length = min(min_length, right - left + 1)
                current_sum -= nums[left]
                left += 1
        
        return min_length if min_length != float('inf') else 0
    
    @staticmethod
    def longest_substring_no_repeat(s: str) -> int:
        """
        Problem: Find length of longest substring without repeating characters.
        
        Example: s = "abcabcbb" → 3 ("abc")
        
        Approach: Sliding window with hash set
        - Expand right, add characters to set
        - Contract left when duplicate found
        """
        char_set = set()
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            # Contract until no duplicate
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            
            char_set.add(s[right])
            max_length = max(max_length, right - left + 1)
        
        return max_length
    
    @staticmethod
    def min_window_substring(s: str, t: str) -> str:
        """
        Problem: Find minimum window in s containing all characters of t.
        
        Example: s = "ADOBECODEBANC", t = "ABC" → "BANC"
        
        Approach: Sliding window with frequency map
        - Track required character counts
        - Expand to satisfy requirements
        - Contract to minimize window
        """
        if not s or not t:
            return ""
        
        # Build frequency map for t
        from collections import Counter
        need = Counter(t)
        required = len(need)
        
        # Track formed characters
        formed = 0
        window_counts = {}
        
        left, right = 0, 0
        result = (float('inf'), 0, 0)  # (length, left, right)
        
        while right < len(s):
            # Add character to window
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1
            
            # Check if this character satisfies requirement
            if char in need and window_counts[char] == need[char]:
                formed += 1
            
            # Try to contract window while valid
            while left <= right and formed == required:
                # Update result if smaller
                if (right - left + 1) < result[0]:
                    result = (right - left + 1, left, right)
                
                # Remove left character
                char = s[left]
                window_counts[char] -= 1
                if char in need and window_counts[char] < need[char]:
                    formed -= 1
                
                left += 1
            
            right += 1
        
        return "" if result[0] == float('inf') else s[result[1]:result[2] + 1]


# ============================================================================
# 3. PREFIX SUM TECHNIQUE
# ============================================================================

class PrefixSumPatterns:
    """
    Prefix Sum patterns:
    
    Pattern 1: Basic Prefix Sum Array
    - Used for: Range sum queries in O(1)
    - prefix[i] = sum of elements 0 to i-1
    
    Pattern 2: Prefix Sum with Hash Map
    - Used for: Subarray sum equals k
    - Store prefix sums and their frequencies
    
    Pattern 3: 2D Prefix Sum
    - Used for: Matrix range sum queries
    - Build cumulative sum matrix
    """
    
    @staticmethod
    def range_sum_query(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
        """
        Problem: Answer multiple range sum queries efficiently.
        
        Example: nums = [1,2,3,4,5], query (1,3) → 9 (2+3+4)
        
        Approach: Build prefix sum array
        - prefix[i] = sum of nums[0..i-1]
        - sum(i,j) = prefix[j+1] - prefix[i]
        """
        n = len(nums)
        prefix = [0] * (n + 1)
        
        # Build prefix sum array
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]
        
        # Answer queries in O(1)
        results = []
        for left, right in queries:
            range_sum = prefix[right + 1] - prefix[left]
            results.append(range_sum)
        
        return results
    
    @staticmethod
    def subarray_sum_equals_k(nums: list[int], k: int) -> int:
        """
        Problem: Count subarrays with sum equal to k.
        
        Example: nums = [1,1,1], k = 2 → 2 ([1,1] at positions 0-1 and 1-2)
        
        Approach: Prefix sum with hash map
        - Track frequency of each prefix sum
        - If prefix[j] - prefix[i] = k, then prefix[i] = prefix[j] - k
        - Count occurrences of (current_prefix - k)
        """
        # Map: prefix_sum -> frequency
        prefix_count = {0: 1}  # Base case: empty prefix
        current_sum = 0
        count = 0
        
        for num in nums:
            current_sum += num
            
            # Check if there's a prefix that gives sum k
            if (current_sum - k) in prefix_count:
                count += prefix_count[current_sum - k]
            
            # Update frequency of current prefix sum
            prefix_count[current_sum] = prefix_count.get(current_sum, 0) + 1
        
        return count
    
    @staticmethod
    def max_subarray_sum(nums: list[int]) -> int:
        """
        Problem: Find maximum subarray sum (Kadane's Algorithm).
        
        Example: nums = [-2,1,-3,4,-1,2,1,-5,4] → 6 ([4,-1,2,1])
        
        Approach: Dynamic programming / Greedy
        - At each position, decide: extend previous or start new
        - Track maximum seen so far
        """
        if not nums:
            return 0
        
        max_current = max_global = nums[0]
        
        for i in range(1, len(nums)):
            # Either extend previous subarray or start new
            max_current = max(nums[i], max_current + nums[i])
            max_global = max(max_global, max_current)
        
        return max_global
    
    @staticmethod
    def product_except_self(nums: list[int]) -> list[int]:
        """
        Problem: Return array where each element is product of all others.
        
        Example: nums = [1,2,3,4] → [24,12,8,6]
        
        Approach: Left and right prefix products
        - left[i] = product of all elements before i
        - right[i] = product of all elements after i
        - result[i] = left[i] * right[i]
        """
        n = len(nums)
        result = [1] * n
        
        # Calculate left products
        left_product = 1
        for i in range(n):
            result[i] = left_product
            left_product *= nums[i]
        
        # Calculate right products and multiply
        right_product = 1
        for i in range(n - 1, -1, -1):
            result[i] *= right_product
            right_product *= nums[i]
        
        return result


# ============================================================================
# 4. HASH MAP APPLICATIONS
# ============================================================================

class HashMapApplications:
    """
    Hash Map patterns:
    
    Pattern 1: Frequency Counting
    - Used for: Anagrams, duplicates, majority element
    
    Pattern 2: Complement Lookup
    - Used for: Two sum, pair finding
    
    Pattern 3: Grouping by Key
    - Used for: Group anagrams, categorize elements
    """
    
    @staticmethod
    def two_sum(nums: list[int], target: int) -> list[int]:
        """
        Problem: Find two numbers that add to target.
        Returns indices.
        
        Example: nums = [2,7,11,15], target = 9 → [0,1]
        
        Approach: Hash map for complement lookup
        - Store seen numbers with their indices
        - For each number, check if complement exists
        """
        seen = {}  # value -> index
        
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        
        return [-1, -1]
    
    @staticmethod
    def group_anagrams(strs: list[str]) -> list[list[str]]:
        """
        Problem: Group anagrams together.
        
        Example: ["eat","tea","tan","ate","nat","bat"]
                 → [["eat","tea","ate"],["tan","nat"],["bat"]]
        
        Approach: Hash map with sorted string as key
        - Anagrams have same sorted representation
        - Group by sorted key
        """
        groups = {}
        
        for s in strs:
            # Use sorted characters as key
            key = ''.join(sorted(s))
            if key not in groups:
                groups[key] = []
            groups[key].append(s)
        
        return list(groups.values())
    
    @staticmethod
    def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
        """
        Problem: Check if there are duplicates within distance k.
        
        Example: nums = [1,2,3,1], k = 3 → True
                 nums = [1,2,3,1,2,3], k = 2 → False
        
        Approach: Sliding window with hash set
        - Maintain set of last k elements
        - Check for duplicates in window
        """
        window = set()
        
        for i, num in enumerate(nums):
            if num in window:
                return True
            
            window.add(num)
            
            # Maintain window size k
            if len(window) > k:
                window.remove(nums[i - k])
        
        return False
    
    @staticmethod
    def majority_element(nums: list[int]) -> int:
        """
        Problem: Find element that appears more than n/2 times.
        
        Example: nums = [3,2,3] → 3
                 nums = [2,2,1,1,1,2,2] → 2
        
        Approach 1: Hash map frequency counting
        Approach 2: Boyer-Moore Voting Algorithm (O(1) space)
        """
        # Hash map approach
        frequency = {}
        threshold = len(nums) // 2
        
        for num in nums:
            frequency[num] = frequency.get(num, 0) + 1
            if frequency[num] > threshold:
                return num
        
        return -1
    
    @staticmethod
    def majority_element_boyer_moore(nums: list[int]) -> int:
        """
        Boyer-Moore Voting Algorithm:
        - Maintain candidate and count
        - Increment for same, decrement for different
        - When count = 0, pick new candidate
        """
        candidate = None
        count = 0
        
        for num in nums:
            if count == 0:
                candidate = num
                count = 1
            elif num == candidate:
                count += 1
            else:
                count -= 1
        
        return candidate


# ============================================================================
# PRACTICE PROBLEMS FOR HOMEWORK
# ============================================================================

class PracticeProblems:
    """
    Homework Problems - Try solving these on your own!
    
    EASY:
    1. Best Time to Buy and Sell Stock
    2. Maximum Average Subarray I
    3. Find All Numbers Disappeared in an Array
    
    MEDIUM:
    4. 3Sum
    5. Container With Most Water
    6. Subarray Sum Equals K
    7. Longest Repeating Character Replacement
    
    HARD:
    8. Trapping Rain Water
    9. Minimum Window Substring
    10. First Missing Positive
    """
    
    @staticmethod
    def best_time_to_buy_sell_stock(prices: list[int]) -> int:
        """
        Problem: Find maximum profit from one buy-sell transaction.
        
        Example: prices = [7,1,5,3,6,4] → 5 (buy at 1, sell at 6)
        
        Approach: Track minimum price, calculate max profit
        """
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            min_price = min(min_price, price)
            profit = price - min_price
            max_profit = max(max_profit, profit)
        
        return max_profit
    
    @staticmethod
    def three_sum(nums: list[int]) -> list[list[int]]:
        """
        Problem: Find all unique triplets that sum to zero.
        
        Example: nums = [-1,0,1,2,-1,-4]
                 → [[-1,-1,2],[-1,0,1]]
        
        Approach: Sort + Two pointers
        - Fix first element, use two pointers for remaining
        - Skip duplicates
        """
        nums.sort()
        result = []
        n = len(nums)
        
        for i in range(n - 2):
            # Skip duplicate first elements
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            left, right = i + 1, n - 1
            
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                
                if total == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    
                    # Skip duplicates
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
    
    @staticmethod
    def container_with_most_water(height: list[int]) -> int:
        """
        Problem: Find two lines forming container with most water.
        
        Example: height = [1,8,6,2,5,4,8,3,7] → 49
        
        Approach: Two pointers from ends
        - Area = min(height[left], height[right]) * width
        - Move shorter line inward
        """
        left, right = 0, len(height) - 1
        max_area = 0
        
        while left < right:
            width = right - left
            h = min(height[left], height[right])
            area = h * width
            max_area = max(max_area, area)
            
            # Move shorter line
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        
        return max_area
    
    @staticmethod
    def longest_repeating_char_replacement(s: str, k: int) -> int:
        """
        Problem: Longest substring with at most k replacements.
        
        Example: s = "ABAB", k = 2 → 4
                 s = "AABABBA", k = 1 → 4
        
        Approach: Sliding window with frequency tracking
        - Track max frequency character in window
        - Window valid if: window_size - max_freq <= k
        """
        from collections import defaultdict
        
        char_count = defaultdict(int)
        left = 0
        max_freq = 0
        max_length = 0
        
        for right in range(len(s)):
            char_count[s[right]] += 1
            max_freq = max(max_freq, char_count[s[right]])
            
            # Contract if invalid
            while (right - left + 1) - max_freq > k:
                char_count[s[left]] -= 1
                left += 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length


# ============================================================================
# TEST CASES
# ============================================================================

def run_tests():
    """Run test cases for all patterns."""
    
    print("=" * 60)
    print("DAY 2: ADVANCED ARRAY TECHNIQUES - TEST CASES")
    print("=" * 60)
    
    # Two Pointer Tests
    print("\n1. TWO POINTER TECHNIQUE")
    print("-" * 40)
    
    tp = TwoPointerPatterns()
    
    # Two Sum Sorted
    result = tp.two_sum_sorted([2, 7, 11, 15], 9)
    print(f"Two Sum Sorted [2,7,11,15], target=9: {result}")
    assert result == [1, 2]
    
    # Remove Duplicates
    nums = [0, 0, 1, 1, 2]
    length = tp.remove_duplicates_sorted(nums)
    print(f"Remove Duplicates [0,0,1,1,2]: length={length}, nums={nums[:length]}")
    assert length == 3
    
    # Sort Colors
    colors = [2, 0, 2, 1, 1, 0]
    tp.sort_colors(colors)
    print(f"Sort Colors [2,0,2,1,1,0]: {colors}")
    assert colors == [0, 0, 1, 1, 2, 2]
    
    # Trap Rain Water
    water = tp.trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    print(f"Trap Rain Water: {water} units")
    assert water == 6
    
    # Sliding Window Tests
    print("\n2. SLIDING WINDOW TECHNIQUE")
    print("-" * 40)
    
    sw = SlidingWindowPatterns()
    
    # Max Subarray Sum Fixed
    max_sum = sw.max_subarray_sum_fixed([2, 1, 5, 1, 3, 2], 3)
    print(f"Max Subarray Sum (k=3) [2,1,5,1,3,2]: {max_sum}")
    assert max_sum == 9
    
    # Min Subarray Length
    min_len = sw.min_subarray_len(7, [2, 3, 1, 2, 4, 3])
    print(f"Min Subarray Length (target=7): {min_len}")
    assert min_len == 2
    
    # Longest Substring No Repeat
    longest = sw.longest_substring_no_repeat("abcabcbb")
    print(f"Longest Substring No Repeat 'abcabcbb': {longest}")
    assert longest == 3
    
    # Prefix Sum Tests
    print("\n3. PREFIX SUM TECHNIQUE")
    print("-" * 40)
    
    ps = PrefixSumPatterns()
    
    # Range Sum Query
    queries = [(1, 3), (0, 4), (2, 2)]
    results = ps.range_sum_query([1, 2, 3, 4, 5], queries)
    print(f"Range Sum Queries {queries}: {results}")
    assert results == [9, 15, 3]
    
    # Subarray Sum Equals K
    count = ps.subarray_sum_equals_k([1, 1, 1], 2)
    print(f"Subarray Sum Equals K (k=2) [1,1,1]: {count}")
    assert count == 2
    
    # Max Subarray Sum (Kadane's)
    max_sub = ps.max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    print(f"Max Subarray Sum (Kadane's): {max_sub}")
    assert max_sub == 6
    
    # Product Except Self
    product = ps.product_except_self([1, 2, 3, 4])
    print(f"Product Except Self [1,2,3,4]: {product}")
    assert product == [24, 12, 8, 6]
    
    # Hash Map Tests
    print("\n4. HASH MAP APPLICATIONS")
    print("-" * 40)
    
    hm = HashMapApplications()
    
    # Two Sum
    two_sum_result = hm.two_sum([2, 7, 11, 15], 9)
    print(f"Two Sum [2,7,11,15], target=9: {two_sum_result}")
    assert two_sum_result == [0, 1]
    
    # Group Anagrams
    anagrams = hm.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    print(f"Group Anagrams: {anagrams}")
    
    # Majority Element
    majority = hm.majority_element_boyer_moore([2, 2, 1, 1, 1, 2, 2])
    print(f"Majority Element [2,2,1,1,1,2,2]: {majority}")
    assert majority == 2
    
    # Practice Problems Tests
    print("\n5. PRACTICE PROBLEMS")
    print("-" * 40)
    
    pp = PracticeProblems()
    
    # Best Time to Buy/Sell Stock
    profit = pp.best_time_to_buy_sell_stock([7, 1, 5, 3, 6, 4])
    print(f"Best Time to Buy/Sell Stock: {profit}")
    assert profit == 5
    
    # Three Sum
    three_sum_result = pp.three_sum([-1, 0, 1, 2, -1, -4])
    print(f"Three Sum: {three_sum_result}")
    assert len(three_sum_result) == 2
    
    # Container With Most Water
    water_area = pp.container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7])
    print(f"Container With Most Water: {water_area}")
    assert water_area == 49
    
    # Longest Repeating Character Replacement
    repeat_len = pp.longest_repeating_char_replacement("AABABBA", 1)
    print(f"Longest Repeating Char Replacement (k=1): {repeat_len}")
    assert repeat_len == 4
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
