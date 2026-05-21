"""
Day 3: String Manipulation and Algorithms
==========================================
Topics Covered:
1. Palindrome Patterns
2. String Matching Algorithms
3. Sliding Window on Strings
4. Trie (Prefix Tree) Structures

Each section includes:
- Concept explanation
- Implementation template
- Practice problems with solutions
"""

# ============================================================================
# 1. PALINDROME PATTERNS
# ============================================================================

class PalindromePatterns:
    """
    Palindrome patterns:

    Pattern 1: Expand Around Center
    - Used for: Finding palindromic substrings
    - Time: O(n²), Space: O(1)

    Pattern 2: Two-Pointer Validation
    - Used for: Checking if string is palindrome
    - Time: O(n), Space: O(1)

    Pattern 3: Dynamic Programming
    - Used for: Counting all palindromic substrings
    - Time: O(n²), Space: O(n²)
    """

    @staticmethod
    def is_palindrome(s: str) -> bool:
        """
        Problem: Check if a string is a palindrome (ignoring case and non-alphanumeric).

        Example: s = "A man, a plan, a canal: Panama" → True
                 s = "race a car" → False

        Approach: Two-pointer validation
        - Left starts at beginning, right at end
        - Skip non-alphanumeric characters
        - Compare characters (case-insensitive)
        """
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

    @staticmethod
    def longest_palindromic_substring(s: str) -> str:
        """
        Problem: Find the longest palindromic substring.

        Example: s = "babad" → "bab" or "aba"
                 s = "cbbd" → "bb"

        Approach: Expand around center
        - Each character (and gap) can be center of palindrome
        - Expand outward while characters match
        - Track longest palindrome found
        """
        if not s:
            return ""

        start, end = 0, 0

        def expand_around_center(left: int, right: int) -> tuple[int, int]:
            """Expand while characters match, return palindrome boundaries."""
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return left + 1, right - 1

        for i in range(len(s)):
            # Odd-length palindrome (single character center)
            left1, right1 = expand_around_center(i, i)
            # Even-length palindrome (two character center)
            left2, right2 = expand_around_center(i, i + 1)

            # Update longest
            if right1 - left1 > end - start:
                start, end = left1, right1
            if right2 - left2 > end - start:
                start, end = left2, right2

        return s[start:end + 1]

    @staticmethod
    def count_palindromic_substrings(s: str) -> int:
        """
        Problem: Count all palindromic substrings.

        Example: s = "abc" → 3 ("a", "b", "c")
                 s = "aaa" → 6 ("a", "a", "a", "aa", "aa", "aaa")

        Approach: Expand around center, count each valid expansion
        - For each center, count palindromes formed
        - Sum all counts
        """
        count = 0

        def expand_around_center(left: int, right: int) -> int:
            """Count palindromes expanding from center."""
            palindrome_count = 0
            while left >= 0 and right < len(s) and s[left] == s[right]:
                palindrome_count += 1
                left -= 1
                right += 1
            return palindrome_count

        for i in range(len(s)):
            # Odd-length palindromes
            count += expand_around_center(i, i)
            # Even-length palindromes
            count += expand_around_center(i, i + 1)

        return count

    @staticmethod
    def valid_palindrome_with_one_deletion(s: str) -> bool:
        """
        Problem: Check if string can be palindrome with at most one deletion.

        Example: s = "abca" → True (delete 'c')
                 s = "abc" → False

        Approach: Two-pointer with fallback
        - Normal palindrome check
        - On mismatch, try deleting left or right character
        """
        def is_palindrome_range(left: int, right: int) -> bool:
            """Check if substring is palindrome."""
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        left, right = 0, len(s) - 1

        while left < right:
            if s[left] != s[right]:
                # Try deleting left character OR right character
                return (is_palindrome_range(left + 1, right) or
                        is_palindrome_range(left, right - 1))
            left += 1
            right -= 1

        return True


# ============================================================================
# 2. STRING MATCHING ALGORITHMS
# ============================================================================

