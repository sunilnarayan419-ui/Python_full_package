"""Generator functions: yield, lazy value production, and streaming records."""


class UniversityGeneratorFunctions:
    def __init__(self, plant_records: list[dict]) -> None:
        self.plant_records = plant_records

    def height_generator(self):
        """A simple generator function yielding heights one at a time."""
        for record in self.plant_records:
            yield record["height_cm"]

    @staticmethod
    def run() -> None:
        data = [
            {"sample_id": "P001", "species": "Wheat", "height_cm": 28.5},
            {"sample_id": "P002", "species": "Rice", "height_cm": 31.2},
            {"sample_id": "P003", "species": "Barley", "height_cm": 24.0},
        ]

        demo = UniversityGeneratorFunctions(data)
        gen = demo.height_generator()
        print(f"Generator object type: {type(gen).__name__}")
        print("Pulling heights lazily:")
        for height in gen:
            print(f"  height_cm={height}")


class InterviewGeneratorFunctions:
    def __init__(self, records: list[dict]) -> None:
        self.records = records

    def valid_measurement_generator(self, key: str):
        """Yields only valid numeric measurements, skipping bad entries defensively."""
        for record in self.records:
            value = record.get(key)
            if isinstance(value, (int, float)) and value >= 0:
                yield value

    @staticmethod
    def run() -> None:
        empty_case: list[dict] = []
        processor = InterviewGeneratorFunctions(empty_case)
        result_empty = list(processor.valid_measurement_generator("height_cm"))
        print(f"Empty input -> collected values: {result_empty}")

        messy_case = [
            {"height_cm": 28.5},
            {"height_cm": "not_a_number"},
            {"height_cm": -5.0},
            {"height_cm": 31.2},
            {},
        ]
        processor = InterviewGeneratorFunctions(messy_case)
        result_messy = list(processor.valid_measurement_generator("height_cm"))
        print(f"Messy input -> collected valid values: {result_messy}")


class IndustryGeneratorFunctions:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def stream_records(self, min_height: float = 0.0):
        """Lazily streams records meeting a minimum height threshold.

        Memory-efficient: does not build an intermediate filtered list.
        """
        for record in self.data:
            height = record.get("height_cm", 0.0)
            if height >= min_height:
                yield record

    def process(self, min_height: float = 25.0) -> dict[str, object]:
        streamed = list(self.stream_records(min_height))
        return {
            "total_samples": len(self.data),
            "passing_threshold": len(streamed),
            "min_height": min_height,
            "records": streamed,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"id": "P001", "height_cm": 28.5},
            {"id": "P002", "height_cm": 19.0},
            {"id": "P003", "height_cm": 31.2},
            {"id": "P004", "height_cm": 22.4},
        ]

        processor = IndustryGeneratorFunctions(sample_data)
        report = processor.process(min_height=25.0)
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityGeneratorFunctions.run()
    InterviewGeneratorFunctions.run()
    IndustryGeneratorFunctions.run()
