class UniversityPositionalArguments:
    def __init__(self, plant_species: str) -> None:
        self.plant_species = plant_species

    def compute_biomass_index(self, height_cm: float, leaf_count: int, stem_diameter_mm: float) -> float:
        return height_cm * 0.4 + leaf_count * 1.5 + stem_diameter_mm * 0.2

    @staticmethod
    def run() -> None:
        plant = UniversityPositionalArguments("Zea mays")
        index = plant.compute_biomass_index(120.0, 14, 18.5)
        print("University - biomass index:", index)


class InterviewPositionalArguments:
    def __init__(self) -> None:
        self.sequences: list[str] = []

    def add_sequence(self, sequence: str) -> None:
        self.sequences.append(sequence)

    def align_pair(self, sequence_a: str, sequence_b: str) -> int:
        matches = 0
        shortest_length = min(len(sequence_a), len(sequence_b))
        for index in range(shortest_length):
            if sequence_a[index] == sequence_b[index]:
                matches += 1
        return matches

    @staticmethod
    def run() -> None:
        aligner = InterviewPositionalArguments()
        aligner.add_sequence("ATCGGGA")
        aligner.add_sequence("ATCGTGA")

        correct_order_matches = aligner.align_pair("ATCGGGA", "ATCGTGA")
        print("Interview - matches (correct order):", correct_order_matches)

        # Demonstrating a common positional-argument mistake: swapping arguments
        # silently changes which value represents "reference" vs "candidate".
        # This is safe here because the function is symmetric, but it is called
        # out explicitly to show why argument order matters.
        swapped_order_matches = aligner.align_pair("ATCGTGA", "ATCGGGA")
        print("Interview - matches (swapped order, same result here):", swapped_order_matches)

        mismatched_lengths = aligner.align_pair("ATCG", "ATCGGGA")
        print("Interview - matches (different lengths):", mismatched_lengths)


class IndustryPositionalArguments:
    """Performs unit-aware conversions for laboratory measurement pipelines."""

    def __init__(self, lab_name: str) -> None:
        self.lab_name = lab_name

    def convert_concentration(
        self, value: float, from_unit: str, to_unit: str
    ) -> float:
        conversion_to_molar = {
            "M": 1.0,
            "mM": 1e-3,
            "uM": 1e-6,
            "nM": 1e-9,
        }
        if from_unit not in conversion_to_molar or to_unit not in conversion_to_molar:
            raise ValueError(f"Unsupported unit conversion: {from_unit} -> {to_unit}")
        value_in_molar = value * conversion_to_molar[from_unit]
        return value_in_molar / conversion_to_molar[to_unit]

    def build_conversion_record(
        self, value: float, from_unit: str, to_unit: str
    ) -> dict[str, object]:
        converted_value = self.convert_concentration(value, from_unit, to_unit)
        return {
            "lab": self.lab_name,
            "original": f"{value} {from_unit}",
            "converted": f"{converted_value} {to_unit}",
        }

    @staticmethod
    def run() -> None:
        converter = IndustryPositionalArguments("Biochemistry Core Lab")
        record = converter.build_conversion_record(5.0, "mM", "uM")
        print("Industry - conversion record:", record)


if __name__ == "__main__":
    UniversityPositionalArguments.run()
    InterviewPositionalArguments.run()
    IndustryPositionalArguments.run()
