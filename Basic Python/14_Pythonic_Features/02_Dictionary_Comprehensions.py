"""Dictionary comprehensions demonstrated through sample and gene metadata."""


class UniversityDictionaryComprehensions:
    """Teach the fundamental syntax of building dictionaries from iterables."""

    def __init__(self, sample_ids: list[str], measurements: list[float]) -> None:
        self.sample_ids = sample_ids
        self.measurements = measurements

    def build_sample_lookup(self) -> dict[str, float]:
        """Map each sample ID to its corresponding measurement."""
        return {
            sample_id: value
            for sample_id, value in zip(self.sample_ids, self.measurements)
        }

    @staticmethod
    def run() -> None:
        sample_ids = ["S001", "S002", "S003"]
        measurements = [7.2, 5.9, 8.4]

        processor = UniversityDictionaryComprehensions(sample_ids, measurements)
        lookup = processor.build_sample_lookup()

        print(f"Sample measurement lookup: {lookup}")


class InterviewDictionaryComprehensions:
    """Solve a practical gene-expression filtering and mapping problem."""

    def __init__(self, gene_expression: dict[str, float]) -> None:
        self.gene_expression = gene_expression

    def filter_significant_genes(self, min_expression: float) -> dict[str, float]:
        """Return genes whose expression meets a minimum threshold.

        Handles an empty input dictionary gracefully.
        """
        if not self.gene_expression:
            return {}

        return {
            gene: value
            for gene, value in self.gene_expression.items()
            if value >= min_expression
        }

    def invert_lookup(self) -> dict[float, str]:
        """Invert gene-to-value mapping, guarding against duplicate values."""
        seen_values: set[float] = set()
        inverted: dict[float, str] = {}

        for gene, value in self.gene_expression.items():
            if value not in seen_values:
                inverted[value] = gene
                seen_values.add(value)

        return inverted

    @staticmethod
    def run() -> None:
        expression_data = {"BRCA1": 3.4, "TP53": 5.1, "EGFR": 1.2, "MYC": 4.8}
        empty_data: dict[str, float] = {}

        case_one = InterviewDictionaryComprehensions(expression_data)
        case_two = InterviewDictionaryComprehensions(empty_data)

        print(f"Significant genes: {case_one.filter_significant_genes(3.0)}")
        print(f"Empty dataset result: {case_two.filter_significant_genes(3.0)}")
        print(f"Inverted lookup: {case_one.invert_lookup()}")


class IndustryDictionaryComprehensions:
    """Generate reusable biological metadata indexes from raw sample records."""

    def __init__(self, sample_records: list[dict[str, str | float]]) -> None:
        self.sample_records = sample_records

    def index_by_sample_id(self) -> dict[str, dict[str, str | float]]:
        """Build a lookup index keyed by sample ID for fast record access."""
        return {
            str(record["sample_id"]): record
            for record in self.sample_records
            if "sample_id" in record
        }

    def species_to_average_height(self) -> dict[str, float]:
        """Compute average plant height per species from sample records."""
        species_set = {str(record["species"]) for record in self.sample_records}

        return {
            species: round(
                sum(
                    float(record["height_cm"])
                    for record in self.sample_records
                    if record["species"] == species
                )
                / sum(1 for record in self.sample_records if record["species"] == species),
                2,
            )
            for species in species_set
        }

    @staticmethod
    def run() -> None:
        records: list[dict[str, str | float]] = [
            {"sample_id": "S001", "species": "Arabidopsis", "height_cm": 12.5},
            {"sample_id": "S002", "species": "Arabidopsis", "height_cm": 14.1},
            {"sample_id": "S003", "species": "Oryza sativa", "height_cm": 45.0},
        ]

        indexer = IndustryDictionaryComprehensions(records)
        sample_index = indexer.index_by_sample_id()
        avg_heights = indexer.species_to_average_height()

        print(f"Sample index keys: {list(sample_index.keys())}")
        print(f"Average height by species: {avg_heights}")


if __name__ == "__main__":
    UniversityDictionaryComprehensions.run()
    InterviewDictionaryComprehensions.run()
    IndustryDictionaryComprehensions.run()
