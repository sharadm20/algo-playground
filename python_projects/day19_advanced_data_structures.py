"""
Day 19: Advanced Data Structures - Python Implementations
"""

class DSU:
    """Disjoint Set Union (Union-Find) with path compression and union by rank"""
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        
        if x_root == y_root:
            return
        
        # Union by rank
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]:
            self.parent[y_root] = x_root
        else:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1

class TrieNode:
    """Trie node for suffix trie"""
    def __init__(self):
        self.children = {}
        self.is_end = False

class SuffixTrie:
    """Suffix Trie implementation"""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        """Search for a word in the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

class BloomFilter:
    """Bloom Filter implementation"""
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [False] * size

    def _hash(self, item, seed):
        """Simple hash function"""
        result = 0
        for char in item:
            result = (result * seed + ord(char)) % self.size
        return result

    def add(self, item):
        """Add an item to the bloom filter"""
        for i in range(self.num_hashes):
            index = self._hash(item, i + 1)
            self.bit_array[index] = True

    def might_contain(self, item):
        """Check if item might be in the bloom filter"""
        for i in range(self.num_hashes):
            index = self._hash(item, i + 1)
            if not self.bit_array[index]:
                return False
        return True

class SkipListNode:
    """Node for skip list"""
    def __init__(self, val=None):
        self.val = val
        self.forward = []

class SkipList:
    """Skip List implementation"""
    def __init__(self, max_level=16):
        self.max_level = max_level
        self.head = SkipListNode()
        self.level = 1
        # Initialize head's forward pointers
        self.head.forward = [None] * (max_level + 1)

    def _random_level(self):
        """Random level generator"""
        level = 1
        while level < self.max_level and (1 << level) & 0xFFFF:
            level += 1
        return level

    def insert(self, val):
        """Insert a value into the skip list"""
        update = [None] * (self.max_level + 1)
        current = self.head

        for i in range(self.level, 0, -1):
            while current.forward[i] and current.forward[i].val < val:
                current = current.forward[i]
            update[i] = current

        current = current.forward[1]

        if current is None or current.val != val:
            new_level = self._random_level()

            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.head
                self.level = new_level

            new_node = SkipListNode(val)
            new_node.forward = [None] * (new_level + 1)

            for i in range(1, new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def search(self, val):
        """Search for a value in the skip list"""
        current = self.head

        for i in range(self.level, 0, -1):
            while current.forward[i] and current.forward[i].val < val:
                current = current.forward[i]

        current = current.forward[1]
        return current is not None and current.val == val

class AVLNode:
    """Node for AVL tree"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    """AVL Tree implementation"""
    def __init__(self):
        self.root = None

    def _height(self, node):
        if not node:
            return 0
        return node.height

    def _balance_factor(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))

        return x

    def _left_rotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def insert(self, key):
        """Insert a key into the AVL tree"""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  # Duplicate keys not allowed

        node.height = 1 + max(self._height(node.left), self._height(node.right))

        balance = self._balance_factor(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def search(self, key):
        """Search for a key in the AVL tree"""
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

# Test functions

def test_dsu():
    """Test DSU implementation"""
    dsu = DSU(10)
    dsu.union(1, 2)
    dsu.union(2, 3)
    dsu.union(4, 5)
    
    assert dsu.find(1) == dsu.find(3)
    assert dsu.find(1) != dsu.find(4)
    
    dsu.union(3, 5)
    assert dsu.find(1) == dsu.find(4)
    
    print("DSU tests passed!")


def test_trie():
    """Test Suffix Trie implementation"""
    trie = SuffixTrie()
    trie.insert("apple")
    trie.insert("app")
    
    assert trie.search("apple")
    assert trie.search("app")
    assert not trie.search("apples")
    
    print("Suffix Trie tests passed!")


def test_bloom_filter():
    """Test Bloom Filter implementation"""
    bloom = BloomFilter(100, 3)
    bloom.add("hello")
    bloom.add("world")
    
    assert bloom.might_contain("hello")
    assert bloom.might_contain("world")
    assert not bloom.might_contain("test")
    
    print("Bloom Filter tests passed!")


def test_skip_list():
    """Test Skip List implementation"""
    skip_list = SkipList()
    skip_list.insert(5)
    skip_list.insert(3)
    skip_list.insert(7)
    skip_list.insert(1)
    
    assert skip_list.search(3)
    assert skip_list.search(7)
    assert not skip_list.search(4)
    
    print("Skip List tests passed!")


def test_avl_tree():
    """Test AVL Tree implementation"""
    avl = AVLTree()
    avl.insert(10)
    avl.insert(20)
    avl.insert(30)
    avl.insert(40)
    avl.insert(50)
    avl.insert(25)
    
    assert avl.search(30)
    assert avl.search(25)
    assert not avl.search(35)
    
    print("AVL Tree tests passed!")


if __name__ == "__main__":
    test_dsu()
    test_trie()
    test_bloom_filter()
    test_skip_list()
    test_avl_tree()
    print("All Day 19 tests passed!")