"""
Script to update Day 2 Word document to include both Python and Rust implementations.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def update_day2_document():
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)
    
    # Title
    title = doc.add_heading('Day 2: Advanced Array Manipulation', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Subtitle
    subtitle = doc.add_paragraph('Arrays & Hashing - Core Techniques Deep Dive')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True
    
    doc.add_paragraph()
    
    # Language note
    lang_note = doc.add_paragraph()
    lang_note.add_run('Available Implementations: ').bold = True
    lang_note.add_run('Python (day2_advanced_arrays.py) ')
    lang_note.add_run('& ').bold = False
    lang_note.add_run('Rust (day2_advanced_arrays.rs)')
    lang_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # Table of Contents
    doc.add_heading('Table of Contents', level=1)
    toc = [
        '1. Topic Overview',
        '2. Conceptual Foundation',
        '3. Core Techniques',
        '   - 3.1 Two-Pointer Technique',
        '   - 3.2 Sliding Window Approach',
        '   - 3.3 Prefix Sum Method',
        '   - 3.4 Hash Map Applications',
        '4. Essential Problems with Solutions',
        '5. Key Insights & Patterns',
        '6. Practice Problems (Homework)',
        '7. Language-Specific Implementation Notes',
        '8. Summary & Next Steps'
    ]
    for item in toc:
        doc.add_paragraph(item, style='List Bullet')
    
    # Section 1: Topic Overview
    doc.add_heading('1. Topic Overview', level=1)
    doc.add_paragraph(
        "Day 2 builds upon the foundational concepts from Day 1, diving deeper into advanced "
        "array manipulation techniques. These patterns form the backbone of efficient algorithm "
        "design and appear frequently in technical interviews and competitive programming."
    )
    doc.add_paragraph(
        "Today's focus is on mastering four critical techniques that transform seemingly complex "
        "problems into elegant, efficient solutions:"
    )
    
    techniques_list = [
        ('Two-Pointer Technique', 'O(n) solutions for pair-finding and partitioning problems'),
        ('Sliding Window Approach', 'Efficient subarray/substring analysis without recomputation'),
        ('Prefix Sum Method', 'O(1) range queries and cumulative calculations'),
        ('Hash Map Applications', 'Frequency counting and complement-based lookups')
    ]
    
    for technique, description in techniques_list:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(technique).bold = True
        p.add_run(f': {description}')
    
    # Section 2: Conceptual Foundation
    doc.add_heading('2. Conceptual Foundation', level=1)
    
    doc.add_heading('Why These Techniques Matter', level=2)
    doc.add_paragraph(
        "Arrays provide O(1) random access, but naive solutions often result in O(n²) or O(n³) "
        "time complexity. The techniques we study today exploit array properties to achieve "
        "linear or near-linear time complexity through:"
    )
    
    doc.add_paragraph('Single-pass processing: Visit each element at most twice', style='List Bullet')
    doc.add_paragraph('Space-time tradeoffs: Use auxiliary space to avoid recomputation', style='List Bullet')
    doc.add_paragraph('Incremental computation: Build solutions progressively', style='List Bullet')
    doc.add_paragraph('Constraint exploitation: Leverage sorted order or value ranges', style='List Bullet')
    
    doc.add_heading('Complexity Comparison', level=2)
    
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    
    # Header row
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Approach'
    header_cells[1].text = 'Time Complexity'
    header_cells[2].text = 'Space Complexity'
    
    # Make header bold
    for cell in header_cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
    
    # Data rows
    data = [
        ('Brute Force (Nested Loops)', 'O(n²)', 'O(1)'),
        ('Two-Pointer', 'O(n)', 'O(1)'),
        ('Sliding Window', 'O(n)', 'O(1) or O(k)'),
        ('Prefix Sum', 'O(n) preprocessing, O(1) query', 'O(n)'),
        ('Hash Map', 'O(n) average', 'O(n)')
    ]
    
    for approach, time, space in data:
        row = table.add_row()
        row.cells[0].text = approach
        row.cells[1].text = time
        row.cells[2].text = space
    
    # Section 3: Core Techniques
    doc.add_heading('3. Core Techniques', level=1)
    
    # 3.1 Two-Pointer Technique
    doc.add_heading('3.1 Two-Pointer Technique', level=2)
    
    doc.add_paragraph(
        "The two-pointer technique uses two indices that traverse the array in coordination "
        "to solve problems in a single pass. This eliminates the need for nested loops."
    )
    
    doc.add_heading('Pattern Variations:', level=3)
    
    doc.add_paragraph('Opposite Direction (Converging Pointers)', style='List Bullet')
    doc.add_paragraph(
        "   - Left pointer starts at beginning, right pointer at end\n"
        "   - Move pointers toward each other based on condition\n"
        "   - Applications: Two Sum (sorted), palindrome checking, container with most water",
        style='List Bullet'
    )
    
    doc.add_paragraph('Same Direction (Fast-Slow Pointers)', style='List Bullet')
    doc.add_paragraph(
        "   - Both pointers move left to right\n"
        "   - Fast pointer scans ahead, slow pointer tracks result\n"
        "   - Applications: Remove duplicates, find middle element, cycle detection",
        style='List Bullet'
    )
    
    doc.add_paragraph('Three-Way Partitioning', style='List Bullet')
    doc.add_paragraph(
        "   - Maintains three regions: less than, equal to, greater than pivot\n"
        "   - Dutch National Flag problem\n"
        "   - Applications: Sort colors, partition around pivot",
        style='List Bullet'
    )
    
    doc.add_heading('Example: Two Sum (Sorted Array)', level=3)
    doc.add_paragraph(
        "Problem: Given a sorted array and target, find two numbers that add to target.\n\n"
        "Algorithm:\n"
        "1. Initialize left=0, right=n-1\n"
        "2. While left < right:\n"
        "   - Calculate sum = nums[left] + nums[right]\n"
        "   - If sum == target: return indices\n"
        "   - If sum < target: left++ (need larger sum)\n"
        "   - If sum > target: right-- (need smaller sum)\n\n"
        "Why it works: Sorted order guarantees that moving left increases sum, "
        "moving right decreases sum."
    )
    
    # 3.2 Sliding Window Approach
    doc.add_heading('3.2 Sliding Window Approach', level=2)
    
    doc.add_paragraph(
        "The sliding window technique maintains a contiguous subarray (window) that slides "
        "through the array, updating the solution incrementally rather than recomputing from scratch."
    )
    
    doc.add_heading('Pattern Variations:', level=3)
    
    doc.add_paragraph('Fixed Size Window', style='List Bullet')
    doc.add_paragraph(
        "   - Window size remains constant (k elements)\n"
        "   - Slide by adding new element, removing oldest\n"
        "   - Applications: Maximum average subarray, moving averages",
        style='List Bullet'
    )
    
    doc.add_paragraph('Dynamic Size Window', style='List Bullet')
    doc.add_paragraph(
        "   - Window expands and contracts based on condition\n"
        "   - Expand right to satisfy condition, contract left to minimize\n"
        "   - Applications: Minimum size subarray sum, longest substring without repeats",
        style='List Bullet'
    )
    
    doc.add_heading('Example: Minimum Size Subarray Sum', level=3)
    doc.add_paragraph(
        "Problem: Find minimum length subarray with sum ≥ target.\n\n"
        "Algorithm:\n"
        "1. Initialize left=0, current_sum=0, min_length=∞\n"
        "2. For right from 0 to n-1:\n"
        "   - Add nums[right] to current_sum (expand)\n"
        "   - While current_sum ≥ target:\n"
        "     * Update min_length = min(min_length, right-left+1)\n"
        "     * Subtract nums[left] from current_sum (contract)\n"
        "     * Increment left\n"
        "3. Return min_length\n\n"
        "Key Insight: Each element is added once and removed at most once, giving O(n) time."
    )
    
    # 3.3 Prefix Sum Method
    doc.add_heading('3.3 Prefix Sum Method', level=2)
    
    doc.add_paragraph(
        "Prefix sum precomputes cumulative sums, enabling O(1) range sum queries. "
        "The technique extends to various cumulative calculations."
    )
    
    doc.add_heading('Core Concept:', level=3)
    doc.add_paragraph(
        "   - prefix[i] = sum of elements from index 0 to i-1\n"
        "   - prefix[0] = 0 (empty prefix)\n"
        "   - sum(i, j) = prefix[j+1] - prefix[i]\n\n"
        "This transforms O(n) range queries into O(1) operations after O(n) preprocessing.",
        style='List Bullet'
    )
    
    doc.add_heading('Advanced Application: Subarray Sum Equals K', level=3)
    doc.add_paragraph(
        "Problem: Count subarrays with sum equal to k.\n\n"
        "Key Insight: If prefix[j] - prefix[i] = k, then subarray nums[i..j-1] has sum k.\n\n"
        "Algorithm:\n"
        "1. Use hash map to store frequency of each prefix sum\n"
        "2. For each position, check if (current_prefix - k) exists in map\n"
        "3. Add frequency count to result\n"
        "4. Update map with current prefix sum\n\n"
        "This achieves O(n) time with O(n) space."
    )
    
    # 3.4 Hash Map Applications
    doc.add_heading('3.4 Hash Map Applications', level=2)
    
    doc.add_paragraph(
        "Hash maps provide O(1) average-case lookup, enabling efficient frequency counting, "
        "complement searches, and grouping operations."
    )
    
    doc.add_heading('Common Patterns:', level=3)
    
    doc.add_paragraph('Frequency Counting', style='List Bullet')
    doc.add_paragraph(
        "   - Track occurrence count of each element\n"
        "   - Applications: Anagrams, majority element, duplicates",
        style='List Bullet'
    )
    
    doc.add_paragraph('Complement Lookup', style='List Bullet')
    doc.add_paragraph(
        "   - Store seen elements, search for target - current\n"
        "   - Applications: Two Sum, pair finding",
        style='List Bullet'
    )
    
    doc.add_paragraph('Grouping by Key', style='List Bullet')
    doc.add_paragraph(
        "   - Use transformed value as key (e.g., sorted string for anagrams)\n"
        "   - Applications: Group anagrams, categorize by property",
        style='List Bullet'
    )
    
    # Section 4: Essential Problems
    doc.add_heading('4. Essential Problems with Solutions', level=1)
    
    problems = [
        {
            'name': 'Two Sum II (Input Array Sorted)',
            'difficulty': 'Medium',
            'pattern': 'Two-Pointer (Opposite Direction)',
            'description': 'Given sorted array and target, find two numbers adding to target.',
            'solution': 'Use converging pointers. If sum < target, move left pointer right. If sum > target, move right pointer left.',
            'complexity': 'Time: O(n), Space: O(1)'
        },
        {
            'name': 'Remove Duplicates from Sorted Array',
            'difficulty': 'Easy',
            'pattern': 'Two-Pointer (Same Direction)',
            'description': 'Remove duplicates in-place, return new length.',
            'solution': 'Slow pointer tracks unique position, fast pointer scans. When different, copy to slow+1.',
            'complexity': 'Time: O(n), Space: O(1)'
        },
        {
            'name': 'Maximum Subarray (Kadane\'s Algorithm)',
            'difficulty': 'Medium',
            'pattern': 'Prefix Sum / Dynamic Programming',
            'description': 'Find contiguous subarray with maximum sum.',
            'solution': 'At each position, decide: extend previous subarray or start new. Track global maximum.',
            'complexity': 'Time: O(n), Space: O(1)'
        },
        {
            'name': 'Longest Substring Without Repeating Characters',
            'difficulty': 'Medium',
            'pattern': 'Sliding Window with Hash Set',
            'description': 'Find length of longest substring with all unique characters.',
            'solution': 'Expand right, add to set. On duplicate, contract left until unique. Track max length.',
            'complexity': 'Time: O(n), Space: O(min(m,n))'
        },
        {
            'name': 'Product of Array Except Self',
            'difficulty': 'Medium',
            'pattern': 'Prefix Products',
            'description': 'Return array where each element is product of all other elements.',
            'solution': 'Compute left products, then right products. Multiply together for result. No division allowed.',
            'complexity': 'Time: O(n), Space: O(1) excluding output'
        },
        {
            'name': 'Trapping Rain Water',
            'difficulty': 'Hard',
            'pattern': 'Two-Pointer with Max Tracking',
            'description': 'Calculate water trapped between bars after rain.',
            'solution': 'Track max from left and right. Water at position = min(left_max, right_max) - height.',
            'complexity': 'Time: O(n), Space: O(1)'
        }
    ]
    
    for i, problem in enumerate(problems, 1):
        doc.add_heading(f'{i}. {problem["name"]}', level=2)
        
        p = doc.add_paragraph()
        p.add_run('Difficulty: ').bold = True
        p.add_run(problem['difficulty'])
        
        p = doc.add_paragraph()
        p.add_run('Pattern: ').bold = True
        p.add_run(problem['pattern'])
        
        p = doc.add_paragraph()
        p.add_run('Description: ').bold = True
        p.add_run(problem['description'])
        
        p = doc.add_paragraph()
        p.add_run('Solution Approach: ').bold = True
        p.add_run(problem['solution'])
        
        p = doc.add_paragraph()
        p.add_run('Complexity: ').bold = True
        p.add_run(problem['complexity'])
    
    # Section 5: Key Insights
    doc.add_heading('5. Key Insights & Patterns', level=1)
    
    insights = [
        ("Recognize Sorted Array Problems", "If input is sorted, consider two-pointer before hash map to achieve O(1) space."),
        ("Identify Window Properties", "Fixed window for size-k problems, dynamic window for optimization with constraints."),
        ("Prefix Sum for Range Queries", "Multiple range sum queries? Build prefix array for O(1) per query."),
        ("Hash Map for Complement", "Looking for pairs with specific sum? Store complements in hash map."),
        ("Track Extremes Incrementally", "For max/min problems, update as you traverse rather than storing all values."),
        ("Contract When Condition Violated", "In sliding window, shrink from left when constraint is broken."),
        ("Precompute for Efficiency", "Prefix sums/products trade O(n) space for O(1) query time.")
    ]
    
    for insight, explanation in insights:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(insight).bold = True
        p.add_run(f': {explanation}')
    
    # Section 6: Practice Problems
    doc.add_heading('6. Practice Problems (Homework)', level=1)
    
    doc.add_heading('Easy Problems', level=2)
    easy_problems = [
        'Best Time to Buy and Sell Stock - Track minimum price, calculate max profit',
        'Maximum Average Subarray I - Fixed size sliding window',
        'Find All Numbers Disappeared in an Array - Index marking or hash set',
        'Valid Anagram - Character frequency counting',
        'Contains Duplicate - Hash set for duplicate detection'
    ]
    for prob in easy_problems:
        doc.add_paragraph(prob, style='List Bullet')
    
    doc.add_heading('Medium Problems', level=2)
    medium_problems = [
        '3Sum - Sort + Two pointers, skip duplicates',
        'Container With Most Water - Two pointers from ends',
        'Subarray Sum Equals K - Prefix sum with hash map',
        'Longest Repeating Character Replacement - Sliding window with frequency',
        'Minimum Window Substring - Dynamic window with character counts',
        '3Sum Closest - Two pointers, track closest sum'
    ]
    for prob in medium_problems:
        doc.add_paragraph(prob, style='List Bullet')
    
    doc.add_heading('Hard Problems', level=2)
    hard_problems = [
        'Trapping Rain Water - Two pointers with max tracking',
        'Minimum Window Substring - Advanced sliding window',
        'First Missing Positive - Index marking technique',
        'Median of Two Sorted Arrays - Binary search partitioning',
        'Maximize Distance to Closest Person - Prefix/suffix tracking'
    ]
    for prob in hard_problems:
        doc.add_paragraph(prob, style='List Bullet')
    
    doc.add_heading('Homework Instructions:', level=2)
    doc.add_paragraph(
        "1. Attempt each problem for at least 20-30 minutes before looking at solutions\n"
        "2. Identify which pattern applies to each problem\n"
        "3. Write clean, well-commented code\n"
        "4. Test with edge cases: empty input, single element, all same values\n"
        "5. Analyze time and space complexity for your solution\n"
        "6. Compare your approach with optimal solutions"
    )
    
    # Section 7: Language-Specific Notes
    doc.add_heading('7. Language-Specific Implementation Notes', level=1)
    
    doc.add_heading('Python Implementation (day2_advanced_arrays.py)', level=2)
    doc.add_paragraph(
        "Python offers concise syntax and built-in data structures that make algorithm "
        "implementation straightforward. Key advantages:"
    )
    python_features = [
        'Dynamic typing - no need to declare types explicitly',
        'Built-in list comprehensions for concise code',
        'dict and set provide O(1) average lookup',
        'slice notation for easy subarray operations',
        'enumerate() for index-value iteration'
    ]
    for feature in python_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_heading('Rust Implementation (day2_advanced_arrays.rs)', level=2)
    doc.add_paragraph(
        "Rust provides memory safety without garbage collection and excellent performance. "
        "Key considerations:"
    )
    rust_features = [
        'Static typing with type inference (let mut x = 0)',
        'Ownership and borrowing for memory safety',
        'HashMap and HashSet from std::collections',
        'Pattern matching with match expressions',
        'Option<T> for nullable values (no null)',
        'Vec<T> for dynamic arrays',
        'Built-in testing framework with #[test]'
    ]
    for feature in rust_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_heading('When to Use Each Language:', level=2)
    
    comparison_table = doc.add_table(rows=1, cols=3)
    comparison_table.style = 'Table Grid'
    
    # Header
    headers = ['Aspect', 'Python', 'Rust']
    for i, header in enumerate(headers):
        comparison_table.rows[0].cells[i].text = header
        for paragraph in comparison_table.rows[0].cells[i].paragraphs:
            for run in paragraph.runs:
                run.bold = True
    
    # Data
    comparisons = [
        ('Learning Curve', 'Easier for beginners', 'Steeper (ownership concepts)'),
        ('Execution Speed', 'Slower (interpreted)', 'Very fast (compiled)'),
        ('Memory Safety', 'Garbage collected', 'Compile-time guarantees'),
        ('Interview Use', 'Commonly accepted', 'Growing popularity'),
        ('Production Use', 'Data science, scripting', 'Systems programming'),
        ('Code Length', 'More concise', 'More verbose but explicit')
    ]
    
    for aspect, python, rust in comparisons:
        row = comparison_table.add_row()
        row.cells[0].text = aspect
        row.cells[1].text = python
        row.cells[2].text = rust
    
    # Section 8: Summary
    doc.add_heading('8. Summary & Next Steps', level=1)
    
    doc.add_heading("Today's Achievements", level=2)
    doc.add_paragraph(
        "You've mastered four fundamental array manipulation techniques that form the foundation "
        "of efficient algorithm design. These patterns appear in 60-70% of array problems on coding "
        "platforms and are essential for technical interviews."
    )
    
    doc.add_heading('Key Takeaways:', level=2)
    takeaways = [
        'Two-pointer technique eliminates nested loops for O(n²) → O(n)',
        'Sliding window avoids recomputation by incremental updates',
        'Prefix sums enable O(1) range queries after preprocessing',
        'Hash maps provide O(1) lookup for complement and frequency problems',
        'Pattern recognition is crucial: identify problem type quickly'
    ]
    for takeaway in takeaways:
        doc.add_paragraph(takeaway, style='List Bullet')
    
    doc.add_heading('Next Steps:', level=2)
    doc.add_paragraph(
        "Day 3 will transition to String problems, where you'll apply these same techniques "
        "in the context of character arrays with semantic meaning. The patterns remain similar, "
        "but strings introduce additional considerations like palindromes, substring matching, "
        "and lexicographic ordering."
    )
    
    doc.add_heading('Recommended Practice Schedule:', level=2)
    schedule = [
        ('Morning (2 hours)', 'Study technique explanations and example solutions'),
        ('Afternoon (2 hours)', 'Solve 3-4 Easy problems independently'),
        ('Evening (1-2 hours)', 'Attempt 2 Medium problems with guidance'),
        ('Before Bed (30 min)', 'Review solutions, note patterns and insights')
    ]
    for time, activity in schedule:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(time).bold = True
        p.add_run(f': {activity}')
    
    doc.add_paragraph()
    doc.add_paragraph(
        "Remember: Mastery comes from deliberate practice, not passive reading. "
        "Code every solution yourself in both languages to reinforce understanding "
        "and appreciate the differences in language features.",
        style='Quote'
    )
    
    # Save document
    doc.save('Day2_Advanced_Arrays.docx')
    print("Day 2 Word document updated successfully: Day2_Advanced_Arrays.docx")


if __name__ == "__main__":
    update_day2_document()
