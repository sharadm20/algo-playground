"""
Script to create Day 7 Review documentation using python-docx.
"""

try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    print("python-docx available")
except ImportError:
    print("Installing python-docx...")
    import subprocess
    subprocess.check_call(["pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Title
title = doc.add_heading('Day 7: Review & Practice', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph('Comprehensive Review of Days 1-6 Concepts', style='Subtitle')
doc.add_paragraph()

# Overview
doc.add_heading('Overview', level=1)
doc.add_paragraph(
    'Today is a comprehensive review day! We will practice mixed problems covering all concepts '
    'from Days 1-6, focusing on pattern recognition, problem-solving strategies, and implementation '
    'fluency. This review will help consolidate your understanding and identify areas for improvement.'
)

doc.add_heading('Topics Covered', level=2)
topics = [
    'Day 1: Arrays & Hashing (hash maps, frequency counting, complement lookup)',
    'Day 2: Advanced Arrays (two-pointer, sliding window, prefix sums)',
    'Day 3: String Manipulation (palindromes, string matching, sliding window, tries)',
    'Day 4: Stack & Queue (monotonic stack, BFS applications)',
    'Day 5: Linked List (fast-slow pointers, reversal, cycle detection, merging)',
    'Day 6: Trees & Binary Trees (traversals, BST, LCA, tree properties)'
]
for topic in topics:
    doc.add_paragraph(topic, style='List Bullet')

# Problem Categories
doc.add_heading('Problem Categories & Patterns', level=1)

# Category 1: Hash Map & Frequency Counting
doc.add_heading('Category 1: Hash Map & Frequency Counting (Days 1-2)', level=2)
doc.add_paragraph()

doc.add_heading('Pattern 1.1: Two Sum Variation', level=3)
doc.add_paragraph(
    'Problem: Given an array of integers and a target sum, find all unique pairs that sum to the target.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Use a hash set to track seen numbers', style='List Bullet')
doc.add_paragraph('For each number, check if (target - num) exists in set', style='List Bullet')
doc.add_paragraph('Time: O(n), Space: O(n)', style='List Bullet')

doc.add_heading('Pattern 1.2: Frequency-Based Grouping', level=3)
doc.add_paragraph(
    'Problem: Group anagrams together from a list of strings.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Sort each string or count character frequency as key', style='List Bullet')
doc.add_paragraph('Use hash map to group strings with same key', style='List Bullet')
doc.add_paragraph('Time: O(n * k log k) where k is max string length, Space: O(n * k)', style='List Bullet')

# Category 2: Two-Pointer & Sliding Window
doc.add_heading('Category 2: Two-Pointer & Sliding Window (Days 2-3)', level=2)
doc.add_paragraph()

doc.add_heading('Pattern 2.1: Container With Most Water', level=3)
doc.add_paragraph(
    'Problem: Given n vertical lines, find two lines that form a container holding the most water.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Use two pointers from both ends', style='List Bullet')
doc.add_paragraph('Move the pointer with shorter line inward', style='List Bullet')
doc.add_paragraph('Area = min(height[left], height[right]) * (right - left)', style='List Bullet')
doc.add_paragraph('Time: O(n), Space: O(1)', style='List Bullet')

doc.add_heading('Pattern 2.2: Longest Substring Without Repeating Characters', level=3)
doc.add_paragraph(
    'Problem: Find the length of the longest substring without repeating characters.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Use sliding window with hash set to track characters', style='List Bullet')
doc.add_paragraph('Expand right pointer, shrink when duplicate found', style='List Bullet')
doc.add_paragraph('Time: O(n), Space: O(min(n, m)) where m is charset size', style='List Bullet')

# Category 3: String Algorithms
doc.add_heading('Category 3: String Algorithms (Day 3)', level=2)
doc.add_paragraph()

doc.add_heading('Pattern 3.1: Palindrome Detection', level=3)
doc.add_paragraph(
    'Problem: Given a string, find the longest palindromic substring.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Expand around center approach', style='List Bullet')
doc.add_paragraph('Each character (and gap) can be center of palindrome', style='List Bullet')
doc.add_paragraph('Time: O(n²), Space: O(1)', style='List Bullet')

doc.add_heading('Pattern 3.2: String Pattern Matching', level=3)
doc.add_paragraph(
    'Problem: Implement strStr() - find first occurrence of needle in haystack.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Rabin-Karp: Rolling hash for efficient matching', style='List Bullet')
doc.add_paragraph('KMP: Build LPS array to skip comparisons', style='List Bullet')
doc.add_paragraph('Time: Rabin-Karp O(n+m) average, KMP O(n+m) worst case', style='List Bullet')

# Category 4: Stack & Queue Applications
doc.add_heading('Category 4: Stack & Queue Applications (Day 4)', level=2)
doc.add_paragraph()

doc.add_heading('Pattern 4.1: Valid Parentheses with Multiple Types', level=3)
doc.add_paragraph(
    'Problem: Given string with parentheses ()[]{} , determine if valid.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Use stack to track opening brackets', style='List Bullet')
doc.add_paragraph('Match closing brackets with stack top', style='List Bullet')
doc.add_paragraph('Time: O(n), Space: O(n)', style='List Bullet')

doc.add_heading('Pattern 4.2: Monotonic Stack - Next Greater Element', level=3)
doc.add_paragraph(
    'Problem: For each element, find the next greater element to its right.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Maintain decreasing stack of indices', style='List Bullet')
doc.add_paragraph('When current > stack top, found next greater', style='List Bullet')
doc.add_paragraph('Time: O(n), Space: O(n)', style='List Bullet')

# Category 5: Linked List Patterns
doc.add_heading('Category 5: Linked List Patterns (Day 5)', level=2)
doc.add_paragraph()

doc.add_heading('Pattern 5.1: Cycle Detection', level=3)
doc.add_paragraph(
    'Problem: Determine if a linked list has a cycle.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Floyd\'s cycle detection (tortoise and hare)', style='List Bullet')
doc.add_paragraph('Fast pointer moves 2 steps, slow moves 1 step', style='List Bullet')
doc.add_paragraph('If cycle exists, they will meet', style='List Bullet')
doc.add_paragraph('Time: O(n), Space: O(1)', style='List Bullet')

doc.add_heading('Pattern 5.2: Merge Sorted Lists', level=3)
doc.add_paragraph(
    'Problem: Merge two sorted linked lists into one sorted list.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('Use dummy node to simplify edge cases', style='List Bullet')
doc.add_paragraph('Compare and link smaller node', style='List Bullet')
doc.add_paragraph('Time: O(n + m), Space: O(1)', style='List Bullet')

# Category 6: Tree Traversals & Properties
doc.add_heading('Category 6: Tree Traversals & Properties (Day 6)', level=2)
doc.add_paragraph()

doc.add_heading('Pattern 6.1: Binary Tree Traversals', level=3)
doc.add_paragraph(
    'Problem: Implement in-order, pre-order, post-order, and level-order traversals.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('In-order: Left-Root-Right (gives sorted order for BST)', style='List Bullet')
doc.add_paragraph('Pre-order: Root-Left-Right (copy tree structure)', style='List Bullet')
doc.add_paragraph('Post-order: Left-Right-Root (delete tree)', style='List Bullet')
doc.add_paragraph('Level-order: BFS with queue (level by level)', style='List Bullet')
doc.add_paragraph('Time: O(n), Space: O(h) for DFS, O(w) for BFS', style='List Bullet')

doc.add_heading('Pattern 6.2: Lowest Common Ancestor', level=3)
doc.add_paragraph(
    'Problem: Find the lowest common ancestor of two nodes in binary tree/BST.'
)
doc.add_paragraph('Key Insights:', style='Heading 4')
doc.add_paragraph('General tree: DFS, return node if p or q found', style='List Bullet')
doc.add_paragraph('BST: Use BST property to optimize (O(h) vs O(n))', style='List Bullet')
doc.add_paragraph('If both smaller, go left; both larger, go right; else current is LCA', style='List Bullet')

# Practice Problems
doc.add_heading('Practice Problems', level=1)

doc.add_heading('Easy Problems', level=2)
easy_problems = [
    ('Two Sum', 'Arrays & Hashing', 'Use hash map to find complement'),
    ('Valid Palindrome', 'String Manipulation', 'Two-pointer validation'),
    ('Valid Parentheses', 'Stack', 'Stack-based matching'),
    ('Maximum Depth of Binary Tree', 'Trees', 'DFS with recursion'),
    ('Merge Two Sorted Lists', 'Linked List', 'Dummy node pattern'),
]

table = doc.add_table(rows=1, cols=3)
table.style = 'Light Grid Accent 1'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Problem'
hdr_cells[1].text = 'Category'
hdr_cells[2].text = 'Key Pattern'

for problem, category, pattern in easy_problems:
    row_cells = table.add_row().cells
    row_cells[0].text = problem
    row_cells[1].text = category
    row_cells[2].text = pattern

doc.add_paragraph()

doc.add_heading('Medium Problems', level=2)
medium_problems = [
    ('3Sum', 'Arrays & Two-Pointer', 'Sort + skip duplicates'),
    ('Container With Most Water', 'Two-Pointer', 'Greedy from both ends'),
    ('Longest Substring Without Repeating', 'Sliding Window', 'Hash set + window'),
    ('Group Anagrams', 'Hash Map', 'Frequency counting'),
    ('Evaluate Reverse Polish Notation', 'Stack', 'Stack-based evaluation'),
    ('Number of Islands', 'BFS/DFS', 'Connected components'),
    ('Find Middle of Linked List', 'Fast-Slow Pointers', 'Tortoise and hare'),
    ('Linked List Cycle II', 'Fast-Slow Pointers', 'Find cycle start'),
    ('Binary Tree Level Order Traversal', 'Trees/BFS', 'Queue-based level processing'),
    ('Validate Binary Search Tree', 'Trees/DFS', 'Range validation'),
    ('Lowest Common Ancestor of BST', 'Trees', 'BST property optimization'),
    ('Diameter of Binary Tree', 'Trees/DFS', 'Height + diameter tracking'),
]

table2 = doc.add_table(rows=1, cols=3)
table2.style = 'Light Grid Accent 1'
table2.alignment = WD_TABLE_ALIGNMENT.CENTER

hdr_cells2 = table2.rows[0].cells
hdr_cells2[0].text = 'Problem'
hdr_cells2[1].text = 'Category'
hdr_cells2[2].text = 'Key Pattern'

for problem, category, pattern in medium_problems:
    row_cells = table2.add_row().cells
    row_cells[0].text = problem
    row_cells[1].text = category
    row_cells[2].text = pattern

doc.add_paragraph()

doc.add_heading('Hard Problems (Bonus)', level=2)
hard_problems = [
    ('Trapping Rain Water', 'Two-Pointer/DP', 'Max height from both sides'),
    ('Minimum Window Substring', 'Sliding Window', 'Hash map + window expansion'),
    ('Word Ladder', 'BFS', 'Shortest transformation path'),
    ('Merge k Sorted Lists', 'Linked List/Divide & Conquer', 'Repeated pairwise merging'),
    ('Serialize and Deserialize Binary Tree', 'Trees', 'Pre-order with markers'),
]

table3 = doc.add_table(rows=1, cols=3)
table3.style = 'Light Grid Accent 1'
table3.alignment = WD_TABLE_ALIGNMENT.CENTER

hdr_cells3 = table3.rows[0].cells
hdr_cells3[0].text = 'Problem'
hdr_cells3[1].text = 'Category'
hdr_cells3[2].text = 'Key Pattern'

for problem, category, pattern in hard_problems:
    row_cells = table3.add_row().cells
    row_cells[0].text = problem
    row_cells[1].text = category
    row_cells[2].text = pattern

doc.add_paragraph()

# Study Strategy
doc.add_heading('Study Strategy for Day 7', level=1)

doc.add_heading('Morning Session (2-3 hours)', level=2)
doc.add_paragraph('1. Review all Day 1-6 materials briefly (30 minutes)', style='List Number')
doc.add_paragraph('2. Solve 3-4 Easy problems without looking at solutions (45 minutes)', style='List Number')
doc.add_paragraph('3. Solve 4-5 Medium problems with time limit of 20-30 min each (2 hours)', style='List Number')

doc.add_heading('Afternoon Session (2-3 hours)', level=2)
doc.add_paragraph('4. Attempt 1-2 Hard problems (1 hour)', style='List Number')
doc.add_paragraph('5. Review solutions and identify weak areas (30 minutes)', style='List Number')
doc.add_paragraph('6. Re-implement solutions for problems you struggled with (1 hour)', style='List Number')

doc.add_heading('Evening Review (1 hour)', level=2)
doc.add_paragraph('7. Summarize key patterns learned today', style='List Number')
doc.add_paragraph('8. Note areas that need more practice', style='List Number')
doc.add_paragraph('9. Plan focus for Day 8 (Graphs introduction)', style='List Number')

# Key Reminders
doc.add_heading('Key Reminders', level=1)
reminders = [
    'Always analyze time and space complexity before coding',
    'Draw diagrams for linked list and tree problems',
    'Use hash maps for frequency counting and complement lookup',
    'Two-pointer techniques work on sorted arrays or with specific constraints',
    'Sliding window requires monotonic property or hash map tracking',
    'Stack is LIFO (last in, first out), Queue is FIFO (first in, first out)',
    'Fast-slow pointer patterns detect cycles and find middle elements',
    'Tree traversals: in-order (BST sorted), pre-order (copy), post-order (delete)',
    'BFS for shortest path, DFS for exploring all paths',
    'Always handle edge cases: empty input, single element, all same elements'
]
for reminder in reminders:
    doc.add_paragraph(reminder, style='List Bullet')

# Save document
output_path = 'C:\\Users\\puppets\\Documents\\ds_and_algo\\Day7_Review.docx'
doc.save(output_path)
print(f"✓ Day 7 Review documentation saved to: {output_path}")
