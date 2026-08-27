"""key= parameter: custom sorting criteria via lambda and named key functions."""


class UniversityKeyFunction:
    def __init__(self, plant_records: list[dict]) -> None:
        self.plant_records = plant_records

    def sort_by_height_lambda(self) -> list[dict]:
        return sorted(self.plant_records, key=lambda record: record["height_cm"])

    @staticmethod
    def run() -> None:
        data = [
            {"sample_id": "P001", "height_cm": 31.2},
            {"sample_id": "P002", "height_cm": 18.0},
            {"sample_id": "P003", "height_cm": 42.8},
        ]

        processor = UniversityKeyFunction(data)
        result = processor.sort_by_height_lambda()

        print(f"Original order: {[r['sample_id'] for r in data]}")
        print(f"Sorted by height_cm (key=lambda): {[r['sample_id'] for r in result]}")


def _phenotype_score_key(record: dict) -> float:
    """Named key function: extracts phenotype score, defaulting missing to 0.0."""
    return record.get("phenotype_score", 0.0)


class InterviewKeyFunction:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def rank_with_named_function(self) -> list[dict]:
        return sorted(self.samples, key=_phenotype_score_key, reverse=True)

    def rank_with_lambda_and_tiebreak(self) -> list[dict]:
        """Ranks by expression level, using sample_id as a tiebreaker."""
        return sorted(
            self.samples,
            key=lambda sample: (
                -sample.get("expression_level", 0.0),
                sample.get("sample_id", ""),
            ),
        )

    @staticmethod
    def run() -> None:
        empty_samples: list[dict] = []
        processor = InterviewKeyFunction(empty_samples)
        print(f"Empty samples -> ranked: {processor.rank_with_named_function()}")

        samples = [
            {"sample_id": "S002", "phenotype_score": 7.5, "expression_level": 12.0},
            {"sample_id": "S001", "phenotype_score": 9.1, "expression_level": 12.0},
            {"sample_id": "S003", "phenotype_score": 4.2, "expression_level": 8.5},
        ]
        processor = InterviewKeyFunction(samples)
        ranked = processor.rank_with_named_function()
        print(f"Ranked by phenotype_score (named key fn): {[s['sample_id'] for s in ranked]}")

        tie_broken = processor.rank_with_lambda_and_tiebreak()
        print(f"Ranked by expression_level with sample_id tiebreak: {[s['sample_id'] for s in tie_broken]}")


class IndustryKeyFunction:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def _quality_key(self, record: dict) -> tuple[float, float]:
        """Domain-specific composite ranking: quality score, then concentration."""
        quality = record.get("quality_score", 0.0)
        concentration = record.get("concentration_ng_per_ul", 0.0)
        return (-quality, -concentration)

    def rank_by_quality(self) -> list[dict]:
        return sorted(self.data, key=self._quality_key)

    def process(self) -> dict[str, object]:
        ranked = self.rank_by_quality()
        return {
            "total_samples": len(self.data),
            "ranked_samples": ranked,
            "best_sample_id": ranked[0]["sample_id"] if ranked else None,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"sample_id": "S001", "quality_score": 0.88, "concentration_ng_per_ul": 45.2},
            {"sample_id": "S002", "quality_score": 0.95, "concentration_ng_per_ul": 30.1},
            {"sample_id": "S003", "quality_score": 0.95, "concentration_ng_per_ul": 52.0},
        ]

        processor = IndustryKeyFunction(sample_data)
        report = processor.process()
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityKeyFunction.run()
    InterviewKeyFunction.run()
    IndustryKeyFunction.run()
