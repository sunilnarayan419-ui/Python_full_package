from __future__ import annotations

from dataclasses import dataclass


class _UniversityBSTNode:
    def __init__(self, key: float) -> None:
        self.key = key
        self.left: _UniversityBSTNode | None = None
        self.right: _UniversityBSTNode | None = None


class UniversityBinarySearchTree:
    """A basic BST storing sample concentration values, where every
    left subtree holds smaller values and every right subtree holds
    larger values."""

    def __init__(self) -> None:
        self.root: _UniversityBSTNode | None = None

    def insert(self, key: float) -> None:
        """Time: O(h) where h is tree height, Space: O(h) recursion."""
        def _insert(node: _UniversityBSTNode | None, key: float) -> _UniversityBSTNode:
            if node is None:
                return _UniversityBSTNode(key)
            if key < node.key:
                node.left = _insert(node.left, key)
            elif key > node.key:
                node.right = _insert(node.right, key)
            return node

        self.root = _insert(self.root, key)

    def search(self, key: float) -> bool:
        """Time: O(h), Space: O(h) recursion."""
        def _search(node: _UniversityBSTNode | None, key: float) -> bool:
            if node is None:
                return False
            if node.key == key:
                return True
            return _search(node.left, key) if key < node.key else _search(node.right, key)

        return _search(self.root, key)

    def inorder(self) -> list[float]:
        """Time: O(n), Space: O(n)."""
        result: list[float] = []

        def visit(node: _UniversityBSTNode | None) -> None:
            if node is None:
                return
            visit(node.left)
            result.append(node.key)
            visit(node.right)

        visit(self.root)
        return result

    @staticmethod
    def run() -> None:
        bst = UniversityBinarySearchTree()
        for value in [15.5, 8.2, 22.1, 4.0, 12.3]:
            bst.insert(value)
        print("University: inorder (sorted) ->", bst.inorder())
        print("University: contains 12.3 ->", bst.search(12.3))
        print("University: contains 99.9 ->", bst.search(99.9))


@dataclass
class _InterviewBSTNode:
    key: float
    left: "_InterviewBSTNode | None" = None
    right: "_InterviewBSTNode | None" = None


class InterviewBinarySearchTree:
    """A BST used to solve interview-style problems on gene-expression
    threshold values: search, insertion, min/max, and BST validation."""

    def __init__(self) -> None:
        self.root: _InterviewBSTNode | None = None

    def insert(self, key: float) -> None:
        """Time: O(h), Space: O(h) recursion. Ignores duplicate keys."""
        def _insert(node: _InterviewBSTNode | None, key: float) -> _InterviewBSTNode:
            if node is None:
                return _InterviewBSTNode(key)
            if key < node.key:
                node.left = _insert(node.left, key)
            elif key > node.key:
                node.right = _insert(node.right, key)
            return node

        self.root = _insert(self.root, key)

    def find_min(self) -> float | None:
        """Time: O(h), Space: O(1). Handles empty tree."""
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return current.key

    def find_max(self) -> float | None:
        """Time: O(h), Space: O(1). Handles empty tree."""
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return current.key

    def is_valid_bst(self) -> bool:
        """Verify the BST invariant holds across the whole tree, not
        just at each node's immediate children (a common interview
        pitfall is checking only local ordering).

        Time: O(n), Space: O(n)
        """
        def validate(
            node: _InterviewBSTNode | None,
            lower: float | None,
            upper: float | None,
        ) -> bool:
            if node is None:
                return True
            if lower is not None and node.key <= lower:
                return False
            if upper is not None and node.key >= upper:
                return False
            return validate(node.left, lower, node.key) and validate(node.right, node.key, upper)

        return validate(self.root, None, None)

    @staticmethod
    def run() -> None:
        bst = InterviewBinarySearchTree()
        print("Interview: empty tree min (edge case) ->", bst.find_min())

        for value in [0.75, 0.32, 0.91, 0.15, 0.55]:
            bst.insert(value)
        print("Interview: min ->", bst.find_min())
        print("Interview: max ->", bst.find_max())
        print("Interview: is valid BST ->", bst.is_valid_bst())


