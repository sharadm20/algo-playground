//! Day 2: Advanced Array Manipulation Techniques
//! ==============================================
//! Topics Covered:
//! 1. Two-Pointer Technique (Advanced)
//! 2. Sliding Window Approach
//! 3. Prefix Sums for Range Queries
//! 4. Hash Map Applications
//!
//! Each section includes:
//! - Concept explanation
//! - Implementation template
//! - Practice problems with solutions

// ============================================================================
// 1. TWO-POINTER TECHNIQUE - ADVANCED PATTERNS
// ============================================================================

/// Two-pointer technique variations:
///
/// Pattern 1: Opposite Direction (Converging Pointers)
/// - Used for: Sorted arrays, pair finding, palindrome checking
/// - Time: O(n), Space: O(1)
///
/// Pattern 2: Same Direction (Fast-Slow Pointers)
/// - Used for: Removing duplicates, finding middle, cycle detection
/// - Time: O(n), Space: O(1)
///
/// Pattern 3: Three-Way Partitioning
/// - Used for: Dutch National Flag, color sorting
/// - Time: O(n), Space: O(1)

/// Problem: Given a sorted array, find two numbers that add to target.
/// Returns 1-indexed positions.
///
/// Example: numbers = [2,7,11,15], target = 9 → [1,2]
///
/// Approach: Opposite direction pointers
/// - Left starts at beginning, right at end
/// - Move pointers based on sum comparison
fn two_sum_sorted(numbers: &[i32], target: i32) -> Vec<i32> {
    let mut left: i32 = 0;
    let mut right: i32 = numbers.len() as i32 - 1;

    while left < right {
        let current_sum = numbers[left as usize] + numbers[right as usize];

        if current_sum == target {
            return vec![left + 1, right + 1]; // 1-indexed
        } else if current_sum < target {
            left += 1; // Need larger sum
        } else {
            right -= 1; // Need smaller sum
        }
    }

    vec![-1, -1] // No solution
}

/// Problem: Remove duplicates from sorted array in-place.
/// Returns the new length.
///
/// Example: nums = [0,0,1,1,2] → length = 3, nums = [0,1,2,_,_]
///
/// Approach: Fast-slow pointers (same direction)
/// - Slow pointer tracks position for next unique element
/// - Fast pointer scans ahead
fn remove_duplicates_sorted(nums: &mut Vec<i32>) -> usize {
    if nums.is_empty() {
        return 0;
    }

    let mut slow = 0; // Position of last unique element

    for fast in 1..nums.len() {
        if nums[fast] != nums[slow] {
            slow += 1;
            nums[slow] = nums[fast];
        }
    }

    slow + 1 // Length is index + 1
}

/// Problem: Sort array of 0s, 1s, and 2s in-place (Dutch National Flag).
///
/// Example: nums = [2,0,2,1,1,0] → [0,0,1,1,2,2]
///
/// Approach: Three-way partitioning
/// - left: boundary for 0s
/// - right: boundary for 2s
/// - current: scanning pointer
fn sort_colors(nums: &mut Vec<i32>) {
    let mut left: i32 = 0;
    let mut right: i32 = nums.len() as i32 - 1;
    let mut current: i32 = 0;

    while current <= right {
        let curr_idx = current as usize;
        if nums[curr_idx] == 0 {
            let left_idx = left as usize;
            nums.swap(curr_idx, left_idx);
            left += 1;
            current += 1;
        } else if nums[curr_idx] == 2 {
            let right_idx = right as usize;
            nums.swap(curr_idx, right_idx);
            right -= 1;
            // Don't increment current - need to check swapped element
        } else {
            // nums[curr_idx] == 1
            current += 1;
        }
    }
}

