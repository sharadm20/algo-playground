// Day 9: Advanced Graph Algorithms
// Topics: Strongly connected components, articulation points & bridges, network flow
// Focus: Advanced graph algorithms for connectivity analysis and flow optimization

use std::collections::{HashMap, HashSet, VecDeque};

// ============================================================
// 1. STRONGLY CONNECTED COMPONENTS - TARJAN'S ALGORITHM
// ============================================================

struct TarjanSCC {
    timer: usize,
    discovery: HashMap<usize, usize>,
    low_link: HashMap<usize, usize>,
    on_stack: HashSet<usize>,
    stack: Vec<usize>,
    sccs: Vec<Vec<usize>>,
}

impl TarjanSCC {
    fn new() -> Self {
        Self {
            timer: 0,
            discovery: HashMap::new(),
            low_link: HashMap::new(),
            on_stack: HashSet::new(),
            stack: Vec::new(),
            sccs: Vec::new(),
        }
    }

    fn find_sccs(&mut self, graph: &HashMap<usize, Vec<usize>>) -> Vec<Vec<usize>> {
        for &node in graph.keys() {
            if !self.discovery.contains_key(&node) {
                self.dfs(graph, node);
            }
        }
        self.sccs.clone()
    }

    fn dfs(&mut self, graph: &HashMap<usize, Vec<usize>>, node: usize) {
        self.discovery.insert(node, self.timer);
        self.low_link.insert(node, self.timer);
        self.timer += 1;
        self.stack.push(node);
        self.on_stack.insert(node);

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if !self.discovery.contains_key(&neighbor) {
                    self.dfs(graph, neighbor);
                    let low_neighbor = *self.low_link.get(&neighbor).unwrap();
                    let low_node = *self.low_link.get(&node).unwrap();
                    self.low_link.insert(node, low_node.min(low_neighbor));
                } else if self.on_stack.contains(&neighbor) {
                    let disc_neighbor = *self.discovery.get(&neighbor).unwrap();
                    let low_node = *self.low_link.get(&node).unwrap();
                    self.low_link.insert(node, low_node.min(disc_neighbor));
                }
            }
        }

        if self.low_link[&node] == self.discovery[&node] {
            let mut scc = Vec::new();
            loop {
                let w = self.stack.pop().unwrap();
                self.on_stack.remove(&w);
                scc.push(w);
                if w == node {
                    break;
                }
            }
            self.sccs.push(scc);
        }
    }
}

// ============================================================
// 2. STRONGLY CONNECTED COMPONENTS - KOSARAJU'S ALGORITHM
// ============================================================

struct KosarajuSCC;

impl KosarajuSCC {
    fn new() -> Self {
        Self
    }

    fn find_sccs(&self, graph: &HashMap<usize, Vec<usize>>) -> Vec<Vec<usize>> {
        // Step 1: Fill stack by finish time
        let mut visited = HashSet::new();
        let mut stack = Vec::new();

        for &node in graph.keys() {
            if !visited.contains(&node) {
                Self::dfs1(graph, node, &mut visited, &mut stack);
            }
        }

        // Step 2: Create reverse graph
        let mut reverse_graph: HashMap<usize, Vec<usize>> = HashMap::new();
        for (&u, neighbors) in graph {
            for &v in neighbors {
                reverse_graph.entry(v).or_insert_with(Vec::new).push(u);
            }
        }

        // Step 3: Process by stack order on reverse graph
        visited.clear();
        let mut sccs = Vec::new();

        while let Some(node) = stack.pop() {
            if !visited.contains(&node) {
                let mut scc = Vec::new();
                Self::dfs2(&reverse_graph, node, &mut visited, &mut scc);
                sccs.push(scc);
            }
        }

        sccs
    }

    fn dfs1(
        graph: &HashMap<usize, Vec<usize>>,
        node: usize,
        visited: &mut HashSet<usize>,
        stack: &mut Vec<usize>,
    ) {
        visited.insert(node);
        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if !visited.contains(&neighbor) {
                    Self::dfs1(graph, neighbor, visited, stack);
                }
            }
        }
        stack.push(node);
    }

    fn dfs2(
        graph: &HashMap<usize, Vec<usize>>,
        node: usize,
        visited: &mut HashSet<usize>,
        scc: &mut Vec<usize>,
    ) {
        visited.insert(node);
        scc.push(node);
        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if !visited.contains(&neighbor) {
                    Self::dfs2(graph, neighbor, visited, scc);
                }
            }
        }
    }
}

// ============================================================
// 3. ARTICULATION POINTS & BRIDGES
// ============================================================

