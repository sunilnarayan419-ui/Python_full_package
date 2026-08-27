"""Demonstrations of the built-in enumerate() function using sample/observation data."""


class UniversityEnumerate:
    """Teach the fundamental behavior of enumerate() for index + value iteration."""

    def __init__(self, species_list: list[str]) -> None:
        self.species_list = species_list

    def numbered_species(self) -> list[str]:
        return [f"{index}: {species}" for index, species in enumerate(self.species_list)]

    @staticmethod
    def run() -> None:
        species_list = ["Wheat", "Rice", "Maize"]

        processor = UniversityEnumerate(species_list)
        for line in processor.numbered_species():
            print(line)


class InterviewEnumerate:
    """Use enumerate() with start= for realistic biological sample numbering."""

    def __init__(self, sample_names: list[str], starting_sample_number: int = 1) -> None:
        self.sample_names = sample_names
        self.starting_sample_number = starting_sample_number

    def sample_id_mapping(self) -> dict[int, str]:
        """Avoid manual counters entirely; enumerate() supplies the numbering."""
        return {
            number: name
            for number, name in enumerate(self.sample_names, start=self.starting_sample_number)
        }

    @staticmethod
    def run() -> None:
        case_one = InterviewEnumerate(["Leaf-A", "Leaf-B", "Leaf-C"], starting_sample_number=1001)
        case_two = InterviewEnumerate([], starting_sample_number=1)

        print(f"Sample ID mapping: {case_one.sample_id_mapping()}")
        print(f"Sample ID mapping (empty): {case_two.sample_id_mapping()}")


class IndustryEnumerate:
    """Generate structured, numbered reports from experimental observations."""

    def __init__(self, observations: list[dict[str, object]]) -> None:
        self.observations = observations

    def numbered_report_lines(self) -> list[str]:
        lines: list[str] = []
        for row_number, observation in enumerate(self.observations, start=1):
            gene = observation["gene"]
            expression = observation["expression_level"]
            lines.append(f"Row {row_number}: {gene} -> {expression}")
        return lines

    @staticmethod
    def run() -> None:
        observations: list[dict[str, object]] = [
            {"gene": "GENE1", "expression_level": 4.2},
            {"gene": "GENE2", "expression_level": 9.1},
            {"gene": "GENE3", "expression_level": 1.3},
        ]

        reporter = IndustryEnumerate(observations)
        for line in reporter.numbered_report_lines():
            print(line)


if __name__ == "__main__":
    UniversityEnumerate.run()
    InterviewEnumerate.run()
    IndustryEnumerate.run()
