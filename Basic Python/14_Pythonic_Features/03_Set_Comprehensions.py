"""Set comprehensions demonstrated through species and mutation data."""


class UniversitySetComprehensions:
    """Teach the fundamental syntax of building sets from iterables."""

    def __init__(self, species_observations: list[str]) -> None:
        self.species_observations = species_observations

    def unique_species(self) -> set[str]:
        """Extract the unique species observed across all samples."""
        return {species for species in self.species_observations}

    @staticmethod
    def run() -> None:
        observations = [
            "Arabidopsis",
            "Oryza sativa",
            "Arabidopsis",
            "Zea mays",
            "Oryza sativa",
        ]

        processor = UniversitySetComprehensions(observations)
        species = processor.unique_species()

        print(f"Observed species (raw list): {observations}")
        print(f"Unique species (set): {species}")


class InterviewSetComprehensions:
    """Solve a practical mutation-deduplication problem with edge cases."""

    def __init__(self, mutation_records: list[str]) -> None:
        self.mutation_records = mutation_records

    def unique_valid_mutations(self) -> set[str]:
        """Return unique, non-empty, uppercase-normalized mutation codes.

        Handles an empty record list and filters out blank entries.
        """
        if not self.mutation_records:
            return set()

        return {
            record.strip().upper()
            for record in self.mutation_records
            if record and record.strip()
        }

    def mutations_shared_with(self, other_mutations: set[str]) -> set[str]:
        """Find mutations shared between this sample and another sample."""
        current = self.unique_valid_mutations()
        return {mutation for mutation in current if mutation in other_mutations}

    @staticmethod
    def run() -> None:
        raw_mutations = ["p.V600E", "  p.v600e", "", "p.G12D", "p.G12D", "   "]
        empty_mutations: list[str] = []

        case_one = InterviewSetComprehensions(raw_mutations)
        case_two = InterviewSetComprehensions(empty_mutations)

        print(f"Unique valid mutations: {case_one.unique_valid_mutations()}")
        print(f"Empty record result: {case_two.unique_valid_mutations()}")
        print(
            "Shared mutations: "
            f"{case_one.mutations_shared_with({'P.G12D', 'P.G13D'})}"
        )


class IndustrySetComprehensions:
    """Normalize and deduplicate a biological dataset for downstream use."""

    def __init__(self, gene_identifiers: list[str]) -> None:
        self.gene_identifiers = gene_identifiers

    def normalized_unique_ids(self) -> set[str]:
        """Standardize gene identifiers to a consistent uppercase format."""
        return {gene_id.strip().upper() for gene_id in self.gene_identifiers if gene_id}

    def duplicate_count(self) -> int:
        """Report how many redundant identifiers exist in the raw dataset.

        A list is used here deliberately to preserve total count, while the
        set comprehension isolates the unique identifiers for comparison.
        """
        unique_ids = self.normalized_unique_ids()
        raw_count = len([gene_id for gene_id in self.gene_identifiers if gene_id])
        return raw_count - len(unique_ids)

    @staticmethod
    def run() -> None:
        gene_ids = ["ENSG001", "ensg001", "ENSG002", "ENSG003", "ensg002", ""]

        deduplicator = IndustrySetComprehensions(gene_ids)
        unique_ids = deduplicator.normalized_unique_ids()
        duplicates = deduplicator.duplicate_count()

        print(f"Normalized unique gene IDs: {unique_ids}")
        print(f"Duplicate identifiers removed: {duplicates}")


if __name__ == "__main__":
    UniversitySetComprehensions.run()
    InterviewSetComprehensions.run()
    IndustrySetComprehensions.run()
