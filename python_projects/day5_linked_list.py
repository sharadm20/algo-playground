"""
Day 5: Linked List - Comprehensive Implementation
Topics: Singly/Doubly Linked Lists, Fast-Slow Pointers, Reversal, Cycle Detection
"""

from typing import Optional, List


# ============================================================
# 1. SINGLY LINKED LIST
# ============================================================

class ListNode:
    """Node for a singly linked list."""
    
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SinglyLinkedList:
    """Singly linked list with common operations."""
    
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, val: int) -> None:
        """Add node at the end."""
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self.size += 1
    
    def prepend(self, val: int) -> None:
        """Add node at the beginning."""
        new_node = ListNode(val, self.head)
        self.head = new_node
        self.size += 1
    
    def delete(self, val: int) -> bool:
        """Delete first occurrence of value."""
        if not self.head:
            return False
        
        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return True
        
        curr = self.head
        while curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
                self.size -= 1
                return True
            curr = curr.next
        return False
    
    def to_list(self) -> List[int]:
        """Convert linked list to Python list."""
        result = []
        curr = self.head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result
    
    def __len__(self) -> int:
        return self.size


# ============================================================
# 2. DOUBLY LINKED LIST
# ============================================================

class DoublyListNode:
    """Node for a doubly linked list."""
    
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    """Doubly linked list with common operations."""
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, val: int) -> None:
        """Add node at the end."""
        new_node = DoublyListNode(val, self.tail, None)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def prepend(self, val: int) -> None:
        """Add node at the beginning."""
        new_node = DoublyListNode(val, None, self.head)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
    
    def delete(self, val: int) -> bool:
        """Delete first occurrence of value."""
        if not self.head:
            return False
        
        curr = self.head
        while curr:
            if curr.val == val:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next
                
                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev
                
                self.size -= 1
                return True
            curr = curr.next
        return False
    
    def to_list(self) -> List[int]:
        """Convert doubly linked list to Python list."""
        result = []
        curr = self.head
        while curr:
            result.append(curr.val)
            curr = curr.next
        return result
    
    def to_list_reverse(self) -> List[int]:
        """Convert doubly linked list to Python list (reverse order)."""
        result = []
        curr = self.tail
        while curr:
            result.append(curr.val)
            curr = curr.prev
        return result
    
    def __len__(self) -> int:
        return self.size


# ============================================================
# 3. FAST-SLOW POINTER TECHNIQUES
# ============================================================

def find_middle(head: ListNode) -> Optional[ListNode]:
    """
    Find the middle node of a linked list using fast-slow pointers.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: Fast pointer moves 2 steps, slow pointer moves 1 step.
    When fast reaches end, slow is at middle.
    """
    if not head:
        return None
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow


def has_cycle(head: ListNode) -> bool:
    """
    Detect if linked list has a cycle using Floyd's cycle detection.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: If there's a cycle, fast and slow pointers will meet.
    This is also known as the "Tortoise and Hare" algorithm.
    """
    if not head or not head.next:
        return False
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False


def find_cycle_start(head: ListNode) -> Optional[ListNode]:
    """
    Find the starting node of a cycle in a linked list.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: After detecting cycle, reset one pointer to head.
    Move both pointers one step at a time - they meet at cycle start.
    """
    if not head or not head.next:
        return None
    
    slow = head
    fast = head
    
    # Detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            # Cycle detected, find start
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    
    return None


def find_kth_from_end(head: ListNode, k: int) -> Optional[ListNode]:
    """
    Find the kth node from the end using two pointers.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: Move first pointer k steps ahead, then move both
    until first reaches end. Second pointer is at kth from end.
    """
    if not head or k <= 0:
        return None
    
    first = head
    second = head
    
    # Move first pointer k steps ahead
    for _ in range(k):
        if not first:
            return None  # k is larger than list length
        first = first.next
    
    # Move both pointers until first reaches end
    while first:
        first = first.next
        second = second.next
    
    return second


# ============================================================
# 4. LINKED LIST REVERSAL
# ============================================================

