class UniversityReturnValues:
    def __init__(self, gene_sequence: str) -> None:
        self.gene_sequence = gene_sequence

    def count_bases(self) -> int:
        return len(self.gene_sequence)

    def base_composition(self) -> tuple[int, int, int, int]:
        adenine = self.gene_sequence.count("A")
        thymine = self.gene_sequence.count("T")
        cytosine = self.gene_sequence.count("C")
        guanine = self.gene_sequence.count("G")
        return adenine, thymine, cytosine, guanine

    def summarize_sequence(self) -> dict[str, int]:
        adenine, thymine, cytosine, guanine = self.base_composition()
        return {"A": adenine, "T": thymine, "C": cytosine, "G": guanine}

    @staticmethod
    def run() -> None:
        analyzer = UniversityReturnValues("ATCGGGCATCGA")
        total_bases = analyzer.count_bases()
        composition = analyzer.base_composition()
        summary = analyzer.summarize_sequence()
        print("University - total bases:", total_bases)
        print("University - composition tuple:", composition)
        print("University - summary dict:", summary)


class InterviewReturnValues:
    def __init__(self, measurements_cm: list[float]) -> None:
        self.measurements_cm = measurements_cm

    def min_max_range(self) -> tuple[float, float, float] | None:
        if not self.measurements_cm:
            return None
        lowest = min(self.measurements_cm)
        highest = max(self.measurements_cm)
        spread = highest - lowest
        return lowest, highest, spread

    def normalized_measurements(self) -> list[float]:
        stats = self.min_max_range()
        if stats is None:
            return []
        lowest, highest, spread = stats
        if spread == 0:
            return [0.0 for _ in self.measurements_cm]
        return [(value - lowest) / spread for value in self.measurements_cm]

    @staticmethod
    def run() -> None:
        experiment = InterviewReturnValues([12.4, 15.1, 9.8, 20.0, 15.1])
        stats = experiment.min_max_range()
        normalized = experiment.normalized_measurements()
        print("Interview - min/max/range:", stats)
        print("Interview - normalized:", normalized)

        empty_experiment = InterviewReturnValues([])
        print("Interview - empty range:", empty_experiment.min_max_range())
        print("Interview - empty normalized:", empty_experiment.normalized_measurements())


class IndustryReturnValues:
    """Runs a small dose-response computation pipeline for a compound."""

    def __init__(self, compound_name: str, doses_mg: list[float], responses_pct: list[float]) -> None:
        if len(doses_mg) != len(responses_pct):
            raise ValueError("doses_mg and responses_pct must be the same length")
        self.compound_name = compound_name
        self.doses_mg = doses_mg
        self.responses_pct = responses_pct

    def compute_statistics(self) -> dict[str, float]:
        if not self.responses_pct:
            return {"mean_response": 0.0, "max_response": 0.0, "min_response": 0.0}
        return {
            "mean_response": sum(self.responses_pct) / len(self.responses_pct),
            "max_response": max(self.responses_pct),
            "min_response": min(self.responses_pct),
        }

    def find_effective_dose(self, target_response_pct: float) -> float | None:
        for dose, response in zip(self.doses_mg, self.responses_pct):
            if response >= target_response_pct:
                return dose
        return None

    def build_report(self, target_response_pct: float) -> dict[str, object]:
        statistics = self.compute_statistics()
        effective_dose = self.find_effective_dose(target_response_pct)
        return {
            "compound": self.compound_name,
            "statistics": statistics,
            "effective_dose_mg": effective_dose,
        }

    @staticmethod
    def run() -> None:
        pipeline = IndustryReturnValues(
            compound_name="Compound-441",
            doses_mg=[1.0, 5.0, 10.0, 20.0],
            responses_pct=[5.0, 22.0, 48.0, 81.0],
        )
        report = pipeline.build_report(target_response_pct=50.0)
        print("Industry - report:", report)


if __name__ == "__main__":
    UniversityReturnValues.run()
    InterviewReturnValues.run()
    IndustryReturnValues.run()
