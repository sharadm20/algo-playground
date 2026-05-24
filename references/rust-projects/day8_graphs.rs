// Day 8: Graphs & Graph Traversal
// Topics: Graph representation, BFS, DFS, topological sort, union-find, shortest path algorithms
// Focus: Understanding graph structures, traversal techniques, and common graph algorithms

use std::collections::{HashMap, HashSet, VecDeque, BinaryHeap};
use std::cmp::Reverse;

// ============================================================
// 1. GRAPH REPRESENTATION
// ============================================================

/// Build adjacency list from edge list
fn build_adjacency_list(edges: &[(usize, usize)], directed: bool) -> HashMap<usize, Vec<usize>> {
    let mut adj = HashMap::new();

    for &(u, v) in edges {
        adj.entry(u).or_insert_with(Vec::new).push(v);
        if !directed {
            adj.entry(v).or_insert_with(Vec::new).push(u);
        }
    }

    adj
}

/// Build adjacency matrix from edge list
fn build_adjacency_matrix(edges: &[(usize, usize)], n: usize, directed: bool) -> Vec<Vec<i32>> {
    let mut matrix = vec![vec![0; n]; n];

    for &(u, v) in edges {
        matrix[u][v] = 1;
        if !directed {
            matrix[v][u] = 1;
        }
    }

    matrix
}

// ============================================================
// 2. BFS ON GRAPHS
// ============================================================

/// BFS traversal from start node
fn bfs_traversal(graph: &HashMap<usize, Vec<usize>>, start: usize) -> Vec<usize> {
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    let mut result = Vec::new();

    visited.insert(start);
    queue.push_back(start);

    while let Some(node) = queue.pop_front() {
        result.push(node);

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if visited.insert(neighbor) {
                    queue.push_back(neighbor);
                }
            }
        }
    }

    result
}

/// BFS shortest path (by number of edges)
fn bfs_shortest_path(
    graph: &HashMap<usize, Vec<usize>>,
    start: usize,
    end: usize,
) -> Vec<usize> {
    if start == end {
        return vec![start];
    }

    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();

    visited.insert(start);
    queue.push_back((start, vec![start]));

    while let Some((node, path)) = queue.pop_front() {
        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if visited.insert(neighbor) {
                    let mut new_path = path.clone();
                    new_path.push(neighbor);

                    if neighbor == end {
                        return new_path;
                    }

                    queue.push_back((neighbor, new_path));
                }
            }
        }
    }

    vec![] // No path exists
}

/// Find all connected components in undirected graph
fn bfs_connected_components(
    graph: &HashMap<usize, Vec<usize>>,
    vertices: &[usize],
) -> Vec<Vec<usize>> {
    let mut visited = HashSet::new();
    let mut components = Vec::new();

    for &vertex in vertices {
        if visited.contains(&vertex) {
            continue;
        }

        // BFS to find all nodes in this component
        let mut component = Vec::new();
        let mut queue = VecDeque::new();

        visited.insert(vertex);
        queue.push_back(vertex);

        while let Some(node) = queue.pop_front() {
            component.push(node);

            if let Some(neighbors) = graph.get(&node) {
                for &neighbor in neighbors {
                    if visited.insert(neighbor) {
                        queue.push_back(neighbor);
                    }
                }
            }
        }

        component.sort();
        components.push(component);
    }

    components
}

/// Check if graph is bipartite (2-colorable)
fn is_bipartite(graph: &HashMap<usize, Vec<usize>>, vertices: &[usize]) -> bool {
    let mut color = HashMap::new();

    for &start in vertices {
        if color.contains_key(&start) {
            continue;
        }

        // BFS with coloring
        let mut queue = VecDeque::new();
        queue.push_back(start);
        color.insert(start, 0);

        while let Some(node) = queue.pop_front() {
            let current_color = color[&node];

            if let Some(neighbors) = graph.get(&node) {
                for &neighbor in neighbors {
                    if let Some(&neighbor_color) = color.get(&neighbor) {
                        if neighbor_color == current_color {
                            return false;
                        }
                    } else {
                        color.insert(neighbor, 1 - current_color);
                        queue.push_back(neighbor);
                    }
                }
            }
        }
    }

    true
}

