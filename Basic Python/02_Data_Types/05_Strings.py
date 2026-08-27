"""Basic strings and biological sequence processing."""


class StringUniversity:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def length(self) -> int:
        return len(self.sequence)


class StringInterview:
    def __init__(self, a: str, b: str) -> None:
        self.a = a
        self.b = b

    def concatenate(self) -> str:
        return self.a + self.b

    def are_equal(self) -> bool:
        return self.a == self.b


class StringIndustry:
    def __init__(self, sample_id: str, species: str, sequence: str) -> None:
        self.sample_id = sample_id
        self.species = species
        self.sequence = sequence

    def header(self) -> str:
        return f">{self.sample_id} {self.species}"


if __name__ == "__main__":
    print(StringUniversity("ATGC").length())

    s = StringInterview("ATGC", "ATGC")
    print(s.concatenate())
    print(s.are_equal())

    print(StringIndustry("S001", "Wheat", "ATGC").header())
