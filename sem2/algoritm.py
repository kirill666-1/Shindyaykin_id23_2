from typing import List
import json

def nearest_neighbor_tsp(nodes: List[int], edges: List[List[int]]) -> tuple[List[int], float]:
    if not nodes: raise ValueError("Список узлов не может быть пустым")
    if not edges: raise ValueError("Список рёбер не может быть пустым")
    all_edge_nodes = {node for edge in edges for node in edge}
    if not all_edge_nodes.issubset(set(nodes)): raise ValueError("Все узлы в рёбрах должны быть из списка nodes")
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
    total_distance = 0.0
    for _ in range(n - 1):
        last = route[-1]
        candidates = [(i, adj_matrix[last][i]) for i in range(n) if not visited[i]]
        if not candidates:
            break
        nearest = min(candidates, key=lambda x: x[1])[0]
        route.append(nearest)
        if adj_matrix[last][nearest] != float('inf'):
            total_distance += adj_matrix[last][nearest]
        visited[nearest] = True
    path = [nodes[i] for i in route]
    if adj_matrix[route[-1]][route[0]] != float('inf'):
        total_distance += adj_matrix[route[-1]][route[0]]
    return path, total_distance

nodes = [1, 2, 3, 4]
edges = [[1, 2], [2, 3], [3, 4], [1, 4]]
path, total_distance = nearest_neighbor_tsp(nodes, edges)
result = {"path": path, "total_distance": float(total_distance)}
print(json.dumps(result))