// ============================================================
// 3. DFS ON GRAPHS
// ============================================================

/// DFS traversal using recursion
fn dfs_recursive(
    graph: &HashMap<usize, Vec<usize>>,
    start: usize,
    visited: &mut HashSet<usize>,
) -> Vec<usize> {
    visited.insert(start);
    let mut result = vec![start];

    if let Some(neighbors) = graph.get(&start) {
        for &neighbor in neighbors {
            if !visited.contains(&neighbor) {
                result.extend(dfs_recursive(graph, neighbor, visited));
            }
        }
    }

    result
}

/// DFS traversal using explicit stack
fn dfs_iterative(graph: &HashMap<usize, Vec<usize>>, start: usize) -> Vec<usize> {
    let mut visited = HashSet::new();
    let mut stack = vec![start];
    let mut result = Vec::new();

    while let Some(node) = stack.pop() {
        if visited.contains(&node) {
            continue;
        }

        visited.insert(node);
        result.push(node);

        // Add unvisited neighbors (reverse for correct order)
        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors.iter().rev() {
                if !visited.contains(&neighbor) {
                    stack.push(neighbor);
                }
            }
        }
    }

    result
}

/// Detect cycle in directed graph using DFS
fn dfs_cycle_detection_directed(
    graph: &HashMap<usize, Vec<usize>>,
    vertices: &[usize],
) -> bool {
    const WHITE: i32 = 0;
    const GRAY: i32 = 1;
    const BLACK: i32 = 2;

    let mut color: HashMap<usize, i32> = vertices.iter().map(|&v| (v, WHITE)).collect();

    fn dfs(graph: &HashMap<usize, Vec<usize>>, node: usize, color: &mut HashMap<usize, i32>) -> bool {
        color.insert(node, GRAY);

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if color[&neighbor] == GRAY {
                    return true;
                }
                if color[&neighbor] == WHITE && dfs(graph, neighbor, color) {
                    return true;
                }
            }
        }

        color.insert(node, BLACK);
        false
    }

    for &vertex in vertices {
        if color[&vertex] == WHITE {
            if dfs(graph, vertex, &mut color) {
                return true;
            }
        }
    }

    false
}

/// Detect cycle in undirected graph using DFS
fn dfs_cycle_detection_undirected(
    graph: &HashMap<usize, Vec<usize>>,
    vertices: &[usize],
) -> bool {
    fn dfs(
        graph: &HashMap<usize, Vec<usize>>,
        node: usize,
        parent: usize,
        visited: &mut HashSet<usize>,
    ) -> bool {
        visited.insert(node);

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if !visited.contains(&neighbor) {
                    if dfs(graph, neighbor, node, visited) {
                        return true;
                    }
                } else if neighbor != parent {
                    return true;
                }
            }
        }

        false
    }

    let mut visited = HashSet::new();

    for &vertex in vertices {
        if !visited.contains(&vertex) {
            if dfs(graph, vertex, usize::MAX, &mut visited) {
                return true;
            }
        }
    }

    false
}

/// Find all paths from start to end using DFS
fn dfs_find_all_paths(
    graph: &HashMap<usize, Vec<usize>>,
    start: usize,
    end: usize,
) -> Vec<Vec<usize>> {
    let mut all_paths = Vec::new();

    fn backtrack(
        graph: &HashMap<usize, Vec<usize>>,
        node: usize,
        end: usize,
        path: &mut Vec<usize>,
        visited: &mut HashSet<usize>,
        all_paths: &mut Vec<Vec<usize>>,
    ) {
        if node == end {
            all_paths.push(path.clone());
            return;
        }

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if !visited.contains(&neighbor) {
                    visited.insert(neighbor);
                    path.push(neighbor);
                    backtrack(graph, neighbor, end, path, visited, all_paths);
                    path.pop();
                    visited.remove(&neighbor);
                }
            }
        }
    }

    let mut visited = HashSet::new();
    visited.insert(start);
    backtrack(graph, start, end, &mut vec![start], &mut visited, &mut all_paths);

    all_paths
}

