"""Extracting sequence regions using slicing."""


class StringSlicingUniversity:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def first_three(self) -> str:
        return self.sequence[:3]


class StringSlicingInterview:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def reverse(self) -> str:
        return self.sequence[::-1]

    def without_last(self) -> str:
        return self.sequence[:-1]


class StringSlicingIndustry:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def extract_orf(self, start: int, length: int) -> str:
        return self.sequence[start:start + length]

    def three_prime_end(self, n: int) -> str:
        return self.sequence[-n:]


if __name__ == "__main__":
    print(StringSlicingUniversity("ATGCATGC").first_three())

    s = StringSlicingInterview("ATGCAT")
    print(s.reverse())
    print(s.without_last())

    ind = StringSlicingIndustry("ATGCATGCATGC")
    print(ind.extract_orf(0, 6))
    print(ind.three_prime_end(3))
