"""09_Sets.py — Python sets through plant science and genomics."""
from __future__ import annotations


class PlantSpeciesSetUniversity:
    """University level: basic set creation and unique elements."""

    def __init__(self, species_list: list[str]) -> None:
        self.species: set[str] = set(species_list)

    def display(self) -> None:
        print(f"University — Unique species ({len(self.species)}):")
        for sp in sorted(self.species):
            print(f"  - {sp}")

    @staticmethod
    def run() -> None:
        raw = ["Wheat", "Rice", "Maize", "Wheat", "Rice", "Barley", "Wheat"]
        demo = PlantSpeciesSetUniversity(raw)
        demo.display()


class GeneIdentifierDeduplicatorInterview:
    """Interview level: detect and remove duplicates from gene identifiers."""

    def __init__(self, gene_ids: list[str]) -> None:
        self.gene_ids = gene_ids

    def unique_ids(self) -> set[str]:
        return set(self.gene_ids)

    def duplicates(self) -> set[str]:
        seen: set[str] = set()
        dupes: set[str] = set()
        for gid in self.gene_ids:
            if gid in seen:
                dupes.add(gid)
            seen.add(gid)
        return dupes

    @staticmethod
    def run() -> None:
        ids = ["AT1G01010", "AT1G01020", "AT1G01010", "AT1G01030", "AT1G01020", "AT1G01040"]
        demo = GeneIdentifierDeduplicatorInterview(ids)
        print("Interview — Gene ID analysis:")
        print(f"  Unique IDs: {sorted(demo.unique_ids())}")
        print(f"  Duplicates: {sorted(demo.duplicates())}")


class NucleotideValidatorIndustry:
    """Industry level: efficient uniqueness and membership validation."""

    VALID_BASES: set[str] = {"A", "T", "G", "C", "N"}

    def __init__(self, sequences: list[str]) -> None:
        self.sequences = sequences

    def validate(self) -> list[tuple[str, bool, set[str]]]:
        results: list[tuple[str, bool, set[str]]] = []
        for seq in self.sequences:
            bases = set(seq.upper())
            is_valid = bases <= self.VALID_BASES
            invalid = bases - self.VALID_BASES
            results.append((seq, is_valid, invalid))
        return results

    @staticmethod
    def run() -> None:
        sequences = ["ATGCGTAC", "ATGXCG", "CGGCGG", "ATGC@T"]
        validator = NucleotideValidatorIndustry(sequences)
        print("Industry — Sequence validation:")
        for seq, valid, invalid in validator.validate():
            status = "valid" if valid else f"invalid ({invalid})"
            print(f"  {seq}: {status}")


if __name__ == "__main__":
    PlantSpeciesSetUniversity.run()
    print()
    GeneIdentifierDeduplicatorInterview.run()
    print()
    NucleotideValidatorIndustry.run()