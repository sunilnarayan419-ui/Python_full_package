from __future__ import annotations

from dataclasses import dataclass, field


class UniversityArrays:
    """Basic array (Python list) operations over plant height measurements (cm)."""

    def __init__(self, measurements: list[float]) -> None:
        self.measurements = measurements

    def get_at(self, index: int) -> float:
        """Time: O(1), Space: O(1)."""
        return self.measurements[index]

    def traverse_and_print(self) -> None:
        """Time: O(n), Space: O(1)."""
        for i, value in enumerate(self.measurements):
            print(f"  index {i}: {value} cm")

    def insert_at_end(self, value: float) -> None:
        """Time: O(1) amortized, Space: O(1)."""
        self.measurements.append(value)

    def delete_at(self, index: int) -> float:
        """Time: O(n) due to shifting, Space: O(1)."""
        return self.measurements.pop(index)

    def update_at(self, index: int, value: float) -> None:
        """Time: O(1), Space: O(1)."""
        self.measurements[index] = value

    def linear_search(self, value: float) -> int:
        """Time: O(n), Space: O(1)."""
        for i, measurement in enumerate(self.measurements):
            if measurement == value:
                return i
        return -1

    def sum_all(self) -> float:
        """Time: O(n), Space: O(1)."""
        return sum(self.measurements)

    @staticmethod
    def run() -> None:
        arr = UniversityArrays([12.5, 20.1, 9.3, 15.7])
        print("University: traversal")
        arr.traverse_and_print()
        arr.insert_at_end(18.0)
        arr.update_at(0, 13.0)
        removed = arr.delete_at(2)
        print("University: removed", removed, "-> final:", arr.measurements)
        print("University: index of 15.7 ->", arr.linear_search(15.7))
        print("University: sum ->", arr.sum_all())


class InterviewArrays:
    """Common array interview patterns applied to lab sample concentration readings."""

    @staticmethod
    def find_max_min(readings: list[float]) -> tuple[float, float]:
        """Single-pass max/min tracking.

        Time: O(n), Space: O(1)
        """
        if not readings:
            raise ValueError("readings must not be empty")
        current_max = current_min = readings[0]
        for value in readings[1:]:
            if value > current_max:
                current_max = value
            if value < current_min:
                current_min = value
        return current_max, current_min

    @staticmethod
    def filter_above_threshold(readings: list[float], threshold: float) -> list[float]:
        """Time: O(n), Space: O(k) where k is the number of matches."""
        return [value for value in readings if value > threshold]

    @staticmethod
    def find_duplicate_sample_ids(sample_ids: list[str]) -> list[str]:
        """Detect duplicate sample IDs using a hash set.

        Time: O(n), Space: O(n)
        """
        seen: set[str] = set()
        duplicates: list[str] = []
        for sample_id in sample_ids:
            if sample_id in seen and sample_id not in duplicates:
                duplicates.append(sample_id)
            seen.add(sample_id)
        return duplicates

    @staticmethod
    def two_pointer_pair_sum(sorted_readings: list[float], target: float) -> tuple[int, int] | None:
        """Find indices of two readings summing to target in a SORTED array.

        Time: O(n), Space: O(1)

        Preconditions: sorted_readings must already be sorted ascending.
        """
        if len(sorted_readings) < 2:
            return None
        left, right = 0, len(sorted_readings) - 1
        while left < right:
            current_sum = sorted_readings[left] + sorted_readings[right]
            if current_sum == target:
                return left, right
            if current_sum < target:
                left += 1
            else:
                right -= 1
        return None

    @staticmethod
    def run() -> None:
        readings = [3.2, 7.9, 1.4, 9.0, 4.5]
        print("Interview: max/min ->", InterviewArrays.find_max_min(readings))
        print("Interview: above 4.0 ->", InterviewArrays.filter_above_threshold(readings, 4.0))

        sample_ids = ["S001", "S002", "S003", "S002", "S004", "S001"]
        print("Interview: duplicate sample IDs ->", InterviewArrays.find_duplicate_sample_ids(sample_ids))

        sorted_readings = sorted(readings)
        print(
            "Interview: pair summing to 11.2 (indices in sorted array) ->",
            InterviewArrays.two_pointer_pair_sum(sorted_readings, 11.2),
        )


@dataclass(slots=True)
class Measurement:
    sample_id: str
    value: float
    unit: str


class MeasurementValidationError(ValueError):
    """Raised when a measurement fails validation."""


class IndustryArrays:
    """A reusable, validated scientific measurement collection component
    for storing and analyzing lab measurements at scale."""

    def __init__(self) -> None:
        self._measurements: list[Measurement] = []

    def add(self, sample_id: str, value: float, unit: str) -> None:
        """Validate and append a measurement.

        Time: O(1) amortized, Space: O(1)
        """
        if not sample_id:
            raise MeasurementValidationError("sample_id must not be empty")
        if value < 0:
            raise MeasurementValidationError(f"value must be non-negative, got {value}")
        if not unit:
            raise MeasurementValidationError("unit must not be empty")
        self._measurements.append(Measurement(sample_id=sample_id, value=value, unit=unit))

    def as_list(self) -> list[Measurement]:
        """Time: O(1), Space: O(1) - returns a reference, not a copy."""
        return self._measurements

    def average_value(self, unit: str | None = None) -> float:
        """Average value, optionally filtered by unit.

        Time: O(n), Space: O(1)
        """
        relevant = [m.value for m in self._measurements if unit is None or m.unit == unit]
        if not relevant:
            return 0.0
        return sum(relevant) / len(relevant)

    def find_by_sample_id(self, sample_id: str) -> Measurement | None:
        """Time: O(n), Space: O(1)."""
        for measurement in self._measurements:
            if measurement.sample_id == sample_id:
                return measurement
        return None

    def top_n_by_value(self, n: int) -> list[Measurement]:
        """Return the n highest-value measurements without mutating storage order.

        Time: O(n log n), Space: O(n)
        """
        if n <= 0:
            return []
        return sorted(self._measurements, key=lambda m: m.value, reverse=True)[:n]

    @staticmethod
    def run() -> None:
        collection = IndustryArrays()
        collection.add("S101", 5.6, "mg/L")
        collection.add("S102", 12.3, "mg/L")
        collection.add("S103", 8.1, "mg/L")
        collection.add("S104", 15.9, "mg/L")

        print("Industry: average concentration ->", round(collection.average_value("mg/L"), 2))
        found = collection.find_by_sample_id("S103")
        print("Industry: found S103 ->", found)
        top_two = collection.top_n_by_value(2)
        print("Industry: top 2 measurements ->", top_two)

        try:
            collection.add("S105", -1.0, "mg/L")
        except MeasurementValidationError as error:
            print("Industry: validation caught ->", error)


if __name__ == "__main__":
    UniversityArrays.run()
    InterviewArrays.run()
    IndustryArrays.run()
