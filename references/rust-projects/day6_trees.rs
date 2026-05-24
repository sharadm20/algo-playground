/// Day 6: Trees & Binary Trees - Comprehensive Implementation in Rust
/// Topics: Binary Tree Structure, Tree Traversal, BST, Tree Properties

use std::cell::RefCell;
use std::rc::Rc;
use std::collections::VecDeque;

// ============================================================
// 1. BINARY TREE NODE DEFINITION
// ============================================================

/// Type alias for cleaner tree node references
type TreeLink = Option<Rc<RefCell<TreeNode>>>;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct TreeNode {
    pub val: i32,
    pub left: TreeLink,
    pub right: TreeLink,
}

impl TreeNode {
    #[inline]
    pub fn new(val: i32) -> Self {
        TreeNode {
            val,
            left: None,
            right: None,
        }
    }
}

/// Helper function to create a binary tree from a vector (level-order)
fn build_tree(values: &[Option<i32>]) -> TreeLink {
    if values.is_empty() {
        return None;
    }

    let root = Rc::new(RefCell::new(TreeNode::new(values[0].unwrap())));
    let mut queue = VecDeque::new();
    queue.push_back((root.clone(), 0));

    while let Some((node, index)) = queue.pop_front() {
        let left_index = 2 * index + 1;
        let right_index = 2 * index + 2;

        if left_index < values.len() {
            if let Some(val) = values[left_index] {
                let left_node = Rc::new(RefCell::new(TreeNode::new(val)));
                node.borrow_mut().left = Some(left_node.clone());
                queue.push_back((left_node, left_index));
            }
        }

        if right_index < values.len() {
            if let Some(val) = values[right_index] {
                let right_node = Rc::new(RefCell::new(TreeNode::new(val)));
                node.borrow_mut().right = Some(right_node.clone());
                queue.push_back((right_node, right_index));
            }
        }
    }

    Some(root)
}

/// Helper function to convert tree to vector (level-order)
fn tree_to_vec(root: &TreeLink) -> Vec<Option<i32>> {
    if root.is_none() {
        return vec![];
    }

    let mut result = Vec::new();
    let mut queue = VecDeque::new();
    queue.push_back(root.clone());

    while let Some(node) = queue.pop_front() {
        if let Some(n) = node {
            result.push(Some(n.borrow().val));
            queue.push_back(n.borrow().left.clone());
            queue.push_back(n.borrow().right.clone());
        } else {
            result.push(None);
        }
    }

    // Remove trailing Nones
    while result.last() == Some(&None) {
        result.pop();
    }

    result
}

// ============================================================
// 2. TREE TRAVERSALS
// ============================================================

/// In-order traversal: Left -> Root -> Right
/// Time: O(n), Space: O(h)
fn inorder_traversal(root: &TreeLink) -> Vec<i32> {
    let mut result = Vec::new();

    fn dfs(node: &TreeLink, result: &mut Vec<i32>) {
        if let Some(n) = node {
            dfs(&n.borrow().left, result);
            result.push(n.borrow().val);
            dfs(&n.borrow().right, result);
        }
    }

    dfs(root, &mut result);
    result
}

/// Pre-order traversal: Root -> Left -> Right
/// Time: O(n), Space: O(h)
fn preorder_traversal(root: &TreeLink) -> Vec<i32> {
    let mut result = Vec::new();

    fn dfs(node: &TreeLink, result: &mut Vec<i32>) {
        if let Some(n) = node {
            result.push(n.borrow().val);
            dfs(&n.borrow().left, result);
            dfs(&n.borrow().right, result);
        }
    }

    dfs(root, &mut result);
    result
}

/// Post-order traversal: Left -> Right -> Root
/// Time: O(n), Space: O(h)
fn postorder_traversal(root: &TreeLink) -> Vec<i32> {
    let mut result = Vec::new();

    fn dfs(node: &TreeLink, result: &mut Vec<i32>) {
        if let Some(n) = node {
            dfs(&n.borrow().left, result);
            dfs(&n.borrow().right, result);
            result.push(n.borrow().val);
        }
    }

    dfs(root, &mut result);
    result
}

