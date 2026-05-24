"""
Create Day 4 Word Document for DSA Study Plan
Topic: Stack & Queue Data Structures
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


def create_day4_document():
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # Title
    title = doc.add_heading('Day 4: Stack & Queue', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle
    subtitle = doc.add_paragraph('LIFO, FIFO, Monotonic Stack, and BFS Applications')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True

    # Date and info
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.add_run('📅 April 1, 2026').bold = True
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
        "Day 4 introduces two fundamental linear data structures: stacks and queues. These structures "
        "form the backbone of many algorithms and are essential for understanding more complex topics "
        "like tree traversal, graph algorithms, and dynamic programming."
    )

    doc.add_paragraph(
        "Stacks follow LIFO (Last In, First Out) ordering, making them perfect for backtracking, "
        "expression evaluation, and undo mechanisms. Queues follow FIFO (First In, First Out) ordering, "
        "enabling breadth-first search, level-order traversal, and task scheduling."
    )

    # ============================================================================
    # CORE TECHNIQUES
    # ============================================================================
    doc.add_heading('Core Techniques', level=1)

    # 1. Stack Operations
    doc.add_heading('1. Stack Operations and Applications', level=2)

    doc.add_paragraph(
        "A stack is a linear data structure that follows the Last In, First Out (LIFO) principle. "
        "The last element added is the first one to be removed."
    )

    doc.add_paragraph('Basic Operations:', style='Heading 3')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('push(x):').bold = True
    p.add_run(' Add element to top - O(1)')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('pop():').bold = True
    p.add_run(' Remove top element - O(1)')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('peek()/top():').bold = True
    p.add_run(' View top element - O(1)')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('is_empty():').bold = True
    p.add_run(' Check if stack is empty - O(1)')

    doc.add_paragraph('Applications:', style='Heading 3')
    doc.add_paragraph(
        "Function call stack, undo mechanisms, expression evaluation, backtracking algorithms, "
        "parentheses matching, depth-first search.", style='List Bullet'
    )

    doc.add_paragraph()

    # Code example: Valid Parentheses (Python)
    doc.add_paragraph('Code Example: Valid Parentheses (Python)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''def is_valid(s: str) -> bool:
    """Check if parentheses string is valid."""
    bracket_map = {')': '(', '}': '{', ']': '['}
    stack = []

    for char in s:
        if char in bracket_map:
            # Closing bracket - check if matches top
            top_element = stack.pop() if stack else '#'
            if bracket_map[char] != top_element:
                return False
        else:
            # Opening bracket - push to stack
            stack.append(char)

    # Valid if stack is empty
    return not stack

# Test cases
print(is_valid("()"))        # True
print(is_valid("()[]{}"))    # True
print(is_valid("(]"))        # False
print(is_valid("([)]"))      # False
print(is_valid("{[]}"))      # True''').font.name = 'Consolas'

    # Code example: Valid Parentheses (Rust)
    doc.add_paragraph('Code Example: Valid Parentheses (Rust)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''fn is_valid(s: &str) -> bool {
    let mut stack: Vec<char> = Vec::new();
    let bracket_map: HashMap<char, char> = [
        (')', '('),
        ('}', '{'),
        (']', '['),
    ].iter().cloned().collect();

    for c in s.chars() {
        if let Some(&opening) = bracket_map.get(&c) {
            // Closing bracket
            if stack.pop() != Some(opening) {
                return false;
            }
        } else {
            // Opening bracket
            stack.push(c);
        }
    }

    stack.is_empty()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_parentheses() {
        assert_eq!(is_valid("()"), true);
        assert_eq!(is_valid("()[]{}"), true);
        assert_eq!(is_valid("(]"), false);
        assert_eq!(is_valid("([)]"), false);
        assert_eq!(is_valid("{[]}"), true);
    }
}''').font.name = 'Consolas'

    doc.add_paragraph()

    # 2. Queue Operations
    doc.add_heading('2. Queue Operations and Applications', level=2)

    doc.add_paragraph(
        "A queue is a linear data structure that follows the First In, First Out (FIFO) principle. "
        "The first element added is the first one to be removed."
    )

    doc.add_paragraph('Basic Operations:', style='Heading 3')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('enqueue(x):').bold = True
    p.add_run(' Add element to rear - O(1)')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('dequeue():').bold = True
    p.add_run(' Remove front element - O(1)')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('front():').bold = True
    p.add_run(' View front element - O(1)')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('is_empty():').bold = True
    p.add_run(' Check if queue is empty - O(1)')

    doc.add_paragraph('Applications:', style='Heading 3')
    doc.add_paragraph(
        "BFS traversal, level-order traversal, task scheduling, buffer management, printer queues, "
        "breadth-first graph algorithms.", style='List Bullet'
    )

    doc.add_paragraph()

    # 3. Monotonic Stack Patterns
    doc.add_heading('3. Monotonic Stack Patterns', level=2)

    doc.add_paragraph(
        "A monotonic stack maintains elements in either increasing or decreasing order. This powerful "
        "technique solves problems involving next greater/smaller elements efficiently."
    )

    # Table for monotonic stack patterns
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    header_cells = table.rows[0].cells
    header_cells[0].text = 'Pattern'
    header_cells[1].text = 'Description'
    header_cells[2].text = 'Applications'

    for cell in header_cells:
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    data = [
        ('Next Greater Element', 'Find next greater element for each item', 'Stock span, temperature problems'),
        ('Daily Temperatures', 'Find distance to next greater element', 'Wait time calculations'),
        ('Largest Rectangle', 'Find max area in histogram', 'Maximal rectangle in matrix'),
    ]

    for pattern, desc, app in data:
        row = table.add_row()
        row.cells[0].text = pattern
        row.cells[1].text = desc
        row.cells[2].text = app

    doc.add_paragraph()

    doc.add_paragraph('Key Insight:', style='Heading 3')
    doc.add_paragraph(
        "For next greater element problems, use a decreasing stack. Elements wait in the stack until "
        "a greater element is found, at which point we've found the answer for the waiting element.",
        style='Intense Quote'
    )

    doc.add_paragraph('Code Example: Daily Temperatures (Python)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''def daily_temperatures(temperatures: list[int]) -> list[int]:
    """Find how many days until warmer temperature for each day."""
    n = len(temperatures)
    result = [0] * n
    stack = []  # Store indices

    for i in range(n):
        # While current temperature is warmer than stack top
        while stack and temperatures[i] > temperatures[stack[-1]]:
            idx = stack.pop()
            result[idx] = i - idx  # Calculate waiting days
        stack.append(i)

    return result

# Test
temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(daily_temperatures(temps))  # [1, 1, 4, 2, 1, 1, 0, 0]''').font.name = 'Consolas'

    doc.add_paragraph()

    # 4. BFS Applications
    doc.add_heading('4. BFS (Breadth-First Search) Applications', level=2)

    doc.add_paragraph(
        "BFS uses a queue to explore nodes level by level. It's essential for finding shortest paths "
        "in unweighted graphs and trees."
    )

    doc.add_paragraph('BFS Patterns:', style='Heading 3')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Level-Order Traversal:').bold = True
    p.add_run(' Process tree nodes level by level')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Shortest Path (Unweighted):').bold = True
    p.add_run(' Find minimum steps in grid/graph')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Multi-Source BFS:').bold = True
    p.add_run(' Start from multiple sources simultaneously')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Connected Components:').bold = True
    p.add_run(' Count islands, regions, clusters')

    doc.add_paragraph('Code Example: Number of Islands (Python)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''def num_islands(grid: list[list[str]]) -> int:
    """Count number of islands in 2D grid ('1' = land, '0' = water)."""
    from collections import deque

    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def bfs(r: int, c: int) -> None:
        """Mark entire island using BFS."""
        queue = deque([(r, c)])
        grid[r][c] = '0'  # Mark as visited

        while queue:
            row, col = queue.popleft()

            # Check all 4 directions
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'  # Mark as visited
                    queue.append((nr, nc))

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                count += 1
                bfs(i, j)

    return count

# Test
grid = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"],
]
print(num_islands(grid))  # 3''').font.name = 'Consolas'

    doc.add_paragraph()

    # ============================================================================
    # ESSENTIAL PROBLEMS
    # ============================================================================
    doc.add_heading('Essential Problems', level=1)

    problems = [
        {
            'title': 'Valid Parentheses',
            'difficulty': 'Easy',
            'pattern': 'Stack-based Validation',
            'problem': 'Given a string of parentheses, determine if it is valid.',
            'example': '"()[]{}" → True, "(]" → False',
            'solution': 'Use stack to track opening brackets. For each closing bracket, check if it matches top of stack. Valid if stack empty at end. O(n) time, O(n) space.'
        },
        {
            'title': 'Min Stack',
            'difficulty': 'Medium',
            'pattern': 'Two-Stack Design',
            'problem': 'Design a stack that supports push, pop, top, and retrieving minimum in O(1).',
            'example': 'push(-2), push(0), push(-3), getMin() → -3',
            'solution': 'Use two stacks: main stack for values, min_stack for tracking minimums. When pushing, also push to min_stack if value ≤ current min. O(1) for all operations.'
        },
        {
            'title': 'Evaluate Reverse Polish Notation',
            'difficulty': 'Medium',
            'pattern': 'Stack-based Expression Evaluation',
            'problem': 'Evaluate arithmetic expression in Reverse Polish Notation.',
            'example': '["2", "1", "+", "3", "*"] → 9  ((2+1)*3)',
            'solution': 'Push numbers onto stack. When operator encountered, pop two operands, compute, push result. O(n) time, O(n) space.'
        },
        {
            'title': 'Daily Temperatures',
            'difficulty': 'Medium',
            'pattern': 'Monotonic Decreasing Stack',
            'problem': 'For each day, find how many days until warmer temperature.',
            'example': '[73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0]',
            'solution': 'Use decreasing stack storing indices. When current > stack top, pop and calculate waiting days. O(n) time, O(n) space.'
        },
        {
            'title': 'Largest Rectangle in Histogram',
            'difficulty': 'Hard',
            'pattern': 'Monotonic Increasing Stack',
            'problem': 'Find largest rectangle in histogram.',
            'example': 'heights = [2,1,5,6,2,3] → 10',
            'solution': 'Use increasing stack. When current < stack top, pop and calculate area with popped height. Width = current index - new stack top - 1. O(n) time, O(n) space.'
        },
        {
            'title': 'Number of Islands',
            'difficulty': 'Medium',
            'pattern': 'BFS/DFS for Connected Components',
            'problem': 'Count number of islands in 2D grid.',
            'example': 'grid with 3 separate land masses → 3',
            'solution': 'Iterate grid, when find \'1\', increment count and use BFS/DFS to mark entire island. O(m*n) time, O(min(m,n)) space for BFS.'
        },
        {
            'title': 'Rotting Oranges',
            'difficulty': 'Medium',
            'pattern': 'Multi-Source BFS',
            'problem': 'Find minimum minutes until no fresh oranges left.',
            'example': 'grid with rotten and fresh oranges → 4 minutes',
            'solution': 'Add all rotten oranges to queue initially. Process level by level (each level = 1 minute). Track fresh count. O(m*n) time, O(m*n) space.'
        },
        {
            'title': 'Word Ladder',
            'difficulty': 'Hard',
            'pattern': 'BFS on Transformation Graph',
            'problem': 'Find shortest transformation sequence between words.',
            'example': 'hit → cog with word_list → 5 steps',
            'solution': 'Build adjacency list using generic intermediate states. BFS from begin_word. O(N*M²) where N=words, M=length. O(N*M²) space.'
        }
    ]

    for prob in problems:
        doc.add_heading(prob['title'], level=3)

        p = doc.add_paragraph()
        p.add_run('Difficulty: ').bold = True
        p.add_run(prob['difficulty'])

        p = doc.add_paragraph()
        p.add_run('Pattern: ').bold = True
        p.add_run(prob['pattern'])

        p = doc.add_paragraph()
        p.add_run('Problem: ').bold = True
        p.add_run(prob['problem'])

        p = doc.add_paragraph()
        p.add_run('Example: ').bold = True
        p.add_run(prob['example'])

        p = doc.add_paragraph()
        p.add_run('Solution: ').bold = True
        p.add_run(prob['solution'])

        doc.add_paragraph()

    # ============================================================================
    # COMPLEXITY COMPARISON
    # ============================================================================
    doc.add_heading('Complexity Comparison', level=1)

    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    header_cells = table.rows[0].cells
    header_cells[0].text = 'Algorithm/Pattern'
    header_cells[1].text = 'Time Complexity'
    header_cells[2].text = 'Space Complexity'

    for cell in header_cells:
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    complexity_data = [
        ('Stack Operations (push/pop/peek)', 'O(1)', 'O(1)'),
        ('Queue Operations (enqueue/dequeue)', 'O(1)', 'O(1)'),
        ('Valid Parentheses', 'O(n)', 'O(n)'),
        ('Min Stack', 'O(1) all ops', 'O(n)'),
        ('Evaluate RPN', 'O(n)', 'O(n)'),
        ('Next Greater Element', 'O(n)', 'O(n)'),
        ('Daily Temperatures', 'O(n)', 'O(n)'),
        ('Largest Rectangle in Histogram', 'O(n)', 'O(n)'),
        ('Number of Islands (BFS)', 'O(m*n)', 'O(min(m,n))'),
        ('Rotting Oranges', 'O(m*n)', 'O(m*n)'),
        ('Word Ladder', 'O(N*M²)', 'O(N*M²)'),
    ]

    for algo, time, space in complexity_data:
        row = table.add_row()
        row.cells[0].text = algo
        row.cells[1].text = time
        row.cells[2].text = space

    doc.add_paragraph()

    # ============================================================================
    # KEY INSIGHTS
    # ============================================================================
    doc.add_heading('Key Insights', level=1)

    insights = [
        ('LIFO vs FIFO:', 'Stack (LIFO) for backtracking/undo; Queue (FIFO) for level-order/BFS'),
        ('Monotonic Stack:', 'Decreasing stack for next greater element; Increasing stack for largest rectangle'),
        ('Two-Stack Min:', 'Track minimum with auxiliary stack that mirrors minimums at each level'),
        ('BFS Level Processing:', 'Track queue size at start of each level to process level by level'),
        ('Multi-Source BFS:', 'Add all sources to queue initially for simultaneous expansion'),
        ('Circular Queue:', 'Use count variable to distinguish full vs empty states'),
        ('RPN Evaluation:', 'Operators come after operands; stack naturally handles order of operations'),
        ('Island Problems:', 'Mark visited cells to avoid counting same island multiple times'),
    ]

    for insight, desc in insights:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(insight).bold = True
        p.add_run(desc)

    doc.add_paragraph()

    # ============================================================================
    # HOMEWORK
    # ============================================================================
    doc.add_heading('Practice Problems (Homework)', level=1)

    doc.add_heading('Easy Problems', level=2)
    easy_problems = [
        'Valid Parentheses - Stack-based bracket matching',
        'Implement Stack using Arrays - Basic LIFO operations',
        'Implement Queue using Arrays - Basic FIFO operations',
        'Number of Islands - BFS/DFS for connected components',
        'Reverse String - Stack-based reversal',
    ]
    for prob in easy_problems:
        doc.add_paragraph(prob, style='List Bullet')

    doc.add_heading('Medium Problems', level=2)
    medium_problems = [
        'Min Stack - Track minimum in O(1)',
        'Evaluate Reverse Polish Notation - Stack-based expression evaluation',
        'Daily Temperatures - Monotonic stack for next greater',
        'Find First and Last Position in Sorted Array - Binary search variant',
        'Rotting Oranges - Multi-source BFS',
        'Level Order Traversal - Queue-based tree traversal',
    ]
    for prob in medium_problems:
        doc.add_paragraph(prob, style='List Bullet')

    doc.add_heading('Hard Problems', level=2)
    hard_problems = [
        'Largest Rectangle in Histogram - Monotonic stack for max area',
        'Maximal Rectangle - Build histograms row by row',
        'Word Ladder - BFS on word transformation graph',
        'Sliding Window Maximum - Monotonic deque for window max',
        'Binary Tree Maximum Path Sum - DFS with stack tracking',
    ]
    for prob in hard_problems:
        doc.add_paragraph(prob, style='List Bullet')

    doc.add_paragraph()

    # ============================================================================
    # RESOURCES
    # ============================================================================
    doc.add_heading('Resources', level=1)

    doc.add_paragraph('Code Files:', style='Heading 3')
    doc.add_paragraph('• Python: python_projects/day4_stack_queue.py', style='List Bullet')
    doc.add_paragraph('• Rust: rust_projects/day4_stack_queue.rs', style='List Bullet')
    doc.add_paragraph('• Cargo Project: rust_projects/day4_stack_queue/', style='List Bullet')

    doc.add_paragraph('Run Commands:', style='Heading 3')
    doc.add_paragraph('• Python: cd python_projects && python day4_stack_queue.py', style='List Bullet')
    doc.add_paragraph('• Rust: cd rust_projects/day4_stack_queue && cargo test', style='List Bullet')

    # Save document
    doc.save('Day4_Stack_Queue.docx')
    print("Day 4 Word document created successfully!")


if __name__ == '__main__':
    create_day4_document()
