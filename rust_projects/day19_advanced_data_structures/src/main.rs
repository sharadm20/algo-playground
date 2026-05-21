// Day 19: Advanced Data Structures - Rust Implementations

use std::collections::HashMap;

// Disjoint Set Union (Union-Find)
struct DSU {
    parent: Vec<usize>,
    rank: Vec<usize>,
}

impl DSU {
    fn new(size: usize) -> Self {
        DSU {
            parent: (0..size).collect(),
            rank: vec![0; size],
        }
    }

    fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            self.parent[x] = self.find(self.parent[x]); // Path compression
        }
        self.parent[x]
    }

    fn union(&mut self, x: usize, y: usize) {
        let x_root = self.find(x);
        let y_root = self.find(y);

        if x_root == y_root {
            return;
        }

        // Union by rank
        if self.rank[x_root] < self.rank[y_root] {
            self.parent[x_root] = y_root;
        } else if self.rank[x_root] > self.rank[y_root] {
            self.parent[y_root] = x_root;
        } else {
            self.parent[y_root] = x_root;
            self.rank[x_root] += 1;
        }
    }
}

// Trie Node for Suffix Trie
#[derive(Debug, Default)]
struct TrieNode {
    children: HashMap<char, TrieNode>,
    is_end: bool,
}

// Suffix Trie
#[derive(Debug, Default)]
struct SuffixTrie {
    root: TrieNode,
}

impl SuffixTrie {
    fn new() -> Self {
        SuffixTrie {
            root: TrieNode::default(),
        }
    }

    fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;
        for c in word.chars() {
            node = node.children.entry(c).or_default();
        }
        node.is_end = true;
    }

    fn search(&self, word: &str) -> bool {
        let mut node = &self.root;
        for c in word.chars() {
            if let Some(next_node) = node.children.get(&c) {
                node = next_node;
            } else {
                return false;
            }
        }
        node.is_end
    }
}

// Bloom Filter
struct BloomFilter {
    size: usize,
    num_hashes: usize,
    bit_array: Vec<bool>,
}

impl BloomFilter {
    fn new(size: usize, num_hashes: usize) -> Self {
        BloomFilter {
            size,
            num_hashes,
            bit_array: vec![false; size],
        }
    }

    fn hash(&self, item: &str, seed: usize) -> usize {
        let mut result: u32 = 0;
        for byte in item.as_bytes() {
            result = result.wrapping_mul(seed as u32).wrapping_add(*byte as u32);
        }
        (result % self.size as u32) as usize
    }

    fn add(&mut self, item: &str) {
        for i in 1..=self.num_hashes {
            let index = self.hash(item, i);
            self.bit_array[index] = true;
        }
    }

    fn might_contain(&self, item: &str) -> bool {
        for i in 1..=self.num_hashes {
            let index = self.hash(item, i);
            if !self.bit_array[index] {
                return false;
            }
        }
        true
    }
}

// Skip List Node
#[derive(Clone)]
struct SkipListNode {
    val: i32,
    forward: Vec<Option<Box<SkipListNode>>>, // Using Option for easier handling
}

// Skip List
struct SkipList {
    max_level: usize,
    head: SkipListNode,
    level: usize,
}

impl SkipList {
    fn new(max_level: usize) -> Self {
        SkipList {
            max_level,
            head: SkipListNode {
                val: i32::MIN, // Use minimum value for head
                forward: vec![None; max_level + 1],
            },
            level: 1,
        }
    }

    fn random_level(&self) -> usize {
        let mut level = 1;
        while level < self.max_level && (1 << level) & 0xFFFF != 0 {
            level += 1;
        }
        level
    }

    fn insert(&mut self, val: i32) {
        let mut update = vec![None; self.max_level + 1];
        let mut current = &self.head;

        for i in (1..=self.level).rev() {
            while let Some(ref node) = current.forward[i] {
                if node.val < val {
                    current = node;
                } else {
                    break;
                }
            }
            update[i] = Some(current as *const SkipListNode);
        }

        let current_next = current.forward[1].as_ref();

        if current_next.is_none() || current_next.unwrap().val != val {
            let new_level = self.random_level();

            if new_level > self.level {
                for i in self.level + 1..=new_level {
                    update[i] = Some(&self.head as *const SkipListNode);
                }
                self.level = new_level;
            }

            let mut new_node = Box::new(SkipListNode {
                val,
                forward: vec![None; new_level + 1],
            });

            for i in 1..=new_level {
                let update_node = unsafe { &mut *(update[i].unwrap() as *mut SkipListNode) };
                new_node.forward[i] = update_node.forward[i].take();
                update_node.forward[i] = Some(new_node.clone());
            }
        }
    }

    fn search(&self, val: i32) -> bool {
        let mut current = &self.head;

        for i in (1..=self.level).rev() {
            while let Some(ref node) = current.forward[i] {
                if node.val < val {
                    current = node;
                } else {
                    break;
                }
            }
        }

        let current_next = current.forward[1].as_ref();
        current_next.is_some() && current_next.unwrap().val == val
    }
}

// AVL Tree Node
#[derive(Clone)]
struct AVLNode {
    key: i32,
    left: Option<Box<AVLNode>>,
    right: Option<Box<AVLNode>>,
    height: i32,
}

impl AVLNode {
    fn new(key: i32) -> Self {
        AVLNode {
            key,
            left: None,
            right: None,
            height: 1,
        }
    }
}

