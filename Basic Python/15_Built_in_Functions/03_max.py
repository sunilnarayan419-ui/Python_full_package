"""Demonstrations of the built-in max() function using plant/gene expression data."""


class UniversityMax:
    """Teach the fundamental behavior of max() on numeric biological data."""

    def __init__(self, plant_heights: list[float]) -> None:
        self.plant_heights = plant_heights

    def tallest_plant_height(self) -> float:
        return max(self.plant_heights)

    @staticmethod
    def run() -> None:
        plant_heights = [55.2, 61.8, 49.3, 72.1, 66.4]

        processor = UniversityMax(plant_heights)
        print(f"Tallest plant height: {processor.tallest_plant_height()} cm")


class InterviewMax:
    """Find maximum biological measurements safely, using key= for records."""

    def __init__(self, gene_records: list[dict[str, object]]) -> None:
        self.gene_records = gene_records

    def highest_expression_gene(self) -> dict[str, object] | None:
        """Return the record with the highest expression value, or None if empty."""
        if not self.gene_records:
            return None
        return max(self.gene_records, key=lambda record: record["expression_level"])

    @staticmethod
    def run() -> None:
        case_one: list[dict[str, object]] = [
            {"gene": "GENE1", "expression_level": 4.2},
            {"gene": "GENE2", "expression_level": 9.1},
            {"gene": "GENE3", "expression_level": 6.7},
        ]
        case_two: list[dict[str, object]] = []

        analyzer_one = InterviewMax(case_one)
        analyzer_two = InterviewMax(case_two)

        top_gene = analyzer_one.highest_expression_gene()
        print(f"Highest expressing gene: {top_gene['gene'] if top_gene else None}")

        top_gene_empty = analyzer_two.highest_expression_gene()
        print(f"Highest expressing gene (empty dataset): {top_gene_empty}")


class IndustryMax:
    """Identify the highest-performing sample within a scientific dataset."""

    def __init__(self, samples: list[dict[str, object]]) -> None:
        self.samples = samples

    def best_performing_sample(self, metric: str) -> dict[str, object] | None:
        """Return the sample with the highest value for the given metric."""
        candidates = [sample for sample in self.samples if metric in sample]
        if not candidates:
            return None
        return max(candidates, key=lambda sample: sample[metric])

    @staticmethod
    def run() -> None:
        samples: list[dict[str, object]] = [
            {"sample_id": "S001", "concentration": 3.4, "purity": 0.91},
            {"sample_id": "S002", "concentration": 5.9, "purity": 0.87},
            {"sample_id": "S003", "concentration": 4.1},
        ]

        reporter = IndustryMax(samples)
        best_concentration = reporter.best_performing_sample("concentration")
        best_purity = reporter.best_performing_sample("purity")

        print(f"Highest concentration sample: {best_concentration['sample_id']}")
        print(f"Highest purity sample: {best_purity['sample_id']}")


if __name__ == "__main__":
    UniversityMax.run()
    InterviewMax.run()
    IndustryMax.run()