/// Level-order traversal (BFS)
/// Time: O(n), Space: O(w)
fn levelorder_traversal(root: &TreeLink) -> Vec<Vec<i32>> {
    if root.is_none() {
        return vec![];
    }

    let mut result = Vec::new();
    let mut queue = VecDeque::new();
    queue.push_back(root.clone());

    while !queue.is_empty() {
        let level_size = queue.len();
        let mut current_level = Vec::new();

        for _ in 0..level_size {
            if let Some(node) = queue.pop_front() {
                if let Some(n) = node {
                    current_level.push(n.borrow().val);
                    if n.borrow().left.is_some() {
                        queue.push_back(n.borrow().left.clone());
                    }
                    if n.borrow().right.is_some() {
                        queue.push_back(n.borrow().right.clone());
                    }
                }
            }
        }

        result.push(current_level);
    }

    result
}

/// Iterative in-order traversal using stack
fn inorder_iterative(root: &TreeLink) -> Vec<i32> {
    let mut result = Vec::new();
    let mut stack = Vec::new();
    let mut current = root.clone();

    while current.is_some() || !stack.is_empty() {
        while let Some(node) = current {
            stack.push(node.clone());
            current = node.borrow().left.clone();
        }

        if let Some(node) = stack.pop() {
            result.push(node.borrow().val);
            current = node.borrow().right.clone();
        }
    }

    result
}

/// Iterative pre-order traversal using stack
fn preorder_iterative(root: &TreeLink) -> Vec<i32> {
    if root.is_none() {
        return vec![];
    }

    let mut result = Vec::new();
    let mut stack = vec![root.clone()];

    while let Some(node) = stack.pop() {
        if let Some(n) = node {
            result.push(n.borrow().val);
            // Push right first so left is processed first
            if n.borrow().right.is_some() {
                stack.push(n.borrow().right.clone());
            }
            if n.borrow().left.is_some() {
                stack.push(n.borrow().left.clone());
            }
        }
    }

    result
}

// ============================================================
// 3. BINARY SEARCH TREE (BST) OPERATIONS
// ============================================================

/// Validate if a binary tree is a valid BST
/// Time: O(n), Space: O(h)
fn is_valid_bst(root: &TreeLink) -> bool {
    fn validate(node: &TreeLink, low: i64, high: i64) -> bool {
        if let Some(n) = node {
            let val = n.borrow().val as i64;
            if val <= low || val >= high {
                return false;
            }
            validate(&n.borrow().left, low, val) &&
            validate(&n.borrow().right, val, high)
        } else {
            true
        }
    }

    validate(root, i64::MIN, i64::MAX)
}

/// Search for a value in BST
/// Time: O(h), Space: O(h)
fn search_bst(root: &TreeLink, val: i32) -> TreeLink {
    if let Some(node) = root {
        let node_val = node.borrow().val;
        if node_val == val {
            return Some(node.clone());
        } else if val < node_val {
            return search_bst(&node.borrow().left, val);
        } else {
            return search_bst(&node.borrow().right, val);
        }
    }
    None
}

/// Insert a value into BST
/// Time: O(h), Space: O(h)
fn insert_bst(root: &TreeLink, val: i32) -> TreeLink {
    if root.is_none() {
        return Some(Rc::new(RefCell::new(TreeNode::new(val))));
    }

    let node_val = root.as_ref().unwrap().borrow().val;
    if val < node_val {
        let new_left = insert_bst(&root.as_ref().unwrap().borrow().left, val);
        root.as_ref().unwrap().borrow_mut().left = new_left;
    } else if val > node_val {
        let new_right = insert_bst(&root.as_ref().unwrap().borrow().right, val);
        root.as_ref().unwrap().borrow_mut().right = new_right;
    }

    root.clone()
}

/// Find minimum node in a subtree
fn get_min_node(node: &TreeLink) -> TreeLink {
    let mut current = node.clone();
    while let Some(n) = current {
        if n.borrow().left.is_none() {
            return Some(n.clone());
        }
        current = n.borrow().left.clone();
    }
    None
}

