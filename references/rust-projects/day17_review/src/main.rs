// Day 17: Binary Search Review & Practice
// Rust Implementations - Mixed Practice Problems

// =============================================================================
// 1. Search in a 2D Matrix
// =============================================================================

fn search_matrix(matrix: &Vec<Vec<i32>>, target: i32) -> bool {
    if matrix.is_empty() || matrix[0].is_empty() {
        return false;
    }
    
    let m = matrix.len();
    let n = matrix[0].len();
    let mut left: i32 = 0;
    let mut right: i32 = (m * n) as i32 - 1;
    
    while left <= right {
        let mid = left + (right - left) / 2;
        let row = (mid as usize) / n;
        let col = (mid as usize) % n;
        let val = matrix[row][col];
        
        if val == target {
            return true;
        } else if val < target {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    false
}

// =============================================================================
// 2. Square Root (Integer)
// =============================================================================

fn my_sqrt(x: i32) -> i32 {
    if x < 2 {
        return x;
    }
    
    let mut left: i64 = 1;
    let mut right: i64 = x as i64 / 2;
    
    while left <= right {
        let mid = left + (right - left) / 2;
        let squared = mid * mid;
        
        if squared == x as i64 {
            return mid as i32;
        } else if squared < x as i64 {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    right as i32
}

// =============================================================================
// 3. Search in Rotated Sorted Array II (with duplicates)
// =============================================================================

fn search_rotated_duplicates(nums: &Vec<i32>, target: i32) -> bool {
    let mut left: i32 = 0;
    let mut right: i32 = nums.len() as i32 - 1;
    
    while left <= right {
        let mid = left + (right - left) / 2;
        
        if nums[mid as usize] == target {
            return true;
        }
        
        // Handle duplicates
        if nums[left as usize] == nums[mid as usize] && nums[mid as usize] == nums[right as usize] {
            left += 1;
            right -= 1;
        } else if nums[left as usize] <= nums[mid as usize] {
            // Left half is sorted
            if nums[left as usize] <= target && target < nums[mid as usize] {
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        } else {
            // Right half is sorted
            if nums[mid as usize] < target && target <= nums[right as usize] {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }
    
    false
}

// =============================================================================
// 4. H-Index II
// =============================================================================

fn h_index(citations: &Vec<i32>) -> i32 {
    let n = citations.len() as i32;
    let mut left: i32 = 0;
    let mut right: i32 = n - 1;
    
    while left <= right {
        let mid = left + (right - left) / 2;
        let h = n - mid;
        
        if citations[mid as usize] == h {
            return h;
        } else if citations[mid as usize] < h {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    n - left
}

// =============================================================================
// 5. Find the Smallest Divisor Given a Threshold
// =============================================================================

fn smallest_divisor(nums: &Vec<i32>, threshold: i32) -> i32 {
    fn check(divisor: i32, nums: &Vec<i32>, threshold: i32) -> bool {
        let mut total = 0;
        for &num in nums {
            total += (num + divisor - 1) / divisor; // ceil division
        }
        total <= threshold
    }
    
    let mut left = 1;
    let mut right = *nums.iter().max().unwrap();
    
    while left < right {
        let mid = left + (right - left) / 2;
        if check(mid, nums, threshold) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    left
}

// =============================================================================
// 6. Find Minimum in Rotated Sorted Array II (with duplicates)
// =============================================================================

fn find_min_rotated_duplicates(nums: &Vec<i32>) -> i32 {
    let mut left: i32 = 0;
    let mut right: i32 = nums.len() as i32 - 1;
    
    while left < right {
        let mid = left + (right - left) / 2;
        
        if nums[mid as usize] > nums[right as usize] {
            left = mid + 1;
        } else if nums[mid as usize] < nums[right as usize] {
            right = mid;
        } else {
            // nums[mid] == nums[right], can't determine which half
            right -= 1;
        }
    }
    
    nums[left as usize]
}

// =============================================================================
// 7. Search Insert Position
// =============================================================================

fn search_insert(nums: &Vec<i32>, target: i32) -> i32 {
    let mut left: i32 = 0;
    let mut right: i32 = nums.len() as i32;
    
    while left < right {
        let mid = left + (right - left) / 2;
        if nums[mid as usize] < target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    
    left
}

// =============================================================================
// 8. Find Peak Element
// =============================================================================

fn find_peak_element(nums: &Vec<i32>) -> i32 {
    let mut left: i32 = 0;
    let mut right: i32 = nums.len() as i32 - 1;
    
    while left < right {
        let mid = left + (right - left) / 2;
        
        if nums[mid as usize] < nums[(mid + 1) as usize] {
            // Peak is on the right
            left = mid + 1;
        } else {
            // Peak is on the left (could be mid)
            right = mid;
        }
    }
    
    left
}

// =============================================================================
// 9. Koko Eating Bananas (Binary Search on Answer)
// =============================================================================

fn min_eating_speed(piles: &Vec<i32>, h: i32) -> i32 {
    fn can_finish(k: i32, piles: &Vec<i32>, h: i32) -> bool {
        let mut hours = 0;
        for &pile in piles {
            hours += (pile + k - 1) / k; // ceil(pile / k)
        }
        hours <= h
    }
    
    let mut left = 1;
    let mut right = *piles.iter().max().unwrap();
    
    while left < right {
        let mid = left + (right - left) / 2;
        if can_finish(mid, piles, h) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    left
}

// =============================================================================
// 10. Capacity to Ship Packages within D Days
// =============================================================================

fn ship_within_days(weights: &Vec<i32>, days: i32) -> i32 {
    fn can_ship(capacity: i32, weights: &Vec<i32>, days: i32) -> bool {
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
    }
    
    let left = *weights.iter().max().unwrap();
    let right: i32 = weights.iter().sum();
    let mut left = left;
    let mut right = right;
    
    while left < right {
        let mid = left + (right - left) / 2;
        if can_ship(mid, weights, days) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    left
}

// =============================================================================
// 11. Split Array Largest Sum
// =============================================================================

fn split_array(nums: &Vec<i32>, m: i32) -> i32 {
    fn can_split(max_sum: i32, nums: &Vec<i32>, m: i32) -> bool {
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
    }
    
    let left = *nums.iter().max().unwrap();
    let right: i32 = nums.iter().sum();
    let mut left = left;
    let mut right = right;
    
    while left < right {
        let mid = left + (right - left) / 2;
        if can_split(mid, nums, m) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }
    
    left
}

// =============================================================================
// 12. Find First and Last Position of Element
// =============================================================================

fn search_range(nums: &Vec<i32>, target: i32) -> Vec<i32> {
    fn find_bound(nums: &Vec<i32>, target: i32, is_first: bool) -> i32 {
        let mut left: i32 = 0;
        let mut right: i32 = nums.len() as i32 - 1;
        let mut bound = -1;
        
        while left <= right {
            let mid = left + (right - left) / 2;
            
            if nums[mid as usize] == target {
                bound = mid;
                if is_first {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else if nums[mid as usize] < target {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        bound
    }
    
    let first = find_bound(nums, target, true);
    if first == -1 {
        return vec![-1, -1];
    }
    let last = find_bound(nums, target, false);
    vec![first, last]
}

// =============================================================================
// TESTS
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_search_matrix() {
        let matrix = vec![
            vec![1, 3, 5, 7],
            vec![10, 11, 16, 20],
            vec![23, 30, 34, 60],
        ];
        assert_eq!(search_matrix(&matrix, 3), true);
        assert_eq!(search_matrix(&matrix, 13), false);
        assert_eq!(search_matrix(&matrix, 60), true);
        assert_eq!(search_matrix(&matrix, 1), true);
        assert_eq!(search_matrix(&vec![], 5), false);
    }

    #[test]
    fn test_my_sqrt() {
        assert_eq!(my_sqrt(4), 2);
        assert_eq!(my_sqrt(8), 2);
        assert_eq!(my_sqrt(0), 0);
        assert_eq!(my_sqrt(1), 1);
        assert_eq!(my_sqrt(16), 4);
        assert_eq!(my_sqrt(25), 5);
    }

    #[test]
    fn test_search_rotated_duplicates() {
        assert_eq!(search_rotated_duplicates(&vec![2, 5, 6, 0, 0, 1, 2], 0), true);
        assert_eq!(search_rotated_duplicates(&vec![2, 5, 6, 0, 0, 1, 2], 3), false);
        assert_eq!(search_rotated_duplicates(&vec![1, 1, 1, 1, 1], 1), true);
        assert_eq!(search_rotated_duplicates(&vec![1, 0, 1, 1, 1], 0), true);
    }

    #[test]
    fn test_h_index() {
        assert_eq!(h_index(&vec![0, 1, 3, 5, 6]), 3);
        assert_eq!(h_index(&vec![1, 2, 100]), 2);
        assert_eq!(h_index(&vec![0]), 0);
        assert_eq!(h_index(&vec![100]), 1);
    }

    #[test]
    fn test_smallest_divisor() {
        assert_eq!(smallest_divisor(&vec![1, 2, 5, 9], 6), 5);
        assert_eq!(smallest_divisor(&vec![44, 22, 33, 11, 1], 5), 44);
        assert_eq!(smallest_divisor(&vec![2, 3, 5, 7, 11], 11), 3);
        assert_eq!(smallest_divisor(&vec![1, 1, 1], 3), 1);
    }

    #[test]
    fn test_find_min_rotated_duplicates() {
        assert_eq!(find_min_rotated_duplicates(&vec![3, 3, 1, 3]), 1);
        assert_eq!(find_min_rotated_duplicates(&vec![2, 2, 2, 0, 1]), 0);
        assert_eq!(find_min_rotated_duplicates(&vec![1, 1, 1, 1]), 1);
        assert_eq!(find_min_rotated_duplicates(&vec![1]), 1);
    }

    #[test]
    fn test_search_insert() {
        assert_eq!(search_insert(&vec![1, 3, 5, 6], 5), 2);
        assert_eq!(search_insert(&vec![1, 3, 5, 6], 2), 1);
        assert_eq!(search_insert(&vec![1, 3, 5, 6], 7), 4);
        assert_eq!(search_insert(&vec![1, 3, 5, 6], 0), 0);
    }

    #[test]
    fn test_find_peak_element() {
        assert_eq!(find_peak_element(&vec![1, 2, 3, 1]), 2); // 3 is peak
        let result = find_peak_element(&vec![1, 2, 1, 3, 5, 6, 4]);
        assert!(result == 1 || result == 5); // 2 or 6
        assert_eq!(find_peak_element(&vec![1]), 0);
        assert_eq!(find_peak_element(&vec![2, 1]), 0);
        assert_eq!(find_peak_element(&vec![1, 2]), 1);
    }

    #[test]
    fn test_min_eating_speed() {
        assert_eq!(min_eating_speed(&vec![3, 6, 7, 11], 8), 4);
        assert_eq!(min_eating_speed(&vec![30, 11, 23, 4, 20], 5), 30);
        assert_eq!(min_eating_speed(&vec![30, 11, 23, 4, 20], 6), 23);
        assert_eq!(min_eating_speed(&vec![1, 1, 1, 1], 4), 1);
    }

    #[test]
    fn test_ship_within_days() {
        assert_eq!(ship_within_days(&vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15);
        assert_eq!(ship_within_days(&vec![3, 2, 2, 4, 1, 4], 3), 6);
        assert_eq!(ship_within_days(&vec![1, 2, 3, 1, 1], 4), 3);
        assert_eq!(ship_within_days(&vec![10], 1), 10);
    }

    #[test]
    fn test_split_array() {
        assert_eq!(split_array(&vec![7, 2, 5, 10, 8], 2), 18);
        assert_eq!(split_array(&vec![1, 2, 3, 4, 5], 2), 9);
        assert_eq!(split_array(&vec![1, 4, 4], 3), 4);
        assert_eq!(split_array(&vec![1, 1, 1, 1], 4), 1);
    }

    #[test]
    fn test_search_range() {
        assert_eq!(search_range(&vec![5, 7, 7, 8, 8, 10], 8), vec![3, 4]);
        assert_eq!(search_range(&vec![5, 7, 7, 8, 8, 10], 6), vec![-1, -1]);
        assert_eq!(search_range(&vec![], 0), vec![-1, -1]);
        assert_eq!(search_range(&vec![1], 1), vec![0, 0]);
        assert_eq!(search_range(&vec![1, 1, 1, 1], 1), vec![0, 3]);
    }
}

fn main() {
    println!("Day 17: Binary Search Review & Practice");
    println!("Run 'cargo test' to verify all implementations!");
}
