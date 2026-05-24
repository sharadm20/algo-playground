class ListNode {
    private int data;
    ListNode next;

    ListNode(int data) {
        this.data = data;
        this.next = null;
    }
    ListNode() {}
    ListNode(int val, ListNode next) { this.data = val; this.next = next; }
    public ListNode merge(ListNode l1, ListNode l2) {
        ListNode temp = new ListNode(0);
        ListNode ptr = temp;

        while(l1 != null && l2 != null) {
            if(l1.data <= l2.data) {
                ptr.next = l1;
                l1 = l1.next;
                ptr = ptr.next;
            }else {
                ptr.next = l2;
                l2 = l2.next;
                ptr = ptr.next;
            }
        }
        ptr.next = (l1 != null) ? l1 : l2;

        return temp.next;
    }

    public ListNode getMiddle(ListNode head) {
        ListNode midPrev = null;

        while(head != null && head.next != null) {
            midPrev = midPrev == null ? head : midPrev.next;
            head = head.next.next;
        }
        ListNode mid = midPrev.next;
        midPrev.next = null;
        return mid;
    }

    public ListNode insertionSortList(ListNode head) {
        if(head == null || head.next == null) return head;
        ListNode mid = getMiddle(head);
        ListNode left = insertionSortList(head);
        ListNode right = insertionSortList(mid);

        return merge(left, right);
    }

    public int getData() {
        return data;
    }

    public ListNode getNext() {
        return next;
    }

    public void setData(int data) {
        this.data = data;
    }

    public void setNext(ListNode next) {
        this.next = next;
    }
}

public class LinkedListReversal {

    ListNode reverseList(ListNode head) {
        ListNode previous = null;
        ListNode current = head;
        while (current != null) {
            ListNode nextElement = current.getNext();
            current.setNext(previous);
            previous = current;
            current = nextElement;
        }
        return previous;
    }

    ListNode reverseListRecursive(ListNode head) {
        if (head == null) {
            return null;
        }
        if (head.getNext() == null) {
            return head;
        }
        ListNode node = reverseListRecursive(head.getNext());
        head.getNext().setNext(head);
        head.setNext(null);
        return node;
    }

}