// ============================================================
// 4. TOPOLOGICAL SORT
// ============================================================

/// Topological sort using Kahn's Algorithm (BFS-based)
fn topological_sort_kahn(
    graph: &HashMap<usize, Vec<usize>>,
    vertices: &[usize],
) -> Vec<usize> {
    // Calculate in-degrees
    let mut in_degree: HashMap<usize, i32> = vertices.iter().map(|&v| (v, 0)).collect();

    for &v in vertices {
        if let Some(neighbors) = graph.get(&v) {
            for &neighbor in neighbors {
                *in_degree.entry(neighbor).or_insert(0) += 1;
            }
        }
    }

    // Queue of nodes with in-degree 0
    let mut queue: VecDeque<usize> = vertices
        .iter()
        .filter(|&&v| in_degree[&v] == 0)
        .cloned()
        .collect();

    let mut result = Vec::new();

    while let Some(node) = queue.pop_front() {
        result.push(node);

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                *in_degree.get_mut(&neighbor).unwrap() -= 1;
                if in_degree[&neighbor] == 0 {
                    queue.push_back(neighbor);
                }
            }
        }
    }

    // Check for cycle
    if result.len() != vertices.len() {
        return vec![]; // Cycle detected
    }

    result
}

/// Topological sort using DFS (post-order reversal)
fn topological_sort_dfs(
    graph: &HashMap<usize, Vec<usize>>,
    vertices: &[usize],
) -> Vec<usize> {
    let mut visited = HashSet::new();
    let mut stack = Vec::new();

    fn dfs(
        graph: &HashMap<usize, Vec<usize>>,
        node: usize,
        visited: &mut HashSet<usize>,
        stack: &mut Vec<usize>,
    ) {
        visited.insert(node);

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if !visited.contains(&neighbor) {
                    dfs(graph, neighbor, visited, stack);
                }
            }
        }

        stack.push(node);
    }

    for &vertex in vertices {
        if !visited.contains(&vertex) {
            dfs(graph, vertex, &mut visited, &mut stack);
        }
    }

    stack.reverse();
    stack
}

/// LeetCode #207: Course Schedule
fn can_finish_courses(num_courses: usize, prerequisites: &[(usize, usize)]) -> bool {
    let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
    let mut in_degree: HashMap<usize, i32> = HashMap::new();

    // Initialize
    for i in 0..num_courses {
        in_degree.insert(i, 0);
    }

    // Build graph
    for &(course, prereq) in prerequisites {
        graph.entry(prereq).or_insert_with(Vec::new).push(course);
        *in_degree.get_mut(&course).unwrap() += 1;
    }

    let mut queue: VecDeque<usize> = (0..num_courses)
        .filter(|&c| in_degree[&c] == 0)
        .collect();

    let mut completed = 0;

    while let Some(course) = queue.pop_front() {
        completed += 1;

        if let Some(next_courses) = graph.get(&course) {
            for &next_course in next_courses {
                *in_degree.get_mut(&next_course).unwrap() -= 1;
                if in_degree[&next_course] == 0 {
                    queue.push_back(next_course);
                }
            }
        }
    }

    completed == num_courses
}

