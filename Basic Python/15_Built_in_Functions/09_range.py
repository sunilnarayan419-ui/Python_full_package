"""Demonstrations of the built-in range() function using experimental sample data."""


class UniversityRange:
    """Teach the fundamental behavior of range() for iteration and numbering."""

    def __init__(self, sample_count: int) -> None:
        self.sample_count = sample_count

    def sample_indices(self) -> list[int]:
        """range() excludes the stop value: indices go from 0 to sample_count - 1."""
        return list(range(self.sample_count))

    @staticmethod
    def run() -> None:
        processor = UniversityRange(sample_count=5)
        print(f"Sample indices: {processor.sample_indices()}")


class InterviewRange:
    """Use range() with start/stop/step for controlled experimental indexing."""

    def __init__(self, first_sample_id: int, last_sample_id: int) -> None:
        self.first_sample_id = first_sample_id
        self.last_sample_id = last_sample_id

    def inclusive_sample_ids(self) -> list[int]:
        """Include the last sample id by adding 1 to the stop value."""
        return list(range(self.first_sample_id, self.last_sample_id + 1))

    def every_other_sample(self) -> list[int]:
        return list(range(self.first_sample_id, self.last_sample_id + 1, 2))

    @staticmethod
    def run() -> None:
        case_one = InterviewRange(first_sample_id=101, last_sample_id=105)
        case_two = InterviewRange(first_sample_id=10, last_sample_id=10)

        print(f"Inclusive sample IDs: {case_one.inclusive_sample_ids()}")
        print(f"Every other sample ID: {case_one.every_other_sample()}")
        print(f"Single-sample range: {case_two.inclusive_sample_ids()}")


class IndustryRange:
    """Batch and reverse-order processing logic for scientific sample pipelines."""

    def __init__(self, total_samples: int, batch_size: int) -> None:
        self.total_samples = total_samples
        self.batch_size = batch_size

    def batch_start_indices(self) -> list[int]:
        return list(range(0, self.total_samples, self.batch_size))

    def reverse_processing_order(self) -> list[int]:
        """Process the most recently added samples first."""
        return list(range(self.total_samples - 1, -1, -1))

    @staticmethod
    def run() -> None:
        processor = IndustryRange(total_samples=10, batch_size=3)
        print(f"Batch start indices: {processor.batch_start_indices()}")
        print(f"Reverse processing order: {processor.reverse_processing_order()}")


if __name__ == "__main__":
    UniversityRange.run()
    InterviewRange.run()
    IndustryRange.run()
