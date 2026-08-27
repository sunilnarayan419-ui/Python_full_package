from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class _UniversityNode:
    def __init__(self, value: str) -> None:
        self.value = value
        self.next: _UniversityNode | None = None


class UniversityLinkedList:
    """A simple singly linked list of sample processing stage names."""

    def __init__(self) -> None:
        self.head: _UniversityNode | None = None

    def insert_at_end(self, value: str) -> None:
        """Time: O(n) to reach the tail, Space: O(1)."""
        new_node = _UniversityNode(value)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def traverse(self) -> list[str]:
        """Time: O(n), Space: O(n) for the returned list."""
        result: list[str] = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def search(self, value: str) -> bool:
        """Time: O(n), Space: O(1)."""
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def delete(self, value: str) -> bool:
        """Time: O(n), Space: O(1)."""
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            return True
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                return True
            current = current.next
        return False

    @staticmethod
    def run() -> None:
        stages = UniversityLinkedList()
        for stage in ["collection", "extraction", "sequencing", "analysis"]:
            stages.insert_at_end(stage)
        print("University: stages ->", stages.traverse())
        print("University: contains 'sequencing' ->", stages.search("sequencing"))
        stages.delete("extraction")
        print("University: after deletion ->", stages.traverse())


@dataclass
class _InterviewNode:
    value: float
    next: "_InterviewNode | None" = None


class EmptyListError(Exception):
    """Raised when an operation requires a non-empty linked list."""


class InterviewLinkedList:
    """Singly linked list of experiment reading values with explicit
    handling of empty-list, single-node, head, and tail edge cases."""

    def __init__(self) -> None:
        self.head: _InterviewNode | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert_at_head(self, value: float) -> None:
        """Time: O(1), Space: O(1)."""
        new_node = _InterviewNode(value, next=self.head)
        self.head = new_node
        self._size += 1

    def insert_at_end(self, value: float) -> None:
        """Time: O(n), Space: O(1)."""
        new_node = _InterviewNode(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def delete_head(self) -> float:
        """Time: O(1), Space: O(1). Raises EmptyListError if empty."""
        if self.head is None:
            raise EmptyListError("cannot delete head of an empty list")
        removed = self.head.value
        self.head = self.head.next
        self._size -= 1
        return removed

    def delete_tail(self) -> float:
        """Time: O(n), Space: O(1). Raises EmptyListError if empty."""
        if self.head is None:
            raise EmptyListError("cannot delete tail of an empty list")
        if self.head.next is None:
            removed = self.head.value
            self.head = None
            self._size -= 1
            return removed
        current = self.head
        while current.next is not None and current.next.next is not None:
            current = current.next
        removed = current.next.value  # type: ignore[union-attr]
        current.next = None
        self._size -= 1
        return removed

    def reverse(self) -> None:
        """Reverse the list in place using three pointers.

        Time: O(n), Space: O(1)
        """
        previous: _InterviewNode | None = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        self.head = previous

    def to_list(self) -> list[float]:
        """Time: O(n), Space: O(n)."""
        result: list[float] = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    @staticmethod
    def run() -> None:
        readings = InterviewLinkedList()
        try:
            readings.delete_head()
        except EmptyListError as error:
            print("Interview: edge case (empty) ->", error)

        for value in [2.1, 4.4, 6.7]:
            readings.insert_at_end(value)
        readings.insert_at_head(0.5)
        print("Interview: before reverse ->", readings.to_list())
        readings.reverse()
        print("Interview: after reverse ->", readings.to_list())
        print("Interview: deleted tail ->", readings.delete_tail())
        print("Interview: deleted head ->", readings.delete_head())
        print("Interview: remaining ->", readings.to_list(), "size:", len(readings))


class ProcessingRecordNode(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: ProcessingRecordNode[T] | None = None


class IndustryLinkedList(Generic[T]):
    """A maintainable singly linked list abstraction for ordered
    scientific processing records (e.g. sequential pipeline stages),
    supporting append, iteration, and safe removal.

    Chosen over a plain list when records are frequently appended one
    at a time by upstream producers and consumed via head-to-tail
    iteration, avoiding list resize/copy overhead for that pattern.
    """

    def __init__(self) -> None:
        self._head: ProcessingRecordNode[T] | None = None
        self._tail: ProcessingRecordNode[T] | None = None
        self._length = 0

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def append(self, value: T) -> None:
        """Append using a tracked tail pointer.

        Time: O(1), Space: O(1)
        """
        node = ProcessingRecordNode(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._length += 1

    def remove_first_match(self, predicate) -> bool:  # noqa: ANN001
        """Remove the first record satisfying predicate.

        Time: O(n), Space: O(1)
        """
        previous: ProcessingRecordNode[T] | None = None
        current = self._head
        while current is not None:
            if predicate(current.value):
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next
                if current is self._tail:
                    self._tail = previous
                self._length -= 1
                return True
            previous = current
            current = current.next
        return False

    def is_empty(self) -> bool:
        return self._head is None

    @staticmethod
    def run() -> None:
        records: IndustryLinkedList[str] = IndustryLinkedList()
        for record in ["intake", "qc_check", "sequencing", "archival"]:
            records.append(record)
        print("Industry: records ->", list(records))
        removed = records.remove_first_match(lambda r: r == "qc_check")
        print("Industry: removed 'qc_check' ->", removed, "-> remaining:", list(records))
        print("Industry: length ->", len(records), "empty ->", records.is_empty())


if __name__ == "__main__":
    UniversityLinkedList.run()
    InterviewLinkedList.run()
    IndustryLinkedList.run()
