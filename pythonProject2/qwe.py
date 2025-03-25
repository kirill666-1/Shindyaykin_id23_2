from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import heapq

app = FastAPI()

# Модель для входных данных (граф)
class Graph(BaseModel):
    graph: Dict[str, List]
    start: int
    end: int

# Модель для результата
class PathResult(BaseModel):
    path: List[int]
    total_distance: float

# Функция алгоритма Дейкстры
def dijkstra(graph_data: dict, start: int, end: int) -> tuple:
    # Преобразуем граф в словарь смежности: {вершина: {сосед: вес}}
    adj_list = {}
    for node in graph_data["nodes"]:
        adj_list[node] = {}
    for edge in graph_data["edges"]:
        u, v, weight = edge
        adj_list[u][v] = weight
        adj_list[v][u] = weight  # Граф неориентированный

    # Инициализация
    distances = {node: float('infinity') for node in graph_data["nodes"]}
    distances[start] = 0
    previous = {node: None for node in graph_data["nodes"]}
    pq = [(0, start)]  # Очередь с приоритетами: (расстояние, вершина)
    visited = set()

    # Основной цикл
    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            break

        # Проверяем соседей
        for neighbor, weight in adj_list[current_node].items():
            if neighbor in visited:
                continue
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # Восстанавливаем путь
    if distances[end] == float('infinity'):
        return [], 0  # Путь не найден

    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous[current_node]
    path.reverse()

    return path, distances[end]

# Эндпоинт
@app.post("/shortest-path/", response_model=PathResult)
async def find_shortest_path(data: Graph):
    # Извлекаем данные из запроса
    graph_data = data.graph
    start = data.start
    end = data.end

    # Находим кратчайший путь
    path, total_distance = dijkstra(graph_data, start, end)

    if not path:
        return {"path": [], "total_distance": 0.0}  # Если пути нет

    return {"path": path, "total_distance": float(total_distance)}

# Пример запуска
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)