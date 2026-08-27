"""Demonstrations of the built-in len() function using plant-science data."""


class UniversityLen:
    """Teach the fundamental behavior of len() on biological collections."""

    def __init__(self, plant_records: list[dict[str, str]]) -> None:
        self.plant_records = plant_records

    def count_samples(self) -> int:
        return len(self.plant_records)

    def sequence_length(self, dna_sequence: str) -> int:
        return len(dna_sequence)

    @staticmethod
    def run() -> None:
        data = [
            {"sample_id": "P001", "species": "Wheat"},
            {"sample_id": "P002", "species": "Rice"},
            {"sample_id": "P003", "species": "Maize"},
        ]
        dna_sequence = "ATCGGTA"

        processor = UniversityLen(data)
        print(f"Total plant samples: {processor.count_samples()}")
        print(f"DNA sequence length: {processor.sequence_length(dna_sequence)}")


class InterviewLen:
    """Solve a realistic problem: safely computing lengths across mixed records."""

    def __init__(self, observations: list[dict[str, object]]) -> None:
        self.observations = observations

    def safe_field_length(self, record: dict[str, object], field: str) -> int:
        """Return len(record[field]) or 0 if the field is missing/None."""
        value = record.get(field)
        if value is None:
            return 0
        try:
            return len(value)  # type: ignore[arg-type]
        except TypeError:
            return 0

    def total_measurement_count(self) -> int:
        """Sum the number of measurements recorded per observation."""
        return sum(self.safe_field_length(obs, "measurements") for obs in self.observations)

    @staticmethod
    def run() -> None:
        observations: list[dict[str, object]] = [
            {"sample_id": "S001", "measurements": [1.2, 1.5, 1.7]},
            {"sample_id": "S002", "measurements": []},
            {"sample_id": "S003", "measurements": None},
            {"sample_id": "S004"},
        ]

        analyzer = InterviewLen(observations)
        for obs in observations:
            length = analyzer.safe_field_length(obs, "measurements")
            print(f"{obs['sample_id']}: {length} measurement(s)")

        print(f"Total measurements across all samples: {analyzer.total_measurement_count()}")


class IndustryLen:
    """Report dataset and sample structure sizes for a scientific dataset."""

    def __init__(self, dataset: dict[str, list[dict[str, object]]]) -> None:
        self.dataset = dataset

    def dataset_summary(self) -> dict[str, int]:
        """Return the number of records per dataset table."""
        return {table: len(records) for table, records in self.dataset.items()}

    def empty_tables(self) -> list[str]:
        return [table for table, records in self.dataset.items() if len(records) == 0]

    @staticmethod
    def run() -> None:
        dataset: dict[str, list[dict[str, object]]] = {
            "plant_samples": [{"id": "P001"}, {"id": "P002"}],
            "gene_expression": [{"gene": "GENE1"}],
            "quality_control": [],
        }

        reporter = IndustryLen(dataset)
        summary = reporter.dataset_summary()
        for table, count in summary.items():
            print(f"Table '{table}' has {count} record(s)")

        print(f"Empty tables: {reporter.empty_tables()}")


if __name__ == "__main__":
    UniversityLen.run()
    InterviewLen.run()
    IndustryLen.run()
