"""
Day 8: Graphs & Graph Traversal
Topics: Graph representation, BFS, DFS, topological sort, union-find, shortest path algorithms
Focus: Understanding graph structures, traversal techniques, and common graph algorithms
"""

from typing import List, Dict, Set, Tuple, Optional
from collections import deque, defaultdict
import heapq


# ============================================================
# 1. GRAPH REPRESENTATION
# ============================================================

class Graph:
    """
    Graph class supporting multiple representations:
    - Adjacency List: O(1) edge lookup, O(V+E) space
    - Adjacency Matrix: O(1) edge check, O(V²) space
    - Edge List: O(E) space, useful for Kruskal's
    """

    def __init__(self):
        self.adj_list: Dict[int, List[int]] = defaultdict(list)
        self.adj_matrix: Dict[int, Dict[int, int]] = defaultdict(dict)
        self.edges: List[Tuple[int, int, int]] = []  # (u, v, weight)

    def add_edge(self, u: int, v: int, weight: int = 1, directed: bool = True):
        """Add edge to all representations"""
        # Adjacency list
        self.adj_list[u].append(v)
        if not directed:
            self.adj_list[v].append(u)

        # Adjacency matrix
        self.adj_matrix[u][v] = weight
        if not directed:
            self.adj_matrix[v][u] = weight

        # Edge list
        self.edges.append((u, v, weight))
        if not directed:
            self.edges.append((v, u, weight))

    def get_neighbors(self, node: int) -> List[int]:
        """Get neighbors from adjacency list"""
        return self.adj_list.get(node, [])

    def has_edge(self, u: int, v: int) -> bool:
        """Check edge existence in O(1) using adjacency matrix"""
        return v in self.adj_matrix.get(u, {})

    def get_vertices(self) -> Set[int]:
        """Get all vertices"""
        return set(self.adj_list.keys())


def build_adjacency_list(edges: List[Tuple[int, int]], directed: bool = True) -> Dict[int, List[int]]:
    """
    Build adjacency list from edge list.

    Time: O(E), Space: O(V + E)
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return dict(adj)


def build_adjacency_matrix(edges: List[Tuple[int, int]], n: int, directed: bool = True) -> List[List[int]]:
    """
    Build adjacency matrix from edge list.

    Time: O(E), Space: O(V²)
    """
    matrix = [[0] * n for _ in range(n)]
    for u, v in edges:
        matrix[u][v] = 1
        if not directed:
            matrix[v][u] = 1
    return matrix


# ============================================================
# 2. BFS ON GRAPHS
# ============================================================

def bfs_traversal(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    BFS traversal from start node.
    Visits nodes level by level.

    Time: O(V + E), Space: O(V)

    Pattern: Queue for FIFO ordering, visited set to avoid cycles
    """
    visited = set([start])
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


def bfs_shortest_path(graph: Dict[int, List[int]], start: int, end: int) -> List[int]:
    """
    Find shortest path (by number of edges) from start to end.

    Time: O(V + E), Space: O(V)

    Pattern: BFS with parent tracking for path reconstruction
    """
    if start == end:
        return [start]

    visited = set([start])
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))

    return []  # No path exists


def bfs_connected_components(graph: Dict[int, List[int]], vertices: List[int]) -> List[List[int]]:
    """
    Find all connected components in undirected graph.

    Time: O(V + E), Space: O(V)

    Pattern: BFS from each unvisited vertex
    """
    visited = set()
    components = []

    for vertex in vertices:
        if vertex not in visited:
            # BFS to find all nodes in this component
            component = []
            queue = deque([vertex])
            visited.add(vertex)

            while queue:
                node = queue.popleft()
                component.append(node)

                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            components.append(sorted(component))

    return components


def is_bipartite(graph: Dict[int, List[int]], vertices: List[int]) -> bool:
    """
    Check if graph is bipartite (2-colorable).

    Time: O(V + E), Space: O(V)

    Pattern: BFS with coloring - adjacent nodes must have different colors
    """
    color = {}  # 0 or 1

    for start in vertices:
        if start in color:
            continue

        # BFS with coloring
        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()

            for neighbor in graph.get(node, []):
                if neighbor not in color:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False

    return True


