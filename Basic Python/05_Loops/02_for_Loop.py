"""for loop iterating over scientific records."""


class PlantSampleIterator:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def total_height(self) -> float:
        total = 0.0
        for s in self.samples:
            total += s["height_cm"]
        return total


class NucleotideCounter:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence.upper()

    def count_each(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for base in self.sequence:
            counts[base] = counts.get(base, 0) + 1
        return counts


class ExpressionRecordProcessor:
    def __init__(self, records: list[dict]) -> None:
        self.records = records

    def summarize(self) -> dict[str, float]:
        total = 0.0
        count = 0
        for r in self.records:
            total += r["value"]
            count += 1
        mean = total / count if count else 0.0
        return {"mean": mean, "n": float(count)}


if __name__ == "__main__":
    print(PlantSampleIterator([
        {"id": "P1", "height_cm": 20.0},
        {"id": "P2", "height_cm": 30.0},
    ]).total_height())

    print(NucleotideCounter("ATGCAT").count_each())

    print(ExpressionRecordProcessor([
        {"gene": "A", "value": 1.5},
        {"gene": "B", "value": 2.5},
    ]).summarize())
