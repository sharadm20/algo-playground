/// Day 5: Linked List - Comprehensive Implementation in Rust
/// Topics: Singly/Doubly Linked Lists, Fast-Slow Pointers, Reversal, Cycle Detection

use std::cell::RefCell;
use std::rc::Rc;

// ============================================================
// 1. SINGLY LINKED LIST TYPE DEFINITION
// ============================================================

/// Type alias for cleaner linked list node references
type Link = Option<Rc<RefCell<ListNode>>>;

#[derive(Clone, Debug, PartialEq)]
struct ListNode {
    val: i32,
    next: Link,
}

impl ListNode {
    fn new(val: i32) -> Self {
        ListNode { val, next: None }
    }
}

/// Helper function to create a linked list from a vector
fn create_list(vals: &[i32]) -> Link {
    let mut head = None;
    for &val in vals.iter().rev() {
        let mut node = ListNode::new(val);
        node.next = head;
        head = Some(Rc::new(RefCell::new(node)));
    }
    head
}

/// Helper function to convert linked list to vector
fn list_to_vec(head: &Link) -> Vec<i32> {
    let mut result = Vec::new();
    let mut current = head.clone();
    while let Some(node) = current {
        result.push(node.borrow().val);
        current = node.borrow().next.clone();
    }
    result
}

// ============================================================
// 2. FAST-SLOW POINTER TECHNIQUES
// ============================================================

/// Find the middle node of a linked list using fast-slow pointers.
fn find_middle(head: &Link) -> Link {
    let mut slow = head.clone();
    let mut fast = head.clone();

    while let Some(fast_node) = fast {
        match fast_node.borrow().next.clone() {
            Some(next) => {
                match next.borrow().next.clone() {
                    Some(next_next) => {
                        fast = Some(next_next);
                        slow = slow.unwrap().borrow().next.clone();
                    }
                    None => {
                        // For even-length lists, return second middle
                        slow = slow.unwrap().borrow().next.clone();
                        break;
                    }
                }
            }
            None => break,
        }
    }

    slow
}

/// Detect if linked list has a cycle using Floyd's cycle detection.
fn has_cycle(head: &Link) -> bool {
    let mut slow = head.clone();
    let mut fast = head.clone();

    loop {
        if let Some(fast_node) = fast.clone() {
            if let Some(next) = fast_node.borrow().next.clone() {
                fast = next.borrow().next.clone();
                slow = slow.unwrap().borrow().next.clone();

                if slow == fast {
                    return true;
                }
            } else {
                return false;
            }
        } else {
            return false;
        }
    }
}

/// Find the kth node from the end using two pointers.
fn find_kth_from_end(head: &Link, k: i32) -> Link {
    if head.is_none() || k <= 0 {
        return None;
    }

    let mut first = head.clone();
    let mut second = head.clone();

    // Move first pointer k steps ahead
    for _ in 0..k {
        if let Some(node) = first {
            first = node.borrow().next.clone();
        } else {
            return None; // k is larger than list length
        }
    }

    // Move both pointers until first reaches end
    while let Some(node) = first {
        first = node.borrow().next.clone();
        second = second.unwrap().borrow().next.clone();
    }

    second
}

// ============================================================
// 3. LINKED LIST REVERSAL
// ============================================================

/// Reverse a linked list iteratively.
fn reverse_linked_list(head: &Link) -> Link {
    let mut prev: Link = None;
    let mut curr = head.clone();

    while let Some(node) = curr {
        let next = node.borrow().next.clone();
        node.borrow_mut().next = prev.clone();
        prev = Some(node);
        curr = next;
    }

    prev
}