// AVL Tree
struct AVLTree {
    root: Option<Box<AVLNode>>,
}

impl AVLTree {
    fn new() -> Self {
        AVLTree { root: None }
    }

    fn height(&self, node: &Option<Box<AVLNode>>) -> i32 {
        node.as_ref().map_or(0, |n| n.height)
    }

    fn balance_factor(&self, node: &Option<Box<AVLNode>>) -> i32 {
        if let Some(n) = node {
            self.height(&n.left) - self.height(&n.right)
        } else {
            0
        }
    }

    fn right_rotate(&self, y: Box<AVLNode>) -> Box<AVLNode> {
        let mut x = y.left.unwrap();
        let t2 = x.right.take();

        x.right = Some(y);
        let y_mut = x.right.as_mut().unwrap();
        y_mut.left = t2;

        y_mut.height = 1 + std::cmp::max(self.height(&y_mut.left), self.height(&y_mut.right));
        x.height = 1 + std::cmp::max(self.height(&x.left), self.height(&x.right));

        x
    }

    fn left_rotate(&self, x: Box<AVLNode>) -> Box<AVLNode> {
        let mut y = x.right.unwrap();
        let t2 = y.left.take();

        y.left = Some(x);
        let x_mut = y.left.as_mut().unwrap();
        x_mut.right = t2;

        x_mut.height = 1 + std::cmp::max(self.height(&x_mut.left), self.height(&x_mut.right));
        y.height = 1 + std::cmp::max(self.height(&y.left), self.height(&y.right));

        y
    }

    fn insert(&mut self, key: i32) {
        self.root = self._insert(self.root.take(), key);
    }

    fn _insert(&self, node: Option<Box<AVLNode>>, key: i32) -> Option<Box<AVLNode>> {
        let mut node = node;
        if node.is_none() {
            return Some(Box::new(AVLNode::new(key)));
        }

        let node_mut = node.as_mut().unwrap();
        if key < node_mut.key {
            node_mut.left = self._insert(node_mut.left.take(), key);
        } else if key > node_mut.key {
            node_mut.right = self._insert(node_mut.right.take(), key);
        } else {
            return node; // Duplicate keys not allowed
        }

        node_mut.height = 1 + std::cmp::max(
            self.height(&node_mut.left),
            self.height(&node_mut.right),
        );

        let balance = self.balance_factor(&self.root);

        // Left Left Case
        if balance > 1 && key < node_mut.left.as_ref().unwrap().key {
            return Some(self.right_rotate(node.unwrap()));
        }

        // Right Right Case
        if balance < -1 && key > node_mut.right.as_ref().unwrap().key {
            return Some(self.left_rotate(node.unwrap()));
        }

        // Left Right Case
        if balance > 1 && key > node_mut.left.as_ref().unwrap().key {
            let left = node_mut.left.take().unwrap();
            node_mut.left = Some(self.left_rotate(left));
            return Some(self.right_rotate(node.unwrap()));
        }

        // Right Left Case
        if balance < -1 && key < node_mut.right.as_ref().unwrap().key {
            let right = node_mut.right.take().unwrap();
            node_mut.right = Some(self.right_rotate(right));
            return Some(self.left_rotate(node.unwrap()));
        }

        node
    }

    fn search(&self, key: i32) -> bool {
        self._search(&self.root, key)
    }

    fn _search(&self, node: &Option<Box<AVLNode>>, key: i32) -> bool {
        if let Some(n) = node {
            if n.key == key {
                return true;
            } else if key < n.key {
                return self._search(&n.left, key);
            } else {
                return self._search(&n.right, key);
            }
        }
        false
    }
}

fn main() {
    println!("Day 19: Advanced Data Structures - Rust Implementations");
    println!("Run tests with: cargo test");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dsu() {
        let mut dsu = DSU::new(10);
        dsu.union(1, 2);
        dsu.union(2, 3);
        dsu.union(4, 5);

        assert_eq!(dsu.find(1), dsu.find(3));
        assert_ne!(dsu.find(1), dsu.find(4));

        dsu.union(3, 5);
        assert_eq!(dsu.find(1), dsu.find(4));
    }

    #[test]
    fn test_trie() {
        let mut trie = SuffixTrie::new();
        trie.insert("apple");
        trie.insert("app");

        assert!(trie.search("apple"));
        assert!(trie.search("app"));
        assert!(!trie.search("apples"));
    }

    #[test]
    fn test_bloom_filter() {
        let mut bloom = BloomFilter::new(100, 3);
        bloom.add("hello");
        bloom.add("world");

        assert!(bloom.might_contain("hello"));
        assert!(bloom.might_contain("world"));
        assert!(!bloom.might_contain("test"));
    }

    #[test]
    fn test_skip_list() {
        let mut skip_list = SkipList::new(16);
        skip_list.insert(5);
        skip_list.insert(3);
        skip_list.insert(7);
        skip_list.insert(1);

        assert!(skip_list.search(3));
        assert!(skip_list.search(7));
        assert!(!skip_list.search(4));
    }

    #[test]
    fn test_avl_tree() {
        let mut avl = AVLTree::new();
        avl.insert(10);
        avl.insert(20);
        avl.insert(30);
        avl.insert(40);
        avl.insert(50);
        avl.insert(25);

        assert!(avl.search(30));
        assert!(avl.search(25));
        assert!(!avl.search(35));
    }
}