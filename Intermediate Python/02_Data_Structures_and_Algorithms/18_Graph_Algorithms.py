from __future__ import annotations

import heapq
from collections import deque
from dataclasses import dataclass, field


class UniversityGraphAlgorithms:
    """Demonstrates basic BFS and DFS traversal over a species
    interaction network."""

    def __init__(self) -> None:
        self.adjacency: dict[str, list[str]] = {}

    def add_edge(self, vertex_a: str, vertex_b: str) -> None:
        """Time: O(1), Space: O(1)."""
        self.adjacency.setdefault(vertex_a, []).append(vertex_b)
        self.adjacency.setdefault(vertex_b, []).append(vertex_a)

    def bfs(self, start: str) -> list[str]:
        """Time: O(V + E), Space: O(V)."""
        visited = {start}
        order: list[str] = []
        queue: deque[str] = deque([start])
        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor in self.adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: str) -> list[str]:
        """Time: O(V + E), Space: O(V)."""
        visited: set[str] = set()
        order: list[str] = []

        def visit(vertex: str) -> None:
            visited.add(vertex)
            order.append(vertex)
            for neighbor in self.adjacency.get(vertex, []):
                if neighbor not in visited:
                    visit(neighbor)

        visit(start)
        return order

    @staticmethod
    def run() -> None:
        network = UniversityGraphAlgorithms()
        network.add_edge("Bee", "Flower")
        network.add_edge("Flower", "Aphid")
        network.add_edge("Aphid", "Ladybug")

        print("University: BFS from Bee ->", network.bfs("Bee"))
        print("University: DFS from Bee ->", network.dfs("Bee"))


class InterviewGraphAlgorithms:
    """Solves common graph traversal and shortest-path interview
    problems over a compound-target interaction network with unweighted
    edges (edge = one interaction hop)."""

    def __init__(self) -> None:
        self.adjacency: dict[str, list[str]] = {}

    def add_edge(self, vertex_a: str, vertex_b: str) -> None:
        """Time: O(1), Space: O(1)."""
        self.adjacency.setdefault(vertex_a, []).append(vertex_b)
        self.adjacency.setdefault(vertex_b, []).append(vertex_a)

    def shortest_path_unweighted(self, start: str, goal: str) -> list[str] | None:
        """BFS-based shortest path (fewest hops) for unweighted graphs.
        Explicitly handles start/goal not present in the graph.

        Time: O(V + E), Space: O(V)
        """
        if start not in self.adjacency or goal not in self.adjacency:
            return None
        if start == goal:
            return [start]

        visited = {start}
        parent: dict[str, str] = {}
        queue: deque[str] = deque([start])
        while queue:
            current = queue.popleft()
            for neighbor in self.adjacency.get(current, []):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                parent[neighbor] = current
                if neighbor == goal:
                    path = [goal]
                    while path[-1] != start:
                        path.append(parent[path[-1]])
                    return list(reversed(path))
                queue.append(neighbor)
        return None

    def connected_components(self) -> list[list[str]]:
        """Find all connected components in the graph.

        Time: O(V + E), Space: O(V)
        """
        visited: set[str] = set()
        components: list[list[str]] = []
        for vertex in self.adjacency:
            if vertex in visited:
                continue
            component: list[str] = []
            queue: deque[str] = deque([vertex])
            visited.add(vertex)
            while queue:
                current = queue.popleft()
                component.append(current)
                for neighbor in self.adjacency.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            components.append(component)
        return components

    @staticmethod
    def run() -> None:
        network = InterviewGraphAlgorithms()
        network.add_edge("CMPD-1", "EGFR")
        network.add_edge("EGFR", "RAS")
        network.add_edge("RAS", "MAPK")
        network.add_edge("CMPD-2", "ALK")  # separate component

        path = network.shortest_path_unweighted("CMPD-1", "MAPK")
        print("Interview: shortest path CMPD-1 -> MAPK ->", path)

        missing_path = network.shortest_path_unweighted("CMPD-1", "UNKNOWN")
        print("Interview: path to missing vertex (edge case) ->", missing_path)

        components = network.connected_components()
        print("Interview: connected components ->", components)


@dataclass(order=True)
class _PathCandidate:
    distance: float
    vertex: str = field(compare=False)


class IndustryGraphAlgorithms:
    """A reusable graph-analysis component for weighted biological
    interaction networks (e.g. metabolic pathway step costs), providing
    Dijkstra's shortest-path algorithm and topological sorting for
    directed acyclic dependency graphs (e.g. reaction step ordering).
    """

    def __init__(self, *, directed: bool = True) -> None:
        self.directed = directed
        self._adjacency: dict[str, list[tuple[str, float]]] = {}

    def add_vertex(self, vertex: str) -> None:
        """Time: O(1), Space: O(1)."""
        self._adjacency.setdefault(vertex, [])

    def add_edge(self, source: str, target: str, weight: float = 1.0) -> None:
        """Time: O(1), Space: O(1). Raises ValueError for negative weights
        since Dijkstra's algorithm requires non-negative edge weights."""
        if weight < 0:
            raise ValueError("Dijkstra's algorithm requires non-negative edge weights")
        self.add_vertex(source)
        self.add_vertex(target)
        self._adjacency[source].append((target, weight))
        if not self.directed:
            self._adjacency[target].append((source, weight))

    def shortest_path_dijkstra(self, start: str) -> dict[str, float]:
        """Compute shortest distances from start to every reachable vertex.

        Time: O((V + E) log V), Space: O(V + E)
        """
        if start not in self._adjacency:
            raise KeyError(f"unknown start vertex: {start}")
        distances: dict[str, float] = {vertex: float("inf") for vertex in self._adjacency}
        distances[start] = 0.0
        priority_queue: list[_PathCandidate] = [_PathCandidate(0.0, start)]
        visited: set[str] = set()

        while priority_queue:
            current = heapq.heappop(priority_queue)
            if current.vertex in visited:
                continue
            visited.add(current.vertex)
            for neighbor, weight in self._adjacency[current.vertex]:
                new_distance = current.distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, _PathCandidate(new_distance, neighbor))

        return distances

    def topological_sort(self) -> list[str]:
        """Kahn's algorithm for topologically ordering a directed acyclic
        graph of reaction-step dependencies.

        Time: O(V + E), Space: O(V)
        Raises ValueError if the graph contains a cycle.
        """
        if not self.directed:
            raise ValueError("topological sort requires a directed graph")

        in_degree: dict[str, int] = {vertex: 0 for vertex in self._adjacency}
        for edges in self._adjacency.values():
            for target, _weight in edges:
                in_degree[target] += 1

        queue: deque[str] = deque(v for v, degree in in_degree.items() if degree == 0)
        order: list[str] = []
        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor, _weight in self._adjacency[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self._adjacency):
            raise ValueError("graph contains a cycle; topological sort is undefined")
        return order

    @staticmethod
    def run() -> None:
        pathway = IndustryGraphAlgorithms(directed=True)
        pathway.add_edge("Glucose", "G6P", weight=1.0)
        pathway.add_edge("G6P", "F6P", weight=1.5)
        pathway.add_edge("F6P", "Pyruvate", weight=2.0)
        pathway.add_edge("G6P", "Pyruvate", weight=5.0)

        distances = pathway.shortest_path_dijkstra("Glucose")
        print("Industry: shortest metabolic distances from Glucose ->", distances)

        order = pathway.topological_sort()
        print("Industry: topological order of reaction steps ->", order)


if __name__ == "__main__":
    UniversityGraphAlgorithms.run()
    InterviewGraphAlgorithms.run()
    IndustryGraphAlgorithms.run()
