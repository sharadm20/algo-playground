"""
Create Day 3 Word Document for DSA Study Plan
Topic: String Manipulation
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


def create_day3_document():
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # Title
    title = doc.add_heading('Day 3: String Manipulation', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle
    subtitle = doc.add_paragraph('Pattern Matching, Palindromes, and Tries')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True

    # Date and info
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.add_run('📅 March 31, 2026').bold = True
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
        "Day 3 transitions from arrays to strings, applying similar techniques while introducing "
        "string-specific algorithms. Strings are fundamental to programming, appearing in everything "
        "from text processing to DNA sequence analysis."
    )

    doc.add_paragraph(
        "Today we'll master four critical areas: palindrome detection, efficient string matching, "
        "sliding window applications on strings, and the trie data structure for prefix-based operations."
    )

    # ============================================================================
    # CORE TECHNIQUES
    # ============================================================================
    doc.add_heading('Core Techniques', level=1)

    # 1. Palindrome Patterns
    doc.add_heading('1. Palindrome Patterns', level=2)

    doc.add_paragraph(
        "Palindromes are strings that read the same forwards and backwards. Detecting and manipulating "
        "palindromes requires careful pointer management."
    )

    # Table for palindrome patterns
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    # Header row
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Pattern'
    header_cells[1].text = 'Description'
    header_cells[2].text = 'Applications'

    for cell in header_cells:
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Data rows
    data = [
        ('Two-Pointer Validation', 'Compare characters from both ends moving inward', 'Check if string is palindrome'),
        ('Expand Around Center', 'Treat each position as potential palindrome center', 'Find longest palindromic substring'),
        ('Dynamic Programming', 'Build palindrome table bottom-up', 'Count all palindromic substrings'),
    ]

    for pattern, desc, app in data:
        row = table.add_row()
        row.cells[0].text = pattern
        row.cells[1].text = desc
        row.cells[2].text = app

    doc.add_paragraph()

    # Code example: Valid Palindrome (Python)
    doc.add_paragraph('Code Example: Valid Palindrome (Python)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''def is_palindrome(s: str) -> bool:
    """Check if string is palindrome, ignoring case and non-alphanumeric."""
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric from left
        while left < right and not s[left].isalnum():
            left += 1
        # Skip non-alphanumeric from right
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True

# Test cases
print(is_palindrome("A man, a plan, a canal: Panama"))  # True
print(is_palindrome("race a car"))  # False
print(is_palindrome("Was it a car or a cat I saw?"))  # True''').font.name = 'Consolas'

    # Code example: Valid Palindrome (Rust)
    doc.add_paragraph('Code Example: Valid Palindrome (Rust)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''fn is_palindrome(s: &str) -> bool {
    let chars: Vec<char> = s.chars().collect();
    let mut left = 0;
    let mut right = chars.len().saturating_sub(1);

    while left < right {
        while left < right && !chars[left].is_alphanumeric() {
            left += 1;
        }
        while left < right && !chars[right].is_alphanumeric() {
            right = right.saturating_sub(1);
        }

        if chars[left].to_ascii_lowercase() != chars[right].to_ascii_lowercase() {
            return false;
        }

        left += 1;
        if right > 0 {
            right -= 1;
        }
    }

    true
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_palindrome() {
        assert_eq!(is_palindrome("A man, a plan, a canal: Panama"), true);
        assert_eq!(is_palindrome("race a car"), false);
        assert_eq!(is_palindrome("Was it a car or a cat I saw?"), true);
    }
}''').font.name = 'Consolas'

    doc.add_paragraph()

    # 2. String Matching Algorithms
    doc.add_heading('2. String Matching Algorithms', level=2)

    doc.add_paragraph(
        "Efficiently finding patterns within text is crucial for search engines, text editors, and bioinformatics."
    )

    # Table for string matching
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    header_cells = table.rows[0].cells
    header_cells[0].text = 'Algorithm'
    header_cells[1].text = 'Time Complexity'
    header_cells[2].text = 'Use Case'

    for cell in header_cells:
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    data = [
        ('Naive Search', 'O(n*m)', 'Simple patterns, small inputs'),
        ('Rabin-Karp', 'O(n+m) average', 'Multiple pattern matching, plagiarism detection'),
        ('KMP (Knuth-Morris-Pratt)', 'O(n+m)', 'Single pattern with many repetitions'),
    ]

    for algo, time, use in data:
        row = table.add_row()
        row.cells[0].text = algo
        row.cells[1].text = time
        row.cells[2].text = use

    doc.add_paragraph()

    # KMP Algorithm explanation
    doc.add_paragraph('KMP Algorithm - Key Insight:', style='Heading 3')
    doc.add_paragraph(
        "The KMP algorithm uses a preprocessing step to build an LPS (Longest Proper Prefix which is "
        "also Suffix) array. This allows the algorithm to skip unnecessary comparisons by leveraging "
        "previously matched characters.", style='Intense Quote'
    )

    doc.add_paragraph('Code Example: KMP Search (Python)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''def kmp_search(text: str, pattern: str) -> list[int]:
    """Find all occurrences of pattern in text using KMP algorithm."""
    if not pattern or not text:
        return []

    result = []
    n, m = len(text), len(pattern)

    def compute_lps() -> list[int]:
        """Compute longest proper prefix which is also suffix array."""
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    lps = compute_lps()
    i = j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == m:
                result.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return result

# Test
text = "ababcabcab"
pattern = "ab"
print(kmp_search(text, pattern))  # [0, 2, 5, 8]''').font.name = 'Consolas'

    doc.add_paragraph()

    # 3. Sliding Window on Strings
    doc.add_heading('3. Sliding Window on Strings', level=2)

    doc.add_paragraph(
        "String sliding window problems often involve character frequency tracking and anagram detection."
    )

    doc.add_paragraph('Key Patterns:', style='Heading 3')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Fixed Window:').bold = True
    p.add_run(' Find all anagrams of pattern p in string s')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Dynamic Window:').bold = True
    p.add_run(' Minimum window containing all characters of target')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Frequency Tracking:').bold = True
    p.add_run(' Use hash maps to count character occurrences')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Permutation Check:').bold = True
    p.add_run(' Compare frequency maps for anagram detection')

    doc.add_paragraph('Code Example: Find All Anagrams (Python)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''def find_all_anagrams(s: str, p: str) -> list[int]:
    """Find all starting indices of p's anagrams in s."""
    from collections import Counter

    if len(p) > len(s):
        return []

    result = []
    p_count = Counter(p)
    window_count = Counter(s[:len(p)])

    if window_count == p_count:
        result.append(0)

    for i in range(len(p), len(s)):
        # Add new character
        window_count[s[i]] += 1
        # Remove old character
        old_char = s[i - len(p)]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]

        if window_count == p_count:
            result.append(i - len(p) + 1)

    return result