/// Problem: Calculate trapped rainwater between bars.
///
/// Example: height = [0,1,0,2,1,0,1,3,2,1,2,1] → 6 units
///
/// Approach: Two pointers from both ends
/// - Track max height from left and right
/// - Water at position = min(left_max, right_max) - height[i]
fn trap_rain_water(height: &[i32]) -> i32 {
    if height.is_empty() {
        return 0;
    }

    let mut left: i32 = 0;
    let mut right: i32 = height.len() as i32 - 1;
    let mut left_max = 0;
    let mut right_max = 0;
    let mut water = 0;

    while left < right {
        let left_idx = left as usize;
        let right_idx = right as usize;

        if height[left_idx] < height[right_idx] {
            if height[left_idx] >= left_max {
                left_max = height[left_idx];
            } else {
                water += left_max - height[left_idx];
            }
            left += 1;
        } else {
            if height[right_idx] >= right_max {
                right_max = height[right_idx];
            } else {
                water += right_max - height[right_idx];
            }
            right -= 1;
        }
    }

    water
}

// ============================================================================
// 2. SLIDING WINDOW TECHNIQUE
// ============================================================================

/// Sliding Window patterns:
///
/// Pattern 1: Fixed Size Window
/// - Used for: Subarray of length k, average calculations
/// - Template: Process first k elements, then slide
///
/// Pattern 2: Dynamic Size Window
/// - Used for: Longest/shortest substring with constraints
/// - Template: Expand right, contract left when condition violated
///
/// Pattern 3: Variable Window with Hash Map
/// - Used for: Character frequency constraints
/// - Template: Track counts, maintain valid window

/// Problem: Find maximum sum of contiguous subarray of size k.
///
/// Example: nums = [2,1,5,1,3,2], k = 3 → 9 (subarray [5,1,3])
///
/// Approach: Fixed size sliding window
/// - Calculate sum of first k elements
/// - Slide window by adding new element, removing old
fn max_subarray_sum_fixed(nums: &[i32], k: usize) -> Option<i32> {
    if nums.len() < k {
        return None;
    }

    // Initialize window sum
    let mut window_sum: i32 = nums[..k].iter().sum();
    let mut max_sum = window_sum;

    // Slide window
    for i in k..nums.len() {
        window_sum += nums[i] - nums[i - k];
        max_sum = max_sum.max(window_sum);
    }

    Some(max_sum)
}

/// Problem: Find minimum length subarray with sum >= target.
///
/// Example: target = 7, nums = [2,3,1,2,4,3] → 2 (subarray [4,3])
///
/// Approach: Dynamic size window
/// - Expand right to increase sum
/// - Contract left when sum >= target
/// - Track minimum valid window size
fn min_subarray_len(target: i32, nums: &[i32]) -> usize {
    let mut left = 0;
    let mut current_sum = 0;
    let mut min_length = usize::MAX;

    for right in 0..nums.len() {
        current_sum += nums[right]; // Expand window

        // Contract while condition is satisfied
        while current_sum >= target {
            min_length = min_length.min(right - left + 1);
            current_sum -= nums[left];
            left += 1;
        }
    }

    if min_length == usize::MAX {
        0
    } else {
        min_length
    }
}

/// Problem: Find length of longest substring without repeating characters.
///
/// Example: s = "abcabcbb" → 3 ("abc")
///
/// Approach: Sliding window with hash set
/// - Expand right, add characters to set
/// - Contract left when duplicate found
fn longest_substring_no_repeat(s: &str) -> usize {
    use std::collections::HashSet;

    let chars: Vec<char> = s.chars().collect();
    let mut char_set = HashSet::new();
    let mut left = 0;
    let mut max_length = 0;

    for right in 0..chars.len() {
        // Contract until no duplicate
        while char_set.contains(&chars[right]) {
            char_set.remove(&chars[left]);
            left += 1;
        }

        char_set.insert(chars[right]);
        max_length = max_length.max(right - left + 1);
    }

    max_length
}

