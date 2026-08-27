"""all(): checking whether every biological condition holds true across a dataset."""


class UniversityAll:
    def __init__(self, germination_flags: list[bool]) -> None:
        self.germination_flags = germination_flags

    def all_seeds_germinated(self) -> bool:
        return all(self.germination_flags)

    @staticmethod
    def run() -> None:
        flags = [True, True, True, False]

        processor = UniversityAll(flags)
        result = processor.all_seeds_germinated()

        print(f"Germination flags: {flags}")
        print(f"All seeds germinated: {result}")


class InterviewAll:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def all_meet_quality_threshold(self, threshold: float) -> bool:
        """Uses a generator expression with all(); demonstrates all([]) == True."""
        return all(
            isinstance(sample.get("health_score"), (int, float))
            and sample["health_score"] >= threshold
            for sample in self.samples
        )

    @staticmethod
    def run() -> None:
        empty_samples: list[dict] = []
        processor = InterviewAll(empty_samples)
        print(
            f"Empty samples -> all meet threshold (vacuously True): "
            f"{processor.all_meet_quality_threshold(0.7)}"
        )

        passing_samples = [
            {"id": "P001", "health_score": 0.91},
            {"id": "P002", "health_score": 0.84},
        ]
        processor = InterviewAll(passing_samples)
        print(f"Passing samples -> all meet threshold: {processor.all_meet_quality_threshold(0.7)}")

        mixed_samples = [
            {"id": "P003", "health_score": 0.91},
            {"id": "P004", "health_score": 0.52},
            {"id": "P005"},
        ]
        processor = InterviewAll(mixed_samples)
        print(f"Mixed samples -> all meet threshold: {processor.all_meet_quality_threshold(0.7)}")


class IndustryAll:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def dataset_passes_validation(self, required_fields: tuple[str, ...]) -> bool:
        """Validates that every record contains all required fields, non-null."""
        return all(
            all(record.get(field) is not None for field in required_fields)
            for record in self.data
        )

    def process(self, required_fields: tuple[str, ...] = ("sample_id", "gene", "expression_level")) -> dict[str, object]:
        is_valid = self.dataset_passes_validation(required_fields)
        return {
            "total_samples": len(self.data),
            "required_fields": list(required_fields),
            "dataset_valid": is_valid,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"sample_id": "RNA001", "gene": "GA20ox", "expression_level": 12.4},
            {"sample_id": "RNA002", "gene": "WUS1", "expression_level": 8.7},
            {"sample_id": "RNA003", "gene": "CRY1AB", "expression_level": 18.2},
        ]

        processor = IndustryAll(sample_data)
        report = processor.process()
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityAll.run()
    InterviewAll.run()
    IndustryAll.run()
