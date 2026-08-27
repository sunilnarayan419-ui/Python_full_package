"""Demonstrations of the built-in hash() function using immutable biological identifiers.

Python hash values are not guaranteed stable across processes and must never
be used as persistent database identifiers. These examples demonstrate
hashability and behavior without hard-coding expected hash numbers.
"""


class UniversityHash:
    """Teach the fundamental behavior of hash() on hashable identifiers."""

    def __init__(self, sample_id: str) -> None:
        self.sample_id = sample_id

    def is_hashable(self) -> bool:
        try:
            hash(self.sample_id)
            return True
        except TypeError:
            return False

    @staticmethod
    def run() -> None:
        processor = UniversityHash(sample_id="P001")
        print(f"sample_id is hashable: {processor.is_hashable()}")
        print(f"Equal strings produce equal hashes: {hash('P001') == hash('P001')}")


class InterviewHash:
    """Demonstrate hashability rules for common biological data structures."""

    @staticmethod
    def try_hash(value: object) -> bool:
        """Return True if the value is hashable, False otherwise."""
        try:
            hash(value)
            return True
        except TypeError:
            return False

    @staticmethod
    def run() -> None:
        gene_name = "GENE1"
        expression_values = (4.2, 9.1, 1.3)  # tuple: hashable if contents are
        measurement_list = [4.2, 9.1, 1.3]  # list: never hashable
        sample_record = {"sample_id": "P001"}  # dict: never hashable

        print(f"str 'GENE1' hashable: {InterviewHash.try_hash(gene_name)}")
        print(f"tuple of floats hashable: {InterviewHash.try_hash(expression_values)}")
        print(f"list of floats hashable: {InterviewHash.try_hash(measurement_list)}")
        print(f"dict record hashable: {InterviewHash.try_hash(sample_record)}")


class IndustryHash:
    """Safe use of immutable identifiers in lookup structures (dict/set)."""

    def __init__(self) -> None:
        self.sample_index: dict[str, dict[str, object]] = {}

    def register_sample(self, sample_id: str, data: dict[str, object]) -> None:
        """Use a hashable, immutable sample_id string as the lookup key.

        This works because hash() is consistent for equal immutable
        identifiers within a single program run, enabling O(1) dict lookups.
        """
        self.sample_index[sample_id] = data

    def lookup_sample(self, sample_id: str) -> dict[str, object] | None:
        return self.sample_index.get(sample_id)

    def unique_species(self, species_list: list[str]) -> set[str]:
        """Use hashable strings in a set to efficiently deduplicate species."""
        return set(species_list)

    @staticmethod
    def run() -> None:
        registry = IndustryHash()
        registry.register_sample("P001", {"species": "Wheat", "height": 58.2})
        registry.register_sample("P002", {"species": "Rice", "height": 61.4})

        print(f"Lookup P001: {registry.lookup_sample('P001')}")
        print(f"Lookup missing sample: {registry.lookup_sample('P999')}")

        species_observed = ["Wheat", "Rice", "Wheat", "Maize", "Rice"]
        print(f"Unique species observed: {registry.unique_species(species_observed)}")


if __name__ == "__main__":
    UniversityHash.run()
    InterviewHash.run()
    IndustryHash.run()
