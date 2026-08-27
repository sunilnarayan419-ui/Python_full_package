"""Demonstrations of the built-in chr() function using scientific Unicode symbols."""


class UniversityChr:
    """Teach the fundamental behavior of chr() for code-point-to-character conversion."""

    def __init__(self, code_point: int) -> None:
        self.code_point = code_point

    def to_character(self) -> str:
        return chr(self.code_point)

    @staticmethod
    def run() -> None:
        processor = UniversityChr(code_point=946)  # Greek small letter beta
        print(f"chr(946) -> {processor.to_character()} (used in beta-diversity notation)")


class InterviewChr:
    """Unicode-aware processing: convert a range of code points safely."""

    @staticmethod
    def safe_chr(code_point: int) -> str | None:
        """Return the character for a code point, or None if it is invalid."""
        if not (0 <= code_point <= 0x10FFFF):
            return None
        return chr(code_point)

    @staticmethod
    def greek_letter_sequence(start_code_point: int, count: int) -> list[str]:
        return [chr(start_code_point + offset) for offset in range(count)]

    @staticmethod
    def run() -> None:
        valid_result = InterviewChr.safe_chr(956)  # micro sign, used in µg, µL
        invalid_result = InterviewChr.safe_chr(-1)

        print(f"Valid code point 956: {valid_result}")
        print(f"Invalid code point -1: {invalid_result}")

        alpha_start = 0x03B1  # Greek small letter alpha
        print(f"Greek letters alpha-delta: {InterviewChr.greek_letter_sequence(alpha_start, 4)}")


class IndustryChr:
    """Safe scientific text/symbol generation for reporting workflows."""

    SYMBOL_CODE_POINTS: dict[str, int] = {
        "micro": 0x00B5,   # µ, e.g. µg, µL, µm
        "alpha": 0x03B1,   # α, e.g. significance level
        "beta": 0x03B2,    # β, e.g. beta-diversity
        "delta": 0x0394,   # Δ, e.g. change in concentration
        "degree": 0x00B0,  # °, e.g. temperature
    }

    def symbol(self, name: str) -> str:
        """Return the character for a known scientific symbol name."""
        code_point = self.SYMBOL_CODE_POINTS.get(name)
        if code_point is None:
            raise ValueError(f"Unknown scientific symbol name: {name}")
        return chr(code_point)

    def format_measurement(self, value: float, unit_symbol_name: str, unit_suffix: str) -> str:
        return f"{value}{self.symbol(unit_symbol_name)}{unit_suffix}"

    @staticmethod
    def run() -> None:
        formatter = IndustryChr()
        print(formatter.format_measurement(12.5, "micro", "g"))
        print(formatter.format_measurement(37.0, "degree", "C"))
        print(f"Significance level symbol: {formatter.symbol('alpha')} = 0.05")


if __name__ == "__main__":
    UniversityChr.run()
    InterviewChr.run()
    IndustryChr.run()
