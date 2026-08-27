"""enumerate(): indexing while iterating over biological data, without manual counters."""


class UniversityEnumerate:
    def __init__(self, plant_names: list[str]) -> None:
        self.plant_names = plant_names

    def numbered_plants(self) -> list[str]:
        return [f"{index}: {name}" for index, name in enumerate(self.plant_names)]

    @staticmethod
    def run() -> None:
        plant_names = ["Wheat", "Rice", "Barley"]

        processor = UniversityEnumerate(plant_names)
        numbered = processor.numbered_plants()

        print(f"Plant names: {plant_names}")
        print("Numbered (0-indexed):")
        for line in numbered:
            print(f"  {line}")


class InterviewEnumerate:
    def __init__(self, observations: list[str]) -> None:
        self.observations = observations

    def sample_labels(self, start: int = 1) -> list[str]:
        """Generates human-friendly sample labels starting from a given number."""
        if not self.observations:
            return []
        return [
            f"Sample-{index:03d}: {observation}"
            for index, observation in enumerate(self.observations, start=start)
        ]

    @staticmethod
    def run() -> None:
        empty_observations: list[str] = []
        processor = InterviewEnumerate(empty_observations)
        print(f"Empty observations -> labels: {processor.sample_labels()}")

        observations = ["wilting", "healthy", "chlorosis"]
        processor = InterviewEnumerate(observations)
        print(f"Default start=1 labels: {processor.sample_labels()}")
        print(f"Custom start=101 labels: {processor.sample_labels(start=101)}")


class IndustryEnumerate:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def build_indexed_report(self, start: int = 1) -> list[dict]:
        """Attaches a stable, human-readable report index to each record."""
        report = []
        for position, record in enumerate(self.data, start=start):
            report.append(
                {
                    "report_index": position,
                    "sample_id": record.get("sample_id", "UNKNOWN"),
                    "height_cm": record.get("height_cm"),
                }
            )
        return report

    def process(self) -> dict[str, object]:
        report = self.build_indexed_report()
        return {
            "total_samples": len(self.data),
            "report": report,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"sample_id": "P001", "height_cm": 28.5},
            {"sample_id": "P002", "height_cm": 31.2},
            {"sample_id": "P003", "height_cm": 24.0},
        ]

        processor = IndustryEnumerate(sample_data)
        report = processor.process()
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityEnumerate.run()
    InterviewEnumerate.run()
    IndustryEnumerate.run()