def reverse_linked_list(head: ListNode) -> Optional[ListNode]:
    """
    Reverse a linked list iteratively.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: Use three pointers (prev, curr, next_temp) to reverse links.
    """
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next  # Save next node
        curr.next = prev       # Reverse link
        prev = curr            # Move prev forward
        curr = next_temp       # Move curr forward
    
    return prev  # New head


def reverse_linked_list_recursive(head: ListNode) -> Optional[ListNode]:
    """
    Reverse a linked list recursively.
    
    Time Complexity: O(n)
    Space Complexity: O(n) - recursion stack
    
    Pattern: Reverse from end backwards, update links on return.
    """
    # Base case
    if not head or not head.next:
        return head
    
    # Reverse rest of list
    new_head = reverse_linked_list_recursive(head.next)
    
    # Reverse current link
    head.next.next = head
    head.next = None
    
    return new_head


def reverse_between(head: ListNode, left: int, right: int) -> Optional[ListNode]:
    """
    Reverse a portion of linked list between positions left and right.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: Find the segment, reverse it, reconnect.
    """
    if not head or left == right:
        return head
    
    # Dummy node to handle edge cases
    dummy = ListNode(0, head)
    prev = dummy
    
    # Move to node before reversal
    for _ in range(left - 1):
        prev = prev.next
    
    # Reverse the segment
    curr = prev.next
    for _ in range(right - left):
        next_node = curr.next
        curr.next = next_node.next
        next_node.next = prev.next
        prev.next = next_node
    
    return dummy.next


# ============================================================
# 5. MERGE TWO SORTED LISTS
# ============================================================

def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Merge two sorted linked lists into one sorted list.
    
    Time Complexity: O(n + m)
    Space Complexity: O(1)
    
    Pattern: Use dummy node and merge by comparing values.
    """
    dummy = ListNode()
    curr = dummy
    
    while list1 and list2:
        if list1.val < list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next
    
    # Attach remaining nodes
    curr.next = list1 if list1 else list2
    
    return dummy.next


def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists using divide and conquer.
    
    Time Complexity: O(n log k) where n is total nodes, k is number of lists
    Space Complexity: O(1)
    
    Pattern: Repeatedly merge pairs (divide and conquer).
    """
    if not lists:
        return None
    
    def merge_two(l1, l2):
        dummy = ListNode()
        curr = dummy
        while l1 and l2:
            if l1.val < l2.val:
                curr.next = l1
                l1 = l1.next
            else:
                curr.next = l2
                l2 = l2.next
            curr = curr.next
        curr.next = l1 if l1 else l2
        return dummy.next
    
    # Merge lists in pairs
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            if i + 1 < len(lists):
                merged.append(merge_two(lists[i], lists[i + 1]))
            else:
                merged.append(lists[i])
        lists = merged
    
    return lists[0] if lists else None


# ============================================================
# 6. ADDITIONAL LINKED LIST PATTERNS
# ============================================================

def remove_nth_from_end(head: ListNode, n: int) -> Optional[ListNode]:
    """
    Remove the nth node from the end of list.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: Two pointers with gap of n nodes.
    """
    dummy = ListNode(0, head)
    first = dummy
    second = dummy
    
    # Move first n+1 steps ahead
    for _ in range(n + 1):
        first = first.next
    
    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next
    
    # Remove nth node
    second.next = second.next.next
    
    return dummy.next


def reorder_list(head: ListNode) -> None:
    """
    Reorder list: L0→Ln→L1→Ln-1→L2→Ln-2→...
    Modifies in-place.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: Find middle, reverse second half, merge alternately.
    """
    if not head or not head.next:
        return
    
    # Find middle
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    curr = slow
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    # Merge two halves
    first = head
    second = prev
    while second.next:
        temp1 = first.next
        temp2 = second.next
        first.next = second
        second.next = temp1
        first = temp1
        second = temp2


def is_palindrome(head: ListNode) -> bool:
    """
    Check if linked list is a palindrome.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Pattern: Find middle, reverse second half, compare.
    """
    if not head or not head.next:
        return True
    
    # Find middle
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    curr = slow
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    # Compare first and reversed second half
    first = head
    second = prev
    while second:
        if first.val != second.val:
            return False
        first = first.next
        second = second.next
    
    return True


