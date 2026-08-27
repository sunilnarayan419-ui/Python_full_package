from __future__ import annotations

from dataclasses import dataclass


class UniversitySearching:
    """Demonstrates linear search and binary search on plant height
    measurements (cm)."""

    def __init__(self, measurements: list[float]) -> None:
        self.measurements = measurements

    def linear_search(self, target: float) -> int:
        """Works on any list, sorted or not.

        Time: O(n), Space: O(1)
        """
        for index, value in enumerate(self.measurements):
            if value == target:
                return index
        return -1

    def binary_search(self, target: float) -> int:
        """Requires self.measurements to already be sorted ascending.

        Time: O(log n), Space: O(1)
        """
        sorted_values = sorted(self.measurements)
        low, high = 0, len(sorted_values) - 1
        while low <= high:
            mid = (low + high) // 2
            if sorted_values[mid] == target:
                return mid
            if sorted_values[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    @staticmethod
    def run() -> None:
        demo = UniversitySearching([12.5, 20.1, 9.3, 15.7, 30.2])
        print("University: linear search for 15.7 ->", demo.linear_search(15.7))
        print("University: binary search for 15.7 (sorted internally) ->", demo.binary_search(15.7))
        print("University: linear search for missing value ->", demo.linear_search(99.9))


class UnsortedInputError(ValueError):
    """Raised when binary search is attempted on unsorted data."""


class InterviewSearching:
    """Robust binary search and common variants for sorted patient
    heart-rate readings (bpm), with explicit precondition checks."""

    @staticmethod
    def _assert_sorted(readings: list[float]) -> None:
        if any(readings[i] > readings[i + 1] for i in range(len(readings) - 1)):
            raise UnsortedInputError("binary search requires ascending-sorted input")

    @staticmethod
    def binary_search(readings: list[float], target: float) -> int:
        """Time: O(log n), Space: O(1). Raises UnsortedInputError if not sorted."""
        InterviewSearching._assert_sorted(readings)
        low, high = 0, len(readings) - 1
        while low <= high:
            mid = (low + high) // 2
            if readings[mid] == target:
                return mid
            if readings[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    @staticmethod
    def find_first_occurrence(readings: list[float], target: float) -> int:
        """Leftmost-bound binary search variant, for duplicate readings.

        Time: O(log n), Space: O(1)
        """
        InterviewSearching._assert_sorted(readings)
        low, high = 0, len(readings) - 1
        result = -1
        while low <= high:
            mid = (low + high) // 2
            if readings[mid] == target:
                result = mid
                high = mid - 1  # keep searching left for an earlier match
            elif readings[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return result

    @staticmethod
    def find_insertion_point(readings: list[float], target: float) -> int:
        """Index where target should be inserted to keep readings sorted.

        Time: O(log n), Space: O(1)
        """
        InterviewSearching._assert_sorted(readings)
        low, high = 0, len(readings)
        while low < high:
            mid = (low + high) // 2
            if readings[mid] < target:
                low = mid + 1
            else:
                high = mid
        return low

    @staticmethod
    def run() -> None:
        readings = [58.0, 60.0, 60.0, 63.0, 71.0, 78.0]
        print("Interview: binary search for 63.0 ->", InterviewSearching.binary_search(readings, 63.0))
        print("Interview: first occurrence of 60.0 ->", InterviewSearching.find_first_occurrence(readings, 60.0))
        print("Interview: insertion point for 65.0 ->", InterviewSearching.find_insertion_point(readings, 65.0))

        try:
            InterviewSearching.binary_search([5.0, 1.0, 3.0], 1.0)
        except UnsortedInputError as error:
            print("Interview: precondition caught ->", error)


@dataclass(slots=True, frozen=True)
class IndexedRecord:
    identifier: str
    sort_value: float


class IndustrySearching:
    """Reusable searching utilities for sorted, indexed scientific
    records, exposed as a small stateless utility class suitable for
    reuse across a production analytics pipeline.
    """

    @staticmethod
    def _validate_sorted(records: list[IndexedRecord]) -> None:
        for i in range(len(records) - 1):
            if records[i].sort_value > records[i + 1].sort_value:
                raise UnsortedInputError(
                    "records must be sorted ascending by sort_value before searching"
                )

    @staticmethod
    def binary_search_by_value(records: list[IndexedRecord], target_value: float) -> IndexedRecord | None:
        """Find a record by its sort_value using binary search.

        Time: O(log n), Space: O(1)
        Raises UnsortedInputError if records are not sorted.
        """
        if not records:
            return None
        IndustrySearching._validate_sorted(records)
        low, high = 0, len(records) - 1
        while low <= high:
            mid = (low + high) // 2
            if records[mid].sort_value == target_value:
                return records[mid]
            if records[mid].sort_value < target_value:
                low = mid + 1
            else:
                high = mid - 1
        return None

    @staticmethod
    def range_query(records: list[IndexedRecord], low_value: float, high_value: float) -> list[IndexedRecord]:
        """Return all records with sort_value in [low_value, high_value]
        using two binary searches to locate the range boundaries.

        Time: O(log n + k) where k is the number of matches
        Space: O(k)
        """
        if low_value > high_value:
            raise ValueError("low_value must not exceed high_value")
        if not records:
            return []
        IndustrySearching._validate_sorted(records)

        def lower_bound(target: float) -> int:
            low, high = 0, len(records)
            while low < high:
                mid = (low + high) // 2
                if records[mid].sort_value < target:
                    low = mid + 1
                else:
                    high = mid
            return low

        start = lower_bound(low_value)
        end = lower_bound(high_value + 1e-9)  # inclusive of exact high_value matches
        return records[start:end]

    @staticmethod
    def run() -> None:
        records = [
            IndexedRecord("REC-1", 2.0),
            IndexedRecord("REC-2", 4.5),
            IndexedRecord("REC-3", 7.1),
            IndexedRecord("REC-4", 9.9),
            IndexedRecord("REC-5", 12.3),
        ]
        found = IndustrySearching.binary_search_by_value(records, 7.1)
        print("Industry: found record ->", found)

        in_range = IndustrySearching.range_query(records, 4.0, 10.0)
        print("Industry: records in [4.0, 10.0] ->", [r.identifier for r in in_range])


if __name__ == "__main__":
    UniversitySearching.run()
    InterviewSearching.run()
    IndustrySearching.run()