/// Problem: Find minimum window in s containing all characters of t.
///
/// Example: s = "ADOBECODEBANC", t = "ABC" → "BANC"
///
/// Approach: Sliding window with frequency map
/// - Track required character counts
/// - Expand to satisfy requirements
/// - Contract to minimize window
fn min_window_substring(s: &str, t: &str) -> String {
    use std::collections::HashMap;

    if s.is_empty() || t.is_empty() {
        return String::new();
    }

    let s_chars: Vec<char> = s.chars().collect();

    // Build frequency map for t
    let mut need: HashMap<char, usize> = HashMap::new();
    for c in t.chars() {
        *need.entry(c).or_insert(0) += 1;
    }
    let required = need.len();

    // Track formed characters
    let mut formed = 0;
    let mut window_counts: HashMap<char, usize> = HashMap::new();

    let mut left = 0;
    let mut right = 0;
    let mut result: Option<(usize, usize, usize)> = None; // (length, left, right)

    while right < s_chars.len() {
        // Add character to window
        let char = s_chars[right];
        *window_counts.entry(char).or_insert(0) += 1;

        // Check if this character satisfies requirement
        if let Some(&needed_count) = need.get(&char) {
            if let Some(&window_count) = window_counts.get(&char) {
                if window_count == needed_count {
                    formed += 1;
                }
            }
        }

        // Try to contract window while valid
        while left <= right && formed == required {
            // Update result if smaller
            let current_len = right - left + 1;
            if result.map_or(true, |r| current_len < r.0) {
                result = Some((current_len, left, right));
            }

            // Remove left character
            let left_char = s_chars[left];
            *window_counts.get_mut(&left_char).unwrap() -= 1;

            if let Some(&needed_count) = need.get(&left_char) {
                if let Some(&window_count) = window_counts.get(&left_char) {
                    if window_count < needed_count {
                        formed -= 1;
                    }
                }
            }

            left += 1;
        }

        right += 1;
    }

    result.map_or(String::new(), |(_, l, r)| {
        s_chars[l..=r].iter().collect()
    })
}

// ============================================================================
// 3. PREFIX SUM TECHNIQUE
// ============================================================================

/// Prefix Sum patterns:
///
/// Pattern 1: Basic Prefix Sum Array
/// - Used for: Range sum queries in O(1)
/// - prefix[i] = sum of elements 0 to i-1
///
/// Pattern 2: Prefix Sum with Hash Map
/// - Used for: Subarray sum equals k
/// - Store prefix sums and their frequencies
///
/// Pattern 3: 2D Prefix Sum
/// - Used for: Matrix range sum queries
/// - Build cumulative sum matrix

/// Problem: Answer multiple range sum queries efficiently.
///
/// Example: nums = [1,2,3,4,5], query (1,3) → 9 (2+3+4)
///
/// Approach: Build prefix sum array
/// - prefix[i] = sum of nums[0..i-1]
/// - sum(i,j) = prefix[j+1] - prefix[i]
fn range_sum_query(nums: &[i32], queries: &[(usize, usize)]) -> Vec<i32> {
    let n = nums.len();
    let mut prefix = vec![0; n + 1];

    // Build prefix sum array
    for i in 0..n {
        prefix[i + 1] = prefix[i] + nums[i];
    }

    // Answer queries in O(1)
    queries
        .iter()
        .map(|&(left, right)| prefix[right + 1] - prefix[left])
        .collect()
}

/// Problem: Count subarrays with sum equal to k.
///
/// Example: nums = [1,1,1], k = 2 → 2 ([1,1] at positions 0-1 and 1-2)
///
/// Approach: Prefix sum with hash map
/// - Track frequency of each prefix sum
/// - If prefix[j] - prefix[i] = k, then prefix[i] = prefix[j] - k
/// - Count occurrences of (current_prefix - k)
fn subarray_sum_equals_k(nums: &[i32], k: i32) -> usize {
    use std::collections::HashMap;

    // Map: prefix_sum -> frequency
    let mut prefix_count: HashMap<i32, usize> = HashMap::new();
    prefix_count.insert(0, 1); // Base case: empty prefix

    let mut current_sum = 0;
    let mut count = 0;

    for &num in nums {
        current_sum += num;

        // Check if there's a prefix that gives sum k
        if let Some(&freq) = prefix_count.get(&(current_sum - k)) {
            count += freq;
        }

        // Update frequency of current prefix sum
        *prefix_count.entry(current_sum).or_insert(0) += 1;
    }

    count
}

