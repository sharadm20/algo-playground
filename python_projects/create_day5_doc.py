"""
Create Day 5 Word Document for DSA Study Plan
Topic: Linked List Data Structures
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


def create_day5_document():
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # Title
    title = doc.add_heading('Day 5: Linked List', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle
    subtitle = doc.add_paragraph('Singly/Doubly Linked Lists, Fast-Slow Pointers, Reversal, Cycle Detection')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True

    # Date and info
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.add_run('📅 April 3, 2026').bold = True
    info.add_run('  |  ')
    info.add_run('⏱️ 4-5 hours').bold = True
    info.add_run('  |  ')
    info.add_run('Difficulty: Intermediate').bold = True

    doc.add_paragraph()  # Spacer

    # ============================================================================
    # TOPIC OVERVIEW
    # ============================================================================
    doc.add_heading('Topic Overview', level=1)

    doc.add_paragraph(
        "Day 5 introduces linked lists, a fundamental linear data structure where elements are connected "
        "through pointers/references. Unlike arrays, linked lists provide efficient insertions and deletions "
        "but sacrifice random access. Mastering linked list manipulation is crucial for technical interviews "
        "and understanding more complex data structures like trees and graphs."
    )

    p = doc.add_paragraph()
    p.add_run('Why Linked Lists Matter:').bold = True

    reasons = [
        'Foundation for trees, graphs, and hash tables with chaining',
        'Dynamic size - no need to pre-allocate memory',
        'Efficient insertions/deletions (O(1) with pointer)',
        'Essential for implementing LRU caches, memory management',
        'Tests pointer manipulation skills in interviews'
    ]

    for reason in reasons:
        doc.add_paragraph(reason, style='List Bullet')

    # ============================================================================
    # CORE CONCEPTS
    # ============================================================================
    doc.add_heading('Core Concepts', level=1)

    doc.add_heading('1. Singly Linked List', level=2)
    doc.add_paragraph(
        "Each node contains data and a pointer to the next node. The list is accessed through a head pointer. "
        "Traversal is only possible in one direction (head to tail)."
    )

    p = doc.add_paragraph()
    p.add_run('Structure:').bold = True

    code_block = doc.add_paragraph()
    code_block_text = """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next"""
    run = code_block.add_run(code_block_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)

    p = doc.add_paragraph()
    p.add_run('Operations:').bold = True

    operations = [
        'Append (end): O(n) - traverse to tail, or O(1) with tail pointer',
        'Prepend (beginning): O(1) - update head pointer',
        'Delete: O(n) - find node, update previous node\'s pointer',
        'Search: O(n) - linear traversal required',
        'Access by index: O(n) - no random access'
    ]

    for op in operations:
        doc.add_paragraph(op, style='List Bullet')

    doc.add_heading('2. Doubly Linked List', level=2)
    doc.add_paragraph(
        "Each node contains data, a pointer to the next node, and a pointer to the previous node. "
        "Allows bidirectional traversal but uses more memory."
    )

    p = doc.add_paragraph()
    p.add_run('Structure:').bold = True

    code_block = doc.add_paragraph()
    code_block_text = """class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next"""
    run = code_block.add_run(code_block_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)

    p = doc.add_paragraph()
    p.add_run('Advantages over Singly Linked List:').bold = True

    advantages = [
        'Bidirectional traversal (forward and backward)',
        'O(1) deletion if node pointer is given (need prev pointer)',
        'Easier to implement operations like reverse traversal',
        'Can delete node in O(1) with both prev and next pointers'
    ]

    for adv in advantages:
        doc.add_paragraph(adv, style='List Bullet')

    p = doc.add_paragraph()
    p.add_run('Disadvantages:').bold = True

    disadvantages = [
        'More memory per node (extra pointer)',
        'More complex operations (must update both prev and next)',
        'Higher constant factor in operations'
    ]

    for dis in disadvantages:
        doc.add_paragraph(dis, style='List Bullet')

    # ============================================================================
    # KEY PATTERNS
    # ============================================================================
    doc.add_heading('Key Patterns & Techniques', level=1)

    doc.add_heading('Pattern 1: Fast-Slow Pointers (Tortoise and Hare)', level=2)

    p = doc.add_paragraph()
    p.add_run('Concept: ').bold = True
    p.add_run(
        "Use two pointers moving at different speeds. Fast pointer moves 2 steps while slow moves 1 step. "
        "This pattern is incredibly powerful for various linked list problems."
    )

    p = doc.add_paragraph()
    p.add_run('Applications:').bold = True

    applications = [
        'Find middle element: When fast reaches end, slow is at middle',
        'Detect cycle: If fast and slow meet, there\'s a cycle',
        'Find cycle start: Reset one pointer to head, move both at same speed',
        'Find kth from end: Move first pointer k steps ahead, then move both'
    ]

    for app in applications:
        doc.add_paragraph(app, style='List Bullet')

    p = doc.add_paragraph()
    p.add_run('Time Complexity: ').bold = True
    p.add_run('O(n) - each pointer traverses the list at most once')

    p = doc.add_paragraph()
    p.add_run('Space Complexity: ').bold = True
    p.add_run('O(1) - only uses two pointers, no extra space')

    doc.add_heading('Pattern 2: Linked List Reversal', level=2)

    p = doc.add_paragraph()
    p.add_run('Concept: ').bold = True
    p.add_run(
        "Reverse the direction of all links using three pointers: prev, curr, and next_temp. "
        "This is one of the most fundamental linked list operations."
    )

    p = doc.add_paragraph()
    p.add_run('Iterative Approach:').bold = True

    code_block = doc.add_paragraph()
    code_block_text = """def reverse_linked_list(head):
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next  # Save next node
        curr.next = prev       # Reverse link
        prev = curr            # Move prev forward
        curr = next_temp       # Move curr forward
    
    return prev  # New head"""
    run = code_block.add_run(code_block_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)

    p = doc.add_paragraph()
    p.add_run('Recursive Approach:').bold = True

    code_block = doc.add_paragraph()
    code_block_text = """def reverse_recursive(head):
    if not head or not head.next:
        return head
    
    new_head = reverse_recursive(head.next)
    head.next.next = head  # Reverse link
    head.next = None
    return new_head"""
    run = code_block.add_run(code_block_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)

    p = doc.add_paragraph()
    p.add_run('Time Complexity: ').bold = True
    p.add_run('O(n) - visit each node once')

    p = doc.add_paragraph()
    p.add_run('Space Complexity: ').bold = True
    p.add_run('O(1) iterative, O(n) recursive (call stack)')

    doc.add_heading('Pattern 3: Merge Sorted Lists', level=2)

    p = doc.add_paragraph()
    p.add_run('Concept: ').bold = True
    p.add_run(
        "Use a dummy node and merge by comparing values. This pattern is essential for "
        "divide-and-conquer algorithms and external sorting."
    )

    p = doc.add_paragraph()
    p.add_run('Algorithm:').bold = True

    steps = [
        'Create dummy node to simplify edge cases',
        'Compare heads of both lists, attach smaller to result',
        'Move pointer of attached list forward',
        'Repeat until one list is exhausted',
        'Attach remaining nodes from non-empty list'
    ]

    for i, step in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {step}')

    p = doc.add_paragraph()
    p.add_run('Time Complexity: ').bold = True
    p.add_run('O(n + m) where n and m are lengths of both lists')

    p = doc.add_paragraph()
    p.add_run('Space Complexity: ').bold = True
    p.add_run('O(1) - only uses pointers, modifies in-place')

    doc.add_heading('Pattern 4: Cycle Detection', level=2)

    p = doc.add_paragraph()
    p.add_run('Floyd\'s Cycle Detection Algorithm:').bold = True

    p = doc.add_paragraph()
    p.add_run(
        "Also known as the \"Tortoise and Hare\" algorithm. Uses two pointers moving at different speeds "
        "to detect if a linked list has a cycle."
    )

    p = doc.add_paragraph()
    p.add_run('Algorithm:').bold = True

    steps = [
        'Initialize slow and fast pointers to head',
        'Move slow one step, fast two steps',
        'If fast reaches null, no cycle exists',
        'If slow and fast meet, cycle exists',
        'To find cycle start: reset slow to head, move both one step at a time until they meet'
    ]

    for i, step in enumerate(steps, 1):
        doc.add_paragraph(f'{i}. {step}')

    p = doc.add_paragraph()
    p.add_run('Why They Meet: ').bold = True
    p.add_run(
        "In a cycle of length k, the distance between slow and fast decreases by 1 each step. "
        "They must meet within k steps."
    )

    # ============================================================================
    # ADDITIONAL PATTERNS
    # ============================================================================
    doc.add_heading('Additional Patterns', level=1)

    doc.add_heading('Remove Nth Node From End', level=2)
    p = doc.add_paragraph()
    p.add_run('Technique: ').bold = True
    p.add_run(
        'Use two pointers with a gap of n nodes. When first reaches end, second is at nth from end.'
    )

    doc.add_heading('Palindrome Check', level=2)
    p = doc.add_paragraph()
    p.add_run('Technique: ').bold = True
    p.add_run(
        'Find middle, reverse second half, compare with first half. Can restore list afterward if needed.'
    )

    doc.add_heading('Intersection of Two Lists', level=2)
    p = doc.add_paragraph()
    p.add_run('Technique: ').bold = True
    p.add_run(
        'Traverse both lists, switch heads when reaching end. They meet at intersection point or both reach null. '
        'This works because both pointers travel the same total distance.'
    )

    doc.add_heading('Reorder List', level=2)
    p = doc.add_paragraph()
    p.add_run('Technique: ').bold = True
    p.add_run(
        'Find middle, reverse second half, merge alternately. Combines multiple patterns into one solution.'
    )

    # ============================================================================
    # PRACTICE PROBLEMS
    # ============================================================================
    doc.add_heading('Practice Problems', level=1)

    problems = [
        {
            'name': 'Reverse Linked List',
            'difficulty': 'Easy',
            'description': 'Reverse a singly linked list iteratively and recursively.',
            'pattern': 'Reversal'
        },
        {
            'name': 'Merge Two Sorted Lists',
            'difficulty': 'Easy',
            'description': 'Merge two sorted linked lists into one sorted list.',
            'pattern': 'Merge'
        },
        {
            'name': 'Linked List Cycle',
            'difficulty': 'Easy',
            'description': 'Determine if a linked list has a cycle.',
            'pattern': 'Fast-Slow Pointers'
        },
        {
            'name': 'Middle of the Linked List',
            'difficulty': 'Easy',
            'description': 'Find the middle node of a linked list.',
            'pattern': 'Fast-Slow Pointers'
        },
        {
            'name': 'Remove Nth Node From End',
            'difficulty': 'Medium',
            'description': 'Remove the nth node from the end of the list.',
            'pattern': 'Two Pointers'
        },
        {
            'name': 'Palindrome Linked List',
            'difficulty': 'Medium',
            'description': 'Check if a linked list is a palindrome.',
            'pattern': 'Reversal + Two Pointers'
        },
        {
            'name': 'Intersection of Two Linked Lists',
            'difficulty': 'Easy',
            'description': 'Find the intersection point of two linked lists.',
            'pattern': 'Two Pointers'
        },
        {
            'name': 'Linked List Cycle II',
            'difficulty': 'Medium',
            'description': 'Find the starting node of a cycle in a linked list.',
            'pattern': 'Fast-Slow Pointers'
        },
        {
            'name': 'Reorder List',
            'difficulty': 'Medium',
            'description': 'Reorder list: L0→Ln→L1→Ln-1→L2→Ln-2→...',
            'pattern': 'Multiple Patterns'
        },
        {
            'name': 'Reverse Linked List II',
            'difficulty': 'Medium',
            'description': 'Reverse a portion of a linked list between positions m and n.',
            'pattern': 'Reversal'
        },
        {
            'name': 'Merge k Sorted Lists',
            'difficulty': 'Hard',
            'description': 'Merge k sorted linked lists using divide and conquer or heap.',
            'pattern': 'Merge + Divide & Conquer'
        },
        {
            'name': 'Copy List with Random Pointer',
            'difficulty': 'Medium',
            'description': 'Create a deep copy of a linked list with random pointers.',
            'pattern': 'Hash Map / Interleaving'
        }
    ]

    for i, problem in enumerate(problems, 1):
        p = doc.add_paragraph()
        p.add_run(f'Problem {i}: {problem["name"]}').bold = True
        p.add_run(f' ({problem["difficulty"]})')

        doc.add_paragraph(problem['description'])
        p = doc.add_paragraph()
        p.add_run('Pattern: ').bold = True
        p.add_run(problem['pattern'])
        doc.add_paragraph()

    # ============================================================================
    # HOMEWORK ASSIGNMENT
    # ============================================================================
    doc.add_heading('Homework Assignment', level=1)

    p = doc.add_paragraph()
    p.add_run('Complete the following problems:').bold = True

    homework = [
        'Reverse a linked list (both iterative and recursive)',
        'Find the middle element of a linked list',
        'Detect if a linked list has a cycle',
        'Merge two sorted linked lists',
        'Remove the nth node from the end of a linked list',
        'Check if a linked list is a palindrome',
        'Find the intersection of two linked lists',
        'Reverse a portion of a linked list between positions left and right'
    ]

    for i, hw in enumerate(homework, 1):
        doc.add_paragraph(f'{i}. {hw}', style='List Number')

    p = doc.add_paragraph()
    p.add_run('Challenge Problems:').bold = True

    challenges = [
        'Merge k sorted linked lists',
        'Reorder a linked list (L0→Ln→L1→Ln-1→...)',
        'Copy a linked list with random pointers'
    ]

    for chal in challenges:
        doc.add_paragraph(chal, style='List Bullet')

    # ============================================================================
    # TIPS & BEST PRACTICES
    # ============================================================================
    doc.add_heading('Tips & Best Practices', level=1)

    tips = [
        'Always handle edge cases: empty list, single node, two nodes',
        'Use dummy nodes to simplify edge case handling',
        'Draw diagrams to visualize pointer movements',
        'Be careful with pointer order - update in correct sequence',
        'Test with cycles by manually creating them in code',
        'For fast-slow pointers, always check fast and fast.next',
        'When reversing, save next node before updating pointers',
        'Use type hints for cleaner, more maintainable code',
        'Consider both iterative and recursive approaches',
        'In Rust, use Rc<RefCell<T>> for shared ownership with interior mutability'
    ]

    for tip in tips:
        doc.add_paragraph(tip, style='List Bullet')

    # ============================================================================
    # COMPLEXITY SUMMARY
    # ============================================================================
    doc.add_heading('Complexity Summary', level=1)

    # Create table
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Light Grid Accent 1'

    # Header row
    hdr_cells = table.rows[0].cells
    headers = ['Operation', 'Time', 'Space', 'Notes']
    for i, header in enumerate(headers):
        hdr_cells[i].text = header
        for paragraph in hdr_cells[i].paragraphs:
            for run in paragraph.runs:
                run.bold = True

    # Data rows
    operations_data = [
        ['Access by index', 'O(n)', 'O(1)', 'No random access'],
        ['Search', 'O(n)', 'O(1)', 'Linear traversal'],
        ['Insert at head', 'O(1)', 'O(1)', 'Update head pointer'],
        ['Insert at tail', 'O(n) or O(1)*', 'O(1)', '*O(1) with tail pointer'],
        ['Delete by value', 'O(n)', 'O(1)', 'Find + update pointer'],
        ['Reverse', 'O(n)', 'O(1)', 'Iterative approach'],
        ['Find middle', 'O(n)', 'O(1)', 'Fast-slow pointers'],
        ['Detect cycle', 'O(n)', 'O(1)', 'Floyd\'s algorithm'],
        ['Merge two lists', 'O(n+m)', 'O(1)', 'Two-pointer merge'],
        ['Merge k lists', 'O(n log k)', 'O(1)', 'Divide & conquer']
    ]

    for row_data in operations_data:
        row_cells = table.add_row().cells
        for i, cell_data in enumerate(row_data):
            row_cells[i].text = cell_data

    # ============================================================================
    # NEXT DAY PREVIEW
    # ============================================================================
    doc.add_heading('Coming Up: Day 6', level=1)

    p = doc.add_paragraph()
    p.add_run('Day 6: Trees & Binary Trees').bold = True

    doc.add_paragraph(
        "Tomorrow we'll explore tree data structures, starting with binary trees. We'll cover tree traversal "
        "(in-order, pre-order, post-order, level-order), binary search trees, and common tree algorithms. "
        "Trees are hierarchical structures that appear in databases, file systems, and many algorithms."
    )

    p = doc.add_paragraph()
    p.add_run('Topics:').bold = True

    topics = [
        'Binary tree structure and properties',
        'Tree traversal techniques (DFS and BFS)',
        'Binary search trees (BST)',
        'Validating BST',
        'Lowest common ancestor',
        'Tree height and diameter',
        'Balanced vs unbalanced trees'
    ]

    for topic in topics:
        doc.add_paragraph(topic, style='List Bullet')

    # Save document
    output_path = 'Day5_Linked_List.docx'
    doc.save(output_path)
    print(f"✓ Day 5 document created: {output_path}")


if __name__ == '__main__':
    create_day5_document()