/// LeetCode #210: Course Schedule II
fn find_course_order(num_courses: usize, prerequisites: &[(usize, usize)]) -> Vec<usize> {
    let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
    let mut in_degree: HashMap<usize, i32> = HashMap::new();

    for i in 0..num_courses {
        in_degree.insert(i, 0);
    }

    for &(course, prereq) in prerequisites {
        graph.entry(prereq).or_insert_with(Vec::new).push(course);
        *in_degree.get_mut(&course).unwrap() += 1;
    }

    let mut queue: VecDeque<usize> = (0..num_courses)
        .filter(|&c| in_degree[&c] == 0)
        .collect();

    let mut order = Vec::new();

    while let Some(course) = queue.pop_front() {
        order.push(course);

        if let Some(next_courses) = graph.get(&course) {
            for &next_course in next_courses {
                *in_degree.get_mut(&next_course).unwrap() -= 1;
                if in_degree[&next_course] == 0 {
                    queue.push_back(next_course);
                }
            }
        }
    }

    if order.len() == num_courses {
        order
    } else {
        vec![]
    }
}

// ============================================================
// 5. UNION-FIND (DISJOINT SET UNION)
// ============================================================

struct UnionFind {
    parent: Vec<usize>,
    rank: Vec<i32>,
    num_components: usize,
}

impl UnionFind {
    fn new(n: usize) -> Self {
        Self {
            parent: (0..n).collect(),
            rank: vec![0; n],
            num_components: n,
        }
    }

    /// Find root with path compression
    fn find(&mut self, x: usize) -> usize {
        if self.parent[x] != x {
            self.parent[x] = self.find(self.parent[x]);
        }
        self.parent[x]
    }

    /// Union by rank
    fn union(&mut self, x: usize, y: usize) -> bool {
        let root_x = self.find(x);
        let root_y = self.find(y);

        if root_x == root_y {
            return false;
        }

        if self.rank[root_x] < self.rank[root_y] {
            self.parent[root_x] = root_y;
        } else if self.rank[root_x] > self.rank[root_y] {
            self.parent[root_y] = root_x;
        } else {
            self.parent[root_y] = root_x;
            self.rank[root_x] += 1;
        }

        self.num_components -= 1;
        true
    }

    fn connected(&mut self, x: usize, y: usize) -> bool {
        self.find(x) == self.find(y)
    }

    fn get_num_components(&self) -> usize {
        self.num_components
    }
}

/// Count connected components using Union-Find
fn count_connected_components_uf(n: usize, edges: &[(usize, usize)]) -> usize {
    let mut uf = UnionFind::new(n);

    for &(u, v) in edges {
        uf.union(u, v);
    }

    uf.get_num_components()
}

/// Detect cycle in undirected graph using Union-Find
fn has_cycle_undirected_uf(n: usize, edges: &[(usize, usize)]) -> bool {
    let mut uf = UnionFind::new(n);

    for &(u, v) in edges {
        if !uf.union(u, v) {
            return true;
        }
    }

    false
}

/// Kruskal's Minimum Spanning Tree
fn kruskal_mst(n: usize, edges: &[(usize, usize, i32)]) -> Vec<(usize, usize, i32)> {
    let mut sorted_edges = edges.to_vec();
    sorted_edges.sort_by_key(|&(_, _, w)| w);

    let mut uf = UnionFind::new(n);
    let mut mst = Vec::new();

    for &(u, v, weight) in &sorted_edges {
        if uf.union(u, v) {
            mst.push((u, v, weight));

            if mst.len() == n - 1 {
                break;
            }
        }
    }

    mst
}

// ============================================================
// 6. SHORTEST PATH ALGORITHMS
// ============================================================

/// Dijkstra's algorithm
fn dijkstra(
    graph: &HashMap<usize, Vec<(usize, i32)>>,
    start: usize,
    n: usize,
) -> Vec<i64> {
    const INF: i64 = i64::MAX;
    let mut dist = vec![INF; n];
    dist[start] = 0;

    // Min-heap: (distance, node)
    let mut pq = BinaryHeap::new();
    pq.push(Reverse((0i64, start)));

    while let Some(Reverse((d, node))) = pq.pop() {
        if d > dist[node] {
            continue;
        }

        if let Some(neighbors) = graph.get(&node) {
            for &(neighbor, weight) in neighbors {
                let new_dist = dist[node] + weight as i64;

                if new_dist < dist[neighbor] {
                    dist[neighbor] = new_dist;
                    pq.push(Reverse((new_dist, neighbor)));
                }
            }
        }
    }

    dist
}

