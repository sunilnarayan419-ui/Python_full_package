"""Converting scientific/genomic input values between types."""


class TypeConversionUniversity:
    @staticmethod
    def to_int(reads: str) -> int:
        return int(reads)

    @staticmethod
    def to_float(value: str) -> float:
        return float(value)

    @staticmethod
    def to_str(value: int) -> str:
        return str(value)


class TypeConversionInterview:
    @staticmethod
    def parse_gc(value: str) -> float:
        return float(value) / 100.0

    @staticmethod
    def parse_species_code(code: int) -> str:
        return f"SP-{code:04d}"


class TypeConversionIndustry:
    @staticmethod
    def _coerce(value: str, target: type) -> int | float | str:
        if target is int:
            return int(value)
        if target is float:
            return float(value)
        return str(value)

    @classmethod
    def normalize(cls, raw: str, kind: str) -> int | float | str:
        target = {"int": int, "float": float, "str": str}[kind]
        return cls._coerce(raw, target)


if __name__ == "__main__":
    print(TypeConversionUniversity.to_int("1234"))
    print(TypeConversionInterview.parse_gc("45.2"))
    print(TypeConversionIndustry.normalize("3.14", "float"))
