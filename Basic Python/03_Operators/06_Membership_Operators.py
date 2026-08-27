"""Membership operators in genomic data validation."""


class BaseMembership:
    DNA_BASES = "ACGT"

    def __init__(self, base: str) -> None:
        self.base = base

    def is_dna_base(self) -> bool:
        return self.base in self.DNA_BASES


class SequenceValidator:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence.upper()

    def has_only_dna(self) -> bool:
        return all(b in "ACGT" for b in self.sequence)


class ChromosomeLookup:
    VALID = {"Chr1", "Chr2", "Chr3", "ChrX"}

    def __init__(self, name: str) -> None:
        self.name = name

    def is_known(self) -> bool:
        return self.name in self.VALID

    def is_unknown(self) -> bool:
        return self.name not in self.VALID


if __name__ == "__main__":
    print(BaseMembership("A").is_dna_base())

    print(SequenceValidator("ATGCAT").has_only_dna())

    c = ChromosomeLookup("Chr1")
    print(c.is_known())
    print(c.is_unknown())