@dataclass(slots=True)
class SampleRecord:
    sample_id: str
    concentration: float


class _IndustryBSTNode:
    __slots__ = ("record", "left", "right")

    def __init__(self, record: SampleRecord) -> None:
        self.record = record
        self.left: _IndustryBSTNode | None = None
        self.right: _IndustryBSTNode | None = None


class IndustryBinarySearchTree:
    """A maintainable BST abstraction, keyed by concentration, for
    indexing sample records with ordered retrieval, range queries, and
    deletion.

    Trade-off note: an unbalanced BST degrades to O(n) on sorted or
    adversarial insertion order. For production workloads with
    unpredictable insert patterns, a self-balancing structure (e.g.
    a red-black tree) or Python's bisect-based sorted list would give
    guaranteed O(log n); this class documents that limitation rather
    than claiming the BST is always optimal.
    """

    def __init__(self) -> None:
        self._root: _IndustryBSTNode | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert(self, record: SampleRecord) -> None:
        """Time: O(h) average O(log n), worst case O(n) if unbalanced.
        Space: O(h) recursion.
        """
        def _insert(node: _IndustryBSTNode | None, record: SampleRecord) -> _IndustryBSTNode:
            if node is None:
                self._size += 1
                return _IndustryBSTNode(record)
            if record.concentration < node.record.concentration:
                node.left = _insert(node.left, record)
            elif record.concentration > node.record.concentration:
                node.right = _insert(node.right, record)
            else:
                node.record = record  # overwrite on exact concentration match
            return node

        self._root = _insert(self._root, record)

    def find_in_range(self, low: float, high: float) -> list[SampleRecord]:
        """Return all records with concentration in [low, high], sorted.

        Time: O(k + h) where k is the number of matches, Space: O(k)
        """
        if low > high:
            raise ValueError("low must not exceed high")
        results: list[SampleRecord] = []

        def visit(node: _IndustryBSTNode | None) -> None:
            if node is None:
                return
            if node.record.concentration > low:
                visit(node.left)
            if low <= node.record.concentration <= high:
                results.append(node.record)
            if node.record.concentration < high:
                visit(node.right)

        visit(self._root)
        return results

    def delete(self, concentration: float) -> bool:
        """Standard BST deletion with in-order successor replacement.

        Time: O(h), Space: O(h) recursion
        """
        deleted = False

        def _delete(node: _IndustryBSTNode | None, concentration: float) -> _IndustryBSTNode | None:
            nonlocal deleted
            if node is None:
                return None
            if concentration < node.record.concentration:
                node.left = _delete(node.left, concentration)
            elif concentration > node.record.concentration:
                node.right = _delete(node.right, concentration)
            else:
                deleted = True
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.record = successor.record
                node.right = _delete(node.right, successor.record.concentration)
            return node

        self._root = _delete(self._root, concentration)
        if deleted:
            self._size -= 1
        return deleted

    @staticmethod
    def run() -> None:
        index = IndustryBinarySearchTree()
        for sample_id, concentration in [
            ("S1", 5.5), ("S2", 2.1), ("S3", 8.9), ("S4", 1.0), ("S5", 4.4),
        ]:
            index.insert(SampleRecord(sample_id, concentration))

        in_range = index.find_in_range(2.0, 6.0)
        print("Industry: samples with concentration in [2.0, 6.0] ->", [r.sample_id for r in in_range])
        deleted = index.delete(2.1)
        print("Industry: deleted concentration 2.1 ->", deleted)
        print("Industry: total remaining ->", len(index))


if __name__ == "__main__":
    UniversityBinarySearchTree.run()
    InterviewBinarySearchTree.run()
    IndustryBinarySearchTree.run()
