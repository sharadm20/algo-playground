// Day 18: Segment Trees & Binary Indexed Trees
//
// This module implements Segment Trees and Binary Indexed Trees (Fenwick Trees)
// for efficient range queries and point updates in Rust.

pub struct SegmentTree {
    n: usize,
    size: usize,
    tree: Vec<i32>,
}

impl SegmentTree {
    /// Create a new SegmentTree from the given data.
    ///
    /// # Arguments
    ///
    /// * `data` - Input array of numbers
    ///
    pub fn new(data: &[i32]) -> Self {
        let n = data.len();
        let mut size = 1;
        while size < n {
            size <<= 1;
        }
        
        let mut tree = vec![0; 2 * size];
        
        // Build the tree
        for i in 0..n {
            tree[size + i] = data[i];
        }
        for i in (1..size).rev() {
            tree[i] = tree[2 * i] + tree[2 * i + 1];
        }
        
        SegmentTree { n, size, tree }
    }
    
    /// Update the value at the given index.
    ///
    /// # Arguments
    ///
    /// * `index` - Index to update (0-based)
    /// * `value` - New value
    ///
    pub fn update(&mut self, index: usize, value: i32) {
        let mut pos = self.size + index;
        self.tree[pos] = value;
        let mut pos = pos / 2;
        
        while pos >= 1 {
            let new_val = self.tree[2 * pos] + self.tree[2 * pos + 1];
            if self.tree[pos] == new_val {
                break;
            }
            self.tree[pos] = new_val;
            pos /= 2;
        }
    }
    
    /// Query the sum of elements in the range [l, r].
    ///
    /// # Arguments
    ///
    /// * `l` - Left index of the range (0-based)
    /// * `r` - Right index of the range (0-based)
    ///
    /// # Returns
    ///
    /// Sum of elements in the range [l, r]
    ///
    pub fn query_range(&self, l: usize, r: usize) -> i32 {
        let mut res = 0;
        let mut l = self.size + l;
        let mut r = self.size + r;
        
        while l <= r {
            if l % 2 == 1 {
                res += self.tree[l];
                l += 1;
            }
            if r % 2 == 0 {
                res += self.tree[r];
                r -= 1;
            }
            l /= 2;
            r /= 2;
        }
        
        res
    }
}

pub struct FenwickTree {
    size: usize,
    tree: Vec<i32>,
}

impl FenwickTree {
    /// Create a new FenwickTree with the given size.
    ///
    /// # Arguments
    ///
    /// * `size` - Size of the tree
    ///
    pub fn new(size: usize) -> Self {
        FenwickTree {
            size,
            tree: vec![0; size + 1],
        }
    }
    
    /// Update the value at the given index by adding delta.
    ///
    /// # Arguments
    ///
    /// * `index` - Index to update (1-based)
    /// * `delta` - Value to add
    ///
    pub fn update(&mut self, mut index: usize, delta: i32) {
        while index <= self.size {
            self.tree[index] += delta;
            index += index & !index + 1;
        }
    }
    
    /// Query the prefix sum up to the given index.
    ///
    /// # Arguments
    ///
    /// * `mut index` - Index to query (1-based)
    ///
    /// # Returns
    ///
    /// Prefix sum up to the given index
    ///
    pub fn query(&self, mut index: usize) -> i32 {
        let mut res = 0;
        while index > 0 {
            res += self.tree[index];
            index -= index & !index + 1;
        }
        res
    }
}

fn count_inversions(arr: &[i32]) -> i32 {
    /// Count the number of inversions in the array using Fenwick Tree.
    ///
    /// # Arguments
    ///
    /// * `arr` - Input array
    ///
    /// # Returns
    ///
    /// Number of inversions in the array
    
    // Coordinate compression
    let mut sorted_arr = arr.to_vec();
    sorted_arr.sort();
    let rank: std::collections::HashMap<i32, usize> = sorted_arr
        .iter()
        .enumerate()
        .map(|(i, &v)| (v, i + 1))
        .collect();
    
    let mut ft = FenwickTree::new(arr.len());
    let mut inversions = 0;
    
    // Traverse from right to left
    for i in (0..arr.len()).rev() {
        let current_rank = rank[&arr[i]];
        inversions += ft.query(current_rank - 1);
        ft.update(current_rank, 1);
    }
    
    inversions
}

#[cfg(test)]
pub mod tests {
    use super::*;
    
    #[test]
    pub fn test_segment_tree() {
        println!("Testing SegmentTree...");
        let data = vec![1, 3, 5, 7, 9, 11];
        let mut st = SegmentTree::new(&data);
        
        // Test range queries
        assert_eq!(st.query_range(0, 5), data.iter().sum());
        assert_eq!(st.query_range(1, 3), 15);
        assert_eq!(st.query_range(2, 4), 21);
        
        // Test updates
        st.update(2, 10); // Change 5 to 10
        assert_eq!(st.query_range(0, 5), 41);
        assert_eq!(st.query_range(2, 2), 10);
        
        println!("SegmentTree tests passed!");
    }
    
    #[test]
    pub fn test_fenwick_tree() {
        println!("Testing FenwickTree...");
        let mut ft = FenwickTree::new(6);
        
        // Test updates and queries
        ft.update(1, 1);
        ft.update(2, 3);
        ft.update(3, 5);
        ft.update(4, 7);
        ft.update(5, 9);
        ft.update(6, 11);
        
        assert_eq!(ft.query(1), 1);
        assert_eq!(ft.query(3), 9);
        assert_eq!(ft.query(6), 36);
        
        // Test range query using prefix sums
        let range_sum = ft.query(6) - ft.query(2);
        assert_eq!(range_sum, 32);
        
        println!("FenwickTree tests passed!");
    }
    
    #[test]
    pub fn test_inversion_count() {
        println!("Testing Inversion Count...");
        
        // Test cases
        assert_eq!(count_inversions(&[2, 4, 1, 3, 5]), 3);
        assert_eq!(count_inversions(&[5, 4, 3, 2, 1]), 10);
        assert_eq!(count_inversions(&[1, 2, 3, 4, 5]), 0);
        
        println!("Inversion Count tests passed!");
    }
}

fn main() {
    println!("Day 18: Segment Trees & Binary Indexed Trees");
    println!("Running tests...");
    
    // Run tests
    tests::test_segment_tree();
    tests::test_fenwick_tree();
    tests::test_inversion_count();
    
    println!("All tests passed successfully!");
}