/// Bellman-Ford algorithm
fn bellman_ford(
    n: usize,
    edges: &[(usize, usize, i32)],
    start: usize,
) -> Vec<i64> {
    const INF: i64 = i64::MAX;
    let mut dist = vec![INF; n];
    dist[start] = 0;

    // Relax all edges V-1 times
    for _ in 0..n - 1 {
        for &(u, v, weight) in edges {
            if dist[u] != INF && dist[u] + weight as i64 < dist[v] {
                dist[v] = dist[u] + weight as i64;
            }
        }
    }

    // Check for negative cycles
    for &(u, v, weight) in edges {
        if dist[u] != INF && dist[u] + weight as i64 < dist[v] {
            return vec![]; // Negative cycle detected
        }
    }

    dist
}

/// Floyd-Warshall algorithm
fn floyd_warshall(n: usize, edges: &[(usize, usize, i32)]) -> Vec<Vec<i64>> {
    const INF: i64 = i64::MAX / 2; // Prevent overflow
    let mut dist = vec![vec![INF; n]; n];

    for i in 0..n {
        dist[i][i] = 0;
    }

    for &(u, v, weight) in edges {
        dist[u][v] = weight as i64;
    }

    // Floyd-Warshall: try each vertex as intermediate
    for k in 0..n {
        for i in 0..n {
            for j in 0..n {
                dist[i][j] = dist[i][j].min(dist[i][k] + dist[k][j]);
            }
        }
    }

    // Check for negative cycles
    for i in 0..n {
        if dist[i][i] < 0 {
            return vec![]; // Negative cycle detected
        }
    }

    dist
}

