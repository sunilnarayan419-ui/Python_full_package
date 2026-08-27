"""Indexing DNA/RNA sequences."""


class StringIndexingUniversity:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def first_base(self) -> str:
        return self.sequence[0]


class StringIndexingInterview:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def last_base(self) -> str:
        return self.sequence[-1]

    def at(self, i: int) -> str:
        return self.sequence[i]


class StringIndexingIndustry:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def codon_at(self, start: int) -> str:
        if start + 3 > len(self.sequence):
            return ""
        return self.sequence[start:start + 3]


if __name__ == "__main__":
    print(StringIndexingUniversity("ATGC").first_base())

    seq = StringIndexingInterview("ATGCAT")
    print(seq.last_base())
    print(seq.at(2))

    print(StringIndexingIndustry("ATGCATGC").codon_at(1))
