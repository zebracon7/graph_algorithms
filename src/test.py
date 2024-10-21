import unittest
from s21_graph import Graph
from s21_graph_algorithms import GraphAlgorithms

class TestGraph(unittest.TestCase):

    def setUp(self):
        """Создание графа с 4 вершинами и добавление рёбер"""
        self.create_test_graph_file()
        self.graph = Graph(4)
        # Загрузка графа из файла
        self.graph.load_graph_from_file("test_graph.txt")

    def create_test_graph_file(self):
        """Создание тестового файла с графом"""
        with open("test_graph.txt", 'w') as f:
            f.write("0 1 0 2\n")
            f.write("1 0 2 0\n")
            f.write("0 2 0 3\n")
            f.write("2 0 3 0\n")

    def test_load_graph_from_file(self):
        """Тест загрузки графа из файла"""
        expected_matrix = [
            [0, 1, 0, 2],
            [1, 0, 2, 0],
            [0, 2, 0, 3],
            [2, 0, 3, 0]
        ]
        self.assertEqual(self.graph.adjacency_matrix.tolist(), expected_matrix)

    def test_add_edge(self):
        """Тест добавления ребра"""
        self.graph.add_edge(1, 3, 5)
        self.assertEqual(self.graph.adjacency_matrix[0][2], 5)
        self.assertEqual(self.graph.adjacency_matrix[2][0], 5)

    def test_export_graph_to_dot(self):
        """Тест экспорта графа в формат DOT"""
        self.graph.export_graph_to_dot("test_graph.dot")
        with open("test_graph.dot", 'r') as f:
            dot_content = f.read()
        expected_content = """graph G {
  1 -- 2;
  1 -- 4;
  2 -- 3;
  3 -- 4;
}
"""
        self.assertEqual(dot_content, expected_content)


class TestGraphAlgorithms(unittest.TestCase):

    def setUp(self):
        """Создание графа и добавление рёбер"""
        self.graph = Graph(4)
        self.graph.load_graph_from_file("test_graph.txt")

    def test_depth_first_search(self):
        """Тест поиска в глубину"""
        result = GraphAlgorithms.depth_first_search(self.graph, 1)
        expected = [1, 2, 3, 4]
        self.assertEqual(result, expected)

    def test_breadth_first_search(self):
        """Тест поиска в ширину"""
        result = GraphAlgorithms.breadth_first_search(self.graph, 1)
        expected = [1, 2, 4, 3]
        self.assertEqual(result, expected)

    def test_get_shortest_path_between_vertices(self):
        """Тест нахождения кратчайшего пути между двумя вершинами"""
        dist, path = GraphAlgorithms.get_shortest_path_between_vertices(self.graph, 1, 4)
        self.assertEqual(dist, 2)
        self.assertEqual(path, [1, 4])

    def test_get_shortest_paths_between_all_vertices(self):
        """Тест нахождения кратчайших путей между всеми вершинами"""
        result = GraphAlgorithms.get_shortest_paths_between_all_vertices(self.graph)
        # Преобразуем результат в обычные целые числа
        result = [[int(cell) for cell in row] for row in result]
        expected = [
            [0, 1, 3, 2],
            [1, 0, 2, 3],
            [3, 2, 0, 3],
            [2, 3, 3, 0]
        ]
        self.assertEqual(result, expected)

    def test_get_least_spanning_tree(self):
        """Тест нахождения минимального остовного дерева"""
        result = GraphAlgorithms.get_least_spanning_tree(self.graph)
        # Преобразуем результат в обычные целые числа
        result = [[int(cell) for cell in row] for row in result]
        expected = [
            [0, 1, 0, 2],
            [1, 0, 2, 0],
            [0, 2, 0, 0],
            [2, 0, 0, 0]
        ]
        self.assertEqual(result, expected)


    def test_solve_traveling_salesman_problem(self):
        """Тест решения задачи коммивояжера"""
        result = GraphAlgorithms.solve_traveling_salesman_problem(self.graph)
        # Измените ожидаемое расстояние и маршрут на основании нового графа
        self.assertEqual(result.distance, 8)  

if __name__ == "__main__":
    unittest.main()
