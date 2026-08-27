"""Demonstrations of the built-in sorted() function using plant/experiment data."""


class UniversitySorted:
    """Teach the fundamental behavior of sorted() on numeric biological data."""

    def __init__(self, plant_heights: list[float]) -> None:
        self.plant_heights = plant_heights

    def ascending_heights(self) -> list[float]:
        return sorted(self.plant_heights)

    def descending_heights(self) -> list[float]:
        return sorted(self.plant_heights, reverse=True)

    @staticmethod
    def run() -> None:
        plant_heights = [55.2, 61.8, 49.3, 72.1, 66.4]

        processor = UniversitySorted(plant_heights)
        print(f"Ascending heights: {processor.ascending_heights()}")
        print(f"Descending heights: {processor.descending_heights()}")


class InterviewSorted:
    """Sort structured biological records using key= for realistic problems."""

    def __init__(self, gene_records: list[dict[str, object]]) -> None:
        self.gene_records = gene_records

    def sorted_by_expression(self, reverse: bool = False) -> list[dict[str, object]]:
        return sorted(
            self.gene_records,
            key=lambda record: record["expression_level"],
            reverse=reverse,
        )

    @staticmethod
    def run() -> None:
        case_one: list[dict[str, object]] = [
            {"gene": "GENE1", "expression_level": 4.2},
            {"gene": "GENE2", "expression_level": 9.1},
            {"gene": "GENE3", "expression_level": 1.3},
        ]
        case_two: list[dict[str, object]] = []

        analyzer_one = InterviewSorted(case_one)
        analyzer_two = InterviewSorted(case_two)

        ranked = analyzer_one.sorted_by_expression(reverse=True)
        print(f"Genes ranked by expression (high to low): {[g['gene'] for g in ranked]}")
        print(f"Sorted result (empty dataset): {analyzer_two.sorted_by_expression()}")

        # sorted() returns a new list; the original list is left untouched.
        original_ids = [g["gene"] for g in case_one]
        print(f"Original order preserved: {original_ids}")


class IndustrySorted:
    """Rank experimental datasets by quality score for reporting workflows."""

    def __init__(self, samples: list[dict[str, object]]) -> None:
        self.samples = samples

    def ranked_samples(self, metric: str, reverse: bool = True) -> list[dict[str, object]]:
        """Return samples sorted by metric, using a stable sort for tie order."""
        return sorted(self.samples, key=lambda sample: sample[metric], reverse=reverse)

    @staticmethod
    def run() -> None:
        samples: list[dict[str, object]] = [
            {"sample_id": "S001", "quality_score": 0.87},
            {"sample_id": "S002", "quality_score": 0.94},
            {"sample_id": "S003", "quality_score": 0.94},
            {"sample_id": "S004", "quality_score": 0.62},
        ]

        reporter = IndustrySorted(samples)
        ranked = reporter.ranked_samples("quality_score")
        print("Sample ranking by quality score:")
        for rank, sample in enumerate(ranked, start=1):
            print(f"  {rank}. {sample['sample_id']} ({sample['quality_score']})")


if __name__ == "__main__":
    UniversitySorted.run()
    InterviewSorted.run()
    IndustrySorted.run()