struct ArticulationPointsAndBridges {
    timer: usize,
    discovery: HashMap<usize, usize>,
    low_link: HashMap<usize, usize>,
    articulation_points: HashSet<usize>,
    bridges: Vec<(usize, usize)>,
}

impl ArticulationPointsAndBridges {
    fn new() -> Self {
        Self {
            timer: 0,
            discovery: HashMap::new(),
            low_link: HashMap::new(),
            articulation_points: HashSet::new(),
            bridges: Vec::new(),
        }
    }

    fn find(
        &mut self,
        graph: &HashMap<usize, Vec<usize>>,
        nodes: &[usize],
    ) -> (HashSet<usize>, Vec<(usize, usize)>) {
        for &node in nodes {
            if !self.discovery.contains_key(&node) {
                self.dfs(graph, node, None);
            }
        }
        (self.articulation_points.clone(), self.bridges.clone())
    }

    fn dfs(&mut self, graph: &HashMap<usize, Vec<usize>>, node: usize, parent: Option<usize>) {
        self.discovery.insert(node, self.timer);
        self.low_link.insert(node, self.timer);
        self.timer += 1;
        let mut children = 0;

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if Some(neighbor) == parent {
                    continue;
                }

                if self.discovery.contains_key(&neighbor) {
                    // Back edge
                    let disc_neighbor = *self.discovery.get(&neighbor).unwrap();
                    let low_node = *self.low_link.get(&node).unwrap();
                    self.low_link.insert(node, low_node.min(disc_neighbor));
                } else {
                    // Tree edge
                    children += 1;
                    self.dfs(graph, neighbor, Some(node));
                    let low_neighbor = *self.low_link.get(&neighbor).unwrap();
                    let low_node = *self.low_link.get(&node).unwrap();
                    self.low_link.insert(node, low_node.min(low_neighbor));

                    // Articulation point condition
                    if parent.is_some() && low_neighbor >= self.discovery[&node] {
                        self.articulation_points.insert(node);
                    }

                    // Bridge condition
                    if low_neighbor > self.discovery[&node] {
                        self.bridges.push((node, neighbor));
                    }
                }
            }
        }

        // Root is articulation point if it has more than one child
        if parent.is_none() && children > 1 {
            self.articulation_points.insert(node);
        }
    }
}

// ============================================================
// 4. EDMONDS-KARP MAX FLOW
// ============================================================

fn edmonds_karp(
    capacity: &HashMap<(usize, usize), usize>,
    source: usize,
    sink: usize,
    nodes: &HashSet<usize>,
) -> usize {
    // Build residual graph
    let mut residual: HashMap<usize, HashMap<usize, usize>> = HashMap::new();
    for ((u, v), cap) in capacity {
        residual.entry(*u).or_default().insert(*v, *cap);
        residual.entry(*v).or_default().entry(*u).or_insert(0);
    }

    let mut total_flow = 0;

    loop {
        // BFS to find augmenting path
        let mut parent: HashMap<usize, usize> = HashMap::new();
        let mut visited = HashSet::new();
        visited.insert(source);
        let mut queue = VecDeque::new();
        queue.push_back((source, usize::MAX));
        let mut flow_to_sink = 0;

        while let Some((node, flow)) = queue.pop_front() {
            if node == sink {
                flow_to_sink = flow;
                break;
            }

            if let Some(neighbors) = residual.get(&node) {
                for (&neighbor, &cap) in neighbors {
                    if !visited.contains(&neighbor) && cap > 0 {
                        visited.insert(neighbor);
                        parent.insert(neighbor, node);
                        let new_flow = flow.min(cap);
                        queue.push_back((neighbor, new_flow));
                    }
                }
            }
        }

        if flow_to_sink == 0 {
            break;
        }

        // Update residual capacities
        total_flow += flow_to_sink;
        let mut node = sink;
        while node != source {
            let prev = parent[&node];
            *residual.get_mut(&prev).unwrap().get_mut(&node).unwrap() -= flow_to_sink;
            *residual.entry(node).or_default().entry(prev).or_insert(0) += flow_to_sink;
            node = prev;
        }
    }

    total_flow
}

// ============================================================
// 5. BIPARTITE MATCHING
// ============================================================

fn max_bipartite_matching(
    graph: &HashMap<usize, Vec<usize>>,
    left_size: usize,
    _right_size: usize,
) -> usize {
    let mut match_right: HashMap<usize, usize> = HashMap::new();
    let mut result = 0;

    for u in 0..left_size {
        let mut seen = HashSet::new();
        if dfs_bipartite(graph, u, &mut seen, &mut match_right) {
            result += 1;
        }
    }

    result
}

