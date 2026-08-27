plant_kingdom = "Plantae"


class UniversityVariableScope:
    def __init__(self, species: str) -> None:
        self.species = species

    def describe_classification(self) -> str:
        # Reads the module-level (global) variable plant_kingdom.
        local_note = "eukaryotic"
        return f"{self.species} belongs to kingdom {plant_kingdom} ({local_note})"

    @staticmethod
    def run() -> None:
        classifier = UniversityVariableScope("Zea mays")
        print("University - classification:", classifier.describe_classification())
        print("University - global kingdom:", plant_kingdom)


class InterviewVariableScope:
    def __init__(self) -> None:
        self.sample_count = 0

    def process_batch(self, sample_ids: list[str]) -> list[str]:
        processed: list[str] = []  # local scope, isolated per call
        for sample_id in sample_ids:
            tag = f"processed-{sample_id}"
            processed.append(tag)
        self.sample_count += len(processed)
        return processed

    @staticmethod
    def run() -> None:
        processor = InterviewVariableScope()
        first_batch = processor.process_batch(["S1", "S2"])
        second_batch = processor.process_batch(["S3"])
        print("Interview - first batch:", first_batch)
        print("Interview - second batch:", second_batch)
        print("Interview - total sample count (instance state):", processor.sample_count)


class IndustryVariableScope:
    """Demonstrates LEGB resolution across nested scopes in a scoring pipeline."""

    default_weight = 1.0  # class-level scope, shared unless overridden per instance

    def __init__(self, pipeline_name: str) -> None:
        self.pipeline_name = pipeline_name

    def score_samples(self, raw_scores: list[float]) -> list[float]:
        weight = self.default_weight  # enclosing-function local variable

        def apply_weight(score: float) -> float:
            # Reads 'weight' from the enclosing function scope (Enclosing in LEGB).
            return score * weight

        return [apply_weight(score) for score in raw_scores]

    @staticmethod
    def run() -> None:
        pipeline = IndustryVariableScope("Growth-Scoring")
        weighted_scores = pipeline.score_samples([10.0, 20.0, 30.0])
        print("Industry - weighted scores:", weighted_scores)
        print("Industry - class-level default weight:", IndustryVariableScope.default_weight)


if __name__ == "__main__":
    UniversityVariableScope.run()
    InterviewVariableScope.run()
    IndustryVariableScope.run()