class StringMatching:
    """
    String Matching patterns:

    Pattern 1: Naive String Matching
    - Used for: Simple substring search
    - Time: O(n*m), Space: O(1)

    Pattern 2: Rabin-Karp Algorithm
    - Used for: Multiple pattern matching
    - Time: O(n+m) average, Space: O(1)

    Pattern 3: KMP (Knuth-Morris-Pratt)
    - Used for: Efficient single pattern matching
    - Time: O(n+m), Space: O(m)
    """

    @staticmethod
    def naive_string_search(text: str, pattern: str) -> list[int]:
        """
        Problem: Find all occurrences of pattern in text.

        Example: text = "ababcabcab", pattern = "ab" → [0, 2, 5, 8]

        Approach: Naive string matching
        - Check pattern at each position in text
        - Simple but can be slow for large inputs
        """
        if not pattern or not text:
            return []

        result = []
        n, m = len(text), len(pattern)

        for i in range(n - m + 1):
            # Check if pattern matches at position i
            if text[i:i + m] == pattern:
                result.append(i)

        return result

    @staticmethod
    def rabin_karp(text: str, pattern: str) -> list[int]:
        """
        Problem: Find all occurrences of pattern in text using rolling hash.

        Example: text = "ababcabcab", pattern = "ab" → [0, 2, 5, 8]

        Approach: Rabin-Karp algorithm
        - Compute hash of pattern
        - Compute rolling hash of text windows
        - Compare hashes, then verify character-by-character
        """
        if not pattern or not text:
            return []

        result = []
        n, m = len(text), len(pattern)

        # Use prime for hashing
        prime = 101
        base = 256  # ASCII characters

        # Compute hash of pattern
        pattern_hash = 0
        text_hash = 0
        h = 1  # base^(m-1) % prime

        for i in range(m - 1):
            h = (h * base) % prime

        # Calculate hash of pattern and first window
        for i in range(m):
            pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
            text_hash = (base * text_hash + ord(text[i])) % prime

        # Slide pattern over text
        for i in range(n - m + 1):
            # Check if hashes match
            if pattern_hash == text_hash:
                # Verify character-by-character
                if text[i:i + m] == pattern:
                    result.append(i)

            # Compute hash for next window
            if i < n - m:
                text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
                text_hash = (text_hash + prime) % prime  # Handle negative

        return result

    @staticmethod
    def kmp_search(text: str, pattern: str) -> list[int]:
        """
        Problem: Find all occurrences of pattern in text using KMP.

        Example: text = "ababcabcab", pattern = "ab" → [0, 2, 5, 8]

        Approach: KMP algorithm
        - Precompute longest proper prefix which is also suffix (LPS) array
        - Use LPS to skip unnecessary comparisons
        - Never backtrack in text
        """
        if not pattern or not text:
            return []

        result = []
        n, m = len(text), len(pattern)

        # Build LPS array
        def compute_lps() -> list[int]:
            """Compute longest proper prefix which is also suffix for each position."""
            lps = [0] * m
            length = 0  # Length of previous longest prefix suffix
            i = 1

            while i < m:
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]  # Try shorter prefix
                    else:
                        lps[i] = 0
                        i += 1

            return lps

        lps = compute_lps()

        # Search using LPS array
        i = j = 0  # i for text, j for pattern

        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1

                if j == m:
                    result.append(i - j)
                    j = lps[j - 1]  # Continue searching
            else:
                if j != 0:
                    j = lps[j - 1]  # Use LPS to skip
                else:
                    i += 1

        return result

    @staticmethod
    def implement_strstr(haystack: str, needle: str) -> int:
        """
        Problem: Find first occurrence of needle in haystack.
        Returns -1 if not found.

        Example: haystack = "sadbutsad", needle = "sad" → 0
                 haystack = "leetcode", needle = "leeto" → -1

        Approach: Optimized naive search
        - Check each position, but skip efficiently
        """
        if not needle:
            return 0
        if len(needle) > len(haystack):
            return -1

        n, m = len(haystack), len(needle)

        for i in range(n - m + 1):
            if haystack[i:i + m] == needle:
                return i

        return -1


