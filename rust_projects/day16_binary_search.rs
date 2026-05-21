/// Day 16: Binary Search & Advanced Searching
/// Topics: Binary search fundamentals, advanced patterns, and binary search on answer

// ============================================================================
// PATTERN 1: Standard Binary Search
// ============================================================================

/// Standard binary search to find exact match - O(log n) time, O(1) space
fn binary_search(arr: &[i32], target: i32) -> i32 {
    let (mut left, mut right) = (0, arr.len() as i32 - 1);
    
    while left <= right {
        let mid = left + (right - left) / 2;
        let mid_idx = mid as usize;
        
        if arr[mid_idx] == target {
            return mid;
        } else if arr[mid_idx] < target {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    -1
}

// ============================================================================
// PATTERN 2: Lower Bound (First Occurrence)
// ============================================================================

/// Find first index where target appears (or insertion point) - O(log n) time, O(1) space
fn lower_bound(arr: &[i32], target: i32) -> i32 {
    let (mut left, mut right) = (0, arr.len() as i32);
    
    while left < right {
        let mid = left + (right - left) / 2;
        let mid_idx = mid as usize;
        
        if arr[mid_idx] < target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    left
}

// ============================================================================
// PATTERN 3: Upper Bound (Last Occurrence)
// ============================================================================

/// Find last index where target appears - O(log n) time, O(1) space
fn upper_bound(arr: &[i32], target: i32) -> i32 {
    let (mut left, mut right) = (0, arr.len() as i32);
    
    while left < right {
        let mid = left + (right - left) / 2;
        let mid_idx = mid as usize;
        
        if arr[mid_idx] <= target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    left - 1
}

// ============================================================================
// PATTERN 4: Search Insert Position
// ============================================================================

/// Find index to insert target while maintaining sorted order - O(log n) time, O(1) space
fn search_insert(arr: &[i32], target: i32) -> i32 {
    lower_bound(arr, target)
}

// ============================================================================
// PATTERN 5: Search in Rotated Sorted Array
// ============================================================================

/// Search in a rotated sorted array - O(log n) time, O(1) space
fn search_rotated(arr: &[i32], target: i32) -> i32 {
    let (mut left, mut right) = (0, arr.len() as i32 - 1);
    
    while left <= right {
        let mid = left + (right - left) / 2;
        let mid_idx = mid as usize;
        
        if arr[mid_idx] == target {
            return mid;
        }
        
        // Check if left half is sorted
        if arr[left as usize] <= arr[mid_idx] {
            // Left half is sorted
            if arr[left as usize] <= target && target < arr[mid_idx] {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            // Right half is sorted
            if arr[mid_idx] < target && target <= arr[right as usize] {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }
    
    -1
}

// ============================================================================
// PATTERN 6: Find Peak Element
// ============================================================================

/// Find a peak element (greater than neighbors) - O(log n) time, O(1) space
fn find_peak_element(arr: &[i32]) -> i32 {
    let (mut left, mut right) = (0, arr.len() as i32 - 1);
    
    while left < right {
        let mid = left + (right - left) / 2;
        let mid_idx = mid as usize;
        
        if arr[mid_idx] < arr[mid_idx + 1] {
            // Peak is on the right
            left = mid + 1;
        } else {
            // Peak is on the left (could be mid)
            right = mid;
        }
    }
    
    left
}

// ============================================================================
// PATTERN 7: Find Minimum in Rotated Sorted Array
// ============================================================================

/// Find minimum element in rotated sorted array - O(log n) time, O(1) space
fn find_min_rotated(arr: &[i32]) -> i32 {
    let (mut left, mut right) = (0, arr.len() as i32 - 1);
    
    while left < right {
        let mid = left + (right - left) / 2;
        let mid_idx = mid as usize;
        let right_idx = right as usize;
        
        if arr[mid_idx] > arr[right_idx] {
            // Minimum is in right half
            left = mid + 1;
        } else {
            // Minimum is in left half (including mid)
            right = mid;
        }
    }
    
    arr[left as usize]
}

// ============================================================================
// PATTERN 8: Single Element in Sorted Array
// ============================================================================

/// Find the single element that appears once (all others appear twice) - O(log n) time, O(1) space
fn single_non_duplicate(arr: &[i32]) -> i32 {
    let (mut left, mut right) = (0, arr.len() as i32 - 1);
    
    while left < right {
        let mid = left + (right - left) / 2;
        
        // Determine if we should look at pairs starting from mid or mid-1
        let (pair_first, pair_second) = if mid % 2 == 0 {
            (mid as usize, (mid + 1) as usize)
        } else {
            ((mid - 1) as usize, mid as usize)
        };
        
        // Check if pair is intact
        if arr[pair_first] == arr[pair_second] {
            // Single element is on the right
            left = pair_second as i32 + 1;
        } else {
            // Single element is on the left (could be pair_first)
            right = pair_first as i32;
        }
    }
    
    arr[left as usize]
}

// ============================================================================
// PATTERN 9: Koko Eating Bananas (Binary Search on Answer)
// ============================================================================

/// Find minimum eating speed k to finish all bananas within h hours - O(n * log(max_pile)) time, O(1) space
fn min_eating_speed(piles: &[i32], h: i32) -> i32 {
    let can_finish = |k: i32| -> bool {
        let mut hours = 0;
        for &pile in piles {
            hours += (pile + k - 1) / k; // ceil(pile / k)
        }
        hours <= h
    };
    
    let (mut left, mut right) = (1, *piles.iter().max().unwrap());
    
    while left < right {
        let mid = left + (right - left) / 2;
        if can_finish(mid) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    left
}

// ============================================================================
// PATTERN 10: Capacity to Ship Packages within D Days
// ============================================================================

/// Find minimum ship capacity to ship all packages within d days - O(n * log(sum_weights)) time, O(1) space
fn ship_within_days(weights: &[i32], days: i32) -> i32 {
    let can_ship = |capacity: i32| -> bool {
        let mut days_needed = 1;
        let mut current_load = 0;
        
        for &weight in weights {
            if current_load + weight > capacity {
                days_needed += 1;
                current_load = 0;
            }
            current_load += weight;
        }
        
        days_needed <= days
    };
    
    let left = *weights.iter().max().unwrap();
    let right = weights.iter().sum();
    let (mut left, mut right) = (left, right);
    
    while left < right {
        let mid = left + (right - left) / 2;
        if can_ship(mid) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    left
}

// ============================================================================
// PATTERN 11: Split Array Largest Sum
// ============================================================================

/// Split array into m subarrays to minimize the largest sum - O(n * log(sum_nums)) time, O(1) space
fn split_array(nums: &[i32], m: i32) -> i32 {
    let can_split = |max_sum: i32| -> bool {
        let mut subarrays = 1;
        let mut current_sum = 0;
        
        for &num in nums {
            if current_sum + num > max_sum {
                subarrays += 1;
                current_sum = num;
            } else {
                current_sum += num;
            }
        }
        
        subarrays <= m
    };
    
    let left = *nums.iter().max().unwrap();
    let right: i32 = nums.iter().map(|&x| x as i64).sum::<i64>() as i32;
    let (mut left, mut right) = (left, right);
    
    while left < right {
        let mid = left + (right - left) / 2;
        if can_split(mid) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    left
}

// ============================================================================
// PATTERN 12: Find First and Last Position of Element
// ============================================================================

/// Find first and last position of target in sorted array - O(log n) time, O(1) space
fn search_range(arr: &[i32], target: i32) -> Vec<i32> {
    fn find_bound(arr: &[i32], target: i32, is_first: bool) -> i32 {
        let (mut left, mut right) = (0, arr.len() as i32 - 1);
        let mut bound = -1;
        
        while left <= right {
            let mid = left + (right - left) / 2;
            let mid_idx = mid as usize;
            
            if arr[mid_idx] == target {
                bound = mid;
                if is_first {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else if arr[mid_idx] < target {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        bound
    }
    
    let first = find_bound(arr, target, true);
    if first == -1 {
        return vec![-1, -1];
    }
    let last = find_bound(arr, target, false);
    vec![first, last]
}

// ============================================================================
// TESTS
// ============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_binary_search() {
        assert_eq!(binary_search(&[1, 2, 3, 4, 5, 6, 7, 8, 9], 5), 4);
        assert_eq!(binary_search(&[1, 2, 3, 4, 5, 6, 7, 8, 9], 1), 0);
        assert_eq!(binary_search(&[1, 2, 3, 4, 5, 6, 7, 8, 9], 9), 8);
        assert_eq!(binary_search(&[1, 2, 3, 4, 5, 6, 7, 8, 9], 10), -1);
        assert_eq!(binary_search(&[], 5), -1);
        assert_eq!(binary_search(&[5], 5), 0);
        assert_eq!(binary_search(&[5], 3), -1);
    }

    #[test]
    fn test_lower_bound() {
        assert_eq!(lower_bound(&[1, 2, 2, 2, 3, 4, 5], 2), 1);
        assert_eq!(lower_bound(&[1, 2, 2, 2, 3, 4, 5], 1), 0);
        assert_eq!(lower_bound(&[1, 2, 2, 2, 3, 4, 5], 5), 6);
        assert_eq!(lower_bound(&[1, 2, 2, 2, 3, 4, 5], 6), 7);
        assert_eq!(lower_bound(&[1, 2, 2, 2, 3, 4, 5], 0), 0);
        assert_eq!(lower_bound(&[], 5), 0);
    }

    #[test]
    fn test_upper_bound() {
        assert_eq!(upper_bound(&[1, 2, 2, 2, 3, 4, 5], 2), 3);
        assert_eq!(upper_bound(&[1, 2, 2, 2, 3, 4, 5], 1), 0);
        assert_eq!(upper_bound(&[1, 2, 2, 2, 3, 4, 5], 5), 6);
        assert_eq!(upper_bound(&[1, 2, 2, 2, 3, 4, 5], 6), 6);
        assert_eq!(upper_bound(&[1, 2, 2, 2, 3, 4, 5], 0), -1);
    }

    #[test]
    fn test_search_insert() {
        assert_eq!(search_insert(&[1, 3, 5, 6], 5), 2);
        assert_eq!(search_insert(&[1, 3, 5, 6], 2), 1);
        assert_eq!(search_insert(&[1, 3, 5, 6], 7), 4);
        assert_eq!(search_insert(&[1, 3, 5, 6], 0), 0);
        assert_eq!(search_insert(&[], 5), 0);
    }

    #[test]
    fn test_search_rotated() {
        assert_eq!(search_rotated(&[4, 5, 6, 7, 0, 1, 2], 0), 4);
        assert_eq!(search_rotated(&[4, 5, 6, 7, 0, 1, 2], 3), -1);
        assert_eq!(search_rotated(&[4, 5, 6, 7, 0, 1, 2], 6), 2);
        assert_eq!(search_rotated(&[1], 0), -1);
        assert_eq!(search_rotated(&[1], 1), 0);
        assert_eq!(search_rotated(&[3, 1], 1), 1);
    }

    #[test]
    fn test_find_peak_element() {
        assert_eq!(find_peak_element(&[1, 2, 3, 1]), 2); // 3 is peak
        let peak = find_peak_element(&[1, 2, 1, 3, 5, 6, 4]);
        assert!(peak == 1 || peak == 5); // 2 or 6
        assert_eq!(find_peak_element(&[1]), 0);
        assert_eq!(find_peak_element(&[2, 1]), 0);
        assert_eq!(find_peak_element(&[1, 2]), 1);
    }

    #[test]
    fn test_find_min_rotated() {
        assert_eq!(find_min_rotated(&[3, 4, 5, 1, 2]), 1);
        assert_eq!(find_min_rotated(&[4, 5, 6, 7, 0, 1, 2]), 0);
        assert_eq!(find_min_rotated(&[11, 13, 15, 17]), 11);
        assert_eq!(find_min_rotated(&[1]), 1);
        assert_eq!(find_min_rotated(&[2, 1]), 1);
    }

    #[test]
    fn test_single_non_duplicate() {
        assert_eq!(single_non_duplicate(&[1, 1, 2, 3, 3, 4, 4, 8, 8]), 2);
        assert_eq!(single_non_duplicate(&[3, 3, 7, 7, 10, 11, 11]), 10);
        assert_eq!(single_non_duplicate(&[1]), 1);
        assert_eq!(single_non_duplicate(&[1, 1, 2]), 2);
        assert_eq!(single_non_duplicate(&[1, 2, 2]), 1);
    }

    #[test]
    fn test_min_eating_speed() {
        assert_eq!(min_eating_speed(&[3, 6, 7, 11], 8), 4);
        assert_eq!(min_eating_speed(&[30, 11, 23, 4, 20], 5), 30);
        assert_eq!(min_eating_speed(&[30, 11, 23, 4, 20], 6), 23);
        assert_eq!(min_eating_speed(&[1, 1, 1, 1], 4), 1);
        assert_eq!(min_eating_speed(&[312884470], 312884469), 2);
    }

    #[test]
    fn test_ship_within_days() {
        assert_eq!(ship_within_days(&[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15);
        assert_eq!(ship_within_days(&[3, 2, 2, 4, 1, 4], 3), 6);
        assert_eq!(ship_within_days(&[1, 2, 3, 1, 1], 4), 3);
        assert_eq!(ship_within_days(&[10], 1), 10);
        assert_eq!(ship_within_days(&[1, 2, 3], 3), 3);
    }

    #[test]
    fn test_split_array() {
        assert_eq!(split_array(&[7, 2, 5, 10, 8], 2), 18);
        assert_eq!(split_array(&[1, 2, 3, 4, 5], 2), 9);
        assert_eq!(split_array(&[1, 4, 4], 3), 4);
        assert_eq!(split_array(&[1, 1, 1, 1], 4), 1);
        assert_eq!(split_array(&[10], 1), 10);
    }

    #[test]
    fn test_search_range() {
        assert_eq!(search_range(&[5, 7, 7, 8, 8, 10], 8), vec![3, 4]);
        assert_eq!(search_range(&[5, 7, 7, 8, 8, 10], 6), vec![-1, -1]);
        assert_eq!(search_range(&[], 0), vec![-1, -1]);
        assert_eq!(search_range(&[1], 1), vec![0, 0]);
        assert_eq!(search_range(&[1, 1, 1, 1], 1), vec![0, 3]);
    }
}

// Main function for running standalone tests
fn main() {
    println!("Day 16: Binary Search & Advanced Searching");
    println!("Run `cargo test` to execute all unit tests.");
}
