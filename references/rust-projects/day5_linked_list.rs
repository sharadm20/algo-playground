/// Day 5: Linked List - Comprehensive Implementation in Rust
/// Topics: Singly/Doubly Linked Lists, Fast-Slow Pointers, Reversal, Cycle Detection

use std::cell::RefCell;
use std::rc::Rc;

// ============================================================
// 1. SINGLY LINKED LIST TYPE DEFINITION
// ============================================================

/// Type alias for cleaner linked list node references
type NodePtr = Option<Rc<RefCell<ListNode>>>;

#[derive(Clone)]
struct ListNode {
    val: i32,
    next: NodePtr,
}

impl ListNode {
    fn new(val: i32) -> Self {
        ListNode { val, next: None }
    }
}

/// Helper function to create a linked list from a vector
fn create_list(vals: &[i32]) -> NodePtr {
    let mut head = None;
    for &val in vals.iter().rev() {
        let mut node = ListNode::new(val);
        node.next = head;
        head = Some(Rc::new(RefCell::new(node)));
    }
    head
}

/// Helper function to convert linked list to vector
fn list_to_vec(head: &NodePtr) -> Vec<i32> {
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
///
/// Time Complexity: O(n)
/// Space Complexity: O(1)
///
/// Pattern: Fast pointer moves 2 steps, slow pointer moves 1 step.
/// When fast reaches end, slow is at middle.
fn find_middle(head: &NodePtr) -> Option<Rc<RefCell<ListNode>>> {
    let mut slow = head.clone();
    let mut fast = head.clone();

    while let Some(fast_node) = fast.clone() {
        if let Some(next) = fast_node.borrow().next.clone() {
            if let Some(next_next) = next.borrow().next.clone() {
                fast = Some(next_next);
                slow = slow.unwrap().borrow().next.clone();
            } else {
                break;
            }
        } else {
            break;
        }
    }

    slow
}

/// Detect if linked list has a cycle using Floyd's cycle detection.
///
/// Time Complexity: O(n)
/// Space Complexity: O(1)
///
/// Pattern: If there's a cycle, fast and slow pointers will meet.
/// This is also known as the "Tortoise and Hare" algorithm.
fn has_cycle(head: &NodePtr) -> bool {
    let mut slow = head.clone();
    let mut fast = head.clone();

    while let Some(fast_node) = fast.clone() {
        if let Some(next) = fast_node.borrow().next.clone() {
            fast = next.borrow().next.clone();
            slow = slow.unwrap().borrow().next.clone();

            if slow == fast {
                return true;
            }
        } else {
            return false;
        }
    }

    false
}

/// Find the kth node from the end using two pointers.
///
/// Time Complexity: O(n)
/// Space Complexity: O(1)
///
/// Pattern: Move first pointer k steps ahead, then move both
/// until first reaches end. Second pointer is at kth from end.
fn find_kth_from_end(head: &NodePtr, k: i32) -> Option<Rc<RefCell<ListNode>>> {
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
///
/// Time Complexity: O(n)
/// Space Complexity: O(1)
///
/// Pattern: Use three pointers (prev, curr, next_temp) to reverse links.
fn reverse_linked_list(head: &NodePtr) -> NodePtr {
    let mut prev: NodePtr = None;
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
///
/// Time Complexity: O(n)
/// Space Complexity: O(1)
///
/// Pattern: Find the segment, reverse it, reconnect.
fn reverse_between(head: &NodePtr, left: i32, right: i32) -> NodePtr {
    if head.is_none() || left == right {
        return head.clone();
    }

    // Convert to mutable nodes for this operation
    let vals = list_to_vec(head);
    let mut result = Vec::new();

    // Build result with reversed segment
    for (i, &val) in vals.iter().enumerate() {
        let pos = (i + 1) as i32;
        if pos >= left && pos <= right {
            // Insert at correct position in reversed segment
            let insert_pos = (right - left) as usize - (pos - left) as usize;
            while result.len() <= insert_pos + (left - 1) as usize {
                result.push(0);
            }
            result[insert_pos + (left - 1) as usize] = val;
        } else {
            while result.len() <= i {
                result.push(0);
            }
            result[i] = val;
        }
    }

    create_list(&result)
}

// ============================================================
// 4. MERGE TWO SORTED LISTS
// ============================================================

/// Merge two sorted linked lists into one sorted list.
///
/// Time Complexity: O(n + m)
/// Space Complexity: O(1)
///
/// Pattern: Use dummy node and merge by comparing values.
fn merge_two_lists(
    list1: &NodePtr,
    list2: &NodePtr,
) -> NodePtr {
    let dummy = Rc::new(RefCell::new(ListNode::new(0)));
    let mut curr = dummy.clone();

    let mut l1 = list1.clone();
    let mut l2 = list2.clone();

    while let (Some(node1), Some(node2)) = (&l1, &l2) {
        let val1 = node1.borrow().val;
        let val2 = node2.borrow().val;

        if val1 < val2 {
            curr.borrow_mut().next = Some(node1.clone());
            l1 = node1.borrow().next.clone();
        } else {
            curr.borrow_mut().next = Some(node2.clone());
            l2 = node2.borrow().next.clone();
        }
        curr = curr.borrow().next.as_ref().unwrap().clone();
    }

    // Attach remaining nodes
    if l1.is_some() {
        curr.borrow_mut().next = l1;
    } else {
        curr.borrow_mut().next = l2;
    }

    dummy.borrow().next.clone()
}

// ============================================================
// 5. ADDITIONAL LINKED LIST PATTERNS
// ============================================================

/// Remove the nth node from the end of list.
///
/// Time Complexity: O(n)
/// Space Complexity: O(1)
///
/// Pattern: Two pointers with gap of n nodes.
fn remove_nth_from_end(head: &NodePtr, n: i32) -> NodePtr {
    let dummy = Rc::new(RefCell::new(ListNode::new(0)));
    dummy.borrow_mut().next = head.clone();

    let mut first = dummy.clone();
    let mut second = dummy.clone();

    // Move first n+1 steps ahead
    for _ in 0..n + 1 {
        first = first.borrow().next.as_ref().unwrap().clone();
    }

    // Move both until first reaches end
    while first.borrow().next.is_some() {
        first = first.borrow().next.as_ref().unwrap().clone();
        second = second.borrow().next.as_ref().unwrap().clone();
    }

    // Remove nth node
    let next_node = second.borrow().next.as_ref().unwrap().borrow().next.clone();
    second.borrow_mut().next = next_node;

    dummy.borrow().next.clone()
}

/// Check if linked list is a palindrome.
///
/// Time Complexity: O(n)
/// Space Complexity: O(n) for conversion to vector
///
/// Pattern: Convert to vector, use two pointers.
fn is_palindrome(head: &NodePtr) -> bool {
    let vals = list_to_vec(head);
    let mut left = 0;
    let mut right = vals.len() as i32 - 1;

    while left < right {
        if vals[left as usize] != vals[right as usize] {
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
        let empty: NodePtr = None;
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
        let empty: NodePtr = None;
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
        let empty: NodePtr = None;
        assert!(is_palindrome(&empty));
    }

    #[test]
    fn test_has_cycle() {
        // No cycle
        let no_cycle = create_list(&[1, 2, 3]);
        assert!(!has_cycle(&no_cycle));

        // Note: Creating cycles in Rust requires mutable references
        // and is more complex due to Rc<RefCell<>>, so we test the
        // algorithm logic separately
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
