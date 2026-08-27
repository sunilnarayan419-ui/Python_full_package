class UniversityKeywordArguments:
    def __init__(self, greenhouse_name: str) -> None:
        self.greenhouse_name = greenhouse_name

    def log_condition(self, temperature_c: float, humidity_pct: float, light_hours: float) -> str:
        return (
            f"{self.greenhouse_name}: temp={temperature_c}C, "
            f"humidity={humidity_pct}%, light={light_hours}h"
        )

    @staticmethod
    def run() -> None:
        greenhouse = UniversityKeywordArguments("Greenhouse-B")
        entry = greenhouse.log_condition(
            temperature_c=24.5, humidity_pct=60.0, light_hours=14.0
        )
        reordered_entry = greenhouse.log_condition(
            light_hours=12.0, temperature_c=22.0, humidity_pct=55.0
        )
        print("University - entry:", entry)
        print("University - reordered entry:", reordered_entry)


class InterviewKeywordArguments:
    def __init__(self) -> None:
        self.mutation_records: list[dict] = []

    def register_mutation(
        self, gene_name: str, position: int, original_base: str, mutated_base: str
    ) -> None:
        self.mutation_records.append(
            {
                "gene_name": gene_name,
                "position": position,
                "original_base": original_base,
                "mutated_base": mutated_base,
            }
        )

    def describe_mutation(self, gene_name: str) -> str | None:
        for record in self.mutation_records:
            if record["gene_name"] == gene_name:
                return (
                    f"{record['gene_name']} position {record['position']}: "
                    f"{record['original_base']}->{record['mutated_base']}"
                )
        return None

    @staticmethod
    def run() -> None:
        tracker = InterviewKeywordArguments()
        tracker.register_mutation(
            gene_name="BRCA1", position=185, original_base="A", mutated_base="G"
        )
        tracker.register_mutation(
            position=999,
            gene_name="TP53",
            mutated_base="T",
            original_base="C",
        )
        print("Interview - BRCA1:", tracker.describe_mutation("BRCA1"))
        print("Interview - TP53:", tracker.describe_mutation("TP53"))
        print("Interview - unknown gene:", tracker.describe_mutation("EGFR"))


class IndustryKeywordArguments:
    """Builds validated experiment configuration records for a lab pipeline."""

    def __init__(self, lab_name: str) -> None:
        if not lab_name.strip():
            raise ValueError("lab_name must not be empty")
        self.lab_name = lab_name

    def create_experiment_config(
        self,
        *,
        experiment_id: str,
        temperature_c: float,
        duration_hours: float,
        replicate_count: int = 3,
    ) -> dict[str, object]:
        if replicate_count < 1:
            raise ValueError("replicate_count must be at least 1")
        if duration_hours <= 0:
            raise ValueError("duration_hours must be positive")
        return {
            "lab": self.lab_name,
            "experiment_id": experiment_id,
            "temperature_c": temperature_c,
            "duration_hours": duration_hours,
            "replicate_count": replicate_count,
        }

    @staticmethod
    def run() -> None:
        configurator = IndustryKeywordArguments("Plant Physiology Lab")
        config = configurator.create_experiment_config(
            experiment_id="EXP-204",
            temperature_c=25.0,
            duration_hours=48.0,
            replicate_count=5,
        )
        print("Industry - config:", config)

        try:
            configurator.create_experiment_config(
                "EXP-205", temperature_c=25.0, duration_hours=24.0  # type: ignore[misc]
            )
        except TypeError as error:
            print("Industry - keyword-only enforcement caught:", error)


if __name__ == "__main__":
    UniversityKeywordArguments.run()
    InterviewKeywordArguments.run()
    IndustryKeywordArguments.run()
