from __future__ import annotations


class UniversityTypeHints:
    """Demonstrate basic type hints on plant height measurements.

    Type hints document intent for readers and static type checkers;
    they are NOT enforced automatically at runtime by Python itself.
    """

    def __init__(self, plant_name: str, height_cm: float) -> None:
        self.plant_name: str = plant_name
        self.height_cm: float = height_cm

    def describe(self) -> str:
        """Time: O(1)."""
        return f"{self.plant_name}: {self.height_cm} cm"

    @staticmethod
    def average_height(heights: list[float]) -> float:
        """Basic collection type hint: list[float].

        Time: O(n)
        """
        if not heights:
            return 0.0
        return sum(heights) / len(heights)

    @staticmethod
    def run() -> None:
        plant = UniversityTypeHints("Basil", 24.5)
        print("University:", plant.describe())
        heights: list[float] = [12.5, 20.1, 9.3, 15.7]
        print("University: average height ->", UniversityTypeHints.average_height(heights))


class InterviewTypeHints:
    """Demonstrate richer type annotations including Optional/Union and
    the modern | union syntax, over lab sample readings that may be
    missing or come from multiple instrument types.
    """

    @staticmethod
    def parse_reading(raw_value: str | float | None) -> float | None:
        """Accept a raw reading from multiple possible sources and
        normalize it. Returns None if the reading is missing or invalid.

        Time: O(1)

        Note: the type hint alone does not validate raw_value at
        runtime - explicit isinstance checks below do that work.
        """
        if raw_value is None:
            return None
        if isinstance(raw_value, (int, float)):
            return float(raw_value)
        try:
            return float(raw_value)
        except ValueError:
            return None

    @staticmethod
    def summarize_readings(readings: list[str | float | None]) -> dict[str, float | int]:
        """Time: O(n), Space: O(1)."""
        valid_values: list[float] = []
        for raw in readings:
            parsed = InterviewTypeHints.parse_reading(raw)
            if parsed is not None:
                valid_values.append(parsed)
        return {
            "count": len(valid_values),
            "average": sum(valid_values) / len(valid_values) if valid_values else 0.0,
        }

    @staticmethod
    def run() -> None:
        raw_readings: list[str | float | None] = [4.2, "5.6", None, "invalid", 3.9]
        summary = InterviewTypeHints.summarize_readings(raw_readings)
        print("Interview: summary of mixed readings ->", summary)
        print("Interview: parsed 'invalid' ->", InterviewTypeHints.parse_reading("invalid"))


type SampleId = str
type ConcentrationMgPerL = float


class InvalidMeasurementError(ValueError):
    """Raised when a measurement fails structural validation."""


class IndustryTypeHints:
    """A strongly typed scientific data-processing interface using
    modern type aliases for clarity, and explicit validation, since
    type hints themselves provide no runtime guarantees.
    """

    def __init__(self) -> None:
        self._measurements: dict[SampleId, list[ConcentrationMgPerL]] = {}

    def record(self, sample_id: SampleId, concentration: ConcentrationMgPerL) -> None:
        """Record a validated concentration reading for a sample.

        Time: O(1) amortized
        Raises InvalidMeasurementError for negative concentrations.
        """
        if concentration < 0:
            raise InvalidMeasurementError(f"concentration must be non-negative, got {concentration}")
        self._measurements.setdefault(sample_id, []).append(concentration)

    def average_for_sample(self, sample_id: SampleId) -> ConcentrationMgPerL | None:
        """Time: O(k) where k is readings for this sample."""
        readings = self._measurements.get(sample_id)
        if not readings:
            return None
        return sum(readings) / len(readings)

    def all_sample_ids(self) -> list[SampleId]:
        """Time: O(n), Space: O(n)."""
        return list(self._measurements.keys())

    @staticmethod
    def run() -> None:
        processor = IndustryTypeHints()
        processor.record("S001", 5.6)
        processor.record("S001", 6.1)
        processor.record("S002", 3.3)

        print("Industry: average for S001 ->", processor.average_for_sample("S001"))
        print("Industry: average for unknown sample ->", processor.average_for_sample("S999"))
        print("Industry: all sample IDs ->", processor.all_sample_ids())

        try:
            processor.record("S003", -1.0)
        except InvalidMeasurementError as error:
            print("Industry: validation caught ->", error)


if __name__ == "__main__":
    UniversityTypeHints.run()
    InterviewTypeHints.run()
    IndustryTypeHints.run()