// ============================================================
// TESTS
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_graph_representation() {
        let edges = vec![(0, 1), (1, 2), (2, 3), (0, 3)];

        // Adjacency list
        let adj = build_adjacency_list(&edges, true);
        assert!(adj[&0].contains(&1));
        assert!(adj[&0].contains(&3));

        // Adjacency matrix
        let matrix = build_adjacency_matrix(&edges, 4, false);
        assert_eq!(matrix[0][1], 1);
        assert_eq!(matrix[1][0], 1); // Undirected
    }

    #[test]
    fn test_bfs() {
        let mut graph = HashMap::new();
        graph.insert(0, vec![1, 2]);
        graph.insert(1, vec![0, 2, 3]);
        graph.insert(2, vec![0, 1, 3, 4]);
        graph.insert(3, vec![1, 2, 4]);
        graph.insert(4, vec![2, 3]);

        // BFS traversal
        let result = bfs_traversal(&graph, 0);
        assert_eq!(result[0], 0);

        // BFS shortest path
        let path = bfs_shortest_path(&graph, 0, 4);
        assert_eq!(path[0], 0);
        assert_eq!(path.last().unwrap(), &4);

        // Connected components
        let mut graph2 = HashMap::new();
        graph2.insert(0, vec![1]);
        graph2.insert(1, vec![0]);
        graph2.insert(2, vec![3]);
        graph2.insert(3, vec![2]);

        let components = bfs_connected_components(&graph2, &[0, 1, 2, 3]);
        assert_eq!(components.len(), 2);

        // Bipartite check
        assert!(is_bipartite(&graph, &[0, 1, 2, 3, 4]));
    }

    #[test]
    fn test_dfs() {
        let mut graph = HashMap::new();
        graph.insert(0, vec![1, 2]);
        graph.insert(1, vec![0, 3]);
        graph.insert(2, vec![0, 3]);
        graph.insert(3, vec![1, 2]);

        // DFS recursive
        let mut visited = HashSet::new();
        let result = dfs_recursive(&graph, 0, &mut visited);
        assert_eq!(result[0], 0);
        assert_eq!(result.len(), 4);

        // DFS iterative
        let result = dfs_iterative(&graph, 0);
        assert_eq!(result[0], 0);
        assert_eq!(result.len(), 4);

        // Cycle detection (directed)
        let mut directed_graph = HashMap::new();
        directed_graph.insert(0, vec![1]);
        directed_graph.insert(1, vec![2]);
        directed_graph.insert(2, vec![0]);

        assert!(dfs_cycle_detection_directed(&directed_graph, &[0, 1, 2]));

        // Find all paths
        let mut simple_graph = HashMap::new();
        simple_graph.insert(0, vec![1, 2]);
        simple_graph.insert(1, vec![2]);
        simple_graph.insert(2, vec![]);

        let paths = dfs_find_all_paths(&simple_graph, 0, 2);
        assert_eq!(paths.len(), 2);
    }

    #[test]
    fn test_topological_sort() {
        let mut graph = HashMap::new();
        graph.insert(0, vec![1, 2]);
        graph.insert(1, vec![3]);
        graph.insert(2, vec![3]);
        graph.insert(3, vec![]);

        let vertices = vec![0, 1, 2, 3];

        let result_kahn = topological_sort_kahn(&graph, &vertices);
        assert_eq!(result_kahn[0], 0);
        assert_eq!(result_kahn.last().unwrap(), &3);

        let result_dfs = topological_sort_dfs(&graph, &vertices);
        assert_eq!(result_dfs[0], 0);

        // Course schedule
        assert!(can_finish_courses(2, &[(1, 0)]));
        assert!(!can_finish_courses(2, &[(1, 0), (0, 1)]));
    }

    #[test]
    fn test_union_find() {
        let mut uf = UnionFind::new(5);

        assert!(!uf.connected(0, 1));
        uf.union(0, 1);
        assert!(uf.connected(0, 1));

        uf.union(1, 2);
        assert!(uf.connected(0, 2));

        assert_eq!(uf.get_num_components(), 3);

        // Connected components
        let edges = vec![(0, 1), (1, 2), (3, 4)];
        assert_eq!(count_connected_components_uf(5, &edges), 2);

        // Cycle detection
        let edges_with_cycle = vec![(0, 1), (1, 2), (2, 0)];
        assert!(has_cycle_undirected_uf(3, &edges_with_cycle));

        // Kruskal's MST
        let edges_weighted = vec![
            (0, 1, 10),
            (0, 2, 6),
            (0, 3, 5),
            (1, 3, 15),
            (2, 3, 4),
        ];
        let mst = kruskal_mst(4, &edges_weighted);
        assert_eq!(mst.len(), 3);
        let total_weight: i32 = mst.iter().map(|&(_, _, w)| w).sum();
        assert_eq!(total_weight, 19);
    }

    #[test]
    fn test_shortest_path() {
        let mut graph = HashMap::new();
        graph.insert(0, vec![(1, 4), (2, 1)]);
        graph.insert(1, vec![(3, 1)]);
        graph.insert(2, vec![(1, 2), (3, 5)]);
        graph.insert(3, vec![]);

        // Dijkstra
        let dist = dijkstra(&graph, 0, 4);
        assert_eq!(dist[0], 0);
        assert_eq!(dist[1], 3); // 0 -> 2 -> 1
        assert_eq!(dist[2], 1);
        assert_eq!(dist[3], 4); // 0 -> 2 -> 1 -> 3

        // Bellman-Ford
        let edges = vec![(0, 1, 4), (0, 2, 1), (1, 3, 1), (2, 1, 2), (2, 3, 5)];
        let dist_bf = bellman_ford(4, &edges, 0);
        assert_eq!(dist_bf[1], 3);
        assert_eq!(dist_bf[3], 4);

        // Floyd-Warshall
        let fw_result = floyd_warshall(4, &edges);
        assert_eq!(fw_result[0][3], 4);
        assert_eq!(fw_result[0][2], 1);

        // Negative cycle detection
        let edges_neg_cycle = vec![(0, 1, 1), (1, 2, -1), (2, 0, -1)];
        assert!(bellman_ford(3, &edges_neg_cycle, 0).is_empty());
    }
}