// ============================================================
// 4. TREE HEIGHT AND DEPTH
// ============================================================

/// Calculate maximum depth (height) of binary tree
/// Time: O(n), Space: O(h)
fn max_depth(root: &TreeLink) -> i32 {
    if root.is_none() {
        return 0;
    }

    let node = root.as_ref().unwrap();
    1 + max_depth(&node.borrow().left).max(max_depth(&node.borrow().right))
}

/// Calculate minimum depth (shortest path to leaf)
/// Time: O(n), Space: O(h)
fn min_depth(root: &TreeLink) -> i32 {
    if root.is_none() {
        return 0;
    }

    let node = root.as_ref().unwrap();
    let left = node.borrow().left.clone();
    let right = node.borrow().right.clone();

    if left.is_none() {
        return 1 + min_depth(&right);
    }
    if right.is_none() {
        return 1 + min_depth(&left);
    }

    1 + min_depth(&left).min(min_depth(&right))
}

// ============================================================
// 5. TREE DIAMETER
// ============================================================

/// Calculate diameter of binary tree
/// Time: O(n), Space: O(h)
fn diameter_of_binary_tree(root: &TreeLink) -> i32 {
    use std::cell::Cell;
    let diameter = Cell::new(0);

    fn height(node: &TreeLink, diameter: &Cell<i32>) -> i32 {
        if node.is_none() {
            return 0;
        }

        let n = node.as_ref().unwrap();
        let left_height = height(&n.borrow().left, diameter);
        let right_height = height(&n.borrow().right, diameter);

        diameter.set(diameter.get().max(left_height + right_height));

        1 + left_height.max(right_height)
    }

    height(root, &diameter);
    diameter.get()
}

// ============================================================
// 6. BALANCED BINARY TREE
// ============================================================

/// Check if binary tree is height-balanced
/// Time: O(n), Space: O(h)
fn is_balanced(root: &TreeLink) -> bool {
    fn check_balance(node: &TreeLink) -> (bool, i32) {
        if node.is_none() {
            return (true, 0);
        }

        let n = node.as_ref().unwrap();
        let (left_balanced, left_height) = check_balance(&n.borrow().left);
        let (right_balanced, right_height) = check_balance(&n.borrow().right);

        let is_current_balanced = left_balanced && right_balanced &&
            (left_height - right_height).abs() <= 1;
        let current_height = 1 + left_height.max(right_height);

        (is_current_balanced, current_height)
    }

    check_balance(root).0
}

// ============================================================
// 7. TREE SYMMETRY
// ============================================================

/// Check if binary tree is symmetric
/// Time: O(n), Space: O(h)
fn is_symmetric(root: &TreeLink) -> bool {
    fn is_mirror(t1: &TreeLink, t2: &TreeLink) -> bool {
        match (t1, t2) {
            (None, None) => true,
            (Some(n1), Some(n2)) => {
                n1.borrow().val == n2.borrow().val &&
                is_mirror(&n1.borrow().left, &n2.borrow().right) &&
                is_mirror(&n1.borrow().right, &n2.borrow().left)
            }
            _ => false,
        }
    }

    is_mirror(root, root)
}

// ============================================================
// 8. TREE PATH SUM
// ============================================================

/// Check if tree has a root-to-leaf path with given sum
/// Time: O(n), Space: O(h)
fn has_path_sum(root: &TreeLink, target_sum: i32) -> bool {
    if root.is_none() {
        return false;
    }

    let node = root.as_ref().unwrap();
    let val = node.borrow().val;
    let left = node.borrow().left.clone();
    let right = node.borrow().right.clone();

    // Check if leaf
    if left.is_none() && right.is_none() {
        return val == target_sum;
    }

    let remaining = target_sum - val;
    has_path_sum(&left, remaining) || has_path_sum(&right, remaining)
}

