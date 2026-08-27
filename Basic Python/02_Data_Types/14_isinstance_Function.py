"""Safe runtime type checking of scientific data."""


class IsInstanceFunctionUniversity:
    def __init__(self, value: object) -> None:
        self.value = value

    def is_numeric(self) -> bool:
        return isinstance(self.value, (int, float))


class IsInstanceFunctionInterview:
    @staticmethod
    def is_sequence(value: object) -> bool:
        return isinstance(value, str) and all(c in "ACGTNacgtn" for c in value)


class IsInstanceFunctionIndustry:
    @staticmethod
    def validate_record(record: dict[str, object]) -> list[str]:
        errors: list[str] = []
        if not isinstance(record.get("sample_id"), str):
            errors.append("sample_id must be str")
        if not isinstance(record.get("reads"), int):
            errors.append("reads must be int")
        if not isinstance(record.get("gc"), (int, float)):
            errors.append("gc must be numeric")
        return errors


if __name__ == "__main__":
    print(IsInstanceFunctionUniversity(0.5).is_numeric())
    print(IsInstanceFunctionInterview.is_sequence("ATGC"))
    print(IsInstanceFunctionIndustry.validate_record(
        {"sample_id": "S1", "reads": 100, "gc": 0.5}
    ))