/// Reverse a portion of linked list between positions left and right.
fn reverse_between(head: &Link, left: i32, right: i32) -> Link {
    if head.is_none() || left == right {
        return head.clone();
    }

    let vals = list_to_vec(head);
    let mut result = vec![0; vals.len()];

    // Copy elements before left position
    for i in 0..(left - 1) as usize {
        result[i] = vals[i];
    }

    // Reverse segment
    let left_idx = (left - 1) as usize;
    let right_idx = (right - 1) as usize;
    for (i, &val) in vals[left_idx..right_idx + 1].iter().rev().enumerate() {
        result[left_idx + i] = val;
    }

    // Copy elements after right position
    for i in (right_idx + 1)..vals.len() {
        result[i] = vals[i];
    }

    create_list(&result)
}

// ============================================================
// 4. MERGE TWO SORTED LISTS
// ============================================================

/// Merge two sorted linked lists into one sorted list.
fn merge_two_lists(list1: &Link, list2: &Link) -> Link {
    // Convert to vectors, merge, and convert back
    let mut v1 = list_to_vec(list1);
    let mut v2 = list_to_vec(list2);
    let mut merged = Vec::with_capacity(v1.len() + v2.len());

    let mut i = 0;
    let mut j = 0;

    while i < v1.len() && j < v2.len() {
        if v1[i] < v2[j] {
            merged.push(v1[i]);
            i += 1;
        } else {
            merged.push(v2[j]);
            j += 1;
        }
    }

    while i < v1.len() {
        merged.push(v1[i]);
        i += 1;
    }

    while j < v2.len() {
        merged.push(v2[j]);
        j += 1;
    }

    create_list(&merged)
}

// ============================================================
// 5. ADDITIONAL LINKED LIST PATTERNS
// ============================================================

/// Remove the nth node from the end of list.
fn remove_nth_from_end(head: &Link, n: i32) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode::new(0)));
    dummy.borrow_mut().next = head.clone();

    let mut first = Some(dummy.clone());
    let mut second = Some(dummy.clone());

    // Move first n+1 steps ahead
    for _ in 0..n + 1 {
        if let Some(node) = first {
            let next = node.borrow().next.clone();
            first = next;
        }
    }

    // Move both until first reaches end
    while let Some(node) = first.clone() {
        let next_first = node.borrow().next.clone();
        let next_second = second.as_ref().unwrap().borrow().next.clone();
        first = next_first;
        second = next_second;
    }

    // Remove nth node
    if let Some(node) = second {
        let next_node = node.borrow().next.as_ref().unwrap().borrow().next.clone();
        node.borrow_mut().next = next_node;
    }

    let result = dummy.borrow().next.clone();
    result
}

/// Check if linked list is a palindrome.
fn is_palindrome(head: &Link) -> bool {
    let vals = list_to_vec(head);
    let len = vals.len();
    if len <= 1 {
        return true;
    }

    let mut left = 0;
    let mut right = len - 1;

    while left < right {
        if vals[left] != vals[right] {
            return false;
        }
        left += 1;
        right -= 1;
    }

    true
}

