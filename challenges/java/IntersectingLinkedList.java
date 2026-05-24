public class IntersectingLinkedList {
    public static void main(String[] args) {
        
    }
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        int c1 = getCount(headA);
        int c2 = getCount(headB);
        int d;

        if (c1 > c2) {
            d = c1 - c2;
            return getNode(d, headA, headB);
        }
        else {
            d = c2 - c1;
            return getNode(d, headB, headA);
        }
    }
    public ListNode getNode(int d, ListNode node1, ListNode node2){
        int i;
        ListNode current1 = node1;
        ListNode current2 = node2;
        for (i = 0; i < d; i++) {
            if (current1 == null) {
                return null;
            }
            current1 = current1.next;
        }
        while (current1 != null && current2 != null) {
            if (current1 == current2) {
                return current1;
            }
            current1 = current1.next;
            current2 = current2.next;
        }

        return null;
    }
    public static int getCount(ListNode head){
        ListNode current = head;
        int count = 0;

        while (current != null) {
            count++;
            current = current.next;
        }

        return count;
    }
}