// ============================================================
// TESTS
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tree_traversals() {
        // Build tree:
        //        1
        //       / \
        //      2   3
        //     / \
        //    4   5
        let values = vec![Some(1), Some(2), Some(3), Some(4), Some(5)];
        let root = build_tree(&values);

        assert_eq!(inorder_traversal(&root), vec![4, 2, 5, 1, 3]);
        assert_eq!(preorder_traversal(&root), vec![1, 2, 4, 5, 3]);
        assert_eq!(postorder_traversal(&root), vec![4, 5, 2, 3, 1]);
        assert_eq!(
            levelorder_traversal(&root),
            vec![vec![1], vec![2, 3], vec![4, 5]]
        );
        assert_eq!(inorder_iterative(&root), vec![4, 2, 5, 1, 3]);
        assert_eq!(preorder_iterative(&root), vec![1, 2, 4, 5, 3]);

        println!("✓ All traversal tests passed");
    }

    #[test]
    fn test_bst_operations() {
        // Build BST:
        //       4
        //      / \
        //     2   7
        //    / \
        //   1   3
        let root = build_tree(&vec![
            Some(4),
            Some(2),
            Some(7),
            Some(1),
            Some(3),
        ]);

        // Validate BST
        assert!(is_valid_bst(&root));

        // Search BST
        let result = search_bst(&root, 2);
        assert!(result.is_some());
        assert_eq!(result.unwrap().borrow().val, 2);

        // Insert BST
        let root = insert_bst(&root, 5);
        assert!(is_valid_bst(&root));

        println!("✓ All BST operation tests passed");
    }

    #[test]
    fn test_tree_properties() {
        // Balanced tree:
        //       1
        //      / \
        //     2   3
        //    / \
        //   4   5
        let balanced = build_tree(&vec![
            Some(1),
            Some(2),
            Some(3),
            Some(4),
            Some(5),
        ]);

        assert_eq!(max_depth(&balanced), 3);
        assert_eq!(min_depth(&balanced), 2);
        assert_eq!(diameter_of_binary_tree(&balanced), 3);
        assert!(is_balanced(&balanced));

        // Unbalanced tree:
        //   1
        //    \
        //     2
        //      \
        //       3
        let unbalanced = build_tree(&vec![
            Some(1),
            None,
            Some(2),
            None,
            None,
            None,
            Some(3),
        ]);

        assert_eq!(max_depth(&unbalanced), 3);
        assert_eq!(min_depth(&unbalanced), 3);
        assert!(!is_balanced(&unbalanced));

        println!("✓ All tree property tests passed");
    }

    #[test]
    fn test_symmetry() {
        // Symmetric tree:
        //     1
        //    / \
        //   2   2
        //  / \ / \
        // 3  4 4  3
        let symmetric = build_tree(&vec![
            Some(1),
            Some(2),
            Some(2),
            Some(3),
            Some(4),
            Some(4),
            Some(3),
        ]);
        assert!(is_symmetric(&symmetric));

        // Asymmetric tree:
        //     1
        //    / \
        //   2   2
        //    \   \
        //     3   3
        let asymmetric = build_tree(&vec![
            Some(1),
            Some(2),
            Some(2),
            None,
            Some(3),
            None,
            Some(3),
        ]);
        assert!(!is_symmetric(&asymmetric));

        println!("✓ All symmetry tests passed");
    }

    #[test]
    fn test_path_sum() {
        // Tree:
        //       5
        //      / \
        //     4   8
        //    /   / \
        //   11  13  4
        //  /  \      \
        // 7    2      1
        let values = vec![
            Some(5),
            Some(4),
            Some(8),
            Some(11),
            None,
            Some(13),
            Some(4),
            Some(7),
            Some(2),
            None,
            None,
            None,
            None,
            None,
            Some(1),
        ];
        let root = build_tree(&values);

        assert!(has_path_sum(&root, 22));
        assert!(!has_path_sum(&root, 26));

        println!("✓ All path sum tests passed");
    }
}

fn main() {
    println!("Day 6: Trees & Binary Trees - Running Tests\n");

    // Run tests with: cargo test
    println!("Run 'cargo test' to execute all unit tests");
}