/// Problem: Find maximum subarray sum (Kadane's Algorithm).
///
/// Example: nums = [-2,1,-3,4,-1,2,1,-5,4] → 6 ([4,-1,2,1])
///
/// Approach: Dynamic programming / Greedy
/// - At each position, decide: extend previous or start new
/// - Track maximum seen so far
fn max_subarray_sum(nums: &[i32]) -> i32 {
    if nums.is_empty() {
        return 0;
    }

    let mut max_current = nums[0];
    let mut max_global = nums[0];

    for &num in nums.iter().skip(1) {
        // Either extend previous subarray or start new
        max_current = num.max(max_current + num);
        max_global = max_global.max(max_current);
    }

    max_global
}

/// Problem: Return array where each element is product of all others.
///
/// Example: nums = [1,2,3,4] → [24,12,8,6]
///
/// Approach: Left and right prefix products
/// - left[i] = product of all elements before i
/// - right[i] = product of all elements after i
/// - result[i] = left[i] * right[i]
fn product_except_self(nums: &[i32]) -> Vec<i32> {
    let n = nums.len();
    let mut result = vec![1; n];

    // Calculate left products
    let mut left_product = 1;
    for i in 0..n {
        result[i] = left_product;
        left_product *= nums[i];
    }

    // Calculate right products and multiply
    let mut right_product = 1;
    for i in (0..n).rev() {
        result[i] *= right_product;
        right_product *= nums[i];
    }

    result
}

// ============================================================================
// 4. HASH MAP APPLICATIONS
// ============================================================================

/// Hash Map patterns:
///
/// Pattern 1: Frequency Counting
/// - Used for: Anagrams, duplicates, majority element
///
/// Pattern 2: Complement Lookup
/// - Used for: Two sum, pair finding
///
/// Pattern 3: Grouping by Key
/// - Used for: Group anagrams, categorize elements

/// Problem: Find two numbers that add to target.
/// Returns indices.
///
/// Example: nums = [2,7,11,15], target = 9 → [0,1]
///
/// Approach: Hash map for complement lookup
/// - Store seen numbers with their indices
/// - For each number, check if complement exists
fn two_sum(nums: &[i32], target: i32) -> Vec<i32> {
    use std::collections::HashMap;

    let mut seen: HashMap<i32, usize> = HashMap::new(); // value -> index

    for (i, &num) in nums.iter().enumerate() {
        let complement = target - num;
        if let Some(&complement_idx) = seen.get(&complement) {
            return vec![complement_idx as i32, i as i32];
        }
        seen.insert(num, i);
    }

    vec![-1, -1]
}

/// Problem: Group anagrams together.
///
/// Example: ["eat","tea","tan","ate","nat","bat"]
///          → [["eat","tea","ate"],["tan","nat"],["bat"]]
///
/// Approach: Hash map with sorted string as key
/// - Anagrams have same sorted representation
/// - Group by sorted key
fn group_anagrams(strs: &[&str]) -> Vec<Vec<String>> {
    use std::collections::HashMap;

    let mut groups: HashMap<String, Vec<String>> = HashMap::new();

    for &s in strs {
        // Use sorted characters as key
        let mut key: Vec<char> = s.chars().collect();
        key.sort_unstable();
        let key: String = key.into_iter().collect();

        groups.entry(key).or_insert_with(Vec::new).push(s.to_string());
    }

    groups.into_values().collect()
}

