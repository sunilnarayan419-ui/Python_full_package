"""filter(): selecting biological samples and measurements based on conditions."""


class UniversityFilter:
    def __init__(self, plant_heights_cm: list[float]) -> None:
        self.plant_heights_cm = plant_heights_cm

    def tall_plants(self, threshold: float) -> list[float]:
        return list(filter(lambda height: height >= threshold, self.plant_heights_cm))

    @staticmethod
    def run() -> None:
        heights_cm = [18.2, 25.5, 31.2, 42.8, 12.0]

        processor = UniversityFilter(heights_cm)
        tall = processor.tall_plants(25.0)

        print(f"All heights: {heights_cm}")
        print(f"Heights >= 25cm: {tall}")


class InterviewFilter:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def healthy_samples(self) -> list[dict]:
        return list(
            filter(
                lambda sample: isinstance(sample.get("health_score"), (int, float))
                and sample.get("health_score", 0) >= 0.7,
                self.samples,
            )
        )

    @staticmethod
    def run() -> None:
        samples = [
            {"id": "P001", "health_score": 0.91},
            {"id": "P002", "health_score": 0.52},
            {"id": "P003", "health_score": 0.84},
            {"id": "P004", "health_score": None},
            {"id": "P005"},
        ]

        processor = InterviewFilter(samples)
        print(f"Healthy samples: {processor.healthy_samples()}")

        empty_processor = InterviewFilter([])
        print(f"Empty dataset: {empty_processor.healthy_samples()}")


class IndustryFilter:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def filter_by_expression_threshold(self, min_level: float) -> list[dict]:
        """Reusable predicate-based filtering step for a QC pipeline."""

        def passes_threshold(record: dict) -> bool:
            level = record.get("expression_level")
            return isinstance(level, (int, float)) and level >= min_level

        return list(filter(passes_threshold, self.data))

    def process(self, min_level: float = 5.0) -> dict[str, object]:
        passing = self.filter_by_expression_threshold(min_level)
        return {
            "total_samples": len(self.data),
            "passing_samples": len(passing),
            "min_level": min_level,
            "records": passing,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"gene": "wus1", "expression_level": 4.2},
            {"gene": "zmm4", "expression_level": 6.1},
            {"gene": "sb_drought1", "expression_level": 8.9},
            {"gene": "cry1ab", "expression_level": 2.5},
        ]

        processor = IndustryFilter(sample_data)
        report = processor.process(min_level=5.0)
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityFilter.run()
    InterviewFilter.run()
    IndustryFilter.run()
