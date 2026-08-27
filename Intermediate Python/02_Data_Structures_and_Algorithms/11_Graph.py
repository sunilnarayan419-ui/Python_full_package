from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


class UniversityGraph:
    """A basic undirected adjacency-list graph of gene-pathway
    relationships."""

    def __init__(self) -> None:
        self.adjacency: dict[str, list[str]] = {}

    def add_vertex(self, vertex: str) -> None:
        """Time: O(1), Space: O(1)."""
        self.adjacency.setdefault(vertex, [])

    def add_edge(self, vertex_a: str, vertex_b: str) -> None:
        """Undirected edge: add each vertex to the other's adjacency list.

        Time: O(1), Space: O(1)
        """
        self.add_vertex(vertex_a)
        self.add_vertex(vertex_b)
        self.adjacency[vertex_a].append(vertex_b)
        self.adjacency[vertex_b].append(vertex_a)

    def neighbors(self, vertex: str) -> list[str]:
        """Time: O(1), Space: O(1)."""
        return self.adjacency.get(vertex, [])

    @staticmethod
    def run() -> None:
        graph = UniversityGraph()
        graph.add_edge("TP53", "Apoptosis_Pathway")
        graph.add_edge("TP53", "Cell_Cycle_Pathway")
        graph.add_edge("BRCA1", "DNA_Repair_Pathway")

        print("University: neighbors of TP53 ->", graph.neighbors("TP53"))
        print("University: full adjacency ->", graph.adjacency)


class InterviewGraph:
    """A directed adjacency-list graph of compound -> target relationships,
    supporting traversal and connectivity queries common in interviews."""

    def __init__(self) -> None:
        self.adjacency: dict[str, list[str]] = {}

    def add_vertex(self, vertex: str) -> None:
        """Time: O(1), Space: O(1)."""
        self.adjacency.setdefault(vertex, [])

    def add_edge(self, source: str, destination: str) -> None:
        """Directed edge from source to destination.

        Time: O(1), Space: O(1)
        """
        self.add_vertex(source)
        self.add_vertex(destination)
        self.adjacency[source].append(destination)

    def bfs(self, start: str) -> list[str]:
        """Breadth-first traversal from start. Handles a start vertex
        not present in the graph.

        Time: O(V + E), Space: O(V)
        """
        if start not in self.adjacency:
            return []
        visited = {start}
        order: list[str] = []
        queue: deque[str] = deque([start])
        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor in self.adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def has_path(self, source: str, destination: str) -> bool:
        """Determine reachability from source to destination via BFS.

        Time: O(V + E), Space: O(V)
        """
        if source not in self.adjacency or destination not in self.adjacency:
            return False
        return destination in self.bfs(source)

    @staticmethod
    def run() -> None:
        graph = InterviewGraph()
        graph.add_edge("CMPD-001", "EGFR")
        graph.add_edge("EGFR", "Cell_Proliferation")
        graph.add_edge("CMPD-002", "ALK")

        print("Interview: BFS from CMPD-001 ->", graph.bfs("CMPD-001"))
        print("Interview: path CMPD-001 -> Cell_Proliferation ->", graph.has_path("CMPD-001", "Cell_Proliferation"))
        print("Interview: path CMPD-002 -> Cell_Proliferation ->", graph.has_path("CMPD-002", "Cell_Proliferation"))
        print("Interview: BFS from missing vertex (edge case) ->", graph.bfs("UNKNOWN"))


@dataclass(slots=True)
class Edge:
    target: str
    relationship: str
    weight: float = 1.0


class UnknownVertexError(KeyError):
    """Raised when referencing a vertex that has not been added."""


class IndustryGraph:
    """A reusable graph representation for scientific relationship
    networks (e.g. species interactions, sample processing stages),
    supporting typed/weighted edges and validated vertex management.
    """

    def __init__(self, *, directed: bool = True) -> None:
        self.directed = directed
        self._adjacency: dict[str, list[Edge]] = {}

    def add_vertex(self, vertex: str) -> None:
        """Time: O(1), Space: O(1)."""
        self._adjacency.setdefault(vertex, [])

    def add_edge(self, source: str, target: str, relationship: str, weight: float = 1.0) -> None:
        """Add a typed, optionally weighted edge.

        Time: O(1), Space: O(1)
        Raises UnknownVertexError if either endpoint hasn't been added.
        """
        if source not in self._adjacency:
            raise UnknownVertexError(f"unknown vertex: {source}")
        if target not in self._adjacency:
            raise UnknownVertexError(f"unknown vertex: {target}")
        self._adjacency[source].append(Edge(target=target, relationship=relationship, weight=weight))
        if not self.directed:
            self._adjacency[target].append(Edge(target=source, relationship=relationship, weight=weight))

    def edges_from(self, vertex: str) -> list[Edge]:
        """Time: O(1), Space: O(1). Raises UnknownVertexError if missing."""
        if vertex not in self._adjacency:
            raise UnknownVertexError(f"unknown vertex: {vertex}")
        return self._adjacency[vertex]

    def vertex_count(self) -> int:
        return len(self._adjacency)

    def edge_count(self) -> int:
        """Time: O(V), Space: O(1)."""
        return sum(len(edges) for edges in self._adjacency.values())

    @staticmethod
    def run() -> None:
        network = IndustryGraph(directed=True)
        for species in ["Bee", "Flower_A", "Aphid", "Ladybug"]:
            network.add_vertex(species)

        network.add_edge("Bee", "Flower_A", relationship="pollinates")
        network.add_edge("Aphid", "Flower_A", relationship="feeds_on", weight=0.6)
        network.add_edge("Ladybug", "Aphid", relationship="predates", weight=0.9)

        print("Industry: edges from Ladybug ->", network.edges_from("Ladybug"))
        print("Industry: vertex count ->", network.vertex_count())
        print("Industry: edge count ->", network.edge_count())

        try:
            network.edges_from("Unknown_Species")
        except UnknownVertexError as error:
            print("Industry: validation caught ->", error)


if __name__ == "__main__":
    UniversityGraph.run()
    InterviewGraph.run()
    IndustryGraph.run()
