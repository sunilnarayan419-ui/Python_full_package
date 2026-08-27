"""any(): checking whether at least one biological condition holds true."""


class UniversityAny:
    def __init__(self, mutation_flags: list[bool]) -> None:
        self.mutation_flags = mutation_flags

    def has_any_mutation(self) -> bool:
        return any(self.mutation_flags)

    @staticmethod
    def run() -> None:
        flags = [False, False, True, False]

        processor = UniversityAny(flags)
        result = processor.has_any_mutation()

        print(f"Mutation flags: {flags}")
        print(f"Any mutation detected: {result}")


class InterviewAny:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def any_abnormal_reading(self, threshold: float) -> bool:
        """Uses a generator expression with any() for short-circuit evaluation."""
        return any(
            isinstance(sample.get("height_cm"), (int, float))
            and sample["height_cm"] > threshold
            for sample in self.samples
        )

    @staticmethod
    def run() -> None:
        empty_samples: list[dict] = []
        processor = InterviewAny(empty_samples)
        print(f"Empty samples -> any abnormal: {processor.any_abnormal_reading(50.0)}")

        normal_samples = [
            {"id": "P001", "height_cm": 28.5},
            {"id": "P002", "height_cm": 31.2},
            {"id": "P003"},
        ]
        processor = InterviewAny(normal_samples)
        print(f"Normal samples -> any abnormal (>50cm): {processor.any_abnormal_reading(50.0)}")

        abnormal_samples = [
            {"id": "P004", "height_cm": 28.5},
            {"id": "P005", "height_cm": 62.0},
        ]
        processor = InterviewAny(abnormal_samples)
        print(
            f"Abnormal samples -> any abnormal (>50cm): "
            f"{processor.any_abnormal_reading(50.0)}"
        )


class IndustryAny:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def has_quality_control_failure(self, min_health_score: float) -> bool:
        """Efficient QC gate: short-circuits on the first failing sample."""
        return any(
            record.get("health_score", 1.0) < min_health_score for record in self.data
        )

    def process(self, min_health_score: float = 0.6) -> dict[str, object]:
        failed = self.has_quality_control_failure(min_health_score)
        return {
            "total_samples": len(self.data),
            "min_health_score": min_health_score,
            "has_qc_failure": failed,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"sample_id": "S001", "health_score": 0.91},
            {"sample_id": "S002", "health_score": 0.72},
            {"sample_id": "S003", "health_score": 0.55},
        ]

        processor = IndustryAny(sample_data)
        report = processor.process(min_health_score=0.6)
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityAny.run()
    InterviewAny.run()
    IndustryAny.run()
