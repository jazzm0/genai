import threading


class Graph:
    def __init__(self, directed=False):
        """
        Initialize the Graph.

        Parameters:
        - directed (bool): Specifies whether the graph is directed. Default is False (undirected).

        Attributes:
        - graph (dict): A dictionary to store vertices and their adjacent vertices.
        - directed (bool): Indicates whether the graph is directed.
        - lock (threading.Lock): A lock to ensure thread safety.
        """
        self.graph = {}
        self.directed = directed
        self.lock = threading.Lock()

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.

        Parameters:
        - vertex: The vertex to add. It must be hashable.

        Ensures that each vertex is represented in the graph dictionary as a key with an empty set as its value.
        """
        if not isinstance(vertex, (int, str, tuple)):
            raise ValueError("Vertex must be a hashable type.")

        with self.lock:
            if vertex not in self.graph:
                self.graph[vertex] = set()

    def add_edge(self, src, dest):
        """
        Add an edge from src to dest. If the graph is undirected, also add from dest to src.

        Parameters:
        - src: The source vertex.
        - dest: The destination vertex.

        Prevents adding duplicate edges and ensures both vertices exist.
        """
        with self.lock:
            if src not in self.graph or dest not in self.graph:
                raise KeyError("Both vertices must exist in the graph.")
            if dest not in self.graph[src]:  # Check to prevent duplicate edges
                self.graph[src].add(dest)
            if not self.directed and src not in self.graph[dest]:
                self.graph[dest].add(src)

    def remove_edge(self, src, dest):
        """
        Remove an edge from src to dest. If the graph is undirected, also remove from dest to src.

        Parameters:
        - src: The source vertex.
        - dest: The destination vertex.
        """
        with self.lock:
            if src in self.graph and dest in self.graph[src]:
                self.graph[src].remove(dest)
            if not self.directed and dest in self.graph and src in self.graph[dest]:
                self.graph[dest].remove(src)

    def remove_vertex(self, vertex):
        """
        Remove a vertex and all edges connected to it.

        Parameters:
        - vertex: The vertex to be removed.
        """
        with self.lock:
            if vertex in self.graph:
                # Remove any edges from other vertices to this one
                for adj in list(self.graph):
                    if vertex in self.graph[adj]:
                        self.graph[adj].remove(vertex)
                # Remove the vertex entry itself
                del self.graph[vertex]

    def get_adjacent_vertices(self, vertex):
        """
        Get a list of vertices adjacent to the specified vertex.

        Parameters:
        - vertex: The vertex whose neighbors are to be retrieved.

        Returns:
        - List of adjacent vertices. Returns an empty list if vertex is not found.
        """
        with self.lock:
            return list(self.graph.get(vertex, []))

    def __str__(self):
        """
        Provide a string representation of the graph's adjacency list for easy printing and debugging.

        Returns:
        - A string representation of the graph dictionary.
        """
        with self.lock:
            return str({k: list(v) for k, v in self.graph.items()})


try:
    g = Graph(directed=True)
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_edge('A', 'B')
    g.add_edge('A', 'B')  # Attempt to add duplicate edge
    print(g)
except Exception as e:
    print(f"Error: {e}")