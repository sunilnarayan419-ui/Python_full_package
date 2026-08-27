class UniversityLambdaFunctions:
    def __init__(self, plant_records: list[dict]) -> None:
        self.plant_records = plant_records

    def sort_by_height(self) -> list[dict]:
        return sorted(self.plant_records, key=lambda record: record["height_cm"])

    def filter_tall_plants(self, threshold_cm: float) -> list[dict]:
        return list(filter(lambda record: record["height_cm"] > threshold_cm, self.plant_records))

    @staticmethod
    def run() -> None:
        plant_records = [
            {"species": "Zea mays", "height_cm": 150.0},
            {"species": "Arabidopsis thaliana", "height_cm": 12.5},
            {"species": "Helianthus annuus", "height_cm": 210.0},
        ]
        catalog = UniversityLambdaFunctions(plant_records)
        sorted_records = catalog.sort_by_height()
        tall_records = catalog.filter_tall_plants(100.0)
        print("University - sorted by height:", sorted_records)
        print("University - tall plants:", tall_records)


class InterviewLambdaFunctions:
    def __init__(self, molecular_weights: list[float]) -> None:
        self.molecular_weights = molecular_weights

    def convert_to_kilodaltons(self) -> list[float]:
        return list(map(lambda weight: weight / 1000, self.molecular_weights))

    def rank_compounds(self, compounds: list[dict]) -> list[dict]:
        if not compounds:
            return []
        return sorted(compounds, key=lambda compound: (-compound["score"], compound["name"]))

    @staticmethod
    def run() -> None:
        weights = InterviewLambdaFunctions([342.1, 498.7, 120.0])
        kilodaltons = weights.convert_to_kilodaltons()
        print("Interview - kilodaltons:", kilodaltons)

        compounds = [
            {"name": "Compound-A", "score": 7.5},
            {"name": "Compound-B", "score": 9.1},
            {"name": "Compound-C", "score": 9.1},
        ]
        ranked = weights.rank_compounds(compounds)
        print("Interview - ranked compounds:", ranked)

        empty_ranked = weights.rank_compounds([])
        print("Interview - empty ranking:", empty_ranked)


class IndustryLambdaFunctions:
    """Applies configurable scoring and sorting strategies to drug candidates."""

    def __init__(self, candidates: list[dict]) -> None:
        self.candidates = candidates

    def rank_by_criterion(self, key_function) -> list[dict]:
        return sorted(self.candidates, key=key_function, reverse=True)

    def top_candidates_by_efficacy(self, count: int) -> list[dict]:
        ranked = self.rank_by_criterion(lambda candidate: candidate["efficacy"])
        return ranked[:count]

    def filter_safe_candidates(self, max_toxicity: float) -> list[dict]:
        return list(filter(lambda candidate: candidate["toxicity"] <= max_toxicity, self.candidates))

    @staticmethod
    def run() -> None:
        candidates = [
            {"name": "Compound-441", "efficacy": 0.82, "toxicity": 0.15},
            {"name": "Compound-902", "efficacy": 0.91, "toxicity": 0.35},
            {"name": "Compound-118", "efficacy": 0.76, "toxicity": 0.05},
        ]
        screener = IndustryLambdaFunctions(candidates)
        top_two = screener.top_candidates_by_efficacy(2)
        safe_candidates = screener.filter_safe_candidates(0.2)
        print("Industry - top efficacy candidates:", top_two)
        print("Industry - safe candidates:", safe_candidates)


if __name__ == "__main__":
    UniversityLambdaFunctions.run()
    InterviewLambdaFunctions.run()
    IndustryLambdaFunctions.run()
