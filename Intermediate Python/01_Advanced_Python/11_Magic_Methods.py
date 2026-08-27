from __future__ import annotations

from typing import Iterator


class UniversityMagicMethods:
    """Demonstrates basic dunder methods: __repr__, __str__, and __len__."""

    class SampleCollection:
        def __init__(self, samples: list[str]) -> None:
            self.samples = samples

        def __repr__(self) -> str:
            return f"SampleCollection({self.samples!r})"

        def __str__(self) -> str:
            return f"{len(self.samples)} samples"

        def __len__(self) -> int:
            return len(self.samples)

    @staticmethod
    def run() -> None:
        collection = UniversityMagicMethods.SampleCollection(["leaf-01", "leaf-02", "root-01"])
        print(str(collection))
        print(repr(collection))
        print(len(collection))


class InterviewMagicMethods:
    """Demonstrates dunder methods enabling iteration, indexing, and
    containment checks, letting a custom class behave like a built-in
    sequence type."""

    class MeasurementSeries:
        def __init__(self, values: list[float]) -> None:
            self._values = list(values)

        def __len__(self) -> int:
            return len(self._values)

        def __getitem__(self, index: int) -> float:
            return self._values[index]

        def __iter__(self) -> Iterator[float]:
            return iter(self._values)

        def __contains__(self, value: float) -> bool:
            return value in self._values

        def __repr__(self) -> str:
            return f"MeasurementSeries({self._values!r})"

    @staticmethod
    def run() -> None:
        series = InterviewMagicMethods.MeasurementSeries([5.1, 5.4, 5.0, 5.9])
        print(series[0])
        print([v for v in series])
        print(5.9 in series)
        print(6.5 in series)


class IndustryMagicMethods:
    """Demonstrates a richer set of dunder methods implementing value
    semantics and ordering for a scientific domain object, so instances
    integrate naturally with sorting, comparisons, and set operations."""

    class GeneExpressionRecord:
        def __init__(self, gene_id: str, expression_level: float) -> None:
            self.gene_id = gene_id
            self.expression_level = expression_level

        def __repr__(self) -> str:
            return f"GeneExpressionRecord(gene_id={self.gene_id!r}, expression_level={self.expression_level})"

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, IndustryMagicMethods.GeneExpressionRecord):
                return NotImplemented
            return self.gene_id == other.gene_id and self.expression_level == other.expression_level

        def __lt__(self, other: "IndustryMagicMethods.GeneExpressionRecord") -> bool:
            if not isinstance(other, IndustryMagicMethods.GeneExpressionRecord):
                return NotImplemented
            return self.expression_level < other.expression_level

        def __hash__(self) -> int:
            return hash((self.gene_id, self.expression_level))

        def __add__(
            self, other: "IndustryMagicMethods.GeneExpressionRecord"
        ) -> "IndustryMagicMethods.GeneExpressionRecord":
            if self.gene_id != other.gene_id:
                raise ValueError("cannot combine records for different genes")
            return IndustryMagicMethods.GeneExpressionRecord(
                self.gene_id, self.expression_level + other.expression_level
            )

    @staticmethod
    def run() -> None:
        records = [
            IndustryMagicMethods.GeneExpressionRecord("BRCA1", 12.4),
            IndustryMagicMethods.GeneExpressionRecord("TP53", 8.1),
            IndustryMagicMethods.GeneExpressionRecord("EGFR", 15.7),
        ]
        print(sorted(records))
        print(max(records))

        replicate = IndustryMagicMethods.GeneExpressionRecord("BRCA1", 3.6)
        combined = records[0] + replicate
        print(combined)

        try:
            records[0] + records[1]
        except ValueError as exc:
            print(f"caught expected error: {exc}")

        print(records[0] in set(records))


if __name__ == "__main__":
    UniversityMagicMethods.run()
    InterviewMagicMethods.run()
    IndustryMagicMethods.run()