/// Problem: Check if there are duplicates within distance k.
///
/// Example: nums = [1,2,3,1], k = 3 → True
///          nums = [1,2,3,1,2,3], k = 2 → False
///
/// Approach: Sliding window with hash set
/// - Maintain set of last k elements
/// - Check for duplicates in window
fn contains_nearby_duplicate(nums: &[i32], k: usize) -> bool {
    use std::collections::HashSet;

    let mut window = HashSet::new();

    for (i, &num) in nums.iter().enumerate() {
        if window.contains(&num) {
            return true;
        }

        window.insert(num);

        // Maintain window size k
        if window.len() > k {
            window.remove(&nums[i - k]);
        }
    }

    false
}

/// Problem: Find element that appears more than n/2 times.
///
/// Example: nums = [3,2,3] → 3
///          nums = [2,2,1,1,1,2,2] → 2
///
/// Approach 1: Hash map frequency counting
/// Approach 2: Boyer-Moore Voting Algorithm (O(1) space)
fn majority_element(nums: &[i32]) -> Option<i32> {
    use std::collections::HashMap;

    let mut frequency: HashMap<i32, usize> = HashMap::new();
    let threshold = nums.len() / 2;

    for &num in nums {
        let count = frequency.entry(num).or_insert(0);
        *count += 1;
        if *count > threshold {
            return Some(num);
        }
    }

    None
}

/// Boyer-Moore Voting Algorithm:
/// - Maintain candidate and count
/// - Increment for same, decrement for different
/// - When count = 0, pick new candidate
fn majority_element_boyer_moore(nums: &[i32]) -> Option<i32> {
    let mut candidate: Option<i32> = None;
    let mut count = 0;

    for &num in nums {
        match candidate {
            None => {
                candidate = Some(num);
                count = 1;
            }
            Some(cand) if cand == num => {
                count += 1;
            }
            Some(_) => {
                count -= 1;
                if count == 0 {
                    candidate = None;
                }
            }
        }
    }

    candidate
}

// ============================================================================
// PRACTICE PROBLEMS FOR HOMEWORK
// ============================================================================

/// Homework Problems - Try solving these on your own!
///
/// EASY:
/// 1. Best Time to Buy and Sell Stock
/// 2. Maximum Average Subarray I
/// 3. Find All Numbers Disappeared in an Array
///
/// MEDIUM:
/// 4. 3Sum
/// 5. Container With Most Water
/// 6. Subarray Sum Equals K
/// 7. Longest Repeating Character Replacement
///
/// HARD:
/// 8. Trapping Rain Water
/// 9. Minimum Window Substring
/// 10. First Missing Positive

/// Problem: Find maximum profit from one buy-sell transaction.
///
/// Example: prices = [7,1,5,3,6,4] → 5 (buy at 1, sell at 6)
///
/// Approach: Track minimum price, calculate max profit
fn best_time_to_buy_sell_stock(prices: &[i32]) -> i32 {
    let mut min_price = i32::MAX;
    let mut max_profit = 0;

    for &price in prices {
        min_price = min_price.min(price);
        let profit = price - min_price;
        max_profit = max_profit.max(profit);
    }

    max_profit
}

/// Problem: Find all unique triplets that sum to zero.
///
/// Example: nums = [-1,0,1,2,-1,-4]
///          → [[-1,-1,2],[-1,0,1]]
///
/// Approach: Sort + Two pointers
/// - Fix first element, use two pointers for remaining
/// - Skip duplicates
fn three_sum(nums: &mut Vec<i32>) -> Vec<Vec<i32>> {
    nums.sort();
    let mut result = Vec::new();
    let n = nums.len();

    for i in 0..n.saturating_sub(2) {
        // Skip duplicate first elements
        if i > 0 && nums[i] == nums[i - 1] {
            continue;
        }

        let mut left = i + 1;
        let mut right = n - 1;

        while left < right {
            let total = nums[i] + nums[left] + nums[right];

            if total == 0 {
                result.push(vec![nums[i], nums[left], nums[right]]);

                // Skip duplicates
                while left < right && nums[left] == nums[left + 1] {
                    left += 1;
                }
                while left < right && nums[right] == nums[right - 1] {
                    right -= 1;
                }

                left += 1;
                right -= 1;
            } else if total < 0 {
                left += 1;
            } else {
                right -= 1;
            }
        }
    }

    result
}

