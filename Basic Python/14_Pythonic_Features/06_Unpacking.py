"""Unpacking demonstrated through biological records and metadata merging."""


class UniversityUnpacking:
    """Teach the fundamental syntax of tuple and list unpacking."""

    def __init__(self, record: tuple[str, str, float]) -> None:
        self.record = record

    def describe_record(self) -> str:
        """Unpack a sample record into its component fields."""
        sample_id, species, height_cm = self.record
        return f"{sample_id} is a {species} measuring {height_cm}cm"

    @staticmethod
    def run() -> None:
        record = ("S001", "Arabidopsis", 12.5)

        processor = UniversityUnpacking(record)
        print(processor.describe_record())

        first, *remaining = [1, 2, 3, 4, 5]
        print(f"First: {first}, Remaining: {remaining}")


class InterviewUnpacking:
    """Solve a practical structured-data unpacking problem with edge cases."""

    def __init__(self, records: list[tuple[str, ...]]) -> None:
        self.records = records

    def separate_ids_and_values(self) -> tuple[list[str], list[tuple[float, ...]]]:
        """Split sample IDs from their trailing numeric measurements.

        Handles records of varying length using starred unpacking, and
        skips records that are missing measurement data entirely.
        """
        sample_ids: list[str] = []
        value_groups: list[tuple[float, ...]] = []

        for record in self.records:
            if len(record) < 2:
                continue
            sample_id, *values = record
            sample_ids.append(sample_id)
            value_groups.append(tuple(float(value) for value in values))

        return sample_ids, value_groups

    @staticmethod
    def run() -> None:
        records: list[tuple[str, ...]] = [
            ("S001", "12.5", "0.95"),
            ("S002", "14.1"),
            ("S003",),
        ]

        processor = InterviewUnpacking(records)
        ids, values = processor.separate_ids_and_values()

        print(f"Sample IDs: {ids}")
        print(f"Value groups: {values}")


class IndustryUnpacking:
    """Compose clean, structured biological records from separate sources."""

    def __init__(
        self,
        metadata: dict[str, str],
        measurements: dict[str, float],
    ) -> None:
        self.metadata = metadata
        self.measurements = measurements

    def merge_record(self) -> dict[str, str | float]:
        """Combine metadata and measurement dictionaries into one record."""
        return {**self.metadata, **self.measurements}

    def unpack_function_arguments(self, *ids: str, **overrides: float) -> dict[str, float]:
        """Demonstrate unpacking positional and keyword arguments together."""
        base_scores = {sample_id: 0.0 for sample_id in ids}
        return {**base_scores, **overrides}

    @staticmethod
    def run() -> None:
        metadata = {"sample_id": "S001", "species": "Arabidopsis"}
        measurements = {"height_cm": 12.5, "purity_score": 0.95}

        composer = IndustryUnpacking(metadata, measurements)
        merged = composer.merge_record()
        overridden = composer.unpack_function_arguments("S001", "S002", S001=0.92)

        print(f"Merged record: {merged}")
        print(f"Overridden scores: {overridden}")


if __name__ == "__main__":
    UniversityUnpacking.run()
    InterviewUnpacking.run()
    IndustryUnpacking.run()
