from typing import List

def nearest_neighbor_tsp(nodes: List[int], edges: List[List[int]]) -> tuple[List[int], float]:
    if not nodes: raise ValueError("Nodes list cannot be empty")
    if not edges: raise ValueError("Edges list cannot be empty")
    all_edge_nodes = {node for edge in edges for node in edge}
    if not all_edge_nodes.issubset(set(nodes)): raise ValueError("All nodes in edges must be in nodes list")
    n = len(nodes)
    adj_matrix = [[float('inf')] * n for _ in range(n)]
    for i in range(n): adj_matrix[i][i] = 0
    for edge in edges:
        u, v = edge
        idx_u = nodes.index(u)
        idx_v = nodes.index(v)
        adj_matrix[idx_u][idx_v] = 1
        adj_matrix[idx_v][idx_u] = 1
    visited = [False] * n
    route = [0]
    visited[0] = True
    for _ in range(n - 1):
        last = route[-1]
        nearest = min([(i, adj_matrix[last][i]) for i in range(n) if not visited[i]], key=lambda x: x[1])[0]
        route.append(nearest)
        visited[nearest] = True
    route.append(0)
    path = [nodes[i] for i in route]
    total_distance = len(route) - 1
    return path, total_distance