def intersection_of_two_lists(headA: ListNode, headB: ListNode) -> Optional[ListNode]:
    """
    Find intersection point of two linked lists.
    
    Time Complexity: O(n + m)
    Space Complexity: O(1)
    
    Pattern: Traverse both lists, switch heads. They meet at intersection.
    """
    if not headA or not headB:
        return None
    
    ptr_a = headA
    ptr_b = headB
    
    # When ptr_a reaches end, switch to headB
    # When ptr_b reaches end, switch to headA
    # They will meet at intersection or both reach None
    while ptr_a != ptr_b:
        ptr_a = ptr_a.next if ptr_a else headB
        ptr_b = ptr_b.next if ptr_b else headA
    
    return ptr_a


# ============================================================
# TESTING
# ============================================================

def test_singly_linked_list():
    """Test singly linked list operations."""
    print("=" * 60)
    print("Testing Singly Linked List")
    print("=" * 60)
    
    ll = SinglyLinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    print(f"After appending 1, 2, 3: {ll.to_list()}")
    assert ll.to_list() == [1, 2, 3]
    
    ll.prepend(0)
    print(f"After prepending 0: {ll.to_list()}")
    assert ll.to_list() == [0, 1, 2, 3]
    
    ll.delete(2)
    print(f"After deleting 2: {ll.to_list()}")
    assert ll.to_list() == [0, 1, 3]
    
    print(f"Size: {len(ll)}")
    assert len(ll) == 3
    print("✓ Singly Linked List tests passed\n")


def test_doubly_linked_list():
    """Test doubly linked list operations."""
    print("=" * 60)
    print("Testing Doubly Linked List")
    print("=" * 60)
    
    dll = DoublyLinkedList()
    dll.append(1)
    dll.append(2)
    dll.append(3)
    print(f"After appending 1, 2, 3: {dll.to_list()}")
    assert dll.to_list() == [1, 2, 3]
    
    dll.prepend(0)
    print(f"After prepending 0: {dll.to_list()}")
    assert dll.to_list() == [0, 1, 2, 3]
    
    print(f"Reverse order: {dll.to_list_reverse()}")
    assert dll.to_list_reverse() == [3, 2, 1, 0]
    
    dll.delete(2)
    print(f"After deleting 2: {dll.to_list()}")
    assert dll.to_list() == [0, 1, 3]
    
    print(f"Size: {len(dll)}")
    assert len(dll) == 3
    print("✓ Doubly Linked List tests passed\n")


def test_fast_slow_pointers():
    """Test fast-slow pointer techniques."""
    print("=" * 60)
    print("Testing Fast-Slow Pointers")
    print("=" * 60)
    
    # Create list: 1 -> 2 -> 3 -> 4 -> 5
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    
    # Find middle
    middle = find_middle(head)
    print(f"Middle of [1,2,3,4,5]: {middle.val}")
    assert middle.val == 3
    
    # Find 2nd from end
    kth = find_kth_from_end(head, 2)
    print(f"2nd from end: {kth.val}")
    assert kth.val == 4
    
    # Test cycle detection
    no_cycle = ListNode(1, ListNode(2, ListNode(3)))
    print(f"Has cycle (no cycle): {has_cycle(no_cycle)}")
    assert has_cycle(no_cycle) == False
    
    # Create cycle: 1 -> 2 -> 3 -> 4 -> 2 (cycle back to node 2)
    node2 = ListNode(2)
    node3 = ListNode(3)
    node4 = ListNode(4)
    node2.next = node3
    node3.next = node4
    node4.next = node2  # Creates cycle
    
    print(f"Has cycle (with cycle): {has_cycle(node2)}")
    assert has_cycle(node2) == True
    
    cycle_start = find_cycle_start(node2)
    print(f"Cycle starts at node with value: {cycle_start.val}")
    assert cycle_start.val == 2
    
    print("✓ Fast-Slow Pointers tests passed\n")


