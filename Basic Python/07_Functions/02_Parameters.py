class UniversityParameters:
    def __init__(self, plant_species: str) -> None:
        self.plant_species = plant_species

    def compute_leaf_area(self, length_cm: float, width_cm: float) -> float:
        return length_cm * width_cm * 0.75

    def classify_growth_stage(self, height_cm: float, leaf_count: int) -> str:
        if height_cm < 10 and leaf_count < 4:
            return "seedling"
        if height_cm < 50:
            return "vegetative"
        return "mature"

    @staticmethod
    def run() -> None:
        study = UniversityParameters("Arabidopsis thaliana")
        area = study.compute_leaf_area(length_cm=5.0, width_cm=2.5)
        stage = study.classify_growth_stage(height_cm=45.0, leaf_count=12)
        print("University - leaf area:", area)
        print("University - growth stage:", stage)


class InterviewParameters:
    def __init__(self) -> None:
        self.enzyme_records: list[dict] = []

    def record_enzyme_activity(
        self, enzyme_name: str, substrate_concentration: float, reaction_rate: float
    ) -> None:
        self.enzyme_records.append(
            {
                "enzyme_name": enzyme_name,
                "substrate_concentration": substrate_concentration,
                "reaction_rate": reaction_rate,
            }
        )

    def find_max_rate(self) -> dict | None:
        if not self.enzyme_records:
            return None
        return max(self.enzyme_records, key=lambda record: record["reaction_rate"])

    def average_rate_for_enzyme(self, enzyme_name: str) -> float:
        matching_rates = [
            record["reaction_rate"]
            for record in self.enzyme_records
            if record["enzyme_name"] == enzyme_name
        ]
        if not matching_rates:
            return 0.0
        return sum(matching_rates) / len(matching_rates)

    @staticmethod
    def run() -> None:
        lab = InterviewParameters()
        lab.record_enzyme_activity("catalase", 0.5, 12.3)
        lab.record_enzyme_activity("catalase", 1.0, 18.9)
        lab.record_enzyme_activity("amylase", 0.5, 6.1)

        print("Interview - max rate record:", lab.find_max_rate())
        print("Interview - catalase average:", lab.average_rate_for_enzyme("catalase"))
        print("Interview - unknown enzyme average:", lab.average_rate_for_enzyme("lipase"))


class IndustryParameters:
    """Computes molecular descriptor scores for drug candidate screening."""

    def __init__(self, candidate_name: str) -> None:
        if not candidate_name.strip():
            raise ValueError("candidate_name must not be empty")
        self.candidate_name = candidate_name

    def compute_drug_likeness_score(
        self,
        molecular_weight: float,
        log_p: float,
        hydrogen_bond_donors: int,
        hydrogen_bond_acceptors: int,
    ) -> float:
        penalties = 0.0
        if molecular_weight > 500:
            penalties += 1.0
        if log_p > 5:
            penalties += 1.0
        if hydrogen_bond_donors > 5:
            penalties += 1.0
        if hydrogen_bond_acceptors > 10:
            penalties += 1.0
        return max(0.0, 4.0 - penalties)

    def evaluate_candidate(
        self,
        molecular_weight: float,
        log_p: float,
        hydrogen_bond_donors: int,
        hydrogen_bond_acceptors: int,
    ) -> dict[str, float | str]:
        score = self.compute_drug_likeness_score(
            molecular_weight, log_p, hydrogen_bond_donors, hydrogen_bond_acceptors
        )
        verdict = "promising" if score >= 3.0 else "needs review"
        return {"candidate": self.candidate_name, "score": score, "verdict": verdict}

    @staticmethod
    def run() -> None:
        screener = IndustryParameters("Compound-441")
        result = screener.evaluate_candidate(
            molecular_weight=320.5,
            log_p=2.1,
            hydrogen_bond_donors=2,
            hydrogen_bond_acceptors=4,
        )
        print("Industry - evaluation:", result)


if __name__ == "__main__":
    UniversityParameters.run()
    InterviewParameters.run()
    IndustryParameters.run()