# ============================================================
# 3. DFS ON GRAPHS
# ============================================================

def dfs_recursive(graph: Dict[int, List[int]], start: int, visited: Optional[Set[int]] = None) -> List[int]:
    """
    DFS traversal using recursion.

    Time: O(V + E), Space: O(V) for recursion stack

    Pattern: Go deep before going wide, natural backtracking
    """
    if visited is None:
        visited = set()

    visited.add(start)
    result = [start]

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))

    return result


def dfs_iterative(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    DFS traversal using explicit stack.

    Time: O(V + E), Space: O(V)

    Pattern: LIFO stack for depth-first exploration
    """
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        result.append(node)

        # Add unvisited neighbors (reverse for correct order)
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return result


def dfs_cycle_detection_directed(graph: Dict[int, List[int]], vertices: List[int]) -> bool:
    """
    Detect cycle in directed graph using DFS.

    Time: O(V + E), Space: O(V)

    Pattern: Track recursion stack - back edge indicates cycle
    WHITE (0) = unvisited, GRAY (1) = in current path, BLACK (2) = completed
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in vertices}

    def dfs(node: int) -> bool:
        color[node] = GRAY  # Mark as being processed

        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:  # Back edge found
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True

        color[node] = BLACK  # Mark as completed
        return False

    for vertex in vertices:
        if color[vertex] == WHITE:
            if dfs(vertex):
                return True

    return False


def dfs_cycle_detection_undirected(graph: Dict[int, List[int]], vertices: List[int]) -> bool:
    """
    Detect cycle in undirected graph using DFS.

    Time: O(V + E), Space: O(V)

    Pattern: Track parent to avoid false positive from edge to parent
    """
    visited = set()

    def dfs(node: int, parent: int) -> bool:
        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Back edge (not to parent)
                return True

        return False

    for vertex in vertices:
        if vertex not in visited:
            if dfs(vertex, -1):
                return True

    return False


def dfs_find_all_paths(graph: Dict[int, List[int]], start: int, end: int) -> List[List[int]]:
    """
    Find all paths from start to end using DFS.

    Time: O(V!), Space: O(V) for recursion depth

    Pattern: Backtracking to explore all possible paths
    """
    all_paths = []

    def backtrack(node: int, path: List[int], visited: Set[int]):
        if node == end:
            all_paths.append(path[:])
            return

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                backtrack(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)

    backtrack(start, [start], {start})
    return all_paths


# ============================================================
# 4. TOPOLOGICAL SORT
# ============================================================

