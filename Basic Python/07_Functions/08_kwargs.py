class UniversityKwargs:
    def __init__(self, plant_species: str) -> None:
        self.plant_species = plant_species

    def record_conditions(self, **conditions: float) -> str:
        parts = [f"{key}={value}" for key, value in conditions.items()]
        return f"{self.plant_species}: " + ", ".join(parts)

    @staticmethod
    def run() -> None:
        plant = UniversityKwargs("Orchid")
        entry = plant.record_conditions(temperature_c=22.0, humidity_pct=65.0, light_lux=8000.0)
        print("University - conditions entry:", entry)


class InterviewKwargs:
    def __init__(self) -> None:
        self.compound_metadata: dict[str, dict] = {}

    def register_compound(self, compound_id: str, **properties: object) -> None:
        self.compound_metadata[compound_id] = dict(properties)

    def get_property(self, compound_id: str, property_name: str) -> object | None:
        compound = self.compound_metadata.get(compound_id)
        if compound is None:
            return None
        return compound.get(property_name)

    @staticmethod
    def run() -> None:
        registry = InterviewKwargs()
        registry.register_compound(
            "CMP-101",
            molecular_weight=342.1,
            solubility="high",
            toxicity_flag=False,
        )
        registry.register_compound("CMP-102", molecular_weight=498.7)

        print("Interview - CMP-101 solubility:", registry.get_property("CMP-101", "solubility"))
        print("Interview - CMP-102 solubility:", registry.get_property("CMP-102", "solubility"))
        print("Interview - unknown compound:", registry.get_property("CMP-999", "solubility"))


class IndustryKwargs:
    """Converts flexible keyword metadata into a structured lab report."""

    REQUIRED_FIELDS = {"sample_id", "collection_date"}

    def __init__(self, facility_name: str) -> None:
        if not facility_name.strip():
            raise ValueError("facility_name must not be empty")
        self.facility_name = facility_name

    def build_sample_report(self, **metadata: object) -> dict[str, object]:
        missing_fields = self.REQUIRED_FIELDS - metadata.keys()
        if missing_fields:
            raise ValueError(f"Missing required metadata fields: {missing_fields}")

        report: dict[str, object] = {"facility": self.facility_name}
        report.update(metadata)
        return report

    @staticmethod
    def run() -> None:
        reporter = IndustryKwargs("Central Sequencing Facility")
        report = reporter.build_sample_report(
            sample_id="SMP-2201",
            collection_date="2026-03-14",
            species="Oryza sativa",
            tissue_type="leaf",
        )
        print("Industry - report:", report)

        try:
            reporter.build_sample_report(species="Oryza sativa")
        except ValueError as error:
            print("Industry - validation error:", error)


if __name__ == "__main__":
    UniversityKwargs.run()
    InterviewKwargs.run()
    IndustryKwargs.run()
