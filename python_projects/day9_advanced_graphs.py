"""
Day 9: Advanced Graph Algorithms
Topics: Strongly connected components, articulation points & bridges, network flow
Focus: Advanced graph algorithms for connectivity analysis and flow optimization
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import deque, defaultdict


# ============================================================
# 1. STRONGLY CONNECTED COMPONENTS (SCC)
# ============================================================

class TarjanSCC:
    """
    Tarjan's Algorithm for finding Strongly Connected Components.
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    A strongly connected component is a maximal subset of vertices where
    every vertex is reachable from every other vertex in the subset.
    """
    
    def __init__(self):
        self.timer = 0
        self.discovery = {}  # discovery time of each node
        self.low_link = {}   # lowest discovery time reachable
        self.on_stack = set()
        self.stack = []
        self.sccs = []
    
    def find_sccs(self, graph: Dict[int, List[int]]) -> List[List[int]]:
        """
        Find all strongly connected components using Tarjan's algorithm.
        
        Args:
            graph: Adjacency list representation of directed graph
            
        Returns:
            List of SCCs, where each SCC is a list of vertices
        """
        self.timer = 0
        self.discovery = {}
        self.low_link = {}
        self.on_stack = set()
        self.stack = []
        self.sccs = []
        
        for node in graph:
            if node not in self.discovery:
                self._dfs(graph, node)
        
        return self.sccs
    
    def _dfs(self, graph: Dict[int, List[int]], node: int):
        """DFS to find SCCs"""
        self.discovery[node] = self.timer
        self.low_link[node] = self.timer
        self.timer += 1
        self.stack.append(node)
        self.on_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in self.discovery:
                # Tree edge
                self._dfs(graph, neighbor)
                self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
            elif neighbor in self.on_stack:
                # Back edge
                self.low_link[node] = min(self.low_link[node], self.discovery[neighbor])
        
        # If node is root of SCC
        if self.low_link[node] == self.discovery[node]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack.remove(w)
                scc.append(w)
                if w == node:
                    break
            self.sccs.append(scc)


class KosarajuSCC:
    """
    Kosaraju's Algorithm for finding Strongly Connected Components.
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Uses two DFS passes:
    1. Fill stack by finish time (reverse post-order)
    2. Process vertices in reverse graph by stack order
    """
    
    def find_sccs(self, graph: Dict[int, List[int]]) -> List[List[int]]:
        """
        Find all strongly connected components using Kosaraju's algorithm.
        
        Args:
            graph: Adjacency list representation of directed graph
            
        Returns:
            List of SCCs, where each SCC is a list of vertices
        """
        # Step 1: Fill stack by finish time
        visited = set()
        stack = []
        
        for node in graph:
            if node not in visited:
                self._dfs1(graph, node, visited, stack)
        
        # Step 2: Create reverse graph
        reverse_graph = defaultdict(list)
        for u in graph:
            for v in graph[u]:
                reverse_graph[v].append(u)
        
        # Step 3: Process by stack order on reverse graph
        visited.clear()
        sccs = []
        
        while stack:
            node = stack.pop()
            if node not in visited:
                scc = []
                self._dfs2(reverse_graph, node, visited, scc)
                sccs.append(scc)
        
        return sccs
    
    def _dfs1(self, graph: Dict[int, List[int]], node: int, visited: Set[int], stack: List[int]):
        """First DFS to fill stack by finish time"""
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                self._dfs1(graph, neighbor, visited, stack)
        stack.append(node)
    
    def _dfs2(self, graph: Dict[int, List[int]], node: int, visited: Set[int], scc: List[int]):
        """Second DFS on reverse graph to collect SCC"""
        visited.add(node)
        scc.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                self._dfs2(graph, neighbor, visited, scc)


# ============================================================
# 2. ARTICULATION POINTS & BRIDGES
# ============================================================

class ArticulationPointsAndBridges:
    """
    Find articulation points (cut vertices) and bridges (cut edges) in undirected graphs.
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Articulation Point: A vertex whose removal increases number of connected components.
    Bridge: An edge whose removal increases number of connected components.
    """
    
    def __init__(self):
        self.timer = 0
        self.discovery = {}
        self.low_link = {}
        self.articulation_points = set()
        self.bridges = []
    
    def find(self, graph: Dict[int, List[int]], num_nodes: int) -> Tuple[Set[int], List[Tuple[int, int]]]:
        """
        Find all articulation points and bridges.
        
        Args:
            graph: Adjacency list representation of undirected graph
            num_nodes: Total number of nodes
            
        Returns:
            Tuple of (articulation_points, bridges)
        """
        self.timer = 0
        self.discovery = {}
        self.low_link = {}
        self.articulation_points = set()
        self.bridges = []
        
        for node in range(num_nodes):
            if node not in self.discovery:
                self._dfs(graph, node, parent=-1)
        
        return self.articulation_points, self.bridges
    
    def _dfs(self, graph: Dict[int, List[int]], node: int, parent: int):
        """DFS to find articulation points and bridges"""
        self.discovery[node] = self.timer
        self.low_link[node] = self.timer
        self.timer += 1
        children = 0
        
        for neighbor in graph.get(node, []):
            if neighbor == parent:
                continue
            
            if neighbor in self.discovery:
                # Back edge
                self.low_link[node] = min(self.low_link[node], self.discovery[neighbor])
            else:
                # Tree edge
                children += 1
                self._dfs(graph, neighbor, node)
                self.low_link[node] = min(self.low_link[node], self.low_link[neighbor])
                
                # Articulation point condition
                if parent != -1 and self.low_link[neighbor] >= self.discovery[node]:
                    self.articulation_points.add(node)
                
                # Bridge condition
                if self.low_link[neighbor] > self.discovery[node]:
                    self.bridges.append((node, neighbor))
        
        # Root is articulation point if it has more than one child
        if parent == -1 and children > 1:
            self.articulation_points.add(node)


# ============================================================
# 3. NETWORK FLOW - FORD-FULKERSON & EDMONDS-KARP
# ============================================================

class FordFulkerson:
    """
    Ford-Fulkerson Algorithm for maximum flow.
    Time Complexity: O(f* * E) where f* is max flow value
    Space Complexity: O(V + E)
    
    Uses DFS to find augmenting paths.
    """
    
    def max_flow(self, capacity: Dict[Tuple[int, int], int], source: int, sink: int, nodes: Set[int]) -> int:
        """
        Calculate maximum flow using DFS-based augmenting paths.
        
        Args:
            capacity: Dictionary mapping (u, v) -> capacity
            source: Source node
            sink: Sink node
            nodes: Set of all nodes
            
        Returns:
            Maximum flow from source to sink
        """
        # Build residual graph
        residual = defaultdict(lambda: defaultdict(int))
        for (u, v), cap in capacity.items():
            residual[u][v] = cap
        
        def dfs_path(s, t, visited, parent):
            """DFS to find augmenting path"""
            if s == t:
                return float('inf')
            
            visited.add(s)
            for v in list(residual[s].keys()):
                if v not in visited and residual[s][v] > 0:
                    parent[v] = s
                    flow = dfs_path(v, t, visited, parent)
                    if flow > 0:
                        return min(residual[s][v], flow)
            
            return 0
        
        total_flow = 0
        
        while True:
            parent = {}
            flow = dfs_path(source, sink, set(), parent)
            
            if flow == 0:
                break
            
            # Update residual capacities
            total_flow += flow
            node = sink
            while node != source:
                prev = parent[node]
                residual[prev][node] -= flow
                residual[node][prev] += flow
                node = prev
        
        return total_flow


class EdmondsKarp:
    """
    Edmonds-Karp Algorithm for maximum flow.
    Time Complexity: O(V * E²)
    Space Complexity: O(V + E)
    
    Uses BFS to find shortest augmenting paths (guaranteed to terminate).
    """
    
    def max_flow(self, capacity: Dict[Tuple[int, int], int], source: int, sink: int, nodes: Set[int]) -> int:
        """
        Calculate maximum flow using BFS-based augmenting paths.
        
        Args:
            capacity: Dictionary mapping (u, v) -> capacity
            source: Source node
            sink: Sink node
            nodes: Set of all nodes
            
        Returns:
            Maximum flow from source to sink
        """
        # Build residual graph
        residual = defaultdict(lambda: defaultdict(int))
        for (u, v), cap in capacity.items():
            residual[u][v] = cap
        
        def bfs_path(s, t, parent):
            """BFS to find augmenting path, returns bottleneck flow"""
            visited = {s}
            queue = deque([(s, float('inf'))])
            
            while queue:
                node, flow = queue.popleft()
                
                if node == t:
                    return flow
                
                for neighbor in list(residual[node].keys()):
                    if neighbor not in visited and residual[node][neighbor] > 0:
                        visited.add(neighbor)
                        parent[neighbor] = node
                        new_flow = min(flow, residual[node][neighbor])
                        queue.append((neighbor, new_flow))
                        
                        if neighbor == t:
                            return new_flow
            
            return 0
        
        total_flow = 0
        parent = {}
        
        while True:
            parent = {}
            flow = bfs_path(source, sink, parent)
            
            if flow == 0:
                break
            
            # Update residual capacities
            total_flow += flow
            node = sink
            while node != source:
                prev = parent[node]
                residual[prev][node] -= flow
                residual[node][prev] += flow
                node = prev
        
        return total_flow


# ============================================================
# 4. BIPARTITE MATCHING
# ============================================================

class BipartiteMatching:
    """
    Maximum Bipartite Matching using augmenting paths.
    Time Complexity: O(V * E)
    Space Complexity: O(V)
    
    A bipartite graph has vertices divided into two sets where edges only go between sets.
    """
    
    def max_matching(self, graph: Dict[int, List[int]], left_size: int, right_size: int) -> int:
        """
        Find maximum bipartite matching.
        
        Args:
            graph: Adjacency list where keys are left vertices, values are lists of right vertices
            left_size: Number of vertices in left partition
            right_size: Number of vertices in right partition
            
        Returns:
            Size of maximum matching
        """
        match_right = [-1] * right_size  # match_right[v] = u means right v matched with left u
        result = 0
        
        for u in range(left_size):
            seen = set()
            if self._dfs(graph, u, seen, match_right):
                result += 1
        
        return result
    
    def _dfs(self, graph: Dict[int, List[int]], u: int, seen: Set[int], match_right: List[int]) -> bool:
        """DFS to find augmenting path"""
        for v in graph.get(u, []):
            if v not in seen:
                seen.add(v)
                
                # If v is not matched or we can find augmenting path from match_right[v]
                if match_right[v] < 0 or self._dfs(graph, match_right[v], seen, match_right):
                    match_right[v] = u
                    return True
        
        return False


# ============================================================
# 5. CRITICAL CONNECTIONS IN NETWORK
# ============================================================

class CriticalConnections:
    """
    Find critical connections (bridges) in a network.
    A critical connection is an edge whose removal disconnects the network.
    Time Complexity: O(V + E)
    Space Complexity: O(V + E)
    """
    
    def find_critical_connections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        """
        Find all critical connections in a network.
        
        Args:
            n: Number of servers (nodes)
            connections: List of undirected connections
            
        Returns:
            List of critical connections
        """
        graph = defaultdict(list)
        for u, v in connections:
            graph[u].append(v)
            graph[v].append(u)
        
        discovery = [-1] * n
        low_link = [-1] * n
        timer = 0
        critical = []
        
        def dfs(node, parent):
            nonlocal timer
            discovery[node] = low_link[node] = timer
            timer += 1
            
            for neighbor in graph[node]:
                if neighbor == parent:
                    continue
                
                if discovery[neighbor] == -1:
                    dfs(neighbor, node)
                    low_link[node] = min(low_link[node], low_link[neighbor])
                    
                    if low_link[neighbor] > discovery[node]:
                        critical.append([node, neighbor])
                else:
                    low_link[node] = min(low_link[node], discovery[neighbor])
        
        for i in range(n):
            if discovery[i] == -1:
                dfs(i, -1)
        
        return critical


# ============================================================
# TESTS
# ============================================================

def test_tarjan_scc():
    """Test Tarjan's SCC algorithm"""
    print("=" * 60)
    print("TEST: Tarjan's SCC Algorithm")
    print("=" * 60)
    
    # Graph with 3 SCCs: {0,1,2}, {3,4,5,6}, {7,8}
    graph = {
        0: [1],
        1: [2],
        2: [0],
        3: [4],
        4: [5],
        5: [3, 6],
        6: [5],
        7: [8],
        8: [7]
    }
    
    tarjan = TarjanSCC()
    sccs = tarjan.find_sccs(graph)
    
    print(f"Graph edges: 0→1, 1→2, 2→0, 3→4, 4→5, 5→3,6, 6→5, 7→8, 8→7")
    print(f"Strongly Connected Components: {sccs}")
    print(f"Number of SCCs: {len(sccs)}")
    assert len(sccs) == 3, f"Expected 3 SCCs, got {len(sccs)}"
    print("✓ PASSED\n")


