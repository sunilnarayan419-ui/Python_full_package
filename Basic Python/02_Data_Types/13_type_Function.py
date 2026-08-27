"""Inspecting Python data types in scientific data processing."""


class TypeFunctionUniversity:
    @staticmethod
    def show(value: object) -> str:
        return f"{value!r} -> {type(value).__name__}"


class TypeFunctionInterview:
    @staticmethod
    def classify(values: list[object]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for v in values:
            name = type(v).__name__
            counts[name] = counts.get(name, 0) + 1
        return counts


class TypeFunctionIndustry:
    @staticmethod
    def expected(label: str, value: object, expected: type) -> str:
        if type(value) is not expected:
            return f"{label}: expected {expected.__name__}, got {type(value).__name__}"
        return f"{label}: OK ({expected.__name__})"


if __name__ == "__main__":
    print(TypeFunctionUniversity.show(0.45))
    print(TypeFunctionInterview.classify([1, 2.0, "x", 3]))
    print(TypeFunctionIndustry.expected("gc", 0.5, float))
