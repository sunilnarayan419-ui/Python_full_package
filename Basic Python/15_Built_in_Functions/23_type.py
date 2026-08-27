"""Demonstrations of the built-in type() function for biological data inspection."""


class UniversityType:
    """Teach the fundamental behavior of type() for runtime type inspection."""

    def __init__(self, value: object) -> None:
        self.value = value

    def type_name(self) -> str:
        return type(self.value).__name__

    @staticmethod
    def run() -> None:
        height_value = UniversityType(58.2)
        species_value = UniversityType("Wheat")
        measurements_value = UniversityType([1.1, 1.2, 1.3])

        print(f"Type of 58.2: {height_value.type_name()}")
        print(f"Type of 'Wheat': {species_value.type_name()}")
        print(f"Type of [1.1, 1.2, 1.3]: {measurements_value.type_name()}")


class InterviewType:
    """Practical debugging: comparing type() output across biological data structures.

    type() checks exact type only. isinstance() (see 22_isinstance.py) is
    generally preferred for validation because it also respects subclasses.
    """

    @staticmethod
    def describe_structure(value: object) -> str:
        return f"{value!r} -> {type(value)}"

    @staticmethod
    def exact_type_matches(value: object, expected_type: type) -> bool:
        """Exact type check: True only if value's type is precisely expected_type."""
        return type(value) is expected_type

    @staticmethod
    def run() -> None:
        sample_values: list[object] = [58.2, "Wheat", [1.1, 1.2], {"sample_id": "P001"}, True]

        for value in sample_values:
            print(InterviewType.describe_structure(value))

        # A subtle pitfall: bool is technically a subclass of int in Python.
        print(f"type(True) is bool: {InterviewType.exact_type_matches(True, bool)}")
        print(f"type(True) is int (exact match, False despite bool subclassing int): "
              f"{InterviewType.exact_type_matches(True, int)}")


class IndustryType:
    """Controlled diagnostic utility for reporting data types across a dataset."""

    def __init__(self, records: list[dict[str, object]]) -> None:
        self.records = records

    def field_type_report(self, field: str) -> dict[str, int]:
        """Count how many records have each distinct type for a given field."""
        counts: dict[str, int] = {}
        for record in self.records:
            if field not in record:
                continue
            type_name = type(record[field]).__name__
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    @staticmethod
    def run() -> None:
        records: list[dict[str, object]] = [
            {"sample_id": "P001", "height": 58.2},
            {"sample_id": "P002", "height": 61},  # int instead of float
            {"sample_id": "P003", "height": "unknown"},  # inconsistent data
        ]

        diagnostics = IndustryType(records)
        report = diagnostics.field_type_report("height")
        print(f"Type distribution for 'height' field: {report}")


if __name__ == "__main__":
    UniversityType.run()
    InterviewType.run()
    IndustryType.run()
