"""Nested loops over hierarchical scientific data."""


class PlantSampleSummarizer:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def total_leaves(self) -> int:
        total = 0
        for s in self.samples:
            for leaf in s.get("leaves", []):
                total += leaf
        return total


class SequencePairScorer:
    def __init__(self, a: str, b: str) -> None:
        self.a = a
        self.b = b

    def matches(self) -> int:
        score = 0
        for x in self.a:
            for y in self.b:
                if x == y:
                    score += 1
        return score


class SampleTissueMatrix:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def measurement_matrix(self) -> list[list[int]]:
        result: list[list[int]] = []
        for s in self.samples:
            row: list[int] = []
            for m in s.get("measurements", []):
                row.append(m)
            result.append(row)
        return result


if __name__ == "__main__":
    print(PlantSampleSummarizer([
        {"id": "P1", "leaves": [3, 4]},
        {"id": "P2", "leaves": [5]},
    ]).total_leaves())

    print(SequencePairScorer("ATGC", "ACGT").matches())

    print(SampleTissueMatrix([
        {"id": "P1", "measurements": [10, 20]},
        {"id": "P2", "measurements": [15]},
    ]).measurement_matrix())
