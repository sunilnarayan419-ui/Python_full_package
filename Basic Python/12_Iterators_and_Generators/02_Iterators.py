"""Iterators: iter(), next(), iterator state, StopIteration, and custom iterators."""


class UniversityIterators:
    def __init__(self, plant_records: list[dict]) -> None:
        self.plant_records = plant_records

    def manual_next_demo(self) -> list[str]:
        """Shows iter() and next() being used step by step."""
        iterator = iter(self.plant_records)
        results = []
        for _ in range(len(self.plant_records)):
            record = next(iterator)
            results.append(record["sample_id"])
        return results

    def exhaust_and_catch_stop_iteration(self) -> str:
        iterator = iter(self.plant_records)
        try:
            while True:
                next(iterator)
        except StopIteration:
            return "Iterator exhausted: StopIteration raised as expected."

    @staticmethod
    def run() -> None:
        data = [
            {"sample_id": "P001", "species": "Wheat", "height_cm": 28.5},
            {"sample_id": "P002", "species": "Rice", "height_cm": 31.2},
        ]

        demo = UniversityIterators(data)
        print(f"Sample IDs via manual next(): {demo.manual_next_demo()}")
        print(demo.exhaust_and_catch_stop_iteration())


class GeneReadIterator:
    """A custom iterator over a fixed sequence of DNA reads."""

    def __init__(self, reads: list[str]) -> None:
        self._reads = reads
        self._index = 0

    def __iter__(self) -> "GeneReadIterator":
        return self

    def __next__(self) -> str:
        if self._index >= len(self._reads):
            raise StopIteration
        read = self._reads[self._index]
        self._index += 1
        return read


class InterviewIterators:
    def __init__(self, reads: list[str]) -> None:
        self.reads = reads

    def safe_first_n(self, n: int) -> list[str]:
        """Pulls up to n items from an iterator without crashing on short input."""
        if n < 0:
            raise ValueError("n must be non-negative")
        iterator = iter(self.reads)
        results: list[str] = []
        for _ in range(n):
            try:
                results.append(next(iterator))
            except StopIteration:
                break
        return results

    def custom_iterator_walkthrough(self) -> list[str]:
        gene_iterator = GeneReadIterator(self.reads)
        collected = []
        for read in gene_iterator:
            collected.append(read.upper())
        return collected

    @staticmethod
    def run() -> None:
        empty_reads: list[str] = []
        processor = InterviewIterators(empty_reads)
        print(f"Empty reads, request 3 -> {processor.safe_first_n(3)}")

        short_reads = ["atcg", "ggcc", "ttaa"]
        processor = InterviewIterators(short_reads)
        print(f"3 reads, request 5 -> {processor.safe_first_n(5)}")
        print(f"Custom iterator uppercase reads: {processor.custom_iterator_walkthrough()}")

        try:
            processor.safe_first_n(-1)
        except ValueError as error:
            print(f"Handled invalid n: {error}")


class SampleBatchIterator:
    """Custom iterator yielding fixed-size batches of sample records."""

    def __init__(self, records: list[dict], batch_size: int) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        self._records = records
        self._batch_size = batch_size
        self._index = 0

    def __iter__(self) -> "SampleBatchIterator":
        return self

    def __next__(self) -> list[dict]:
        if self._index >= len(self._records):
            raise StopIteration
        batch = self._records[self._index : self._index + self._batch_size]
        self._index += self._batch_size
        return batch


class IndustryIterators:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def process(self, batch_size: int = 2) -> dict[str, object]:
        batcher = SampleBatchIterator(self.data, batch_size)
        batches = list(batcher)
        return {
            "total_samples": len(self.data),
            "batch_size": batch_size,
            "batch_count": len(batches),
            "batches": batches,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"sample_id": "P001", "height_cm": 28.5},
            {"sample_id": "P002", "height_cm": 31.2},
            {"sample_id": "P003", "height_cm": 26.9},
            {"sample_id": "P004", "height_cm": 33.4},
            {"sample_id": "P005", "height_cm": 29.7},
        ]

        processor = IndustryIterators(sample_data)
        report = processor.process(batch_size=2)
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityIterators.run()
    InterviewIterators.run()
    IndustryIterators.run()