# ============================================================================
# 3. SLIDING WINDOW ON STRINGS
# ============================================================================

class StringSlidingWindow:
    """
    String Sliding Window patterns:

    Pattern 1: Character Frequency Window
    - Used for: Anagram finding, permutation checking
    - Time: O(n), Space: O(1) (fixed alphabet)

    Pattern 2: Unique Character Window
    - Used for: Longest substring without repeating
    - Time: O(n), Space: O(min(n, alphabet_size))

    Pattern 3: Replacement Window
    - Used for: Character replacement problems
    - Time: O(n), Space: O(1)
    """

    @staticmethod
    def find_all_anagrams(s: str, p: str) -> list[int]:
        """
        Problem: Find all starting indices of p's anagrams in s.

        Example: s = "cbaebabacd", p = "abc" → [0, 6]
                 (anagrams: "cba" at 0, "bac" at 6)

        Approach: Sliding window with frequency map
        - Build frequency map for pattern
        - Maintain window of same length
        - Compare frequency maps
        """
        from collections import Counter

        if len(p) > len(s):
            return []

        result = []
        p_count = Counter(p)
        window_count = Counter(s[:len(p)])

        # Check first window
        if window_count == p_count:
            result.append(0)

        # Slide window
        for i in range(len(p), len(s)):
            # Add new character
            window_count[s[i]] += 1
            # Remove old character
            old_char = s[i - len(p)]
            window_count[old_char] -= 1
            if window_count[old_char] == 0:
                del window_count[old_char]

            # Check if anagram
            if window_count == p_count:
                result.append(i - len(p) + 1)

        return result

    @staticmethod
    def permutation_in_string(s1: str, s2: str) -> bool:
        """
        Problem: Check if s2 contains a permutation of s1.

        Example: s1 = "ab", s2 = "eidbaooo" → True ("ba")
                 s1 = "ab", s2 = "eidboaoo" → False

        Approach: Sliding window with frequency comparison
        - Fixed window size = len(s1)
        - Compare character frequencies
        """
        from collections import Counter

        if len(s1) > len(s2):
            return False

        s1_count = Counter(s1)
        window_count = Counter(s2[:len(s1)])

        if window_count == s1_count:
            return True

        # Slide window
        for i in range(len(s1), len(s2)):
            # Add new character
            window_count[s2[i]] += 1
            # Remove old character
            old_char = s2[i - len(s1)]
            window_count[old_char] -= 1
            if window_count[old_char] == 0:
                del window_count[old_char]

            if window_count == s1_count:
                return True

        return False

    @staticmethod
    def minimum_window_substring(s: str, t: str) -> str:
        """
        Problem: Find minimum window in s containing all characters of t.

        Example: s = "ADOBECODEBANC", t = "ABC" → "BANC"

        Approach: Dynamic sliding window with frequency map
        - Expand right to satisfy requirements
        - Contract left to minimize window
        - Track minimum valid window
        """
        from collections import Counter

        if not s or not t:
            return ""

        need = Counter(t)
        required = len(need)

        formed = 0
        window_counts = {}

        left = 0
        min_length = float('inf')
        result = (0, 0)  # (left, right)

        for right in range(len(s)):
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1

            # Check if this character satisfies requirement
            if char in need and window_counts[char] == need[char]:
                formed += 1

            # Contract window while valid
            while formed == required:
                # Update minimum
                if right - left + 1 < min_length:
                    min_length = right - left + 1
                    result = (left, right)

                # Remove left character
                window_counts[s[left]] -= 1
                if s[left] in need and window_counts[s[left]] < need[s[left]]:
                    formed -= 1
                left += 1

        return "" if min_length == float('inf') else s[result[0]:result[1] + 1]

    @staticmethod
    def longest_substring_with_k_replacements(s: str, k: int) -> int:
        """
        Problem: Longest substring with at most k character replacements.

        Example: s = "AABABBA", k = 1 → 4 ("AABBB" with 1 replacement)
                 s = "ABAB", k = 2 → 4

        Approach: Sliding window with max frequency tracking
        - Track max frequency character in window
        - Window valid if: window_size - max_freq <= k
        - Expand window, contract when invalid
        """
        from collections import defaultdict

        char_count = defaultdict(int)
        left = 0
        max_freq = 0
        max_length = 0

        for right in range(len(s)):
            char_count[s[right]] += 1
            max_freq = max(max_freq, char_count[s[right]])

            # Contract if invalid: need more than k replacements
            while (right - left + 1) - max_freq > k:
                char_count[s[left]] -= 1
                left += 1

            max_length = max(max_length, right - left + 1)

        return max_length


