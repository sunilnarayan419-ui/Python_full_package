"""yield: pausing/resuming function execution and generator state."""


class UniversityYield:
    def __init__(self, plant_records: list[dict]) -> None:
        self.plant_records = plant_records

    def paused_reader(self):
        """Demonstrates that yield pauses execution and resumes on next()."""
        for record in self.plant_records:
            print(f"  [about to yield] {record['sample_id']}")
            yield record["sample_id"]
            print(f"  [resumed after] {record['sample_id']}")

    @staticmethod
    def run() -> None:
        data = [
            {"sample_id": "P001", "species": "Wheat"},
            {"sample_id": "P002", "species": "Rice"},
        ]

        demo = UniversityYield(data)
        gen = demo.paused_reader()

        print("Calling next() once, manually:")
        first_id = next(gen)
        print(f"Received: {first_id}")

        print("Calling next() again to resume:")
        second_id = next(gen)
        print(f"Received: {second_id}")


class InterviewYield:
    def __init__(self, readings: list[float]) -> None:
        self.readings = readings

    def running_average_generator(self):
        """A stateful generator: yields a running average after each new reading.

        Demonstrates that local state (total, count) persists across yields.
        """
        total = 0.0
        count = 0
        for reading in self.readings:
            if not isinstance(reading, (int, float)):
                continue
            total += reading
            count += 1
            yield total / count

    @staticmethod
    def run() -> None:
        empty_readings: list[float] = []
        processor = InterviewYield(empty_readings)
        result_empty = list(processor.running_average_generator())
        print(f"Empty readings -> running averages: {result_empty}")

        mixed_readings = [10.0, "bad", 20.0, 30.0]
        processor = InterviewYield(mixed_readings)
        result_mixed = list(processor.running_average_generator())
        print(f"Mixed readings -> running averages: {result_mixed}")


class IndustryYield:
    def __init__(self, sequencing_data: list[str]) -> None:
        self.data = sequencing_data

    def chunked_sequence_yielder(self, chunk_size: int):
        """Yields fixed-size chunks of a DNA sequence, one at a time.

        Memory-efficient: never holds all chunks in memory simultaneously
        for a single sequence.
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        for sequence in self.data:
            for start in range(0, len(sequence), chunk_size):
                yield sequence[start : start + chunk_size]

    def process(self, chunk_size: int = 4) -> dict[str, object]:
        chunks = list(self.chunked_sequence_yielder(chunk_size))
        return {
            "total_sequences": len(self.data),
            "chunk_size": chunk_size,
            "total_chunks": len(chunks),
            "chunks": chunks,
        }

    @staticmethod
    def run() -> None:
        sequencing_data = ["ATCGGGTA", "TTAACCGGTT"]

        processor = IndustryYield(sequencing_data)
        report = processor.process(chunk_size=4)
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityYield.run()
    InterviewYield.run()
    IndustryYield.run()
