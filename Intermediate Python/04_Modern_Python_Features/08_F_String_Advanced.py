from __future__ import annotations

from datetime import datetime


class UniversityFStringAdvanced:
    """Format basic scientific measurements using f-strings, including
    precision and simple width/alignment."""

    @staticmethod
    def format_measurement(sample_id: str, value: float) -> str:
        """Time: O(1)."""
        return f"{sample_id:<8} | value = {value:.2f} mg/L"

    @staticmethod
    def run() -> None:
        readings = [("S001", 5.678), ("S02", 12.3), ("S100", 0.941)]
        print("University:")
        for sample_id, value in readings:
            print(" ", UniversityFStringAdvanced.format_measurement(sample_id, value))


class InterviewFStringAdvanced:
    """Build structured, readable output using advanced formatting:
    width, alignment, numeric formatting, percentages, and the debug
    '=' specifier."""

    @staticmethod
    def format_qc_report(sample_id: str, pass_rate: float, total_reads: int) -> str:
        """Percentage formatting and thousands separators.

        Time: O(1)
        """
        return f"{sample_id:<10}{pass_rate:>7.1%}{total_reads:>15,} reads"

    @staticmethod
    def debug_reading(concentration: float) -> str:
        """The = specifier prints both the expression text and its value,
        useful for quick diagnostic logging.

        Time: O(1)
        """
        return f"{concentration=:.3f}"

    @staticmethod
    def run() -> None:
        print("Interview:")
        print(" ", InterviewFStringAdvanced.format_qc_report("S001", 0.947, 1_284_512))
        print(" ", InterviewFStringAdvanced.format_qc_report("S002", 0.812, 998_120))
        concentration = 4.216789
        print(" ", InterviewFStringAdvanced.debug_reading(concentration))


class IndustryFStringAdvanced:
    """Generate clean, maintainable scientific report lines using
    formatting specs kept in small named constants rather than scattered
    magic format strings, suitable for structured log output."""

    _ID_WIDTH = 12
    _VALUE_WIDTH = 10
    _PRECISION = 3

    @staticmethod
    def format_report_line(sample_id: str, concentration: float, timestamp: datetime) -> str:
        """Combine alignment, fixed precision, and a formatted timestamp
        into one consistent report line format.

        Time: O(1)
        """
        width = IndustryFStringAdvanced._VALUE_WIDTH
        precision = IndustryFStringAdvanced._PRECISION
        return (
            f"{sample_id:<{IndustryFStringAdvanced._ID_WIDTH}}"
            f"{concentration:>{width}.{precision}f} mg/L"
            f"  [{timestamp:%Y-%m-%d %H:%M}]"
        )

    @staticmethod
    def format_scientific_notation(value: float) -> str:
        """Scientific notation formatting for very small/large values,
        such as molar concentrations.

        Time: O(1)
        """
        return f"{value:.3e} M"

    @staticmethod
    def build_summary_report(readings: list[tuple[str, float]], timestamp: datetime) -> str:
        """Time: O(n), Space: O(n) for the joined report string."""
        lines = [
            IndustryFStringAdvanced.format_report_line(sample_id, value, timestamp)
            for sample_id, value in readings
        ]
        return "\n".join(lines)

    @staticmethod
    def run() -> None:
        timestamp = datetime(2026, 8, 13, 9, 30)
        readings = [("S001", 5.6712), ("S002", 12.389), ("S003", 0.0456)]
        report = IndustryFStringAdvanced.build_summary_report(readings, timestamp)
        print("Industry:\n" + report)

        molar_concentration = 0.0000032
        print("Industry:", IndustryFStringAdvanced.format_scientific_notation(molar_concentration))


if __name__ == "__main__":
    UniversityFStringAdvanced.run()
    InterviewFStringAdvanced.run()
    IndustryFStringAdvanced.run()