fn dfs_bipartite(
    graph: &HashMap<usize, Vec<usize>>,
    u: usize,
    seen: &mut HashSet<usize>,
    match_right: &mut HashMap<usize, usize>,
) -> bool {
    if let Some(neighbors) = graph.get(&u) {
        for &v in neighbors {
            if !seen.contains(&v) {
                seen.insert(v);

                let matched = match_right.get(&v).copied();
                if matched.is_none()
                    || dfs_bipartite(graph, matched.unwrap(), seen, match_right)
                {
                    match_right.insert(v, u);
                    return true;
                }
            }
        }
    }
    false
}

// ============================================================
// 6. CRITICAL CONNECTIONS IN NETWORK
// ============================================================

fn find_critical_connections(n: usize, connections: &[(usize, usize)]) -> Vec<(usize, usize)> {
    let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
    for &(u, v) in connections {
        graph.entry(u).or_default().push(v);
        graph.entry(v).or_default().push(u);
    }

    let mut discovery = vec![usize::MAX; n];
    let mut low_link = vec![usize::MAX; n];
    let mut timer: usize = 0;
    let mut critical = Vec::new();

    fn dfs(
        node: usize,
        parent: Option<usize>,
        graph: &HashMap<usize, Vec<usize>>,
        discovery: &mut Vec<usize>,
        low_link: &mut Vec<usize>,
        timer: &mut usize,
        critical: &mut Vec<(usize, usize)>,
    ) {
        discovery[node] = *timer;
        low_link[node] = *timer;
        *timer += 1;

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                if Some(neighbor) == parent {
                    continue;
                }

                if discovery[neighbor] == usize::MAX {
                    dfs(
                        neighbor,
                        Some(node),
                        graph,
                        discovery,
                        low_link,
                        timer,
                        critical,
                    );
                    low_link[node] = low_link[node].min(low_link[neighbor]);

                    if low_link[neighbor] > discovery[node] {
                        critical.push((node, neighbor));
                    }
                } else {
                    low_link[node] = low_link[node].min(discovery[neighbor]);
                }
            }
        }
    }

    for i in 0..n {
        if discovery[i] == usize::MAX {
            dfs(i, None, &graph, &mut discovery, &mut low_link, &mut timer, &mut critical);
        }
    }

    critical
}