/// Problem: Find two lines forming container with most water.
///
/// Example: height = [1,8,6,2,5,4,8,3,7] → 49
///
/// Approach: Two pointers from ends
/// - Area = min(height[left], height[right]) * width
/// - Move shorter line inward
fn container_with_most_water(height: &[i32]) -> i32 {
    let mut left: i32 = 0;
    let mut right: i32 = height.len() as i32 - 1;
    let mut max_area = 0;

    while left < right {
        let left_idx = left as usize;
        let right_idx = right as usize;
        let width = right - left;
        let h = height[left_idx].min(height[right_idx]);
        let area = h * width;
        max_area = max_area.max(area);

        // Move shorter line
        if height[left_idx] < height[right_idx] {
            left += 1;
        } else {
            right -= 1;
        }
    }

    max_area
}

/// Problem: Longest substring with at most k replacements.
///
/// Example: s = "ABAB", k = 2 → 4
///          s = "AABABBA", k = 1 → 4
///
/// Approach: Sliding window with frequency tracking
/// - Track max frequency character in window
/// - Window valid if: window_size - max_freq <= k
fn longest_repeating_char_replacement(s: &str, k: usize) -> usize {
    use std::collections::HashMap;

    let chars: Vec<char> = s.chars().collect();
    let mut char_count: HashMap<char, usize> = HashMap::new();
    let mut left = 0;
    let mut max_freq = 0;
    let mut max_length = 0;

    for right in 0..chars.len() {
        let count = char_count.entry(chars[right]).or_insert(0);
        *count += 1;
        max_freq = max_freq.max(*count);

        // Contract if invalid
        while (right - left + 1) - max_freq > k {
            *char_count.get_mut(&chars[left]).unwrap() -= 1;
            left += 1;
        }

        max_length = max_length.max(right - left + 1);
    }

    max_length
}

// ============================================================================
// TEST CASES
// ============================================================================

