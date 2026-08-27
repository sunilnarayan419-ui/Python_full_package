"""Demonstrations of the built-in id() function using mutable biological records.

id() values are runtime-specific and not guaranteed stable across processes.
These examples demonstrate identity behavior without asserting fixed numbers.
"""


class UniversityId:
    """Teach the fundamental behavior of id() for object identity."""

    def __init__(self, record: dict[str, object]) -> None:
        self.record = record

    def is_same_object(self, other_record: dict[str, object]) -> bool:
        return id(self.record) == id(other_record)

    @staticmethod
    def run() -> None:
        record_a = {"sample_id": "P001", "height": 58.2}
        record_b = record_a  # same object, different name
        record_c = {"sample_id": "P001", "height": 58.2}  # equal, different object

        processor = UniversityId(record_a)
        print(f"record_a is record_b (same object): {processor.is_same_object(record_b)}")
        print(f"record_a is record_c (equal value, new object): {processor.is_same_object(record_c)}")


class InterviewId:
    """Distinguish identity (id()/is) from equality (==) using biological records."""

    @staticmethod
    def describe_relationship(first: dict[str, object], second: dict[str, object]) -> str:
        same_identity = first is second
        same_value = first == second

        if same_identity:
            return "same object (identity and value are necessarily equal)"
        if same_value:
            return "different objects, but equal values"
        return "different objects with different values"

    @staticmethod
    def run() -> None:
        reference = {"sample_id": "P001", "height": 58.2}
        alias = reference
        duplicate = {"sample_id": "P001", "height": 58.2}
        different = {"sample_id": "P002", "height": 61.4}

        print(f"reference vs alias: {InterviewId.describe_relationship(reference, alias)}")
        print(f"reference vs duplicate: {InterviewId.describe_relationship(reference, duplicate)}")
        print(f"reference vs different: {InterviewId.describe_relationship(reference, different)}")


class IndustryId:
    """Track reference behavior when mutating shared biological data structures."""

    def __init__(self, samples: list[dict[str, object]]) -> None:
        self.samples = samples

    def mutate_first_sample(self, updated_height: float) -> None:
        """Mutating in place affects every reference to the same object."""
        self.samples[0]["height"] = updated_height

    def demonstrate_shared_reference_risk(self) -> None:
        shared_record = self.samples[0]
        alias = shared_record  # both variables reference the same dict object

        alias["height"] = 999.0  # mutating through the alias affects shared_record too

        same_object = id(shared_record) == id(alias)
        print(f"shared_record and alias refer to the same object: {same_object}")
        print(f"shared_record height after mutation via alias: {shared_record['height']}")

    @staticmethod
    def run() -> None:
        samples: list[dict[str, object]] = [
            {"sample_id": "S001", "height": 58.2},
            {"sample_id": "S002", "height": 61.4},
        ]

        processor = IndustryId(samples)
        processor.demonstrate_shared_reference_risk()


if __name__ == "__main__":
    UniversityId.run()
    InterviewId.run()
    IndustryId.run()