// ============================================================
// TESTS
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tarjan_scc() {
        let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
        graph.insert(0, vec![1]);
        graph.insert(1, vec![2]);
        graph.insert(2, vec![0]);
        graph.insert(3, vec![4]);
        graph.insert(4, vec![5]);
        graph.insert(5, vec![3, 6]);
        graph.insert(6, vec![5]);
        graph.insert(7, vec![8]);
        graph.insert(8, vec![7]);

        let mut tarjan = TarjanSCC::new();
        let sccs = tarjan.find_sccs(&graph);

        assert_eq!(sccs.len(), 3, "Expected 3 SCCs");
        println!("✓ test_tarjan_scc passed");
    }

    #[test]
    fn test_kosaraju_scc() {
        let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
        graph.insert(0, vec![1]);
        graph.insert(1, vec![2]);
        graph.insert(2, vec![0]);
        graph.insert(3, vec![4]);
        graph.insert(4, vec![5]);
        graph.insert(5, vec![3, 6]);
        graph.insert(6, vec![5]);
        graph.insert(7, vec![8]);
        graph.insert(8, vec![7]);

        let kosaraju = KosarajuSCC::new();
        let sccs = kosaraju.find_sccs(&graph);

        assert_eq!(sccs.len(), 3, "Expected 3 SCCs");
        println!("✓ test_kosaraju_scc passed");
    }

    #[test]
    fn test_articulation_points_and_bridges() {
        let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
        graph.insert(0, vec![1]);
        graph.insert(1, vec![0, 2]);
        graph.insert(2, vec![1, 3]);
        graph.insert(3, vec![2, 4]);
        graph.insert(4, vec![3]);

        let mut finder = ArticulationPointsAndBridges::new();
        let nodes = vec![0, 1, 2, 3, 4];
        let (art_points, bridges) = finder.find(&graph, &nodes);

        assert!(art_points.contains(&1), "Node 1 should be articulation point");
        assert!(art_points.contains(&2), "Node 2 should be articulation point");
        assert!(art_points.contains(&3), "Node 3 should be articulation point");
        assert_eq!(bridges.len(), 4, "Expected 4 bridges");
        println!("✓ test_articulation_points_and_bridges passed");
    }

    #[test]
    fn test_edmonds_karp() {
        let mut capacity: HashMap<(usize, usize), usize> = HashMap::new();
        capacity.insert((0, 1), 16);
        capacity.insert((0, 2), 13);
        capacity.insert((1, 2), 10);
        capacity.insert((1, 3), 12);
        capacity.insert((2, 1), 4);
        capacity.insert((2, 4), 14);
        capacity.insert((3, 2), 9);
        capacity.insert((3, 5), 20);
        capacity.insert((4, 3), 7);
        capacity.insert((4, 5), 4);

        let nodes: HashSet<usize> = (0..6).collect();
        let max_flow = edmonds_karp(&capacity, 0, 5, &nodes);

        assert_eq!(max_flow, 23, "Expected max flow 23");
        println!("✓ test_edmonds_karp passed");
    }

    #[test]
    fn test_bipartite_matching() {
        let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
        graph.insert(0, vec![0, 1]);
        graph.insert(1, vec![2, 3]);
        graph.insert(2, vec![0]);

        let matching = max_bipartite_matching(&graph, 3, 4);

        assert_eq!(matching, 3, "Expected matching size 3");
        println!("✓ test_bipartite_matching passed");
    }

    #[test]
    fn test_critical_connections() {
        let n = 6;
        let connections = vec![
            (0, 1),
            (1, 2),
            (2, 0), // Cycle 0-1-2
            (1, 3), // Bridge
            (3, 4),
            (4, 5),
            (5, 3), // Cycle 3-4-5
        ];

        let critical = find_critical_connections(n, &connections);

        assert_eq!(critical.len(), 1, "Expected 1 critical connection");
        assert!(
            critical.contains(&(1, 3)) || critical.contains(&(3, 1)),
            "Edge (1,3) should be critical"
        );
        println!("✓ test_critical_connections passed");
    }

    #[test]
    fn test_tarjan_scc_single_cycle() {
        let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
        graph.insert(0, vec![1]);
        graph.insert(1, vec![2]);
        graph.insert(2, vec![0]);

        let mut tarjan = TarjanSCC::new();
        let sccs = tarjan.find_sccs(&graph);

        assert_eq!(sccs.len(), 1, "Single cycle should have 1 SCC");
        assert_eq!(sccs[0].len(), 3, "All nodes should be in one SCC");
        println!("✓ test_tarjan_scc_single_cycle passed");
    }

    #[test]
    fn test_articulation_points_linear() {
        let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
        graph.insert(0, vec![1]);
        graph.insert(1, vec![0, 2]);
        graph.insert(2, vec![1, 3]);
        graph.insert(3, vec![2]);

        let mut finder = ArticulationPointsAndBridges::new();
        let nodes = vec![0, 1, 2, 3];
        let (art_points, bridges) = finder.find(&graph, &nodes);

        assert!(art_points.contains(&1));
        assert!(art_points.contains(&2));
        assert_eq!(bridges.len(), 3);
        println!("✓ test_articulation_points_linear passed");
    }
}

fn main() {
    println!("Day 9: Advanced Graph Algorithms");
    println!("{}", "=".repeat(60));

    // Test Tarjan's SCC
    println!("\nTesting Tarjan's SCC Algorithm...");
    let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();
    graph.insert(0, vec![1]);
    graph.insert(1, vec![2]);
    graph.insert(2, vec![0]);
    graph.insert(3, vec![4]);
    graph.insert(4, vec![5]);
    graph.insert(5, vec![3, 6]);
    graph.insert(6, vec![5]);

    let mut tarjan = TarjanSCC::new();
    let sccs = tarjan.find_sccs(&graph);
    println!("Found {} SCCs", sccs.len());

    // Test Edmonds-Karp
    println!("\nTesting Edmonds-Karp Max Flow...");
    let mut capacity: HashMap<(usize, usize), usize> = HashMap::new();
    capacity.insert((0, 1), 16);
    capacity.insert((0, 2), 13);
    capacity.insert((1, 3), 12);
    capacity.insert((2, 1), 4);
    capacity.insert((2, 4), 14);
    capacity.insert((3, 2), 9);
    capacity.insert((3, 5), 20);
    capacity.insert((4, 3), 7);
    capacity.insert((4, 5), 4);

    let nodes: HashSet<usize> = (0..6).collect();
    let max_flow = edmonds_karp(&capacity, 0, 5, &nodes);
    println!("Max Flow: {}", max_flow);

    // Test Critical Connections
    println!("\nTesting Critical Connections...");
    let connections = vec![(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 5), (5, 3)];
    let critical = find_critical_connections(6, &connections);
    println!("Found {} critical connections", critical.len());

    println!("\n{}", "=".repeat(60));
    println!("Run 'cargo test' to run all tests");
}