fn run_tests() {
    println!("{}", "=".repeat(60));
    println!("DAY 2: ADVANCED ARRAY TECHNIQUES - TEST CASES");
    println!("{}", "=".repeat(60));

    // Two Pointer Tests
    println!("\n1. TWO POINTER TECHNIQUE");
    println!("{}", "-".repeat(40));

    // Two Sum Sorted
    let result = two_sum_sorted(&[2, 7, 11, 15], 9);
    println!("Two Sum Sorted [2,7,11,15], target=9: {:?}", result);
    assert_eq!(result, vec![1, 2]);

    // Remove Duplicates
    let mut nums = vec![0, 0, 1, 1, 2];
    let length = remove_duplicates_sorted(&mut nums);
    println!(
        "Remove Duplicates [0,0,1,1,2]: length={}, nums={:?}",
        length,
        &nums[..length]
    );
    assert_eq!(length, 3);

    // Sort Colors
    let mut colors = vec![2, 0, 2, 1, 1, 0];
    sort_colors(&mut colors);
    println!("Sort Colors [2,0,2,1,1,0]: {:?}", colors);
    assert_eq!(colors, vec![0, 0, 1, 1, 2, 2]);

    // Trap Rain Water
    let water = trap_rain_water(&[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]);
    println!("Trap Rain Water: {} units", water);
    assert_eq!(water, 6);

    // Sliding Window Tests
    println!("\n2. SLIDING WINDOW TECHNIQUE");
    println!("{}", "-".repeat(40));

    // Max Subarray Sum Fixed
    let max_sum = max_subarray_sum_fixed(&[2, 1, 5, 1, 3, 2], 3);
    println!(
        "Max Subarray Sum (k=3) [2,1,5,1,3,2]: {:?}",
        max_sum
    );
    assert_eq!(max_sum, Some(9));

    // Min Subarray Length
    let min_len = min_subarray_len(7, &[2, 3, 1, 2, 4, 3]);
    println!("Min Subarray Length (target=7): {}", min_len);
    assert_eq!(min_len, 2);

    // Longest Substring No Repeat
    let longest = longest_substring_no_repeat("abcabcbb");
    println!("Longest Substring No Repeat 'abcabcbb': {}", longest);
    assert_eq!(longest, 3);

    // Prefix Sum Tests
    println!("\n3. PREFIX SUM TECHNIQUE");
    println!("{}", "-".repeat(40));

    // Range Sum Query
    let queries = vec![(1, 3), (0, 4), (2, 2)];
    let results = range_sum_query(&[1, 2, 3, 4, 5], &queries);
    println!("Range Sum Queries {:?}: {:?}", queries, results);
    assert_eq!(results, vec![9, 15, 3]);

    // Subarray Sum Equals K
    let count = subarray_sum_equals_k(&[1, 1, 1], 2);
    println!("Subarray Sum Equals K (k=2) [1,1,1]: {}", count);
    assert_eq!(count, 2);

    // Max Subarray Sum (Kadane's)
    let max_sub = max_subarray_sum(&[-2, 1, -3, 4, -1, 2, 1, -5, 4]);
    println!("Max Subarray Sum (Kadane's): {}", max_sub);
    assert_eq!(max_sub, 6);

    // Product Except Self
    let product = product_except_self(&[1, 2, 3, 4]);
    println!("Product Except Self [1,2,3,4]: {:?}", product);
    assert_eq!(product, vec![24, 12, 8, 6]);

    // Hash Map Tests
    println!("\n4. HASH MAP APPLICATIONS");
    println!("{}", "-".repeat(40));

    // Two Sum
    let two_sum_result = two_sum(&[2, 7, 11, 15], 9);
    println!("Two Sum [2,7,11,15], target=9: {:?}", two_sum_result);
    assert_eq!(two_sum_result, vec![0, 1]);

    // Group Anagrams
    let anagrams = group_anagrams(&["eat", "tea", "tan", "ate", "nat", "bat"]);
    println!("Group Anagrams: {:?}", anagrams);

    // Majority Element
    let majority = majority_element_boyer_moore(&[2, 2, 1, 1, 1, 2, 2]);
    println!("Majority Element [2,2,1,1,1,2,2]: {:?}", majority);
    assert_eq!(majority, Some(2));

    // Practice Problems Tests
    println!("\n5. PRACTICE PROBLEMS");
    println!("{}", "-".repeat(40));

    // Best Time to Buy/Sell Stock
    let profit = best_time_to_buy_sell_stock(&[7, 1, 5, 3, 6, 4]);
    println!("Best Time to Buy/Sell Stock: {}", profit);
    assert_eq!(profit, 5);

    // Three Sum
    let mut three_sum_nums = vec![-1, 0, 1, 2, -1, -4];
    let three_sum_result = three_sum(&mut three_sum_nums);
    println!("Three Sum: {:?}", three_sum_result);
    assert_eq!(three_sum_result.len(), 2);

    // Container With Most Water
    let water_area = container_with_most_water(&[1, 8, 6, 2, 5, 4, 8, 3, 7]);
    println!("Container With Most Water: {}", water_area);
    assert_eq!(water_area, 49);

    // Longest Repeating Character Replacement
    let repeat_len = longest_repeating_char_replacement("AABABBA", 1);
    println!("Longest Repeating Char Replacement (k=1): {}", repeat_len);
    assert_eq!(repeat_len, 4);

    println!("\n{}", "=".repeat(60));
    println!("ALL TESTS PASSED!");
    println!("{}", "=".repeat(60));
}

