import networkx as nx
import matplotlib.pyplot as plt

# Матрица смежности
matrix = [
    [0, 1, 0, 2],
    [1, 0, 2, 0],
    [0, 2, 0, 3],
    [2, 0, 3, 0]
]

# Создаем граф
G = nx.DiGraph()  # Для ориентированного графа, можно заменить на nx.Graph() для неориентированного

# Добавляем вершины
num_vertices = len(matrix)
for i in range(num_vertices):
    G.add_node(i)

# Добавляем ребра с весами
for i in range(num_vertices):
    for j in range(num_vertices):
        if matrix[i][j] != 0:  # Если вес ребра не равен 0
            G.add_edge(i, j, weight=matrix[i][j])

# Визуализация графа
pos = nx.spring_layout(G)  # Расположение вершин
edges = G.edges(data=True)
weights = [edge[2]['weight'] for edge in edges]

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): f'{matrix[i][j]}' for i in range(num_vertices) for j in range(num_vertices) if matrix[i][j] != 0})
nx.draw_networkx_edges(G, pos, edge_color=weights, width=2, arrowstyle='-|>', arrowsize=15, edge_cmap=plt.cm.Blues)

plt.title("Визуализация графа")
plt.show()
