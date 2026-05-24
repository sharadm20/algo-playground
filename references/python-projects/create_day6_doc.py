"""
Create Day 6 Word Document for DSA Study Plan
Topic: Trees & Binary Trees
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


def create_day6_document():
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # Title
    title = doc.add_heading('Day 6: Trees & Binary Trees', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subtitle
    subtitle = doc.add_paragraph('Binary Tree Structure, Tree Traversal, BST, Tree Properties')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].italic = True

    # Date and info
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info.add_run('📅 April 4, 2026').bold = True
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
        "Day 6 introduces binary trees, a hierarchical data structure where each node has at most two children. "
        "Trees are fundamental in computer science, enabling efficient searching, sorting, and organization of data. "
        "Binary Search Trees (BSTs) are particularly important, providing O(log n) operations when balanced. "
        "Understanding tree traversal and manipulation is essential for solving complex algorithmic problems."
    )

    p = doc.add_paragraph()
    p.add_run('Key Characteristics of Trees:').bold = True

    bullets = [
        "Hierarchical structure with parent-child relationships",
        "Each node has at most 2 children (left and right) in binary trees",
        "Root node has no parent; leaf nodes have no children",
        "No cycles (unlike graphs)",
        "Path from root to any node is unique",
        "Height/depth measured in edges or nodes from root"
    ]

    for bullet in bullets:
        doc.add_paragraph(bullet, style='List Bullet')

    # ============================================================================
    # PATTERN 1: TREE TRAVERSALS
    # ============================================================================
    doc.add_heading('Pattern 1: Tree Traversals (4 Types)', level=1)

    doc.add_heading('1.1 In-Order Traversal (Left → Root → Right)', level=2)
    
    doc.add_paragraph(
        "In-order traversal visits the left subtree, then the root, then the right subtree. "
        "For Binary Search Trees, this produces values in sorted order—a critical property. "
        "This is the most commonly used traversal for BST operations."
    )

    p = doc.add_paragraph()
    p.add_run('Algorithm:').bold = True

    algo_steps = [
        "Recursively traverse left subtree",
        "Visit the root node",
        "Recursively traverse right subtree"
    ]
    for i, step in enumerate(algo_steps, 1):
        doc.add_paragraph(f"{i}. {step}", style='List Number')

    p = doc.add_paragraph()
    p.add_run('Time Complexity: ').bold = True
    p.add_run('O(n) - visit each node exactly once')
    p = doc.add_paragraph()
    p.add_run('Space Complexity: ').bold = True
    p.add_run('O(h) - recursion stack, where h is tree height')

    p = doc.add_paragraph()
    p.add_run('Python Implementation:').bold = True

    code = doc.add_paragraph()
    code.style = doc.styles['No Spacing']
    code.add_run(
        "def inorder_traversal(root):\n"
        "    result = []\n"
        "    def dfs(node):\n"
        "        if node:\n"
        "            dfs(node.left)\n"
        "            result.append(node.val)\n"
        "            dfs(node.right)\n"
        "    dfs(root)\n"
        "    return result"
    ).font.name = 'Consolas'

    doc.add_heading('1.2 Pre-Order Traversal (Root → Left → Right)', level=2)
    
    doc.add_paragraph(
        "Pre-order traversal visits the root first, then left subtree, then right subtree. "
        "Useful for creating a copy of the tree or serializing the tree structure. "
        "Also used in prefix expression evaluation."
    )

    p = doc.add_paragraph()
    p.add_run('Use Cases: ').bold = True
    uses = [
        "Tree serialization/deserialization",
        "Creating exact tree copies",
        "Expression trees (prefix notation)",
        "Computing directory structure sizes"
    ]
    for use in uses:
        doc.add_paragraph(use, style='List Bullet')

    doc.add_heading('1.3 Post-Order Traversal (Left → Right → Root)', level=2)
    
    doc.add_paragraph(
        "Post-order traversal visits left subtree, then right subtree, then the root. "
        "Essential for operations that require processing children before parent, "
        "such as tree deletion or computing tree properties."
    )

    p = doc.add_paragraph()
    p.add_run('Use Cases: ').bold = True
    uses = [
        "Safe tree deletion (delete children before parent)",
        "Computing tree height/diameter",
        "Expression trees (postfix notation)",
        "Bottom-up tree processing"
    ]
    for use in uses:
        doc.add_paragraph(use, style='List Bullet')

    doc.add_heading('1.4 Level-Order Traversal (BFS)', level=2)
    
    doc.add_paragraph(
        "Level-order traversal visits nodes level by level, from left to right. "
        "This is a breadth-first search (BFS) approach using a queue. "
        "Essential for finding node depths, level averages, or right-side view."
    )

    p = doc.add_paragraph()
    p.add_run('Algorithm:').bold = True

    code = doc.add_paragraph()
    code.style = doc.styles['No Spacing']
    code.add_run(
        "def levelorder_traversal(root):\n"
        "    if not root:\n"
        "        return []\n"
        "    result = []\n"
        "    queue = deque([root])\n"
        "    while queue:\n"
        "        level_size = len(queue)\n"
        "        current_level = []\n"
        "        for _ in range(level_size):\n"
        "            node = queue.popleft()\n"
        "            current_level.append(node.val)\n"
        "            if node.left:\n"
        "                queue.append(node.left)\n"
        "            if node.right:\n"
        "                queue.append(node.right)\n"
        "        result.append(current_level)\n"
        "    return result"
    ).font.name = 'Consolas'

    # ============================================================================
    # PATTERN 2: BINARY SEARCH TREES
    # ============================================================================
    doc.add_heading('Pattern 2: Binary Search Trees (BST)', level=1)

    doc.add_paragraph(
        "A Binary Search Tree is a binary tree with a critical ordering property: "
        "for any node, all values in its left subtree are smaller, and all values "
        "in its right subtree are larger. This property enables efficient search, "
        "insertion, and deletion operations."
    )

    p = doc.add_paragraph()
    p.add_run('BST Property: ').bold = True
    p.add_run('left.val < root.val < right.val for all nodes')

    doc.add_heading('2.1 Validating a BST', level=2)
    
    doc.add_paragraph(
        "To validate a BST, we cannot simply check that left < root < right locally. "
        "We must ensure all nodes in the left subtree are smaller than the root, "
        "and all nodes in the right subtree are larger. This requires passing down "
        "valid ranges (min/max bounds) during traversal."
    )

    p = doc.add_paragraph()
    p.add_run('Common Mistake: ').bold = True
    p.add_run(
        "Only checking immediate children is insufficient. A node might be larger than its "
        "parent but still belong in the left subtree of an ancestor."
    )

    p = doc.add_paragraph()
    p.add_run('Correct Approach: ').bold = True
    p.add_run('Pass valid range (low, high) down during recursion')

    code = doc.add_paragraph()
    code.style = doc.styles['No Spacing']
    code.add_run(
        "def is_valid_bst(root, low=-∞, high=∞):\n"
        "    if not root:\n"
        "        return True\n"
        "    if root.val <= low or root.val >= high:\n"
        "        return False\n"
        "    return (is_valid_bst(root.left, low, root.val) and\n"
        "            is_valid_bst(root.right, root.val, high))"
    ).font.name = 'Consolas'

    p = doc.add_paragraph()
    p.add_run('Time: ').bold = True
    p.add_run('O(n)  ')
    p.add_run('Space: ').bold = True
    p.add_run('O(h)')

    doc.add_heading('2.2 BST Operations: Search, Insert, Delete', level=2)
    
    doc.add_paragraph(
        "BST operations leverage the ordering property to efficiently locate the correct position. "
        "Search and insert are straightforward recursive operations. Delete is more complex, "
        "requiring handling three cases: leaf nodes, nodes with one child, and nodes with two children."
    )

    p = doc.add_paragraph()
    p.add_run('Delete Cases:').bold = True

    cases = [
        "Leaf node: Simply remove it",
        "One child: Replace with child",
        "Two children: Find inorder successor (smallest in right subtree), copy its value, then delete successor"
    ]
    for i, case in enumerate(cases, 1):
        doc.add_paragraph(f"{i}. {case}", style='List Number')

    # ============================================================================
    # PATTERN 3: LOWEST COMMON ANCESTOR
    # ============================================================================
    doc.add_heading('Pattern 3: Lowest Common Ancestor (LCA)', level=1)

    doc.add_paragraph(
        "The Lowest Common Ancestor of two nodes p and q is the deepest node that is an ancestor "
        "of both p and q. This problem appears frequently in interviews and has elegant solutions."
    )

    doc.add_heading('3.1 LCA in General Binary Tree', level=2)
    
    doc.add_paragraph(
        "For a general binary tree, we use post-order traversal. If we find p in the left subtree "
        "and q in the right subtree (or vice versa), the current node is the LCA. If both are in "
        "the same subtree, continue searching there."
    )

    code = doc.add_paragraph()
    code.style = doc.styles['No Spacing']
    code.add_run(
        "def lowest_common_ancestor(root, p, q):\n"
        "    if not root or root == p or root == q:\n"
        "        return root\n"
        "    left = LCA(root.left, p, q)\n"
        "    right = LCA(root.right, p, q)\n"
        "    if left and right:\n"
        "        return root  # p and q in different subtrees\n"
        "    return left if left else right"
    ).font.name = 'Consolas'

    p = doc.add_paragraph()
    p.add_run('Time: ').bold = True
    p.add_run('O(n)  ')
    p.add_run('Space: ').bold = True
    p.add_run('O(h)')

    doc.add_heading('3.2 LCA in BST (Optimized)', level=2)
    
    doc.add_paragraph(
        "For BSTs, we can optimize using the BST property. If both p and q are smaller than root, "
        "LCA must be in the left subtree. If both are larger, LCA is in the right subtree. "
        "Otherwise, root is the LCA (they're on different sides)."
    )

    p = doc.add_paragraph()
    p.add_run('Time: ').bold = True
    p.add_run('O(h) - much faster than general tree!')

    # ============================================================================
    # PATTERN 4: TREE HEIGHT & DIAMETER
    # ============================================================================
    doc.add_heading('Pattern 4: Tree Height and Diameter', level=1)

    doc.add_heading('4.1 Maximum Depth (Height)', level=2)
    
    doc.add_paragraph(
        "The maximum depth/height of a binary tree is the number of nodes (or edges) along the "
        "longest path from the root node down to the farthest leaf node. This is computed using "
        "post-order traversal: height = 1 + max(left_height, right_height)."
    )

    code = doc.add_paragraph()
    code.style = doc.styles['No Spacing']
    code.add_run(
        "def max_depth(root):\n"
        "    if not root:\n"
        "        return 0\n"
        "    return 1 + max(max_depth(root.left),\n"
        "                   max_depth(root.right))"
    ).font.name = 'Consolas'

    doc.add_heading('4.2 Diameter of Binary Tree', level=2)
    
    doc.add_paragraph(
        "The diameter is the length of the longest path between any two nodes in the tree. "
        "This path may or may not pass through the root. The key insight: the longest path "
        "through any node is left_height + right_height. We compute height while tracking "
        "the maximum diameter found so far."
    )

    p = doc.add_paragraph()
    p.add_run('Key Insight: ').bold = True
    p.add_run(
        "For each node, the longest path through it = left_height + right_height. "
        "Track the maximum across all nodes."
    )

    code = doc.add_paragraph()
    code.style = doc.styles['No Spacing']
    code.add_run(
        "def diameter_of_binary_tree(root):\n"
        "    diameter = [0]\n"
        "    def height(node):\n"
        "        if not node:\n"
        "            return 0\n"
        "        left_h = height(node.left)\n"
        "        right_h = height(node.right)\n"
        "        diameter[0] = max(diameter[0], left_h + right_h)\n"
        "        return 1 + max(left_h, right_h)\n"
        "    height(root)\n"
        "    return diameter[0]"
    ).font.name = 'Consolas'

    p = doc.add_paragraph()
    p.add_run('Time: ').bold = True
    p.add_run('O(n)  ')
    p.add_run('Space: ').bold = True
    p.add_run('O(h)')

    # ============================================================================
    # PATTERN 5: BALANCED BINARY TREE
    # ============================================================================
    doc.add_heading('Pattern 5: Balanced Binary Tree', level=1)

    doc.add_paragraph(
        "A binary tree is balanced if for every node, the heights of its left and right subtrees "
        "differ by at most 1. Balanced trees guarantee O(log n) operations. An unbalanced tree "
        "can degenerate into a linked list with O(n) operations."
    )

    p = doc.add_paragraph()
    p.add_run('Balance Condition: ').bold = True
    p.add_run('|left_height - right_height| ≤ 1 for all nodes')

    doc.add_paragraph(
        "Naive approach computes height for each node separately (O(n²)). Optimized approach "
        "computes height and checks balance simultaneously in a single traversal (O(n))."
    )

    code = doc.add_paragraph()
    code.style = doc.styles['No Spacing']
    code.add_run(
        "def is_balanced(root):\n"
        "    def check(node):\n"
        "        if not node:\n"
        "            return (True, 0)\n"
        "        left_bal, left_h = check(node.left)\n"
        "        right_bal, right_h = check(node.right)\n"
        "        is_bal = (left_bal and right_bal and\n"
        "                 abs(left_h - right_h) <= 1)\n"
        "        return (is_bal, 1 + max(left_h, right_h))\n"
        "    return check(root)[0]"
    ).font.name = 'Consolas'

    # ============================================================================
    # PATTERN 6: TREE SYMMETRY
    # ============================================================================
    doc.add_heading('Pattern 6: Tree Symmetry', level=1)

    doc.add_paragraph(
        "A binary tree is symmetric if it is a mirror of itself. This means the left subtree "
        "is a mirror reflection of the right subtree. We check this by comparing two trees "
        "simultaneously: t1.left with t2.right and t1.right with t2.left."
    )

    code = doc.add_paragraph()
    code.style = doc.styles['No Spacing']
    code.add_run(
        "def is_symmetric(root):\n"
        "    def is_mirror(t1, t2):\n"
        "        if not t1 and not t2:\n"
        "            return True\n"
        "        if not t1 or not t2:\n"
        "            return False\n"
        "        return (t1.val == t2.val and\n"
        "                is_mirror(t1.left, t2.right) and\n"
        "                is_mirror(t1.right, t2.left))\n"
        "    return is_mirror(root, root)"
    ).font.name = 'Consolas'

    # ============================================================================
    # PATTERN 7: PATH SUM
    # ============================================================================
    doc.add_heading('Pattern 7: Path Sum', level=1)

    doc.add_paragraph(
        "Path sum problems ask whether there exists a root-to-leaf path where the sum of node "
        "values equals a target. These are solved with DFS, subtracting node values from the "
        "target sum as we traverse. At leaf nodes, we check if the remaining sum is zero."
    )

    p = doc.add_paragraph()
    p.add_run('Variants:').bold = True

    variants = [
        "Path Sum I: Return boolean (exists such path?)",
        "Path Sum II: Return all valid paths",
        "Path Sum III: Count paths (not necessarily root-to-leaf)"
    ]
    for variant in variants:
        doc.add_paragraph(variant, style='List Bullet')

    # ============================================================================
    # PRACTICE PROBLEMS
    # ============================================================================
    doc.add_heading('Practice Problems', level=1)

    doc.add_heading('Easy Problems', level=2)
    easy_problems = [
        "Maximum Depth of Binary Tree (LeetCode 104)",
        "Symmetric Tree (LeetCode 101)",
        "Path Sum (LeetCode 112)",
        "Inorder Traversal (LeetCode 94)"
    ]
    for prob in easy_problems:
        doc.add_paragraph(prob, style='List Bullet')

    doc.add_heading('Medium Problems', level=2)
    medium_problems = [
        "Validate Binary Search Tree (LeetCode 98)",
        "Lowest Common Ancestor of BST (LeetCode 235)",
        "Diameter of Binary Tree (LeetCode 543)",
        "Balanced Binary Tree (LeetCode 110)",
        "Binary Tree Level Order Traversal (LeetCode 102)"
    ]
    for prob in medium_problems:
        doc.add_paragraph(prob, style='List Bullet')

    doc.add_heading('Hard Problems', level=2)
    hard_problems = [
        "Binary Tree Maximum Path Sum (LeetCode 124)",
        "Serialize and Deserialize Binary Tree (LeetCode 297)",
        "Lowest Common Ancestor of Binary Tree (LeetCode 236)"
    ]
    for prob in hard_problems:
        doc.add_paragraph(prob, style='List Bullet')

    # ============================================================================
    # KEY TAKEAWAYS
    # ============================================================================
    doc.add_heading('Key Takeaways', level=1)

    takeaways = [
        "Four traversal methods: in-order, pre-order, post-order, level-order—each has specific use cases",
        "In-order traversal of BST yields sorted values",
        "BST validation requires passing ranges, not just checking local property",
        "Tree height and diameter can be computed simultaneously in O(n)",
        "Balance condition: |left_height - right_height| ≤ 1",
        "LCA in general tree: O(n) with post-order; in BST: O(h) using BST property",
        "Path sum problems use DFS with target subtraction",
        "Recursive solutions are elegant; iterative solutions use stacks/queues"
    ]

    for takeaway in takeaways:
        doc.add_paragraph(takeaway, style='List Bullet')

    # ============================================================================
    # SUMMARY TABLE
    # ============================================================================
    doc.add_heading('Complexity Summary', level=1)

    table = doc.add_table(rows=9, cols=3)
    table.style = 'Light Grid Accent 1'

    headers = ['Operation', 'Time', 'Space']
    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = header
        table.rows[0].cells[i].paragraphs[0].runs[0].bold = True

    data = [
        ['In-order Traversal', 'O(n)', 'O(h)'],
        ['Pre-order Traversal', 'O(n)', 'O(h)'],
        ['Post-order Traversal', 'O(n)', 'O(h)'],
        ['Level-order Traversal', 'O(n)', 'O(w)'],
        ['Validate BST', 'O(n)', 'O(h)'],
        ['Tree Height', 'O(n)', 'O(h)'],
        ['Tree Diameter', 'O(n)', 'O(h)'],
        ['Check Balanced', 'O(n)', 'O(h)'],
    ]

    for i, row_data in enumerate(data, 1):
        for j, cell_data in enumerate(row_data):
            table.rows[i].cells[j].text = cell_data

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('Note: ').bold = True
    p.add_run('n = number of nodes, h = tree height, w = maximum width')

    # Save document
    doc.save('Day6_Trees.docx')
    print("✓ Day6_Trees.docx created successfully!")


if __name__ == "__main__":
    create_day6_document()