# ============================================================================
# 4. TRIE (PREFIX TREE) STRUCTURES
# ============================================================================

class TrieNode:
    """Node in a Trie structure."""

    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end_of_word = False


class Trie:
    """
    Trie (Prefix Tree) implementation.

    Use cases:
    - Autocomplete systems
    - Spell checkers
    - IP routing
    - Word search games

    Time Complexity:
    - Insert: O(m) where m is word length
    - Search: O(m)
    - StartsWith: O(m)

    Space Complexity: O(n * m) where n is number of words
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.

        Example: insert("apple") creates path: a -> p -> p -> l -> e (end)
        """
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Search for a complete word in the trie.

        Returns True only if the word exists and is marked as complete.

        Example: search("apple") → True
                 search("app") → False (if only "apple" was inserted)
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word in trie starts with given prefix.

        Example: starts_with("app") → True (if "apple" exists)
        """
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> TrieNode | None:
        """Find the node at the end of prefix path."""
        node = self.root

        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]

        return node

    def find_all_words_with_prefix(self, prefix: str) -> list[str]:
        """
        Find all words in trie that start with given prefix.

        Example: If trie has ["apple", "application", "app"],
                 find_all_words_with_prefix("app") → ["apple", "application", "app"]
        """
        node = self._find_node(prefix)
        if node is None:
            return []

        result = []
        self._dfs(node, prefix, result)
        return result

    def _dfs(self, node: TrieNode, current_word: str, result: list[str]) -> None:
        """DFS to collect all words from a node."""
        if node.is_end_of_word:
            result.append(current_word)

        for char, child_node in node.children.items():
            self._dfs(child_node, current_word + char, result)


class TrieApplications:
    """Applications of Trie data structure."""

    @staticmethod
    def implement_trie_operations(words: list[str], operations: list[tuple[str, str]]) -> list[bool]:
        """
        Problem: Implement trie with insert, search, and startsWith operations.

        Example: words = ["apple"], operations = [("search", "apple"), ("startsWith", "app")]
                 → [True, True]
        """
        trie = Trie()

        # Insert all words
        for word in words:
            trie.insert(word)

        # Perform operations
        results = []
        for op_type, value in operations:
            if op_type == "insert":
                trie.insert(value)
                results.append(None)
            elif op_type == "search":
                results.append(trie.search(value))
            elif op_type == "startsWith":
                results.append(trie.starts_with(value))

        return results

    @staticmethod
    def word_search_on_board(board: list[list[str]], words: list[str]) -> list[str]:
        """
        Problem: Find all words from a list that can be formed on the board.
        Words can be formed by connecting adjacent cells (horizontally or vertically).
        Each cell can only be used once per word.

        Example: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
                 words = ["oath","pea","oath","rain"]
                 → ["oath", "rain"]

        Approach: Trie + Backtracking
        - Build trie from word list
        - DFS from each cell, following trie paths
        - Mark visited cells, backtrack after exploration
        """
        if not board or not board[0]:
            return []

        # Build trie
        trie = Trie()
        for word in words:
            trie.insert(word)

        result = set()
        rows, cols = len(board), len(board[0])

        def dfs(row: int, col: int, node: TrieNode, path: str) -> None:
            """DFS to find words starting from cell."""
            # Check bounds and if cell visited
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return
            if board[row][col] == '#':  # Visited marker
                return

            char = board[row][col]
            if char not in node.children:
                return

            # Move to next node
            node = node.children[char]
            path += char

            # Check if word found
            if node.is_end_of_word:
                result.add(path)

            # Mark as visited
            temp = board[row][col]
            board[row][col] = '#'

            # Explore neighbors
            dfs(row + 1, col, node, path)
            dfs(row - 1, col, node, path)
            dfs(row, col + 1, node, path)
            dfs(row, col - 1, node, path)

            # Backtrack
            board[row][col] = temp

        # Start DFS from each cell
        for i in range(rows):
            for j in range(cols):
                dfs(i, j, trie.root, "")

        return list(result)


# ============================================================================
# 5. STRING MANIPULATION PATTERNS
# ============================================================================

class StringManipulation:
    """
    String Manipulation patterns:

    Pattern 1: In-Place Reversal
    - Used for: Reverse words, reverse string
    - Time: O(n), Space: O(1) or O(n) depending on mutability

    Pattern 2: String Compression
    - Used for: Run-length encoding
    - Time: O(n), Space: O(1) excluding output

    Pattern 3: String Tokenization
    - Used for: Parsing, splitting
    - Time: O(n), Space: O(n)
    """

    @staticmethod
    def reverse_string(s: list[str]) -> None:
        """
        Problem: Reverse string in-place (as character array).

        Example: s = ["h","e","l","l","o"] → ["o","l","l","e","h"]

        Approach: Two-pointer swap
        - Left starts at beginning, right at end
        - Swap and move toward center
        """
        left, right = 0, len(s) - 1

        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1

    @staticmethod
    def reverse_words_in_string(s: str) -> str:
        """
        Problem: Reverse the order of words in a string.

        Example: s = "the sky is blue" → "blue is sky the"
                 s = "  hello world  " → "world hello"

        Approach: Split, reverse, join
        - Split by whitespace (handles multiple spaces)
        - Reverse word order
        - Join with single space
        """
        words = s.split()
        words.reverse()
        return ' '.join(words)

    @staticmethod
    def rotate_string(s: str, goal: str) -> bool:
        """
        Problem: Check if s can be rotated to become goal.

        Example: s = "abcde", goal = "cdeab" → True
                 s = "abcde", goal = "abced" → False

        Approach: String concatenation trick
        - If goal is rotation of s, then goal is substring of s + s
        - Also check lengths are equal
        """
        return len(s) == len(goal) and goal in (s + s)

    @staticmethod
    def string_compression(chars: list[str]) -> int:
        """
        Problem: Compress character array using run-length encoding.
        Returns new length, modifies array in-place.

        Example: chars = ["a","a","b","b","c","c","c"]
                 → length = 6, chars = ["a","2","b","2","c","3"]

        Approach: Two-pointer compression
        - Read pointer scans characters
        - Write pointer writes compressed output
        - Count consecutive identical characters
        """
        write = 0
        read = 0

        while read < len(chars):
            char = chars[read]
            count = 0

            # Count consecutive identical characters
            while read < len(chars) and chars[read] == char:
                read += 1
                count += 1

            # Write character
            chars[write] = char
            write += 1

            # Write count if > 1
            if count > 1:
                for digit in str(count):
                    chars[write] = digit
                    write += 1

        return write

    @staticmethod
    def group_anagrams(strs: list[str]) -> list[list[str]]:
        """
        Problem: Group anagrams together.

        Example: ["eat","tea","tan","ate","nat","bat"]
                 → [["eat","tea","ate"],["tan","nat"],["bat"]]

        Approach: Hash map with sorted key
        - Anagrams have same sorted representation
        - Group by sorted string as key
        """
        from collections import defaultdict

        groups = defaultdict(list)

        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)

        return list(groups.values())

    @staticmethod
    def encode_decode_words(words: list[str]) -> tuple[str, list[str]]:
        """
        Problem: Encode list of words to string, then decode back.

        Approach: Length-prefix encoding
        - Encode: "word" → "4#word"
        - Decode: read length, then read that many characters
        """
        def encode(word_list: list[str]) -> str:
            """Encode words with length prefix."""
            return ''.join(f"{len(w)}#{w}" for w in word_list)

        def decode(s: str) -> list[str]:
            """Decode length-prefixed string."""
            result = []
            i = 0

            while i < len(s):
                # Find delimiter
                j = s.find('#', i)
                length = int(s[i:j])
                # Extract word
                word = s[j + 1:j + 1 + length]
                result.append(word)
                i = j + 1 + length

            return result

        encoded = encode(words)
        decoded = decode(encoded)

        return encoded, decoded


# ============================================================================
# PRACTICE PROBLEMS FOR HOMEWORK
# ============================================================================

class PracticeProblems:
    """
    Homework Problems - Try solving these on your own!

    EASY:
    1. Valid Palindrome
    2. Reverse String
    3. Valid Anagram
    4. First Unique Character in String

    MEDIUM:
    5. Longest Palindromic Substring
    6. Group Anagrams
    7. Find All Anagrams in a String
    8. Minimum Window Substring
    9. Longest Substring Without Repeating Characters

    HARD:
    10. Regular Expression Matching
    11. Edit Distance
    12. Word Search II
    """

    @staticmethod
    def first_unique_character(s: str) -> int:
        """
        Problem: Find index of first non-repeating character.

        Example: s = "leetcode" → 0 ('l')
                 s = "loveleetcode" → 2 ('v')
                 s = "aabb" → -1

        Approach: Two-pass with frequency map
        - First pass: count character frequencies
        - Second pass: find first character with count 1
        """
        from collections import Counter

        char_count = Counter(s)

        for i, char in enumerate(s):
            if char_count[char] == 1:
                return i

        return -1

    @staticmethod
    def valid_anagram(s: str, t: str) -> bool:
        """
        Problem: Check if t is an anagram of s.

        Example: s = "anagram", t = "nagaram" → True
                 s = "rat", t = "car" → False

        Approach: Character frequency comparison
        - Count frequencies in both strings
        - Compare frequency maps
        """
        from collections import Counter

        return Counter(s) == Counter(t)

    @staticmethod
    def longest_substring_no_repeat(s: str) -> int:
        """
        Problem: Find length of longest substring without repeating characters.

        Example: s = "abcabcbb" → 3 ("abc")
                 s = "bbbbb" → 1 ("b")
                 s = "pwwkew" → 3 ("wke")

        Approach: Sliding window with hash set
        - Expand right, add to set
        - On duplicate, contract left until no duplicate
        """
        char_set = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1

            char_set.add(s[right])
            max_length = max(max_length, right - left + 1)

        return max_length

    @staticmethod
    def regular_expression_matching(s: str, p: str) -> bool:
        """
        Problem: Implement regular expression matching with '.' and '*'.
        '.' matches any single character
        '*' matches zero or more of preceding element

        Example: s = "aa", p = "a*" → True
                 s = "ab", p = ".*" → True
                 s = "aab", p = "c*a*b" → True

        Approach: Dynamic programming
        - dp[i][j] = whether s[:i] matches p[:j]
        - Handle '*' by considering zero or more occurrences
        """
        m, n = len(s), len(p)

        # dp[i][j] = s[:i] matches p[:j]
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True  # Empty matches empty

        # Handle patterns like a*, a*b*, a*b*c* matching empty string
        for j in range(2, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                    # Characters match
                    dp[i][j] = dp[i - 1][j - 1]
                elif p[j - 1] == '*':
                    # Zero occurrences of preceding char
                    dp[i][j] = dp[i][j - 2]
                    # One or more if preceding char matches
                    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                        dp[i][j] = dp[i][j] or dp[i - 1][j]

        return dp[m][n]

    @staticmethod
    def edit_distance(word1: str, word2: str) -> int:
        """
        Problem: Minimum operations to convert word1 to word2.
        Operations: insert, delete, replace

        Example: word1 = "horse", word2 = "ros" → 3
                 (horse → rorse → rose → ros)

        Approach: Dynamic programming
        - dp[i][j] = min operations to convert word1[:i] to word2[:j]
        - Consider insert, delete, replace at each position
        """
        m, n = len(word1), len(word2)

        # dp[i][j] = min operations for word1[:i] -> word2[:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base cases
        for i in range(m + 1):
            dp[i][0] = i  # Delete all characters
        for j in range(n + 1):
            dp[0][j] = j  # Insert all characters

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    # Characters match, no operation needed
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Min of insert, delete, replace
                    dp[i][j] = 1 + min(
                        dp[i][j - 1],      # Insert
                        dp[i - 1][j],      # Delete
                        dp[i - 1][j - 1]   # Replace
                    )

        return dp[m][n]


# ============================================================================
# TEST CASES
# ============================================================================

def run_tests():
    """Run test cases for all patterns."""

    print("=" * 60)
    print("DAY 3: STRING MANIPULATION - TEST CASES")
    print("=" * 60)

    # Palindrome Tests
    print("\n1. PALINDROME PATTERNS")
    print("-" * 40)

    pp = PalindromePatterns()

    # Is Palindrome
    result = pp.is_palindrome("A man, a plan, a canal: Panama")
    print(f"Is Palindrome 'A man, a plan...': {result}")
    assert result is True

    result = pp.is_palindrome("race a car")
    print(f"Is Palindrome 'race a car': {result}")
    assert result is False

    # Longest Palindromic Substring
    longest = pp.longest_palindromic_substring("babad")
    print(f"Longest Palindrome in 'babad': {longest}")
    assert longest in ["bab", "aba"]

    longest = pp.longest_palindromic_substring("cbbd")
    print(f"Longest Palindrome in 'cbbd': {longest}")
    assert longest == "bb"

    # Count Palindromic Substrings
    count = pp.count_palindromic_substrings("abc")
    print(f"Count Palindromes in 'abc': {count}")
    assert count == 3

    count = pp.count_palindromic_substrings("aaa")
    print(f"Count Palindromes in 'aaa': {count}")
    assert count == 6

    # String Matching Tests
    print("\n2. STRING MATCHING ALGORITHMS")
    print("-" * 40)

    sm = StringMatching()

    # Naive Search
    indices = sm.naive_string_search("ababcabcab", "ab")
    print(f"Naive Search 'ab' in 'ababcabcab': {indices}")
    assert indices == [0, 2, 5, 8]

    # Rabin-Karp
    indices = sm.rabin_karp("ababcabcab", "ab")
    print(f"Rabin-Karp 'ab' in 'ababcabcab': {indices}")
    assert indices == [0, 2, 5, 8]

    # KMP Search
    indices = sm.kmp_search("ababcabcab", "ab")
    print(f"KMP Search 'ab' in 'ababcabcab': {indices}")
    assert indices == [0, 2, 5, 8]

    # Implement strStr
    pos = sm.implement_strstr("sadbutsad", "sad")
    print(f"strStr('sadbutsad', 'sad'): {pos}")
    assert pos == 0

    pos = sm.implement_strstr("leetcode", "leeto")
    print(f"strStr('leetcode', 'leeto'): {pos}")
    assert pos == -1

    # Sliding Window Tests
    print("\n3. SLIDING WINDOW ON STRINGS")
    print("-" * 40)

    ssw = StringSlidingWindow()

    # Find All Anagrams
    anagrams = ssw.find_all_anagrams("cbaebabacd", "abc")
    print(f"Find Anagrams of 'abc' in 'cbaebabacd': {anagrams}")
    assert anagrams == [0, 6]

    # Permutation in String
    has_perm = ssw.permutation_in_string("ab", "eidbaooo")
    print(f"Permutation of 'ab' in 'eidbaooo': {has_perm}")
    assert has_perm is True

    # Minimum Window Substring
    window = ssw.minimum_window_substring("ADOBECODEBANC", "ABC")
    print(f"Min Window 'ABC' in 'ADOBECODEBANC': {window}")
    assert window == "BANC"

    # Longest Substring with K Replacements
    longest = ssw.longest_substring_with_k_replacements("AABABBA", 1)
    print(f"Longest Substring (k=1) in 'AABABBA': {longest}")
    assert longest == 4

    # Trie Tests
    print("\n4. TRIE STRUCTURES")
    print("-" * 40)

    trie = Trie()
    trie.insert("apple")
    trie.insert("application")
    trie.insert("app")

    search_result = trie.search("apple")
    print(f"Trie Search 'apple': {search_result}")
    assert search_result is True

    search_result = trie.search("app")
    print(f"Trie Search 'app': {search_result}")
    assert search_result is True

    prefix_result = trie.starts_with("app")
    print(f"Trie StartsWith 'app': {prefix_result}")
    assert prefix_result is True

    prefix_result = trie.starts_with("appl")
    print(f"Trie StartsWith 'appl': {prefix_result}")
    assert prefix_result is True

    words = trie.find_all_words_with_prefix("app")
    print(f"Trie Words with prefix 'app': {words}")
    assert set(words) == {"apple", "application", "app"}

    # String Manipulation Tests
    print("\n5. STRING MANIPULATION")
    print("-" * 40)

    sm = StringManipulation()

    # Reverse String
    chars = ["h", "e", "l", "l", "o"]
    sm.reverse_string(chars)
    print(f"Reverse String 'hello': {chars}")
    assert chars == ["o", "l", "l", "e", "h"]

    # Reverse Words
    reversed_words = sm.reverse_words_in_string("  hello world  ")
    print(f"Reverse Words '  hello world  ': '{reversed_words}'")
    assert reversed_words == "world hello"

    # Rotate String
    is_rotation = sm.rotate_string("abcde", "cdeab")
    print(f"Rotate String 'abcde' -> 'cdeab': {is_rotation}")
    assert is_rotation is True

    # String Compression
    chars = ["a", "a", "b", "b", "c", "c", "c"]
    length = sm.string_compression(chars)
    print(f"String Compression: length={length}, chars={chars[:length]}")
    assert length == 6
    assert chars[:length] == ["a", "2", "b", "2", "c", "3"]

    # Group Anagrams
    groups = sm.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    print(f"Group Anagrams: {groups}")
    assert len(groups) == 3

    # Practice Problems Tests
    print("\n6. PRACTICE PROBLEMS")
    print("-" * 40)

    pp = PracticeProblems()

    # First Unique Character
    idx = pp.first_unique_character("leetcode")
    print(f"First Unique in 'leetcode': index {idx}")
    assert idx == 0

    idx = pp.first_unique_character("aabb")
    print(f"First Unique in 'aabb': index {idx}")
    assert idx == -1

    # Valid Anagram
    is_anagram = pp.valid_anagram("anagram", "nagaram")
    print(f"Valid Anagram 'anagram' & 'nagaram': {is_anagram}")
    assert is_anagram is True

    # Longest Substring No Repeat
    longest = pp.longest_substring_no_repeat("abcabcbb")
    print(f"Longest No Repeat 'abcabcbb': {longest}")
    assert longest == 3

    # Edit Distance
    distance = pp.edit_distance("horse", "ros")
    print(f"Edit Distance 'horse' -> 'ros': {distance}")
    assert distance == 3

    distance = pp.edit_distance("intention", "execution")
    print(f"Edit Distance 'intention' -> 'execution': {distance}")
    assert distance == 5

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