def test_kosaraju_scc():
    """Test Kosaraju's SCC algorithm"""
    print("=" * 60)
    print("TEST: Kosaraju's SCC Algorithm")
    print("=" * 60)
    
    # Same graph as above
    graph = {
        0: [1],
        1: [2],
        2: [0],
        3: [4],
        4: [5],
        5: [3, 6],
        6: [5],
        7: [8],
        8: [7]
    }
    
    kosaraju = KosarajuSCC()
    sccs = kosaraju.find_sccs(graph)
    
    print(f"Strongly Connected Components: {sccs}")
    print(f"Number of SCCs: {len(sccs)}")
    assert len(sccs) == 3, f"Expected 3 SCCs, got {len(sccs)}"
    print("✓ PASSED\n")


def test_articulation_points_and_bridges():
    """Test articulation points and bridges detection"""
    print("=" * 60)
    print("TEST: Articulation Points & Bridges")
    print("=" * 60)
    
    # Graph: 0-1-2-3-4 (linear chain)
    # Articulation points: 1, 2, 3
    # Bridges: (0,1), (1,2), (2,3), (3,4)
    graph = {
        0: [1],
        1: [0, 2],
        2: [1, 3],
        3: [2, 4],
        4: [3]
    }
    
    finder = ArticulationPointsAndBridges()
    art_points, bridges = finder.find(graph, 5)
    
    print(f"Graph: 0-1-2-3-4 (linear chain)")
    print(f"Articulation Points: {art_points}")
    print(f"Bridges: {bridges}")
    
    assert 1 in art_points, "Node 1 should be articulation point"
    assert 2 in art_points, "Node 2 should be articulation point"
    assert 3 in art_points, "Node 3 should be articulation point"
    assert len(bridges) == 4, f"Expected 4 bridges, got {len(bridges)}"
    print("✓ PASSED\n")


