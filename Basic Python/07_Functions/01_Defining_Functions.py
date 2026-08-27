class UniversityDefiningFunctions:
    def __init__(self, plant_records: list[dict]) -> None:
        self.plant_records = plant_records

    def count_samples(self) -> int:
        return len(self.plant_records)

    def average_height_cm(self) -> float:
        if not self.plant_records:
            return 0.0
        total = sum(record["height_cm"] for record in self.plant_records)
        return total / len(self.plant_records)

    def describe_sample(self, index: int) -> str:
        record = self.plant_records[index]
        return f"{record['species']} - {record['height_cm']} cm"

    @staticmethod
    def run() -> None:
        plant_records = [
            {"species": "Zea mays", "height_cm": 152.0},
            {"species": "Arabidopsis thaliana", "height_cm": 12.5},
            {"species": "Glycine max", "height_cm": 68.3},
        ]
        analyzer = UniversityDefiningFunctions(plant_records)
        print("University - sample count:", analyzer.count_samples())
        print("University - average height:", analyzer.average_height_cm())
        print("University - description:", analyzer.describe_sample(0))


class InterviewDefiningFunctions:
    def __init__(self, plant_samples: list[dict]) -> None:
        self.plant_samples = plant_samples

    def tallest_sample(self) -> dict | None:
        if not self.plant_samples:
            return None
        tallest = self.plant_samples[0]
        for sample in self.plant_samples[1:]:
            if sample["height_cm"] > tallest["height_cm"]:
                tallest = sample
        return tallest

    def species_above_threshold(self, threshold_cm: float) -> list[str]:
        result: list[str] = []
        for sample in self.plant_samples:
            if sample["height_cm"] > threshold_cm:
                result.append(sample["species"])
        return result

    def handle_empty_dataset(self) -> str:
        if not self.plant_samples:
            return "No samples available for analysis."
        return f"{len(self.plant_samples)} samples available."

    @staticmethod
    def run() -> None:
        plant_samples = [
            {"species": "Zea mays", "height_cm": 152.0},
            {"species": "Helianthus annuus", "height_cm": 210.7},
            {"species": "Arabidopsis thaliana", "height_cm": 12.5},
        ]
        solver = InterviewDefiningFunctions(plant_samples)
        print("Interview - tallest sample:", solver.tallest_sample())
        print("Interview - above 50cm:", solver.species_above_threshold(50.0))

        empty_solver = InterviewDefiningFunctions([])
        print("Interview - empty check:", empty_solver.handle_empty_dataset())
        print("Interview - empty tallest:", empty_solver.tallest_sample())


class IndustryDefiningFunctions:
    """Encapsulates reusable operations for a plant phenotyping pipeline."""

    def __init__(self, plant_records: list[dict]) -> None:
        self._validate_records(plant_records)
        self.plant_records = plant_records

    @staticmethod
    def _validate_records(records: list[dict]) -> None:
        required_keys = {"species", "height_cm"}
        for record in records:
            missing = required_keys - record.keys()
            if missing:
                raise ValueError(f"Record missing required keys: {missing}")
            if record["height_cm"] < 0:
                raise ValueError("height_cm cannot be negative")

    def summarize_by_species(self) -> dict[str, float]:
        totals: dict[str, list[float]] = {}
        for record in self.plant_records:
            totals.setdefault(record["species"], []).append(record["height_cm"])
        return {
            species: sum(heights) / len(heights)
            for species, heights in totals.items()
        }

    def generate_report(self) -> str:
        summary = self.summarize_by_species()
        lines = [f"{species}: {avg_height:.2f} cm avg" for species, avg_height in summary.items()]
        return "\n".join(lines)

    @staticmethod
    def run() -> None:
        plant_records = [
            {"species": "Zea mays", "height_cm": 150.0},
            {"species": "Zea mays", "height_cm": 158.0},
            {"species": "Glycine max", "height_cm": 65.0},
        ]
        pipeline = IndustryDefiningFunctions(plant_records)
        print("Industry - summary:", pipeline.summarize_by_species())
        print("Industry - report:")
        print(pipeline.generate_report())


if __name__ == "__main__":
    UniversityDefiningFunctions.run()
    InterviewDefiningFunctions.run()
    IndustryDefiningFunctions.run()