def topological_sort_kahn(graph: Dict[int, List[int]], vertices: List[int]) -> List[int]:
    """
    Topological sort using Kahn's Algorithm (BFS-based).

    Time: O(V + E), Space: O(V)

    Pattern: Process nodes with in-degree 0, reduce in-degrees

    Applications: Course scheduling, task dependencies, build systems
    """
    # Calculate in-degrees
    in_degree = defaultdict(int)
    for v in vertices:
        if v not in in_degree:
            in_degree[v] = 0
        for neighbor in graph.get(v, []):
            in_degree[neighbor] += 1

    # Queue of nodes with in-degree 0
    queue = deque([v for v in vertices if in_degree[v] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycle
    if len(result) != len(vertices):
        return []  # Cycle detected

    return result


def topological_sort_dfs(graph: Dict[int, List[int]], vertices: List[int]) -> List[int]:
    """
    Topological sort using DFS (post-order reversal).

    Time: O(V + E), Space: O(V)

    Pattern: Add to stack after processing all descendants, then reverse
    """
    visited = set()
    stack = []

    def dfs(node: int):
        visited.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)

        stack.append(node)  # Add after processing descendants

    for vertex in vertices:
        if vertex not in visited:
            dfs(vertex)

    return stack[::-1]  # Reverse for topological order


def can_finish_courses(num_courses: int, prerequisites: List[Tuple[int, int]]) -> bool:
    """
    LeetCode #207: Course Schedule
    Determine if all courses can be finished (no cycle in dependency graph).

    Time: O(V + E), Space: O(V + E)

    Pattern: Cycle detection using Kahn's algorithm
    """
    # Build graph and in-degree count
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Start with courses having no prerequisites
    queue = deque([c for c in range(num_courses) if in_degree[c] == 0])
    completed = 0

    while queue:
        course = queue.popleft()
        completed += 1

        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return completed == num_courses


def find_course_order(num_courses: int, prerequisites: List[Tuple[int, int]]) -> List[int]:
    """
    LeetCode #210: Course Schedule II
    Return valid order to take all courses.

    Time: O(V + E), Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([c for c in range(num_courses) if in_degree[c] == 0])
    order = []

    while queue:
        course = queue.popleft()
        order.append(course)

        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return order if len(order) == num_courses else []


# ============================================================
# 5. UNION-FIND (DISJOINT SET UNION)
# ============================================================

class UnionFind:
    """
    Union-Find with path compression and union by rank.

    Operations:
    - find: O(α(n)) ≈ O(1) amortized
    - union: O(α(n)) ≈ O(1) amortized
    - connected: O(α(n)) ≈ O(1) amortized

    Where α is the inverse Ackermann function (nearly constant)

    Applications: Connected components, cycle detection, Kruskal's MST
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.num_components = n

    def find(self, x: int) -> int:
        """
        Find root of x with path compression.
        Path: Make all nodes point directly to root
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union sets containing x and y by rank.
        Returns True if merged, False if already same set.
        """
        root_x, root_y = self.find(x), self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        # Union by rank: attach shorter tree to taller tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.num_components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are in same set"""
        return self.find(x) == self.find(y)

    def get_num_components(self) -> int:
        """Return number of connected components"""
        return self.num_components


def count_connected_components_uf(n: int, edges: List[Tuple[int, int]]) -> int:
    """
    Count connected components using Union-Find.

    Time: O(E · α(V)), Space: O(V)
    """
    uf = UnionFind(n)

    for u, v in edges:
        uf.union(u, v)

    return uf.get_num_components()


def has_cycle_undirected_uf(n: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Detect cycle in undirected graph using Union-Find.

    Time: O(E · α(V)), Space: O(V)

    Pattern: If edge connects nodes already in same set, cycle exists
    """
    uf = UnionFind(n)

    for u, v in edges:
        if not uf.union(u, v):  # Already connected
            return True

    return False


def kruskal_mst(n: int, edges: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Kruskal's Minimum Spanning Tree algorithm.

    Time: O(E log E) for sorting, Space: O(V)

    Pattern: Greedily add smallest edges that don't create cycle

    Returns list of edges in MST: [(u, v, weight), ...]
    """
    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda x: x[2])

    uf = UnionFind(n)
    mst = []
    mst_weight = 0

    for u, v, weight in sorted_edges:
        if uf.union(u, v):  # No cycle created
            mst.append((u, v, weight))
            mst_weight += weight

            if len(mst) == n - 1:  # MST complete
                break

    return mst


# ============================================================
# 6. SHORTEST PATH ALGORITHMS
# ============================================================

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    """
    Dijkstra's algorithm for single-source shortest path.

    Time: O((V + E) log V) with min-heap, Space: O(V)

    Requirements: Non-negative edge weights
    Pattern: Greedy + priority queue, always pick closest unvisited node

    Returns: Dict mapping node -> shortest distance from start
    """
    # Initialize distances
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0

    # Min-heap: (distance, node)
    pq = [(0, start)]

    while pq:
        d, node = heapq.heappop(pq)

        # Skip if we found a shorter path already
        if d > dist[node]:
            continue

        for neighbor, weight in graph.get(node, []):
            new_dist = dist[node] + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    return dict(dist)


def dijkstra_with_path(graph: Dict[int, List[Tuple[int, int]]], start: int, end: int) -> Tuple[int, List[int]]:
    """
    Dijkstra's with path reconstruction.

    Returns: (shortest_distance, path)
    """
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    parent = {}

    pq = [(0, start)]

    while pq:
        d, node = heapq.heappop(pq)

        if d > dist[node]:
            continue

        if node == end:
            # Reconstruct path
            path = []
            current = end
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            return d, path[::-1]

        for neighbor, weight in graph.get(node, []):
            new_dist = dist[node] + weight

            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

    return float('inf'), []  # No path exists


def bellman_ford(n: int, edges: List[Tuple[int, int, int]], start: int) -> Dict[int, int]:
    """
    Bellman-Ford algorithm for single-source shortest path.

    Time: O(V · E), Space: O(V)

    Capabilities: Handles negative edge weights, detects negative cycles

    Returns: Dict mapping node -> shortest distance from start
             Returns empty dict if negative cycle exists
    """
    # Initialize distances
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0

    # Relax all edges V-1 times
    for _ in range(n - 1):
        for u, v, weight in edges:
            if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight

    # Check for negative cycles
    for u, v, weight in edges:
        if dist[u] != float('inf') and dist[u] + weight < dist[v]:
            return {}  # Negative cycle detected

    return dict(dist)


def floyd_warshall(n: int, edges: List[Tuple[int, int, int]]) -> List[List[int]]:
    """
    Floyd-Warshall algorithm for all-pairs shortest path.

    Time: O(V³), Space: O(V²)

    Capabilities: Finds shortest paths between ALL pairs, detects negative cycles

    Returns: V×V matrix where result[i][j] = shortest distance from i to j
             Uses float('inf') for unreachable pairs
    """
    # Initialize distance matrix
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]

    # Distance to self is 0
    for i in range(n):
        dist[i][i] = 0

    # Set edge weights
    for u, v, weight in edges:
        dist[u][v] = weight

    # Floyd-Warshall: try each vertex as intermediate
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    # Check for negative cycles (negative value on diagonal)
    for i in range(n):
        if dist[i][i] < 0:
            return []  # Negative cycle detected

    return dist


