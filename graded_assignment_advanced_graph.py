import heapq

import numpy as np

from graded_assignment_graph import Graph


class Graph_Advanced(Graph):
    def shortest_path(self, start, end):
        # Priority queue to store (distance, vertex) tuples
        pq = [(0, start)]
        # Dictionary to store the shortest distance to each vertex
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0
        # Dictionary to store the previous vertex in the shortest path
        previous = {vertex: None for vertex in self.graph}

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            # If we reached the end vertex, reconstruct the path
            if current_vertex == end:
                path = []
                while current_vertex is not None:
                    path.append(current_vertex)
                    current_vertex = previous[current_vertex]
                path.reverse()
                return (current_distance, path)

            # If a shorter path to current_vertex has been found, skip processing
            if current_distance > distances[current_vertex]:
                continue

            # Explore neighbors
            for neighbor, weight in self.graph[current_vertex].items():
                distance = current_distance + weight

                # If a shorter path to neighbor is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))

        # If the end vertex is not reachable, return infinity and an empty path
        return float('inf'), []

    def tsp_small_graph(self, start):
        vertices = list(self.graph.keys())
        n = len(vertices)
        all_indices = range(n)
        start_index = vertices.index(start)

        # Create a distance matrix for easier access
        dist = np.full((n, n), float('inf'))
        for i, u in enumerate(vertices):
            for j, v in enumerate(vertices):
                if i != j:
                    dist[i][j] = self._get_edge_weight(u, v)

        # Initialize memoization table
        memo = {}

        def visit(mask, pos):
            if (mask, pos) in memo:
                return memo[(mask, pos)]

            if mask == (1 << n) - 1:
                return dist[pos][start_index]

            ans = float('inf')
            for city in all_indices:
                if mask & (1 << city) == 0:
                    new_mask = mask | (1 << city)
                    ans = min(ans, dist[pos][city] + visit(new_mask, city))

            memo[(mask, pos)] = ans
            return ans

        min_distance = visit(1 << start_index, start_index)

        # Reconstruct the path
        mask = 1 << start_index
        pos = start_index
        path = [start]

        for _ in range(n - 1):
            next_city = min(
                (dist[pos][city] + visit(mask | (1 << city), city), city)
                for city in all_indices
                if mask & (1 << city) == 0
            )[1]
            path.append(vertices[next_city])
            mask |= 1 << next_city
            pos = next_city

        path.append(start)

        return min_distance, path
    #
    # def tsp_large_graph(self, start):
    #     """
    #     Solve the Travelling Salesman Problem for a large (~1000 node) complete graph starting from a specified node.
    #     No requirement to find the optimal tour. Must run under 0.5 second and its solution must no
    #
    #     Parameters:
    #     start: The starting node.
    #
    #     Returns:
    #     A tuple containing the total distance of the tour and a list of nodes representing the tour path.
    #     """
    #     # Your code here
    #     return dist, path
    #
    # def tsp_medium_graph(self, start):
    #     """
    #     Solve the Travelling Salesman Problem for a medium (~100 node) complete graph starting from a specified node.
    #     Expected to perform better than tsp_large_graph. Must run under 1 second.
    #
    #     Parameters:
    #     start: The starting node.
    #
    #     Returns:
    #     A tuple containing the total distance of the tour and a list of nodes representing the tour path.
    #     """
    #
    #     # Your code here
    #     return dist, path
