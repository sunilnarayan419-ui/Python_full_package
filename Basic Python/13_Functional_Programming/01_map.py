"""map(): applying transformations to biological measurement collections."""


class UniversityMap:
    def __init__(self, plant_heights_cm: list[float]) -> None:
        self.plant_heights_cm = plant_heights_cm

    def convert_to_meters(self) -> list[float]:
        return list(map(lambda height: height / 100, self.plant_heights_cm))

    @staticmethod
    def run() -> None:
        heights_cm = [25.5, 31.2, 42.8, 19.0]

        processor = UniversityMap(heights_cm)
        heights_m = processor.convert_to_meters()

        print(f"Plant heights in cm: {heights_cm}")
        print(f"Plant heights in meters: {heights_m}")


class InterviewMap:
    def __init__(self, expression_records: list[dict]) -> None:
        self.expression_records = expression_records

    def normalize_expression(self, baseline: float) -> list[float]:
        """Maps raw expression values to fold-change vs a baseline.

        Skips records with missing or non-numeric expression values.
        """
        if baseline == 0:
            raise ValueError("baseline must be non-zero")

        def safe_fold_change(record: dict) -> float | None:
            value = record.get("expression_level")
            if not isinstance(value, (int, float)):
                return None
            return value / baseline

        mapped = map(safe_fold_change, self.expression_records)
        return [value for value in mapped if value is not None]

    @staticmethod
    def run() -> None:
        empty_case: list[dict] = []
        processor = InterviewMap(empty_case)
        print(f"Empty records -> fold changes: {processor.normalize_expression(2.0)}")

        mixed_case = [
            {"gene": "wus1", "expression_level": 4.0},
            {"gene": "zmm4", "expression_level": "unreadable"},
            {"gene": "sb_drought1", "expression_level": 6.0},
        ]
        processor = InterviewMap(mixed_case)
        print(f"Mixed records -> fold changes: {processor.normalize_expression(2.0)}")


class IndustryMap:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def transform_concentrations(self, unit_factor: float = 1000.0) -> list[dict]:
        """Reusable pipeline step: converts concentration units across all samples."""

        def convert(record: dict) -> dict:
            return {
                "sample_id": record["sample_id"],
                "concentration_ng_per_ul": record["concentration_ug_per_ml"] * unit_factor,
            }

        return list(map(convert, self.data))

    def process(self) -> dict[str, object]:
        transformed = self.transform_concentrations()
        return {
            "total_samples": len(self.data),
            "transformed_records": transformed,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"sample_id": "S001", "concentration_ug_per_ml": 0.85},
            {"sample_id": "S002", "concentration_ug_per_ml": 1.20},
            {"sample_id": "S003", "concentration_ug_per_ml": 0.63},
        ]

        processor = IndustryMap(sample_data)
        report = processor.process()
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityMap.run()
    InterviewMap.run()
    IndustryMap.run()
