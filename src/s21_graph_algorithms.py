import ctypes
import sys
import random
import numpy as np
from stack import Stack
from queue import Queue

# Структура для хранения результата задачи коммивояжера (TSP)
class TsmResult(ctypes.Structure):
    _fields_ = [("vertices", ctypes.POINTER(ctypes.c_int)), ("distance", ctypes.c_double)]

# Класс с различными алгоритмами на графах
class GraphAlgorithms:

    # Нерекурсивный поиск в глубину (DFS)
    @staticmethod
    def depth_first_search(graph, start_vertex):
        visited = [False] * graph.vertices  # Список посещённых вершин
        result = []  # Результат обхода
        stack = Stack()  # Стек для обхода графа

        stack.push(start_vertex)  # Добавляем стартовую вершину в стек
        while not stack.is_empty():
            v = stack.pop()  # Берём вершину из стека
            if not visited[v - 1]:  # Если вершина ещё не посещена
                visited[v - 1] = True  # Помечаем вершину как посещённую
                result.append(v)  # Добавляем вершину в результат
                # Добавляем смежные вершины в стек в обратном порядке
                for neighbor in range(graph.vertices, 0, -1):
                    if graph.adjacency_matrix[v - 1][neighbor - 1] > 0:
                        stack.push(neighbor)
        return result

    # Поиск в ширину (BFS)
    @staticmethod
    def breadth_first_search(graph, start_vertex):
        visited = [False] * graph.vertices  # Список посещённых вершин
        result = []  # Результат обхода
        queue = Queue()  # Очередь для обхода графа

        queue.push(start_vertex)  # Добавляем стартовую вершину в очередь
        while not queue.is_empty():
            v = queue.pop()  # Берём вершину из очереди
            if not visited[v - 1]:  # Если вершина ещё не посещена
                visited[v - 1] = True  # Помечаем вершину как посещённую
                result.append(v)  # Добавляем вершину в результат
                # Добавляем смежные вершины в очередь
                for neighbor in range(1, graph.vertices + 1):
                    if graph.adjacency_matrix[v - 1][neighbor - 1] > 0:
                        queue.push(neighbor)
        return result

    # Алгоритм Дейкстры для нахождения кратчайшего пути между двумя вершинами
    @staticmethod
    def get_shortest_path_between_vertices(graph, vertex1, vertex2):
        dist = [sys.maxsize] * graph.vertices  # Инициализация расстояний до всех вершин бесконечностью
        dist[vertex1 - 1] = 0  # Расстояние до начальной вершины равно 0
        visited = [False] * graph.vertices  # Список посещённых вершин
        parent = [-1] * graph.vertices  # Для отслеживания пути

        for _ in range(graph.vertices):
            # Найдём вершину с минимальным расстоянием, которая ещё не посещена
            min_distance = sys.maxsize
            min_vertex = -1
            for v in range(graph.vertices):
                if not visited[v] and dist[v] < min_distance:
                    min_distance = dist[v]
                    min_vertex = v

            if min_vertex == -1:  # Если нет доступных вершин
                break

            visited[min_vertex] = True  # Помечаем вершину как посещённую

            # Обновляем значения расстояний для смежных вершин
            for neighbor in range(graph.vertices):
                if graph.adjacency_matrix[min_vertex][neighbor] > 0 and not visited[neighbor]:
                    new_distance = dist[min_vertex] + graph.adjacency_matrix[min_vertex][neighbor]
                    if new_distance < dist[neighbor]:
                        dist[neighbor] = new_distance
                        parent[neighbor] = min_vertex  # Запоминаем предыдущую вершину

        # Восстанавливаем путь от конечной вершины к начальной
        path = []
        current = vertex2 - 1
        while current != -1:
            path.insert(0, current + 1)
            current = parent[current]

        return dist[vertex2 - 1], path

    # Алгоритм Флойда-Уоршелла для нахождения кратчайших путей между всеми вершинами
    @staticmethod
    def get_shortest_paths_between_all_vertices(graph):
        dist = [[sys.maxsize] * graph.vertices for _ in range(graph.vertices)]  # Инициализация матрицы расстояний

        # Заполняем матрицу расстояний исходными значениями
        for i in range(graph.vertices):
            for j in range(graph.vertices):
                if i == j:
                    dist[i][j] = 0  # Расстояние до самой себя равно 0
                elif graph.adjacency_matrix[i][j] > 0:
                    dist[i][j] = graph.adjacency_matrix[i][j]

        # Алгоритм Флойда-Уоршелла
        for k in range(graph.vertices):
            for i in range(graph.vertices):
                for j in range(graph.vertices):
                    if dist[i][k] < sys.maxsize and dist[k][j] < sys.maxsize:
                        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        return dist

    # Алгоритм Прима для нахождения минимального остовного дерева (MST)
    @staticmethod
    def get_least_spanning_tree(graph):
        vertices = graph.vertices
        selected = [False] * vertices  # Список выбранных вершин
        result = [[0] * vertices for _ in range(vertices)]  # Матрица для хранения MST
        edge_count = 0
        selected[0] = True  # Начинаем с первой вершины

        while edge_count < vertices - 1:
            min_weight = sys.maxsize
            x = 0
            y = 0
            for i in range(vertices):
                if selected[i]:  # Проверяем только выбранные вершины
                    for j in range(vertices):
                        if not selected[j] and 0 < graph.adjacency_matrix[i][j] < min_weight:
                            min_weight = graph.adjacency_matrix[i][j]
                            x, y = i, j
            result[x][y] = result[y][x] = graph.adjacency_matrix[x][y]  # Добавляем ребро в MST
            selected[y] = True  # Помечаем вершину как выбранную
            edge_count += 1

        return result

    # Муравьиный алгоритм для решения задачи коммивояжера (TSP)
    @staticmethod
    def solve_traveling_salesman_problem(graph):
        num_ants = 10  # Количество муравьёв
        num_iterations = 100  # Количество итераций
        evaporation_rate = 0.5  # Скорость испарения феромонов
        alpha = 1.0  # Влияние феромонов
        beta = 2.0  # Влияние эвристической информации
        pheromone_deposit = 100  # Количество феромона, выделяемого муравьем

        vertices = graph.vertices
        distance_matrix = graph.adjacency_matrix

        if vertices <= 1:
            raise ValueError("Граф должен содержать более одной вершины")

        pheromones = np.ones((vertices, vertices)) / vertices  # Инициализация матрицы феромонов

        # Вычисляем вероятности перехода для каждого муравья
        def calculate_transition_probabilities(current_vertex, visited, pheromones, distance_matrix):
            probabilities = []
            total = 0
            for next_vertex in range(vertices):
                if next_vertex not in visited:  # Проверяем только непосещённые вершины
                    pheromone_level = pheromones[current_vertex][next_vertex] ** alpha
                    visibility = (1 / distance_matrix[current_vertex][next_vertex]) ** beta if distance_matrix[current_vertex][next_vertex] > 0 else 0
                    probability = pheromone_level * visibility
                    probabilities.append(probability)
                    total += probability
                else:
                    probabilities.append(0)
            if total == 0:  # Если нет доступных переходов, равномерно распределяем вероятности
                probabilities = [1 / (vertices - len(visited)) if i not in visited else 0 for i in range(vertices)]
            else:
                probabilities = [prob / total for prob in probabilities]
            return probabilities

        # Выбор следующей вершины на основе вероятностей
        def select_next_vertex(probabilities):
            return np.random.choice(vertices, p=probabilities)

        best_route = None
        best_distance = sys.maxsize

        # Основной цикл муравьиного алгоритма
        for _ in range(num_iterations):
            all_routes = []
            all_distances = []

            for ant in range(num_ants):
                route = []
                visited = set()
                current_vertex = random.randint(0, vertices - 1)  # Случайный старт
                route.append(current_vertex)
                visited.add(current_vertex)

                while len(visited) < vertices:
                    probabilities = calculate_transition_probabilities(current_vertex, visited, pheromones, distance_matrix)
                    next_vertex = select_next_vertex(probabilities)
                    route.append(next_vertex)
                    visited.add(next_vertex)
                    current_vertex = next_vertex

                route.append(route[0])  # Возвращаемся к начальной вершине
                distance = sum(distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))

                all_routes.append(route)
                all_distances.append(distance)

                if distance < best_distance:
                    best_distance = distance
                    best_route = route

            # Обновление феромонов
            pheromones *= (1 - evaporation_rate)
            for route, distance in zip(all_routes, all_distances):
                for i in range(len(route) - 1):
                    pheromones[route[i]][route[i + 1]] += pheromone_deposit / distance

        # Возвращаем результат решения TSP
        vertices_array = (ctypes.c_int * len(best_route))(*best_route)
        result = TsmResult(vertices=ctypes.cast(vertices_array, ctypes.POINTER(ctypes.c_int)), distance=best_distance)
        return result
