class UniversityDefaultArguments:
    def __init__(self, plant_species: str) -> None:
        self.plant_species = plant_species

    def water_requirement_liters(self, days: int = 7, liters_per_day: float = 1.5) -> float:
        return days * liters_per_day

    def describe_watering_plan(self, days: int = 7, liters_per_day: float = 1.5) -> str:
        total = self.water_requirement_liters(days, liters_per_day)
        return f"{self.plant_species} needs {total:.1f} L over {days} days"

    @staticmethod
    def run() -> None:
        plant = UniversityDefaultArguments("Solanum lycopersicum")
        default_plan = plant.describe_watering_plan()
        custom_plan = plant.describe_watering_plan(days=14, liters_per_day=2.0)
        print("University - default plan:", default_plan)
        print("University - custom plan:", custom_plan)


class InterviewDefaultArguments:
    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name
        self.readings: list[float] = []

    def add_reading(self, value: float) -> None:
        self.readings.append(value)

    def summarize(self, precision: int = 2, include_count: bool = True) -> str:
        if not self.readings:
            return f"{self.experiment_name}: no readings recorded"
        average = sum(self.readings) / len(self.readings)
        summary = f"{self.experiment_name}: avg={average:.{precision}f}"
        if include_count:
            summary += f" (n={len(self.readings)})"
        return summary

    @staticmethod
    def run() -> None:
        trial = InterviewDefaultArguments("pH-Trial-1")
        for reading in (6.8, 7.1, 6.9, 7.0):
            trial.add_reading(reading)

        print("Interview - default summary:", trial.summarize())
        print("Interview - precise summary:", trial.summarize(precision=4))
        print("Interview - no count summary:", trial.summarize(include_count=False))

        empty_trial = InterviewDefaultArguments("Empty-Trial")
        print("Interview - empty summary:", empty_trial.summarize())


class IndustryDefaultArguments:
    """Configures a reproducible sequencing quality-control step."""

    DEFAULT_MIN_QUALITY_SCORE: float = 30.0
    DEFAULT_MIN_READ_LENGTH: int = 50

    def __init__(self, sample_id: str) -> None:
        if not sample_id.strip():
            raise ValueError("sample_id must not be empty")
        self.sample_id = sample_id

    def filter_reads(
        self,
        reads: list[dict],
        min_quality_score: float = DEFAULT_MIN_QUALITY_SCORE,
        min_read_length: int = DEFAULT_MIN_READ_LENGTH,
    ) -> list[dict]:
        return [
            read
            for read in reads
            if read["quality_score"] >= min_quality_score
            and read["length"] >= min_read_length
        ]

    def build_qc_report(
        self,
        reads: list[dict],
        min_quality_score: float = DEFAULT_MIN_QUALITY_SCORE,
        min_read_length: int = DEFAULT_MIN_READ_LENGTH,
    ) -> dict[str, object]:
        passed_reads = self.filter_reads(reads, min_quality_score, min_read_length)
        return {
            "sample_id": self.sample_id,
            "total_reads": len(reads),
            "passed_reads": len(passed_reads),
            "min_quality_score": min_quality_score,
            "min_read_length": min_read_length,
        }

    @staticmethod
    def run() -> None:
        pipeline = IndustryDefaultArguments("Sample-A17")
        reads = [
            {"quality_score": 35.0, "length": 75},
            {"quality_score": 22.0, "length": 60},
            {"quality_score": 40.0, "length": 40},
        ]
        default_report = pipeline.build_qc_report(reads)
        strict_report = pipeline.build_qc_report(reads, min_quality_score=38.0)
        print("Industry - default QC report:", default_report)
        print("Industry - strict QC report:", strict_report)


if __name__ == "__main__":
    UniversityDefaultArguments.run()
    InterviewDefaultArguments.run()
    IndustryDefaultArguments.run()
