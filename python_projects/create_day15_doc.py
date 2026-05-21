"""
Script to create Day 15 Heaps, Tries, and Bit Manipulation documentation using python-docx.
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
title = doc.add_heading('Day 15: Heaps, Tries, & Bit Manipulation', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph('Priority Queues, Prefix Trees, and Bitwise Operations', style='Subtitle')
doc.add_paragraph()

# Overview
doc.add_heading('Overview', level=1)
doc.add_paragraph(
    'Today we cover three powerful data structures and techniques: Heaps (Priority Queues) for efficient '
    'extremum retrieval, Tries for prefix-based string operations, and Bit Manipulation for space-efficient '
    'computations. These patterns are essential for competitive programming and technical interviews.'
)

doc.add_heading('Topics Covered', level=2)
topics = [
    'Heaps & Priority Queues (min-heap, max-heap, heapify, heap operations)',
    'Top K Elements Pattern (frequency counting, streaming data)',
    'Merge K Sorted Lists (heap-based merging)',
    'Trie Data Structure (insert, search, prefix operations)',
    'Word Search & Autocomplete with Tries',
    'Bit Manipulation Fundamentals (AND, OR, XOR, shifts, masks)',
    'Bit Manipulation Applications (single number, counting bits, power of two)'
]
for topic in topics:
    doc.add_paragraph(topic, style='List Bullet')

# Section 1: Heaps & Priority Queues
doc.add_heading('1. Heaps & Priority Queues', level=1)

doc.add_heading('1.1 Conceptual Foundation', level=2)
doc.add_paragraph(
    'A heap is a specialized tree-based data structure that satisfies the heap property. In a min-heap, '
    'for any node i, the value of i is less than or equal to its children\'s values. In a max-heap, the '
    'opposite holds. Heaps are commonly used to implement priority queues, where we need efficient access '
    'to the minimum or maximum element.'
)

doc.add_paragraph('Key Properties:', style='Heading 4')
doc.add_paragraph('Complete binary tree (filled left to right)', style='List Bullet')
doc.add_paragraph('Min-heap: parent <= children; Max-heap: parent >= children', style='List Bullet')
doc.add_paragraph('Array representation: children of index i are at 2i+1 and 2i+2', style='List Bullet')
doc.add_paragraph('Root is always the minimum (min-heap) or maximum (max-heap)', style='List Bullet')

doc.add_heading('1.2 Time Complexities', level=2)

# Complexity table
table = doc.add_table(rows=6, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['Operation', 'Time Complexity', 'Space Complexity']
operations = [
    ['Push/Insert', 'O(log n)', 'O(n)'],
    ['Pop/Extract', 'O(log n)', 'O(1)'],
    ['Peek/Top', 'O(1)', 'O(1)'],
    ['Heapify', 'O(n)', 'O(1)'],
    ['Search', 'O(n)', 'O(1)']
]

for i, header in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.style.font.bold = True

for i, row_data in enumerate(operations):
    for j, cell_data in enumerate(row_data):
        table.rows[i + 1].cells[j].text = cell_data

doc.add_paragraph()

doc.add_heading('1.3 Common Patterns', level=2)

doc.add_heading('Pattern 1: Top K Frequent Elements', level=3)
doc.add_paragraph(
    'Problem: Given an array, find the k most frequent elements. Use a min-heap of size k to track '
    'the top k elements while iterating through frequencies. When heap size exceeds k, remove the '
    'minimum (least frequent). This gives O(n log k) time instead of O(n log n) for full sorting.'
)

doc.add_heading('Pattern 2: Merge K Sorted Lists', level=3)
doc.add_paragraph(
    'Problem: Merge k sorted linked lists into one sorted list. Use a min-heap of size k, initially '
    'containing the first element of each list. Extract minimum and insert next element from the same '
    'list. Time: O(n log k) where n is total elements and k is number of lists.'
)

doc.add_heading('Pattern 3: Find Median from Data Stream', level=3)
doc.add_paragraph(
    'Problem: Design a data structure that supports addNum and findMedian. Maintain two heaps: a max-heap '
    'for the lower half and a min-heap for the upper half. Balance sizes to ensure efficient median '
    'retrieval. Median is either top of one heap (odd count) or average of both tops (even count).'
)

# Section 2: Trie Data Structure
doc.add_heading('2. Trie (Prefix Tree)', level=1)

doc.add_heading('2.1 Conceptual Foundation', level=2)
doc.add_paragraph(
    'A trie, also called a prefix tree, is a tree-like data structure used to store a dynamic set of '
    'strings. Each node represents a character, and paths from root to nodes represent prefixes. Tries '
    'are particularly efficient for string operations like autocomplete, spell checking, and IP routing.'
)

doc.add_paragraph('Key Properties:', style='Heading 4')
doc.add_paragraph('Root represents empty string', style='List Bullet')
doc.add_paragraph('Each edge represents a character', style='List Bullet')
doc.add_paragraph('Nodes may have multiple children (one per character)', style='List Bullet')
doc.add_paragraph('Special marker indicates end of word', style='List Bullet')
doc.add_paragraph('Common prefixes share the same path', style='List Bullet')

doc.add_heading('2.2 Time Complexities', level=2)

# Trie complexity table
table2 = doc.add_table(rows=5, cols=3)
table2.alignment = WD_TABLE_ALIGNMENT.CENTER
headers2 = ['Operation', 'Time Complexity', 'Space Complexity']
trie_ops = [
    ['Insert', 'O(m)', 'O(m * n)'],
    ['Search', 'O(m)', 'O(1)'],
    ['StartsWith', 'O(m)', 'O(1)'],
    ['Delete', 'O(m)', 'O(1)']
]

for i, header in enumerate(headers2):
    cell = table2.rows[0].cells[i]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.style.font.bold = True

for i, row_data in enumerate(trie_ops):
    for j, cell_data in enumerate(row_data):
        table2.rows[i + 1].cells[j].text = cell_data

doc.add_paragraph()
doc.add_paragraph('Where m = word length, n = number of words', style='Quote')

doc.add_heading('2.3 Common Patterns', level=2)

doc.add_heading('Pattern 1: Autocomplete System', level=3)
doc.add_paragraph(
    'Use trie to store dictionary words. For autocomplete, traverse to the prefix node, then perform '
    'DFS to collect all words with that prefix. Combine with frequency tracking for ranking suggestions.'
)

doc.add_heading('Pattern 2: Word Search on Board', level=3)
doc.add_paragraph(
    'Given a 2D board and a list of words, find all words that can be formed. Build trie from word list, '
    'then DFS from each cell, following trie edges. Mark visited cells to avoid reuse.'
)

doc.add_heading('Pattern 3: Longest Common Prefix', level=3)
doc.add_paragraph(
    'Insert all strings into trie, then traverse from root following the path where all strings share '
    'characters. Stop at first branching point or word end.'
)

# Section 3: Bit Manipulation
doc.add_heading('3. Bit Manipulation', level=1)

doc.add_heading('3.1 Conceptual Foundation', level=2)
doc.add_paragraph(
    'Bit manipulation involves working directly with binary representations of integers. Understanding '
    'bitwise operations enables efficient solutions to problems involving sets, subsets, and mathematical '
    'properties. Many bit manipulation solutions achieve O(1) space and O(n) time complexity.'
)

doc.add_paragraph('Basic Operations:', style='Heading 4')
doc.add_paragraph('AND (&): 1 if both bits are 1', style='List Bullet')
doc.add_paragraph('OR (|): 1 if at least one bit is 1', style='List Bullet')
doc.add_paragraph('XOR (^): 1 if bits are different (commutative, associative)', style='List Bullet')
doc.add_paragraph('NOT (~): Flips all bits', style='List Bullet')
doc.add_paragraph('Left Shift (<<): Multiply by 2', style='List Bullet')
doc.add_paragraph('Right Shift (>>): Divide by 2', style='List Bullet')

doc.add_heading('3.2 Key Bit Manipulation Tricks', level=2)

tricks = [
    'Check if power of 2: n > 0 and (n & (n - 1)) == 0',
    'Get bit at position i: (n >> i) & 1',
    'Set bit at position i: n | (1 << i)',
    'Clear bit at position i: n & ~(1 << i)',
    'Toggle bit at position i: n ^ (1 << i)',
    'XOR of same number is 0: n ^ n = 0',
    'XOR with 0 is identity: n ^ 0 = n',
    'Count set bits: n & (n - 1) clears lowest set bit',
    'Swap without temp: a ^= b; b ^= a; a ^= b',
    'Get lowest set bit: n & (-n)'
]

for i, trick in enumerate(tricks, 1):
    doc.add_paragraph(f'{i}. {trick}')

doc.add_heading('3.3 Common Patterns', level=2)

doc.add_heading('Pattern 1: Single Number (XOR)', level=3)
doc.add_paragraph(
    'Problem: Given array where every element appears twice except one, find the single element. '
    'XOR all elements: duplicates cancel out, leaving only the unique element. Time: O(n), Space: O(1).'
)

doc.add_heading('Pattern 2: Counting Bits', level=3)
doc.add_paragraph(
    'Problem: For each number from 0 to n, count the number of 1-bits. Use dynamic programming: '
    'bits[i] = bits[i >> 1] + (i & 1) or bits[i] = bits[i & (i-1)] + 1. Time: O(n), Space: O(n).'
)

doc.add_heading('Pattern 3: Subsets with Bitmask', level=3)
doc.add_paragraph(
    'Problem: Generate all subsets of a set. Use integers from 0 to 2^n - 1 as bitmasks, where bit i '
    'indicates whether element i is in the subset. Time: O(2^n), Space: O(1) auxiliary.'
)

# Practice Problems
doc.add_heading('4. Practice Problems', level=1)

doc.add_heading('4.1 Heap Problems', level=2)
heap_problems = [
    'Top K Frequent Elements: Use min-heap of size k to track most frequent',
    'Kth Largest Element in Array: Use min-heap or quickselect',
    'Merge K Sorted Lists: Use min-heap to merge efficiently',
    'Find Median from Data Stream: Use two heaps (max-heap and min-heap)',
    'Sliding Window Maximum: Use deque or heap with lazy removal'
]
for prob in heap_problems:
    doc.add_paragraph(prob, style='List Bullet')

doc.add_heading('4.2 Trie Problems', level=2)
trie_problems = [
    'Implement Trie: Insert, search, and prefix operations',
    'Word Search II: Find all words from dictionary on board',
    'Longest Word in Dictionary: Find longest buildable word',
    'Map Sum Pairs: Trie with value aggregation',
    'Design Add and Search Words: Wildcard search with trie'
]
for prob in trie_problems:
    doc.add_paragraph(prob, style='List Bullet')

doc.add_heading('4.3 Bit Manipulation Problems', level=2)
bit_problems = [
    'Single Number: XOR all elements to find unique',
    'Number of 1 Bits: Count set bits (Hamming weight)',
    'Counting Bits: DP with bit manipulation',
    'Reverse Bits: Bit reversal with shifts',
    'Power of Two: Check with n & (n-1)',
    'Sum of Two Integers: Addition using only XOR and AND'
]
for prob in bit_problems:
    doc.add_paragraph(prob, style='List Bullet')

# Key Takeaways
doc.add_heading('5. Key Takeaways', level=1)

takeaways = [
    'Heaps provide O(log n) insertion and extraction of min/max, ideal for priority-based processing',
    'Top K problems benefit from heaps of size k instead of full sorting',
    'Two heaps (max-heap + min-heap) efficiently solve median-finding and range problems',
    'Tries excel at prefix operations and string set membership queries',
    'Bit manipulation enables O(1) space solutions for subset and uniqueness problems',
    'XOR properties (n ^ n = 0, n ^ 0 = n) are powerful for cancellation-based solutions',
    'Bitmasks represent subsets compactly when n is small (n ≤ 20-25)',
    'Understanding time/space tradeoffs is crucial: heaps for streaming, tries for prefix queries, bits for compactness'
]

for i, takeaway in enumerate(takeaways, 1):
    doc.add_paragraph(f'{i}. {takeaway}')

# Complexity Summary
doc.add_heading('6. Complexity Summary', level=1)

table3 = doc.add_table(rows=8, cols=4)
table3.alignment = WD_TABLE_ALIGNMENT.CENTER
headers3 = ['Data Structure', 'Operation', 'Time', 'Space']
summary_data = [
    ['Min-Heap', 'Push/Pop', 'O(log n)', 'O(n)'],
    ['Min-Heap', 'Heapify', 'O(n)', 'O(1)'],
    ['Trie', 'Insert/Search', 'O(m)', 'O(m * n)'],
    ['Bit Manipulation', 'Single Ops', 'O(1)', 'O(1)'],
    ['Bit Manipulation', 'Count Bits', 'O(1)', 'O(1)'],
    ['Bitmask', 'Generate Subsets', 'O(2^n)', 'O(1) aux'],
    ['Two Heaps', 'Find Median', 'O(1)', 'O(n)']
]

for i, header in enumerate(headers3):
    cell = table3.rows[0].cells[i]
    cell.text = header
    for paragraph in cell.paragraphs:
        paragraph.style.font.bold = True

for i, row_data in enumerate(summary_data):
    for j, cell_data in enumerate(row_data):
        table3.rows[i + 1].cells[j].text = cell_data

doc.add_paragraph()
doc.add_paragraph('Where m = key length, n = number of keys/elements', style='Quote')

# Save
output_path = 'C:/Users/puppets/Documents/ds_and_algo/Day15_Heaps_Tries_Bits.docx'
doc.save(output_path)
print(f"Document saved to {output_path}")
