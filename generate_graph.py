import random

from graded_assignment_advanced_graph import Graph_Advanced


def generate_graph(nodes, edges=None, complete=False, weight_bounds=(1, 600), seed=None):
    random.seed(seed)
    graph = Graph_Advanced()
    if edges is not None and complete:
        raise ValueError("edges must be None if complete is set to True")

    for i in range(nodes):
        graph.add_vertex(i)
    if complete:
        for i in range(nodes):
            for j in range(i + 1, nodes):
                weight = random.randint(weight_bounds[0], weight_bounds[1])
                graph.add_edge(i, j, weight)
    else:
        for i in range(nodes):
            for _ in range(edges):
                j = random.randint(0, nodes - 1)
                while j == i or j in graph.get_adjacent_vertices(i):  # Ensure the edge is not a loop or a duplicate
                    j = random.randint(0, nodes - 1)
                weight = random.randint(weight_bounds[0], weight_bounds[1])
                graph.add_edge(i, j, weight)
    return graph


for i in range(42, 47):
    graph = generate_graph(nodes=1000, complete=True, seed=i)
    print(graph.tsp_large_graph(0))
    print("\n")
