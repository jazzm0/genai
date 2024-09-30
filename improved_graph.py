import threading

class Graph:
    def __init__(self, directed=False):
        self.graph = {}
        self.directed = directed
        self.lock = threading.Lock()  # Lock for thread safety

    def add_vertex(self, vertex):
        with self.lock:
            if vertex not in self.graph:
                self.graph[vertex] = []

    def add_edge(self, src, dest):
        with self.lock:
            if src not in self.graph:
                self.add_vertex(src)
            if dest not in self.graph:
                self.add_vertex(dest)
            self.graph[src].append(dest)
            if not self.directed:
                self.graph[dest].append(src)

    def remove_edge(self, src, dest):
        with self.lock:
            if src in self.graph and dest in self.graph[src]:
                self.graph[src].remove(dest)
            if not self.directed and dest in self.graph and src in self.graph[dest]:
                self.graph[dest].remove(src)

    def remove_vertex(self, vertex):
        with self.lock:
            if vertex in self.graph:
                # Remove any edges from other vertices to this one
                for adj in list(self.graph):
                    if vertex in self.graph[adj]:
                        self.graph[adj].remove(vertex)
                # Remove the vertex entry
                del self.graph[vertex]

    def get_adjacent_vertices(self, vertex):
        with self.lock:
            if vertex in self.graph:
                return self.graph[vertex]
            else:
                raise ValueError(f"Vertex '{vertex}' does not exist in the graph")

    def __str__(self):
        with self.lock:
            return str(self.graph)

# Example usage
if __name__ == "__main__":
    g = Graph(directed=False)
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B")
    print(g)  # Output: {'A': ['B'], 'B': ['A']}

    g.remove_edge("A", "B")
    print(g)  # Output: {'A': [], 'B': []}

    g.add_edge("A", "B")
    g.remove_vertex("B")
    print(g)  # Output: {'A': []}