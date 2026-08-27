from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


class UniversityStack:
    """Basic LIFO stack demonstrated with an experiment processing history."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        """Time: O(1) amortized, Space: O(1)."""
        self._items.append(item)

    def pop(self) -> str:
        """Time: O(1), Space: O(1)."""
        return self._items.pop()

    def peek(self) -> str:
        """Time: O(1), Space: O(1)."""
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    @staticmethod
    def run() -> None:
        history = UniversityStack()
        for step in ["load_sample", "calibrate", "run_assay"]:
            history.push(step)
        print("University: last step performed ->", history.peek())
        undone = history.pop()
        print("University: undid step ->", undone)
        print("University: is empty ->", history.is_empty())


class StackUnderflowError(Exception):
    """Raised when popping/peeking an empty stack."""


class InterviewStack:
    """Stack implementation used to solve a realistic interview problem:
    validating that nested reaction-step brackets in a lab protocol
    notation are balanced, e.g. "(A(B)C)".
    """

    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        """Time: O(1) amortized, Space: O(1)."""
        self._items.append(item)

    def pop(self) -> str:
        """Time: O(1), Space: O(1). Raises StackUnderflowError if empty."""
        if not self._items:
            raise StackUnderflowError("cannot pop from an empty stack")
        return self._items.pop()

    def peek(self) -> str:
        """Time: O(1), Space: O(1). Raises StackUnderflowError if empty."""
        if not self._items:
            raise StackUnderflowError("cannot peek an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    @staticmethod
    def is_balanced_protocol(notation: str) -> bool:
        """Validate that parentheses in a protocol notation are balanced.

        Time: O(n), Space: O(n)
        """
        if not notation:
            return True
        stack = InterviewStack()
        for char in notation:
            if char == "(":
                stack.push(char)
            elif char == ")":
                if stack.is_empty():
                    return False
                stack.pop()
        return stack.is_empty()

    @staticmethod
    def run() -> None:
        test_cases = ["(A(B)C)", "(A(BC)", "()", "", "A)B("]
        for notation in test_cases:
            result = InterviewStack.is_balanced_protocol(notation)
            print(f"Interview: '{notation}' balanced -> {result}")

        stack = InterviewStack()
        try:
            stack.pop()
        except StackUnderflowError as error:
            print("Interview: edge case caught ->", error)


@dataclass(slots=True)
class ProtocolStep:
    name: str
    parameters: dict[str, float] = field(default_factory=dict)


class IndustryStack:
    """A reusable, validated stack abstraction for tracking executed
    protocol steps in a lab-automation system, backed by collections.deque
    for O(1) amortized push/pop at both ends and efficient memory use.
    """

    def __init__(self, max_size: int | None = None) -> None:
        if max_size is not None and max_size <= 0:
            raise ValueError("max_size must be positive when provided")
        self._items: deque[ProtocolStep] = deque()
        self._max_size = max_size

    def push(self, step: ProtocolStep) -> None:
        """Time: O(1), Space: O(1). Raises OverflowError if capacity is exceeded."""
        if self._max_size is not None and len(self._items) >= self._max_size:
            raise OverflowError(f"stack capacity of {self._max_size} exceeded")
        self._items.append(step)

    def pop(self) -> ProtocolStep:
        """Time: O(1), Space: O(1). Raises StackUnderflowError if empty."""
        if not self._items:
            raise StackUnderflowError("no protocol steps to undo")
        return self._items.pop()

    def peek(self) -> ProtocolStep:
        """Time: O(1), Space: O(1). Raises StackUnderflowError if empty."""
        if not self._items:
            raise StackUnderflowError("no protocol steps recorded")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def history_snapshot(self) -> list[str]:
        """Return step names, most recent last, without mutating the stack.

        Time: O(n), Space: O(n)
        """
        return [step.name for step in self._items]

    @staticmethod
    def run() -> None:
        executor = IndustryStack(max_size=5)
        executor.push(ProtocolStep("mix_reagents", {"volume_ml": 5.0}))
        executor.push(ProtocolStep("incubate", {"minutes": 30.0}))
        executor.push(ProtocolStep("centrifuge", {"rpm": 3000.0}))
        print("Industry: history ->", executor.history_snapshot())
        last_step = executor.pop()
        print("Industry: undid ->", last_step.name)
        print("Industry: current top ->", executor.peek().name)
        print("Industry: remaining count ->", len(executor))


if __name__ == "__main__":
    UniversityStack.run()
    InterviewStack.run()
    IndustryStack.run()
