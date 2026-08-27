"""List comprehensions demonstrated through plant and gene-expression data."""


class UniversityListComprehensions:
    """Teach the fundamental syntax and purpose of list comprehensions."""

    def __init__(self, plant_heights_cm: list[float]) -> None:
        self.plant_heights_cm = plant_heights_cm

    def convert_to_meters(self) -> list[float]:
        """Transform every height from centimeters to meters."""
        return [height / 100 for height in self.plant_heights_cm]

    def filter_tall_plants(self, threshold_cm: float) -> list[float]:
        """Keep only plants taller than the given threshold."""
        return [height for height in self.plant_heights_cm if height > threshold_cm]

    @staticmethod
    def run() -> None:
        heights = [25.5, 31.2, 42.8, 18.0, 55.6]

        processor = UniversityListComprehensions(heights)
        meters = processor.convert_to_meters()
        tall_plants = processor.filter_tall_plants(threshold_cm=30.0)

        print(f"Plant heights in meters: {meters}")
        print(f"Plants taller than 30cm: {tall_plants}")


class InterviewListComprehensions:
    """Solve a realistic gene-expression filtering problem with edge cases."""

    def __init__(self, gene_expression: dict[str, float]) -> None:
        self.gene_expression = gene_expression

    def upregulated_genes(self, fold_change_threshold: float) -> list[str]:
        """Return gene names whose expression exceeds the threshold.

        Handles an empty dataset and skips non-numeric or missing values.
        """
        if not self.gene_expression:
            return []

        return [
            gene
            for gene, value in self.gene_expression.items()
            if isinstance(value, (int, float)) and value >= fold_change_threshold
        ]

    def normalize_and_round(self, max_value: float, decimals: int = 2) -> list[float]:
        """Normalize expression values against a maximum, rounding results.

        Guards against a zero max_value to avoid division errors.
        """
        if max_value == 0:
            return []

        return [
            round(value / max_value, decimals)
            for value in self.gene_expression.values()
            if value is not None
        ]

    @staticmethod
    def run() -> None:
        expression_data = {
            "BRCA1": 3.4,
            "TP53": 5.1,
            "EGFR": 1.2,
            "MYC": 4.8,
        }
        empty_data: dict[str, float] = {}

        case_one = InterviewListComprehensions(expression_data)
        case_two = InterviewListComprehensions(empty_data)

        print(f"Upregulated genes: {case_one.upregulated_genes(3.0)}")
        print(f"Empty dataset result: {case_two.upregulated_genes(3.0)}")
        print(f"Normalized values: {case_one.normalize_and_round(max_value=5.1)}")


class IndustryListComprehensions:
    """A small, reusable pipeline for cleaning biological measurement data."""

    def __init__(self, raw_measurements: list[float | None]) -> None:
        self.raw_measurements = raw_measurements

    def remove_invalid_readings(self) -> list[float]:
        """Drop missing or non-positive sensor readings."""
        return [
            reading
            for reading in self.raw_measurements
            if reading is not None and reading > 0
        ]

    def scale_readings(self, readings: list[float], factor: float) -> list[float]:
        """Apply a linear scale factor to a cleaned list of readings."""
        return [reading * factor for reading in readings]

    def build_clean_pipeline(self, scale_factor: float) -> list[float]:
        """Run the full clean-and-scale pipeline in sequence."""
        cleaned = self.remove_invalid_readings()
        return self.scale_readings(cleaned, scale_factor)

    @staticmethod
    def run() -> None:
        sensor_readings: list[float | None] = [12.4, None, -3.0, 8.9, 0.0, 15.1]

        pipeline = IndustryListComprehensions(sensor_readings)
        result = pipeline.build_clean_pipeline(scale_factor=1.05)

        print(f"Raw readings: {sensor_readings}")
        print(f"Cleaned and scaled readings: {result}")


if __name__ == "__main__":
    UniversityListComprehensions.run()
    InterviewListComprehensions.run()
    IndustryListComprehensions.run()