def test_ford_fulkerson():
    """Test Ford-Fulkerson max flow"""
    print("=" * 60)
    print("TEST: Ford-Fulkerson Max Flow")
    print("=" * 60)
    
    # Standard max flow example
    capacity = {
        (0, 1): 16, (0, 2): 13,
        (1, 2): 10, (1, 3): 12,
        (2, 1): 4, (2, 4): 14,
        (3, 2): 9, (3, 5): 20,
        (4, 3): 7, (4, 5): 4
    }
    
    ff = FordFulkerson()
    max_flow = ff.max_flow(capacity, 0, 5, {0, 1, 2, 3, 4, 5})
    
    print(f"Network: Standard 6-node example")
    print(f"Max Flow from 0 to 5: {max_flow}")
    assert max_flow == 23, f"Expected max flow 23, got {max_flow}"
    print("✓ PASSED\n")


def test_edmonds_karp():
    """Test Edmonds-Karp max flow"""
    print("=" * 60)
    print("TEST: Edmonds-Karp Max Flow")
    print("=" * 60)
    
    # Same capacity graph
    capacity = {
        (0, 1): 16, (0, 2): 13,
        (1, 2): 10, (1, 3): 12,
        (2, 1): 4, (2, 4): 14,
        (3, 2): 9, (3, 5): 20,
        (4, 3): 7, (4, 5): 4
    }
    
    ek = EdmondsKarp()
    max_flow = ek.max_flow(capacity, 0, 5, {0, 1, 2, 3, 4, 5})
    
    print(f"Max Flow from 0 to 5: {max_flow}")
    assert max_flow == 23, f"Expected max flow 23, got {max_flow}"
    print("✓ PASSED\n")


