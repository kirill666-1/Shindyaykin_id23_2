import requests  # Импортируем библиотеку для работы с HTTP-запросами

# Адрес сервера
url = "http://localhost:8000/shortest-path/"

# Данные для запроса (граф, начальная и конечная точки)
data = {
    "graph": {
        "nodes": [1, 2, 3, 4],  # Список вершин графа
        "edges": [              # Список рёбер: [вершина1, вершина2, вес]
            [1, 2, 1],
            [2, 3, 2],
            [3, 4, 1],
            [1, 4, 5]
        ]
    },
    "start": 1,  # Начальная точка
    "end": 4     # Конечная точка
}

# Отправляем POST-запрос
response = requests.post(url, json=data)

# Проверяем статус ответа
if response.status_code == 200:
    # Если всё ок, выводим результат
    result = response.json()
    print("Кратчайший путь:", result["path"])
    print("Общее расстояние:", result["total_distance"])
else:
    # Если ошибка, выводим код ошибки
    print(f"Ошибка: {response.status_code}, {response.text}")