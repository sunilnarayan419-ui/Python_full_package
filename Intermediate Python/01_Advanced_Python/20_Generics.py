from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")
NumericT = TypeVar("NumericT", int, float)


class UniversityGenerics:
    """Demonstrates a basic generic container class using TypeVar and
    Generic, holding a single labeled measurement of any numeric type."""

    class LabeledValue(Generic[T]):
        def __init__(self, label: str, value: T) -> None:
            self.label = label
            self.value = value

        def __repr__(self) -> str:
            return f"LabeledValue(label={self.label!r}, value={self.value!r})"

    @staticmethod
    def run() -> None:
        height = UniversityGenerics.LabeledValue[float]("height_cm", 12.5)
        count = UniversityGenerics.LabeledValue[int]("leaf_count", 8)
        print(height)
        print(count)


class InterviewGenerics:
    """Demonstrates a generic, reusable bounded buffer that works across
    different sample types while preserving static type information,
    showing how generics avoid duplicated container code."""

    class SampleBuffer(Generic[T]):
        def __init__(self, capacity: int) -> None:
            if capacity <= 0:
                raise ValueError("capacity must be positive")
            self._capacity = capacity
            self._items: list[T] = []

        def add(self, item: T) -> None:
            if len(self._items) >= self._capacity:
                self._items.pop(0)
            self._items.append(item)

        def latest(self) -> T | None:
            return self._items[-1] if self._items else None

        def all_items(self) -> list[T]:
            return list(self._items)

    @staticmethod
    def run() -> None:
        temperature_buffer: InterviewGenerics.SampleBuffer[float] = InterviewGenerics.SampleBuffer(capacity=3)
        for value in (21.5, 22.0, 22.8, 23.1):
            temperature_buffer.add(value)
        print(temperature_buffer.all_items())

        label_buffer: InterviewGenerics.SampleBuffer[str] = InterviewGenerics.SampleBuffer(capacity=2)
        label_buffer.add("sample-A")
        label_buffer.add("sample-B")
        print(label_buffer.latest())


class IndustryGenerics:
    """Demonstrates a reusable, constrained generic repository abstraction
    for scientific domain models, using a bound TypeVar to guarantee that
    stored items expose an identifier, while remaining generic over the
    concrete record type used across different pipelines."""

    class Identifiable(Generic[T]):
        """Marker-like base requiring an identifiable record type."""

        record_id: str

    RecordT = TypeVar("RecordT", bound="IndustryGenerics.Identifiable")

    class SequencingRecord(Identifiable):
        def __init__(self, record_id: str, read_count: int) -> None:
            self.record_id = record_id
            self.read_count = read_count

        def __repr__(self) -> str:
            return f"SequencingRecord(record_id={self.record_id!r}, read_count={self.read_count})"

    class AssayRecord(Identifiable):
        def __init__(self, record_id: str, absorbance: float) -> None:
            self.record_id = record_id
            self.absorbance = absorbance

        def __repr__(self) -> str:
            return f"AssayRecord(record_id={self.record_id!r}, absorbance={self.absorbance})"

    class Repository(Generic[RecordT]):
        """A generic, type-safe in-memory repository reusable across any
        record type that satisfies the Identifiable bound."""

        def __init__(self) -> None:
            self._records: dict[str, "IndustryGenerics.RecordT"] = {}

        def add(self, record: "IndustryGenerics.RecordT") -> None:
            if record.record_id in self._records:
                raise ValueError(f"duplicate record_id: {record.record_id}")
            self._records[record.record_id] = record

        def get(self, record_id: str) -> "IndustryGenerics.RecordT":
            if record_id not in self._records:
                raise KeyError(f"no record found for id: {record_id}")
            return self._records[record_id]

        def all(self) -> list["IndustryGenerics.RecordT"]:
            return list(self._records.values())

    @staticmethod
    def run() -> None:
        sequencing_repo: IndustryGenerics.Repository[IndustryGenerics.SequencingRecord] = (
            IndustryGenerics.Repository()
        )
        sequencing_repo.add(IndustryGenerics.SequencingRecord("seq-001", 4_500_000))
        sequencing_repo.add(IndustryGenerics.SequencingRecord("seq-002", 3_900_000))
        print(sequencing_repo.all())

        assay_repo: IndustryGenerics.Repository[IndustryGenerics.AssayRecord] = IndustryGenerics.Repository()
        assay_repo.add(IndustryGenerics.AssayRecord("assay-001", 0.842))
        print(assay_repo.get("assay-001"))

        try:
            sequencing_repo.add(IndustryGenerics.SequencingRecord("seq-001", 1_000_000))
        except ValueError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityGenerics.run()
    InterviewGenerics.run()
    IndustryGenerics.run()
