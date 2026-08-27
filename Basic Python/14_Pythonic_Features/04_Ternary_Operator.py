"""Ternary (conditional) expressions demonstrated through plant health checks."""


class UniversityTernaryOperator:
    """Teach the fundamental syntax of the conditional expression."""

    def __init__(self, plant_height_cm: float) -> None:
        self.plant_height_cm = plant_height_cm

    def classify_growth(self, threshold_cm: float) -> str:
        """Label a plant as 'tall' or 'short' using a single expression."""
        return "tall" if self.plant_height_cm >= threshold_cm else "short"

    @staticmethod
    def run() -> None:
        plant_a = UniversityTernaryOperator(plant_height_cm=42.0)
        plant_b = UniversityTernaryOperator(plant_height_cm=15.0)

        print(f"Plant A classification: {plant_a.classify_growth(30.0)}")
        print(f"Plant B classification: {plant_b.classify_growth(30.0)}")


class InterviewTernaryOperator:
    """Solve a practical sample-status classification problem."""

    def __init__(self, sample_reading: float | None) -> None:
        self.sample_reading = sample_reading

    def determine_status(self, pass_threshold: float) -> str:
        """Determine pass/fail/invalid status for a single sample reading.

        Handles a missing (None) reading as an explicit invalid case rather
        than letting a comparison against None raise an error.
        """
        return (
            "invalid"
            if self.sample_reading is None
            else "pass" if self.sample_reading >= pass_threshold else "fail"
        )

    @staticmethod
    def run() -> None:
        valid_sample = InterviewTernaryOperator(sample_reading=0.92)
        failing_sample = InterviewTernaryOperator(sample_reading=0.41)
        missing_sample = InterviewTernaryOperator(sample_reading=None)

        print(f"Valid sample status: {valid_sample.determine_status(0.75)}")
        print(f"Failing sample status: {failing_sample.determine_status(0.75)}")
        print(f"Missing sample status: {missing_sample.determine_status(0.75)}")


class IndustryTernaryOperator:
    """Apply concise, readable scientific rule evaluation across a dataset."""

    def __init__(self, expression_levels: dict[str, float]) -> None:
        self.expression_levels = expression_levels

    def classify_expression_level(self, gene: str, high_threshold: float) -> str:
        """Classify a single gene's expression as 'high' or 'normal'."""
        value = self.expression_levels.get(gene, 0.0)
        return "high" if value >= high_threshold else "normal"

    def classify_all_genes(self, high_threshold: float) -> dict[str, str]:
        """Classify every gene in the dataset using the same clear rule."""
        return {
            gene: ("high" if value >= high_threshold else "normal")
            for gene, value in self.expression_levels.items()
        }

    @staticmethod
    def run() -> None:
        expression_data = {"BRCA1": 6.2, "TP53": 2.1, "EGFR": 5.9}

        classifier = IndustryTernaryOperator(expression_data)
        single_result = classifier.classify_expression_level("BRCA1", high_threshold=5.0)
        all_results = classifier.classify_all_genes(high_threshold=5.0)

        print(f"BRCA1 classification: {single_result}")
        print(f"All gene classifications: {all_results}")


if __name__ == "__main__":
    UniversityTernaryOperator.run()
    InterviewTernaryOperator.run()
    IndustryTernaryOperator.run()