# ============================================================
# TESTS
# ============================================================

def test_graph_representation():
    """Test graph building functions"""
    edges = [(0, 1), (1, 2), (2, 3), (0, 3)]

    # Adjacency list
    adj = build_adjacency_list(edges)
    assert set(adj[0]) == {1, 3}
    assert adj[1] == [2]

    # Adjacency matrix (undirected by default for this test)
    matrix = build_adjacency_matrix(edges, 4, directed=False)
    assert matrix[0][1] == 1
    assert matrix[0][3] == 1
    assert matrix[1][0] == 1  # Undirected

    print("✓ Graph representation tests passed")


def test_bfs():
    """Test BFS functions"""
    graph = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1, 3, 4],
        3: [1, 2, 4],
        4: [2, 3]
    }

    # BFS traversal
    result = bfs_traversal(graph, 0)
    assert result[0] == 0
    assert set(result[:3]) == {0, 1, 2}

    # BFS shortest path
    path = bfs_shortest_path(graph, 0, 4)
    assert path[0] == 0
    assert path[-1] == 4
    assert len(path) == 3  # 0 -> 2 -> 4

    # Connected components
    graph2 = {0: [1], 1: [0], 2: [3], 3: [2]}
    components = bfs_connected_components(graph2, [0, 1, 2, 3])
    assert len(components) == 2

    # Bipartite check (path graph is bipartite)
    bipartite_graph = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    assert is_bipartite(bipartite_graph, [0, 1, 2, 3])

    # Non-bipartite (triangle)
    graph3 = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    assert not is_bipartite(graph3, [0, 1, 2])

    print("✓ BFS tests passed")


def test_dfs():
    """Test DFS functions"""
    graph = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2]
    }

    # DFS recursive
    result = dfs_recursive(graph, 0)
    assert result[0] == 0
    assert len(result) == 4

    # DFS iterative
    result = dfs_iterative(graph, 0)
    assert result[0] == 0
    assert len(result) == 4

    # Cycle detection (directed)
    directed_graph = {0: [1], 1: [2], 2: [0]}
    assert dfs_cycle_detection_directed(directed_graph, [0, 1, 2])

    # No cycle (directed)
    dag = {0: [1, 2], 1: [3], 2: [3], 3: []}
    assert not dfs_cycle_detection_directed(dag, [0, 1, 2, 3])

    # Cycle detection (undirected)
    assert dfs_cycle_detection_undirected(graph, [0, 1, 2, 3])

    # Find all paths
    paths = dfs_find_all_paths({0: [1, 2], 1: [2], 2: []}, 0, 2)
    assert len(paths) == 2  # [0,1,2] and [0,2]

    print("✓ DFS tests passed")