def test_bipartite_matching():
    """Test maximum bipartite matching"""
    print("=" * 60)
    print("TEST: Maximum Bipartite Matching")
    print("=" * 60)
    
    # Left: {0,1,2}, Right: {0,1,2,3}
    # Edges: 0→{0,1}, 1→{2,3}, 2→{0}
    graph = {
        0: [0, 1],
        1: [2, 3],
        2: [0]
    }
    
    bm = BipartiteMatching()
    matching = bm.max_matching(graph, 3, 4)
    
    print(f"Bipartite graph: Left={{0,1,2}}, Right={{0,1,2,3}}")
    print(f"Edges: 0→{{0,1}}, 1→{{2,3}}, 2→{{0}}")
    print(f"Maximum Matching Size: {matching}")
    assert matching == 3, f"Expected matching size 3, got {matching}"
    print("✓ PASSED\n")


def test_critical_connections():
    """Test critical connections detection"""
    print("=" * 60)
    print("TEST: Critical Connections in Network")
    print("=" * 60)
    
    # Network with critical connections
    n = 6
    connections = [
        [0, 1], [1, 2], [2, 0],  # Cycle 0-1-2
        [1, 3],                   # Bridge
        [3, 4], [4, 5], [5, 3]   # Cycle 3-4-5
    ]
    
    cc = CriticalConnections()
    critical = cc.find_critical_connections(n, connections)
    
    print(f"Network: 6 nodes with connections as above")
    print(f"Critical Connections: {critical}")
    assert len(critical) == 1, f"Expected 1 critical connection, got {len(critical)}"
    assert [1, 3] in critical or [3, 1] in critical, "Edge (1,3) should be critical"
    print("✓ PASSED\n")


if __name__ == "__main__":
    print("Day 9: Advanced Graph Algorithms")
    print("=" * 60)
    print()
    
    test_tarjan_scc()
    test_kosaraju_scc()
    test_articulation_points_and_bridges()
    test_ford_fulkerson()
    test_edmonds_karp()
    test_bipartite_matching()
    test_critical_connections()
    
    print("=" * 60)
    print("All tests passed!")
    print("=" * 60)