# Test
s = "cbaebabacd"
p = "abc"
print(find_all_anagrams(s, p))  # [0, 6]''').font.name = 'Consolas'

    doc.add_paragraph()

    # 4. Trie (Prefix Tree)
    doc.add_heading('4. Trie (Prefix Tree)', level=2)

    doc.add_paragraph(
        "Tries are tree-like structures optimized for string operations, especially prefix-based queries."
    )

    doc.add_paragraph('Structure and Operations:', style='Heading 3')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Structure:').bold = True
    p.add_run(' Each node represents a character, paths form words')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Insert:').bold = True
    p.add_run(' O(m) where m is word length')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Search:').bold = True
    p.add_run(' O(m) for exact word lookup')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Prefix Search:').bold = True
    p.add_run(' O(m) to check if any word starts with prefix')

    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Applications:').bold = True
    p.add_run(' Autocomplete, spell checkers, word games')

    doc.add_paragraph('Code Example: Trie Implementation (Python)', style='Heading 3')
    code_para = doc.add_paragraph()
    code_para.add_run('''class TrieNode:
    """Node in a Trie structure."""
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end_of_word = False


class Trie:
    """Trie (Prefix Tree) implementation."""
    
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Search for a complete word in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Check if any word in trie starts with given prefix."""
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str):
        """Find the node at the end of prefix path."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

# Test
trie = Trie()
trie.insert("apple")
print(trie.search("apple"))    # True
print(trie.search("app"))      # False
print(trie.starts_with("app")) # True''').font.name = 'Consolas'

    doc.add_paragraph()

    # ============================================================================
    # ESSENTIAL PROBLEMS
    # ============================================================================
    doc.add_heading('Essential Problems', level=1)

    problems = [
        {
            'title': 'Valid Palindrome',
            'difficulty': 'Easy',
            'pattern': 'Two-Pointer Validation',
            'problem': 'Check if string is palindrome, ignoring non-alphanumeric characters.',
            'example': '"A man, a plan, a canal: Panama" → True',
            'solution': 'Two pointers from ends, skip non-alphanumeric, compare case-insensitive. O(n) time, O(1) space.'
        },
        {
            'title': 'Longest Palindromic Substring',
            'difficulty': 'Medium',
            'pattern': 'Expand Around Center',
            'problem': 'Find the longest substring that is a palindrome.',
            'example': 's = "babad" → "bab" or "aba"',
            'solution': 'For each position, expand around center (both odd and even length). Track longest palindrome found. O(n²) time, O(1) space.'
        },
        {
            'title': 'Find All Anagrams in a String',
            'difficulty': 'Medium',
            'pattern': 'Sliding Window with Frequency Map',
            'problem': "Find all starting indices of p's anagrams in s.",
            'example': 's = "cbaebabacd", p = "abc" → [0, 6]',
            'solution': 'Fixed-size sliding window with character frequency comparison. Build frequency map for p, slide window over s, compare maps. O(n) time, O(1) space.'
        },
        {
            'title': 'Minimum Window Substring',
            'difficulty': 'Hard',
            'pattern': 'Dynamic Sliding Window',
            'problem': 'Find minimum window in s containing all characters of t.',
            'example': 's = "ADOBECODEBANC", t = "ABC" → "BANC"',
            'solution': 'Expand right to satisfy requirements, contract left to minimize. Track character frequencies and count of satisfied requirements. O(n) time, O(1) space.'
        },
        {
            'title': 'Implement Trie (Prefix Tree)',
            'difficulty': 'Medium',
            'pattern': 'Trie Data Structure',
            'problem': 'Implement trie with insert, search, and startsWith operations.',
            'example': 'insert("apple"), search("apple") → True, search("app") → False',
            'solution': 'Build tree where each node has children map and end-of-word flag. Insert creates path, search follows path and checks end flag. O(m) per operation.'
        },
        {
            'title': 'Word Search II',
            'difficulty': 'Hard',
            'pattern': 'Trie + Backtracking',
            'problem': 'Find all words from list that can be formed on board.',
            'example': 'board with letters, words = ["oath","pea","rain"] → ["oath", "rain"]',
            'solution': 'Build trie from word list, DFS from each cell following trie paths. Mark visited cells, backtrack after exploration. O(m*n*4^L) where L is max word length.'
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
        ('Palindrome Check (Two-Pointer)', 'O(n)', 'O(1)'),
        ('Longest Palindromic Substring', 'O(n²)', 'O(1)'),
        ('Naive String Search', 'O(n*m)', 'O(1)'),
        ('Rabin-Karp', 'O(n+m) average', 'O(1)'),
        ('KMP', 'O(n+m)', 'O(m)'),
        ('Sliding Window (Anagrams)', 'O(n)', 'O(1)'),
        ('Trie Operations', 'O(m) per operation', 'O(n*m)'),
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
        ('Expand Around Center:', 'For palindrome problems, consider both odd-length (single char center) and even-length (two char center) cases'),
        ('String Immutability:', 'In languages with immutable strings, convert to character array for in-place modifications'),
        ('Frequency Map Comparison:', 'For anagram/permutation problems, compare character counts rather than sorting'),
        ('Trie for Prefixes:', 'When problem involves prefix searches or autocomplete, trie is often optimal'),
        ('Rolling Hash:', 'Rabin-Karp uses rolling hash to avoid recomputing hash from scratch for each window'),
        ('LPS Array:', "KMP's LPS (Longest Proper Prefix which is also Suffix) array enables skipping unnecessary comparisons"),
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
        'Valid Palindrome - Two-pointer validation with alphanumeric filtering',
        'Reverse String - In-place reversal using two-pointer swap',
        'Valid Anagram - Character frequency comparison',
        'First Unique Character in String - Two-pass with frequency map',
        'Implement strStr() - Naive string matching',
    ]
    for prob in easy_problems:
        doc.add_paragraph(prob, style='List Bullet')

    doc.add_heading('Medium Problems', level=2)
    medium_problems = [
        'Longest Palindromic Substring - Expand around center technique',
        'Group Anagrams - Hash map with sorted key',
        'Find All Anagrams in a String - Fixed sliding window',
        'Longest Substring Without Repeating Characters - Dynamic window with set',
        'Minimum Window Substring - Dynamic window with frequency map',
    ]
    for prob in medium_problems:
        doc.add_paragraph(prob, style='List Bullet')

    doc.add_heading('Hard Problems', level=2)
    hard_problems = [
        "Regular Expression Matching - Dynamic programming with '.' and '*'",
        'Edit Distance - DP for minimum insert/delete/replace operations',
        'Word Search II - Trie + backtracking on 2D board',
        'Count Palindromic Substrings - Expand around center with counting',
    ]
    for prob in hard_problems:
        doc.add_paragraph(prob, style='List Bullet')

    doc.add_paragraph()

    # ============================================================================
    # RESOURCES
    # ============================================================================
    doc.add_heading('Resources', level=1)

    doc.add_paragraph('Code Files:', style='Heading 3')
    doc.add_paragraph('• Python: python_projects/day3_strings.py', style='List Bullet')
    doc.add_paragraph('• Rust: rust_projects/day3_strings.rs', style='List Bullet')
    doc.add_paragraph('• Cargo Project: rust_projects/day3_strings/', style='List Bullet')

    doc.add_paragraph('Run Commands:', style='Heading 3')
    doc.add_paragraph('• Python: cd python_projects && python day3_strings.py', style='List Bullet')
    doc.add_paragraph('• Rust: cd rust_projects/day3_strings && cargo run', style='List Bullet')

    # Save document
    doc.save('Day3_String_Manipulation.docx')
    print("Day 3 Word document created successfully!")


if __name__ == '__main__':
    create_day3_document()
