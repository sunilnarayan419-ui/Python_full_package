"""Demonstrations of the built-in min() function using plant/expression data."""


class UniversityMin:
    """Teach the fundamental behavior of min() on numeric biological data."""

    def __init__(self, plant_heights: list[float]) -> None:
        self.plant_heights = plant_heights

    def shortest_plant_height(self) -> float:
        return min(self.plant_heights)

    @staticmethod
    def run() -> None:
        plant_heights = [55.2, 61.8, 49.3, 72.1, 66.4]

        processor = UniversityMin(plant_heights)
        print(f"Shortest plant height: {processor.shortest_plant_height()} cm")


class InterviewMin:
    """Find minimum biological measurements safely, using key= for dictionaries."""

    def __init__(self, gene_records: list[dict[str, object]]) -> None:
        self.gene_records = gene_records

    def lowest_expression_gene(self) -> dict[str, object] | None:
        """Return the record with the lowest expression value, or None if empty."""
        if not self.gene_records:
            return None
        return min(self.gene_records, key=lambda record: record["expression_level"])

    @staticmethod
    def run() -> None:
        case_one: list[dict[str, object]] = [
            {"gene": "GENE1", "expression_level": 4.2},
            {"gene": "GENE2", "expression_level": 9.1},
            {"gene": "GENE3", "expression_level": 1.3},
        ]
        case_two: list[dict[str, object]] = []

        analyzer_one = InterviewMin(case_one)
        analyzer_two = InterviewMin(case_two)

        low_gene = analyzer_one.lowest_expression_gene()
        print(f"Lowest expressing gene: {low_gene['gene'] if low_gene else None}")

        low_gene_empty = analyzer_two.lowest_expression_gene()
        print(f"Lowest expressing gene (empty dataset): {low_gene_empty}")


class IndustryMin:
    """Identify the lowest-value/lowest-risk sample within a scientific dataset."""

    def __init__(self, samples: list[dict[str, object]]) -> None:
        self.samples = samples

    def lowest_risk_sample(self, metric: str) -> dict[str, object] | None:
        """Return the sample with the lowest value for the given risk metric."""
        candidates = [sample for sample in self.samples if metric in sample]
        if not candidates:
            return None
        return min(candidates, key=lambda sample: sample[metric])

    @staticmethod
    def run() -> None:
        samples: list[dict[str, object]] = [
            {"sample_id": "S001", "contamination_risk": 0.12, "cost": 45.0},
            {"sample_id": "S002", "contamination_risk": 0.03, "cost": 60.0},
            {"sample_id": "S003", "contamination_risk": 0.20},
        ]

        reporter = IndustryMin(samples)
        lowest_risk = reporter.lowest_risk_sample("contamination_risk")
        lowest_cost = reporter.lowest_risk_sample("cost")

        print(f"Lowest contamination risk sample: {lowest_risk['sample_id']}")
        print(f"Lowest cost sample: {lowest_cost['sample_id']}")


if __name__ == "__main__":
    UniversityMin.run()
    InterviewMin.run()
    IndustryMin.run()