fn main() {
    run_tests();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_two_sum_sorted() {
        assert_eq!(two_sum_sorted(&[2, 7, 11, 15], 9), vec![1, 2]);
        assert_eq!(two_sum_sorted(&[1, 3, 5, 7], 10), vec![2, 4]); // 3+7=10 at indices 1,3 (0-indexed) -> 2,4 (1-indexed)
    }

    #[test]
    fn test_remove_duplicates() {
        let mut nums = vec![0, 0, 1, 1, 2];
        assert_eq!(remove_duplicates_sorted(&mut nums), 3);
        assert_eq!(&nums[..3], &[0, 1, 2]);
    }

    #[test]
    fn test_sort_colors() {
        let mut colors = vec![2, 0, 2, 1, 1, 0];
        sort_colors(&mut colors);
        assert_eq!(colors, vec![0, 0, 1, 1, 2, 2]);
    }

    #[test]
    fn test_trap_rain_water() {
        assert_eq!(trap_rain_water(&[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6);
        assert_eq!(trap_rain_water(&[4, 2, 0, 3, 2, 5]), 9);
    }

    #[test]
    fn test_max_subarray_sum_fixed() {
        assert_eq!(max_subarray_sum_fixed(&[2, 1, 5, 1, 3, 2], 3), Some(9));
        assert_eq!(max_subarray_sum_fixed(&[1, 2, 3], 5), None);
    }

    #[test]
    fn test_min_subarray_len() {
        assert_eq!(min_subarray_len(7, &[2, 3, 1, 2, 4, 3]), 2);
        assert_eq!(min_subarray_len(100, &[1, 2, 3]), 0);
    }

    #[test]
    fn test_longest_substring_no_repeat() {
        assert_eq!(longest_substring_no_repeat("abcabcbb"), 3);
        assert_eq!(longest_substring_no_repeat("bbbbb"), 1);
        assert_eq!(longest_substring_no_repeat("pwwkew"), 3);
    }

    #[test]
    fn test_range_sum_query() {
        assert_eq!(
            range_sum_query(&[1, 2, 3, 4, 5], &[(1, 3), (0, 4), (2, 2)]),
            vec![9, 15, 3]
        );
    }

    #[test]
    fn test_subarray_sum_equals_k() {
        assert_eq!(subarray_sum_equals_k(&[1, 1, 1], 2), 2);
        assert_eq!(subarray_sum_equals_k(&[1, 2, 3], 3), 2);
    }

    #[test]
    fn test_max_subarray_sum() {
        assert_eq!(max_subarray_sum(&[-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6);
        assert_eq!(max_subarray_sum(&[-1, -2, -3]), -1);
    }

    #[test]
    fn test_product_except_self() {
        assert_eq!(product_except_self(&[1, 2, 3, 4]), vec![24, 12, 8, 6]);
    }

    #[test]
    fn test_two_sum() {
        assert_eq!(two_sum(&[2, 7, 11, 15], 9), vec![0, 1]);
        assert_eq!(two_sum(&[3, 2, 4], 6), vec![1, 2]);
    }

    #[test]
    fn test_group_anagrams() {
        let result = group_anagrams(&["eat", "tea", "tan", "ate", "nat", "bat"]);
        assert_eq!(result.len(), 3);
    }

    #[test]
    fn test_majority_element() {
        assert_eq!(
            majority_element_boyer_moore(&[2, 2, 1, 1, 1, 2, 2]),
            Some(2)
        );
    }

    #[test]
    fn test_best_time_to_buy_sell_stock() {
        assert_eq!(best_time_to_buy_sell_stock(&[7, 1, 5, 3, 6, 4]), 5);
        assert_eq!(best_time_to_buy_sell_stock(&[7, 6, 4, 3, 1]), 0);
    }

    #[test]
    fn test_three_sum() {
        let mut nums = vec![-1, 0, 1, 2, -1, -4];
        let result = three_sum(&mut nums);
        assert_eq!(result.len(), 2);
    }

    #[test]
    fn test_container_with_most_water() {
        assert_eq!(container_with_most_water(&[1, 8, 6, 2, 5, 4, 8, 3, 7]), 49);
    }

    #[test]
    fn test_longest_repeating_char_replacement() {
        assert_eq!(longest_repeating_char_replacement("AABABBA", 1), 4);
        assert_eq!(longest_repeating_char_replacement("ABAB", 2), 4);
    }
}