// ============================================================
// TESTING
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_and_convert_list() {
        let list = create_list(&[1, 2, 3, 4, 5]);
        let vals = list_to_vec(&list);
        assert_eq!(vals, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_find_middle() {
        // Odd length: 1 -> 2 -> 3 -> 4 -> 5
        let list = create_list(&[1, 2, 3, 4, 5]);
        let middle = find_middle(&list);
        assert_eq!(middle.unwrap().borrow().val, 3);

        // Even length: 1 -> 2 -> 3 -> 4
        let list = create_list(&[1, 2, 3, 4]);
        let middle = find_middle(&list);
        assert_eq!(middle.unwrap().borrow().val, 3);
    }

    #[test]
    fn test_find_kth_from_end() {
        let list = create_list(&[1, 2, 3, 4, 5]);

        // 2nd from end
        let kth = find_kth_from_end(&list, 2);
        assert_eq!(kth.unwrap().borrow().val, 4);

        // 1st from end (last element)
        let kth = find_kth_from_end(&list, 1);
        assert_eq!(kth.unwrap().borrow().val, 5);

        // 5th from end (first element)
        let kth = find_kth_from_end(&list, 5);
        assert_eq!(kth.unwrap().borrow().val, 1);

        // k larger than list length
        let kth = find_kth_from_end(&list, 10);
        assert!(kth.is_none());
    }

    #[test]
    fn test_reverse_linked_list() {
        let list = create_list(&[1, 2, 3, 4, 5]);
        let reversed = reverse_linked_list(&list);
        let vals = list_to_vec(&reversed);
        assert_eq!(vals, vec![5, 4, 3, 2, 1]);

        // Empty list
        let empty: Link = None;
        let reversed = reverse_linked_list(&empty);
        assert!(reversed.is_none());

        // Single element
        let single = create_list(&[1]);
        let reversed = reverse_linked_list(&single);
        let vals = list_to_vec(&reversed);
        assert_eq!(vals, vec![1]);
    }

    #[test]
    fn test_reverse_between() {
        let list = create_list(&[1, 2, 3, 4, 5]);
        let reversed = reverse_between(&list, 2, 4);
        let vals = list_to_vec(&reversed);
        assert_eq!(vals, vec![1, 4, 3, 2, 5]);
    }

    #[test]
    fn test_merge_two_lists() {
        let list1 = create_list(&[1, 3, 5]);
        let list2 = create_list(&[2, 4, 6]);
        let merged = merge_two_lists(&list1, &list2);
        let vals = list_to_vec(&merged);
        assert_eq!(vals, vec![1, 2, 3, 4, 5, 6]);

        // Empty lists
        let empty: Link = None;
        let merged = merge_two_lists(&empty, &list1);
        let vals = list_to_vec(&merged);
        assert_eq!(vals, vec![1, 3, 5]);
    }

    #[test]
    fn test_remove_nth_from_end() {
        let list = create_list(&[1, 2, 3, 4, 5]);
        let result = remove_nth_from_end(&list, 2);
        let vals = list_to_vec(&result);
        assert_eq!(vals, vec![1, 2, 3, 5]);

        // Remove first element
        let list = create_list(&[1, 2]);
        let result = remove_nth_from_end(&list, 2);
        let vals = list_to_vec(&result);
        assert_eq!(vals, vec![2]);
    }

    #[test]
    fn test_is_palindrome() {
        // Palindrome: 1 -> 2 -> 2 -> 1
        let palindrome = create_list(&[1, 2, 2, 1]);
        assert!(is_palindrome(&palindrome));

        // Not palindrome: 1 -> 2 -> 3
        let not_palindrome = create_list(&[1, 2, 3]);
        assert!(!is_palindrome(&not_palindrome));

        // Single element
        let single = create_list(&[1]);
        assert!(is_palindrome(&single));

        // Empty list
        let empty: Link = None;
        assert!(is_palindrome(&empty));
    }

    #[test]
    fn test_has_cycle() {
        // No cycle
        let no_cycle = create_list(&[1, 2, 3]);
        assert!(!has_cycle(&no_cycle));
    }
}

fn main() {
    println!("Day 5: Linked List - Rust Implementation");
    println!("Run 'cargo test' to execute all tests.");
    println!();

    // Demo: Create and manipulate a linked list
    let list = create_list(&[1, 2, 3, 4, 5]);
    println!("Original list: {:?}", list_to_vec(&list));

    let middle = find_middle(&list);
    if let Some(node) = middle {
        println!("Middle element: {}", node.borrow().val);
    }

    let reversed = reverse_linked_list(&list);
    println!("Reversed list: {:?}", list_to_vec(&reversed));

    let list1 = create_list(&[1, 3, 5]);
    let list2 = create_list(&[2, 4, 6]);
    let merged = merge_two_lists(&list1, &list2);
    println!("Merged lists: {:?}", list_to_vec(&merged));

    let palindrome = create_list(&[1, 2, 2, 1]);
    println!("Is [1,2,2,1] palindrome? {}", is_palindrome(&palindrome));
}