def test_reversal():
    """Test linked list reversal."""
    print("=" * 60)
    print("Testing Linked List Reversal")
    print("=" * 60)
    
    # Create list: 1 -> 2 -> 3 -> 4 -> 5
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    
    # Iterative reversal
    reversed_head = reverse_linked_list(head)
    result = []
    curr = reversed_head
    while curr:
        result.append(curr.val)
        curr = curr.next
    print(f"Iterative reverse [1,2,3,4,5]: {result}")
    assert result == [5, 4, 3, 2, 1]
    
    # Recursive reversal
    head2 = ListNode(1, ListNode(2, ListNode(3)))
    reversed_head2 = reverse_linked_list_recursive(head2)
    result2 = []
    curr = reversed_head2
    while curr:
        result2.append(curr.val)
        curr = curr.next
    print(f"Recursive reverse [1,2,3]: {result2}")
    assert result2 == [3, 2, 1]
    
    # Reverse between
    head3 = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    reversed_between = reverse_between(head3, 2, 4)
    result3 = []
    curr = reversed_between
    while curr:
        result3.append(curr.val)
        curr = curr.next
    print(f"Reverse between positions 2-4 [1,2,3,4,5]: {result3}")
    assert result3 == [1, 4, 3, 2, 5]
    
    print("✓ Reversal tests passed\n")


def test_merge():
    """Test merging sorted lists."""
    print("=" * 60)
    print("Testing Merge Sorted Lists")
    print("=" * 60)
    
    # Merge two lists
    list1 = ListNode(1, ListNode(3, ListNode(5)))
    list2 = ListNode(2, ListNode(4, ListNode(6)))
    merged = merge_two_lists(list1, list2)
    
    result = []
    curr = merged
    while curr:
        result.append(curr.val)
        curr = curr.next
    print(f"Merge [1,3,5] and [2,4,6]: {result}")
    assert result == [1, 2, 3, 4, 5, 6]
    
    # Merge k lists
    lists = [
        ListNode(1, ListNode(4, ListNode(5))),
        ListNode(1, ListNode(3, ListNode(4))),
        ListNode(2, ListNode(6))
    ]
    merged_k = merge_k_lists(lists)
    
    result_k = []
    curr = merged_k
    while curr:
        result_k.append(curr.val)
        curr = curr.next
    print(f"Merge k lists: {result_k}")
    assert result_k == [1, 1, 2, 3, 4, 4, 5, 6]
    
    print("✓ Merge tests passed\n")


def test_additional_patterns():
    """Test additional linked list patterns."""
    print("=" * 60)
    print("Testing Additional Patterns")
    print("=" * 60)
    
    # Remove nth from end
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    result = remove_nth_from_end(head, 2)
    res_list = []
    curr = result
    while curr:
        res_list.append(curr.val)
        curr = curr.next
    print(f"Remove 2nd from end [1,2,3,4,5]: {res_list}")
    assert res_list == [1, 2, 3, 5]
    
    # Is palindrome
    palindrome = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))
    result = is_palindrome(palindrome)
    print(f"Is [1,2,2,1] palindrome: {result}")
    assert result == True
    
    not_palindrome = ListNode(1, ListNode(2, ListNode(3)))
    result = is_palindrome(not_palindrome)
    print(f"Is [1,2,3] palindrome: {result}")
    assert result == False
    
    # Intersection
    common = ListNode(8, ListNode(4, ListNode(5)))
    list_a = ListNode(4, ListNode(1, common))
    list_b = ListNode(5, ListNode(6, ListNode(1, common)))
    intersection = intersection_of_two_lists(list_a, list_b)
    print(f"Intersection at node: {intersection.val if intersection else None}")
    assert intersection.val == 8
    
    print("✓ Additional Patterns tests passed\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DAY 5: LINKED LIST - COMPREHENSIVE TESTING")
    print("=" * 60 + "\n")
    
    test_singly_linked_list()
    test_doubly_linked_list()
    test_fast_slow_pointers()
    test_reversal()
    test_merge()
    test_additional_patterns()
    
    print("=" * 60)
    print("ALL TESTS PASSED! ✓")
    print("=" * 60)
