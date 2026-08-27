"""Demonstrations of the built-in isinstance() function for biological data validation."""


class UniversityIsinstance:
    """Teach the fundamental behavior of isinstance() for runtime type checking."""

    def __init__(self, value: object) -> None:
        self.value = value

    def is_numeric(self) -> bool:
        return isinstance(self.value, (int, float))

    @staticmethod
    def run() -> None:
        height_value = UniversityIsinstance(58.2)
        species_value = UniversityIsinstance("Wheat")

        print(f"58.2 is numeric: {height_value.is_numeric()}")
        print(f"'Wheat' is numeric: {species_value.is_numeric()}")


class InterviewIsinstance:
    """Defensive input validation for a realistic biological record processor."""

    @staticmethod
    def validate_record(record: object) -> list[str]:
        """Return a list of validation errors for a plant sample record."""
        errors: list[str] = []

        if not isinstance(record, dict):
            return ["record must be a dictionary"]

        if not isinstance(record.get("sample_id"), str):
            errors.append("sample_id must be a string")

        if not isinstance(record.get("height"), (int, float)):
            errors.append("height must be a number")

        measurements = record.get("measurements")
        if measurements is not None and not isinstance(measurements, (list, tuple)):
            errors.append("measurements must be a list or tuple if provided")

        return errors

    @staticmethod
    def run() -> None:
        valid_record = {"sample_id": "P001", "height": 58.2, "measurements": [1.1, 1.2]}
        invalid_record = {"sample_id": 123, "height": "tall"}
        not_a_record = "this is not a record"

        print(f"Valid record errors: {InterviewIsinstance.validate_record(valid_record)}")
        print(f"Invalid record errors: {InterviewIsinstance.validate_record(invalid_record)}")
        print(f"Non-dict input errors: {InterviewIsinstance.validate_record(not_a_record)}")


class IndustryIsinstance:
    """Reusable, defensive data-validation logic for a scientific data pipeline."""

    EXPECTED_TYPES: dict[str, type | tuple[type, ...]] = {
        "sample_id": str,
        "height": (int, float),
        "species": str,
        "measurements": (list, tuple),
    }

    def validate_field_types(self, record: dict[str, object]) -> dict[str, bool]:
        """Check each expected field against its allowed type(s), where present."""
        results: dict[str, bool] = {}
        for field, expected_type in self.EXPECTED_TYPES.items():
            if field not in record:
                continue
            results[field] = isinstance(record[field], expected_type)
        return results

    def is_fully_valid(self, record: dict[str, object]) -> bool:
        checks = self.validate_field_types(record)
        return all(checks.values()) if checks else False

    @staticmethod
    def run() -> None:
        validator = IndustryIsinstance()
        records: list[dict[str, object]] = [
            {"sample_id": "P001", "height": 58.2, "species": "Wheat", "measurements": [1.1]},
            {"sample_id": "P002", "height": "not_a_number", "species": "Rice"},
        ]

        for record in records:
            checks = validator.validate_field_types(record)
            print(f"{record.get('sample_id')}: {checks} -> fully valid: {validator.is_fully_valid(record)}")


if __name__ == "__main__":
    UniversityIsinstance.run()
    InterviewIsinstance.run()
    IndustryIsinstance.run()