def test_topological_sort():
    """Test topological sort functions"""
    # DAG: 0 -> 1 -> 3, 0 -> 2 -> 3
    graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
    vertices = [0, 1, 2, 3]

    result_kahn = topological_sort_kahn(graph, vertices)
    assert result_kahn[0] == 0
    assert result_kahn[-1] == 3

    result_dfs = topological_sort_dfs(graph, vertices)
    assert result_dfs[0] == 0
    assert result_dfs[-1] == 3

    # Course schedule
    assert can_finish_courses(2, [(1, 0)])
    assert not can_finish_courses(2, [(1, 0), (0, 1)])  # Cycle

    # Course order
    order = find_course_order(4, [(1, 0), (2, 0), (3, 1), (3, 2)])
    assert order[0] == 0
    assert order[-1] == 3

    print("✓ Topological sort tests passed")


def test_union_find():
    """Test Union-Find functions"""
    uf = UnionFind(5)

    assert not uf.connected(0, 1)
    uf.union(0, 1)
    assert uf.connected(0, 1)

    uf.union(1, 2)
    assert uf.connected(0, 2)

    assert uf.get_num_components() == 3  # {0,1,2}, {3}, {4}

    # Connected components
    edges = [(0, 1), (1, 2), (3, 4)]
    assert count_connected_components_uf(5, edges) == 2

    # Cycle detection
    edges_with_cycle = [(0, 1), (1, 2), (2, 0)]
    assert has_cycle_undirected_uf(3, edges_with_cycle)

    # Kruskal's MST
    edges_weighted = [
        (0, 1, 10), (0, 2, 6), (0, 3, 5),
        (1, 3, 15), (2, 3, 4)
    ]
    mst = kruskal_mst(4, edges_weighted)
    assert len(mst) == 3  # n-1 edges
    total_weight = sum(w for _, _, w in mst)
    assert total_weight == 19  # 5 + 4 + 10

    print("✓ Union-Find tests passed")


def test_shortest_path():
    """Test shortest path algorithms"""
    # Weighted graph
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }

    # Dijkstra
    dist = dijkstra(graph, 0)
    assert dist[0] == 0
    assert dist[1] == 3  # 0 -> 2 -> 1
    assert dist[2] == 1
    assert dist[3] == 4  # 0 -> 2 -> 1 -> 3

    # Dijkstra with path
    d, path = dijkstra_with_path(graph, 0, 3)
    assert d == 4
    assert path == [0, 2, 1, 3]

    # Bellman-Ford
    edges = [(0, 1, 4), (0, 2, 1), (1, 3, 1), (2, 1, 2), (2, 3, 5)]
    dist_bf = bellman_ford(4, edges, 0)
    assert dist_bf[1] == 3
    assert dist_bf[3] == 4

    # Floyd-Warshall
    fw_result = floyd_warshall(4, edges)
    assert fw_result[0][3] == 4
    assert fw_result[0][2] == 1

    # Negative weight (Bellman-Ford handles)
    edges_neg = [(0, 1, 4), (0, 2, 3), (1, 2, -2), (2, 3, 1)]
    dist_neg = bellman_ford(4, edges_neg, 0)
    assert dist_neg[2] == 2  # 0 -> 1 -> 2

    # Negative cycle detection
    edges_neg_cycle = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]
    assert bellman_ford(3, edges_neg_cycle, 0) == {}

    print("✓ Shortest path tests passed")


if __name__ == "__main__":
    print("Running Day 8: Graphs & Graph Traversal Tests\n")

    test_graph_representation()
    test_bfs()
    test_dfs()
    test_topological_sort()
    test_union_find()
    test_shortest_path()

    print("\n✅ All tests passed!")
