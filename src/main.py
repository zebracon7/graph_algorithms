from s21_graph import Graph
from s21_graph_algorithms import GraphAlgorithms

def main():
    # Загружаем граф из файла
    filename = input("Введите имя файла с графом (например, graph.txt): ")
    graph = Graph(0)
    graph.load_graph_from_file(filename)

    while True:
        print("\nВыберите действие:")
        print("1. Вывести матрицу смежности графа")
        print("2. Поиск в глубину (DFS)")
        print("3. Поиск в ширину (BFS)")
        print("4. Поиск кратчайшего пути между двумя вершинами (Алгоритм Дейкстры)")
        print("5. Поиск кратчайших путей между всеми вершинами (Алгоритм Флойда-Уоршелла)")
        print("6. Поиск минимального остовного дерева (Алгоритм Прима)")
        print("7. Решение задачи коммивояжера (Муравьиный алгоритм)")
        print("0. Выход")
        
        choice = input("Введите номер действия: ")

        if choice == "1":
            print("\nМатрица смежности графа:")
            for row in graph.adjacency_matrix:
                print(' '.join(map(str, row)))

        elif choice == "2":
            start_vertex = int(input("Введите начальную вершину для поиска в глубину: "))
            result = GraphAlgorithms.depth_first_search(graph, start_vertex)
            print(f"Результат поиска в глубину: {result}")

        elif choice == "3":
            start_vertex = int(input("Введите начальную вершину для поиска в ширину: "))
            result = GraphAlgorithms.breadth_first_search(graph, start_vertex)
            print(f"Результат поиска в ширину: {result}")

        elif choice == "4":
            vertex1 = int(input("Введите первую вершину: "))
            vertex2 = int(input("Введите вторую вершину: "))
            distance, path = GraphAlgorithms.get_shortest_path_between_vertices(graph, vertex1, vertex2)
            print(f"Кратчайший путь между вершинами {vertex1} и {vertex2}: {path}")
            print(f"Расстояние: {distance}")

        elif choice == "5":
            result = GraphAlgorithms.get_shortest_paths_between_all_vertices(graph)
            print("\nМатрица кратчайших путей между всеми вершинами:")
            for row in result:
                print([int(x) for x in row])

        elif choice == "6":
            result = GraphAlgorithms.get_least_spanning_tree(graph)
            print("\nМатрица смежности минимального остовного дерева:")
            for row in result:
                print(' '.join(map(str, row)))

        elif choice == "7":
                try:
                    result = GraphAlgorithms.solve_traveling_salesman_problem(graph)
                    vertices = [result.vertices[i] for i in range(graph.vertices)]
                    print("Результат решения задачи коммивояжера:")
                    print(f"Маршрут: {vertices}")
                    print(f"Расстояние: {result.distance}")
                except NotImplementedError as e:
                    print(e)
                except ValueError as e:
                    print('Для данного графа задача коммивояжера не может быть решена.')
                
        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Пожалуйста, введите номер от 0 до 7.")


if __name__ == "__main__":
    main()
