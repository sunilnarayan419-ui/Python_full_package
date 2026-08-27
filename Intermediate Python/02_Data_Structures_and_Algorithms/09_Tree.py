from __future__ import annotations

from dataclasses import dataclass, field


class _UniversityTreeNode:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list[_UniversityTreeNode] = []


class UniversityTree:
    """A simple general tree modeling an experiment's sample hierarchy."""

    def __init__(self, root_name: str) -> None:
        self.root = _UniversityTreeNode(root_name)

    def add_child(self, parent_node: _UniversityTreeNode, child_name: str) -> _UniversityTreeNode:
        """Time: O(1), Space: O(1)."""
        child = _UniversityTreeNode(child_name)
        parent_node.children.append(child)
        return child

    def preorder(self) -> list[str]:
        """Visit node, then children, left to right.

        Time: O(n), Space: O(n)
        """
        result: list[str] = []

        def visit(node: _UniversityTreeNode) -> None:
            result.append(node.name)
            for child in node.children:
                visit(child)

        visit(self.root)
        return result

    def height(self) -> int:
        """Longest path from root to a leaf, in edges.

        Time: O(n), Space: O(n) recursion depth
        """
        def depth(node: _UniversityTreeNode) -> int:
            if not node.children:
                return 0
            return 1 + max(depth(child) for child in node.children)

        return depth(self.root)

    @staticmethod
    def run() -> None:
        tree = UniversityTree("Experiment_001")
        sample_a = tree.add_child(tree.root, "Sample_A")
        tree.add_child(tree.root, "Sample_B")
        tree.add_child(sample_a, "Measurement_A1")
        tree.add_child(sample_a, "Measurement_A2")

        print("University: preorder traversal ->", tree.preorder())
        print("University: tree height ->", tree.height())


@dataclass
class _InterviewTreeNode:
    value: int
    left: "_InterviewTreeNode | None" = None
    right: "_InterviewTreeNode | None" = None


class InterviewTree:
    """A binary tree used to solve traversal and structural interview
    problems over measurement-magnitude values."""

    def __init__(self, root: _InterviewTreeNode | None = None) -> None:
        self.root = root

    def inorder(self) -> list[int]:
        """Left, node, right - yields sorted order for a valid BST.

        Time: O(n), Space: O(n)
        """
        result: list[int] = []

        def visit(node: _InterviewTreeNode | None) -> None:
            if node is None:
                return
            visit(node.left)
            result.append(node.value)
            visit(node.right)

        visit(self.root)
        return result

    def postorder(self) -> list[int]:
        """Left, right, node.

        Time: O(n), Space: O(n)
        """
        result: list[int] = []

        def visit(node: _InterviewTreeNode | None) -> None:
            if node is None:
                return
            visit(node.left)
            visit(node.right)
            result.append(node.value)

        visit(self.root)
        return result

    def max_depth(self) -> int:
        """Handles the empty-tree edge case explicitly.

        Time: O(n), Space: O(n)
        """
        def depth(node: _InterviewTreeNode | None) -> int:
            if node is None:
                return 0
            return 1 + max(depth(node.left), depth(node.right))

        return depth(self.root)

    def is_balanced(self) -> bool:
        """Check whether every subtree's left/right heights differ by <= 1.

        Time: O(n), Space: O(n)
        """
        def check(node: _InterviewTreeNode | None) -> tuple[bool, int]:
            if node is None:
                return True, 0
            left_balanced, left_height = check(node.left)
            right_balanced, right_height = check(node.right)
            balanced = (
                left_balanced
                and right_balanced
                and abs(left_height - right_height) <= 1
            )
            return balanced, 1 + max(left_height, right_height)

        balanced, _ = check(self.root)
        return balanced

    @staticmethod
    def run() -> None:
        empty_tree = InterviewTree()
        print("Interview: empty tree max depth (edge case) ->", empty_tree.max_depth())

        root = _InterviewTreeNode(50, left=_InterviewTreeNode(30), right=_InterviewTreeNode(70))
        root.left.left = _InterviewTreeNode(20)  # type: ignore[union-attr]
        root.right.right = _InterviewTreeNode(90)  # type: ignore[union-attr]
        tree = InterviewTree(root)

        print("Interview: inorder ->", tree.inorder())
        print("Interview: postorder ->", tree.postorder())
        print("Interview: max depth ->", tree.max_depth())
        print("Interview: is balanced ->", tree.is_balanced())


@dataclass(slots=True)
class HierarchyNode:
    label: str
    node_type: str  # "experiment" | "sample" | "measurement"
    value: float | None = None
    children: list["HierarchyNode"] = field(default_factory=list)


class InvalidHierarchyError(ValueError):
    """Raised when hierarchy structure rules are violated."""


_ALLOWED_CHILD_TYPES: dict[str, set[str]] = {
    "experiment": {"sample"},
    "sample": {"measurement"},
    "measurement": set(),
}


class IndustryTree:
    """A reusable hierarchical scientific data structure representing
    an experiment -> sample -> measurement hierarchy, with structural
    validation and reusable traversal utilities.
    """

    def __init__(self, experiment_label: str) -> None:
        self.root = HierarchyNode(label=experiment_label, node_type="experiment")

    def add_node(self, parent: HierarchyNode, child: HierarchyNode) -> None:
        """Attach a child, enforcing the experiment->sample->measurement rule.

        Time: O(1), Space: O(1)
        Raises InvalidHierarchyError on an illegal parent/child pairing.
        """
        allowed = _ALLOWED_CHILD_TYPES.get(parent.node_type, set())
        if child.node_type not in allowed:
            raise InvalidHierarchyError(
                f"{parent.node_type!r} cannot have a child of type {child.node_type!r}"
            )
        parent.children.append(child)

    def all_measurement_values(self) -> list[float]:
        """Collect every measurement value in the hierarchy.

        Time: O(n), Space: O(n)
        """
        values: list[float] = []

        def visit(node: HierarchyNode) -> None:
            if node.node_type == "measurement" and node.value is not None:
                values.append(node.value)
            for child in node.children:
                visit(child)

        visit(self.root)
        return values

    def height(self) -> int:
        """Time: O(n), Space: O(n)."""
        def depth(node: HierarchyNode) -> int:
            if not node.children:
                return 0
            return 1 + max(depth(child) for child in node.children)

        return depth(self.root)

    @staticmethod
    def run() -> None:
        hierarchy = IndustryTree("Experiment_2026_A")
        sample_1 = HierarchyNode("Sample_1", "sample")
        sample_2 = HierarchyNode("Sample_2", "sample")
        hierarchy.add_node(hierarchy.root, sample_1)
        hierarchy.add_node(hierarchy.root, sample_2)
        hierarchy.add_node(sample_1, HierarchyNode("pH_reading", "measurement", value=6.8))
        hierarchy.add_node(sample_1, HierarchyNode("temp_reading", "measurement", value=37.1))
        hierarchy.add_node(sample_2, HierarchyNode("pH_reading", "measurement", value=7.0))

        print("Industry: all measurement values ->", hierarchy.all_measurement_values())
        print("Industry: hierarchy height ->", hierarchy.height())

        try:
            hierarchy.add_node(hierarchy.root, HierarchyNode("bad_reading", "measurement", value=1.0))
        except InvalidHierarchyError as error:
            print("Industry: validation caught ->", error)


if __name__ == "__main__":
    UniversityTree.run()
    InterviewTree.run()
    IndustryTree.run()
