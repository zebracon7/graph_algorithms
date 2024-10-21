import numpy as np

class Graph:
    def __init__(self, vertices):
        """Инициализация графа с матрицей смежности"""
        self.vertices = vertices
        self.adjacency_matrix = np.zeros((vertices, vertices), dtype=int)

    def load_graph_from_file(self, filename):
        """Загрузка графа из файла с матрицей смежности"""
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.vertices = len(lines)
            self.adjacency_matrix = np.zeros((self.vertices, self.vertices), dtype=int)
            for i, line in enumerate(lines):
                self.adjacency_matrix[i] = list(map(int, line.strip().split()))

    def export_graph_to_dot(self, filename):
        """Экспорт графа в формате DOT для визуализации"""
        with open(filename, 'w') as f:
            f.write("graph G {\n")
            for i in range(self.vertices):
                for j in range(i, self.vertices):
                    if self.adjacency_matrix[i][j] != 0:
                        f.write(f"  {i+1} -- {j+1};\n")
            f.write("}\n")

    def add_edge(self, u, v, weight=1):
        """Добавление ребра между вершинами u и v с весом weight"""
        self.adjacency_matrix[u-1][v-1] = weight
        self.adjacency_matrix[v-1][u-1] = weight
