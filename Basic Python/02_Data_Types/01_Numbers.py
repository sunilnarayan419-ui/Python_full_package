"""Numbers in Python with plant science examples."""


class NumberUniversity:
    def __init__(self, a: int, b: float, c: complex) -> None:
        self.a = a
        self.b = b
        self.c = c

    def add_all(self) -> complex:
        return self.a + self.b + self.c


class NumberInterview:
    def __init__(self, samples: list[int | float]) -> None:
        self.samples = samples

    def total(self) -> int | float:
        return sum(self.samples)

    def average(self) -> float:
        if not self.samples:
            return 0.0
        return float(sum(self.samples)) / len(self.samples)


class NumberIndustry:
    def __init__(self, chromosome_lengths: dict[str, int]) -> None:
        self.chromosome_lengths = chromosome_lengths

    def total_length(self) -> int:
        return sum(self.chromosome_lengths.values())

    def is_within_range(self, chromosome: str, min_len: int, max_len: int) -> bool:
        length = self.chromosome_lengths.get(chromosome, 0)
        return min_len <= length <= max_len


if __name__ == "__main__":
    print(NumberUniversity(10, 2.5, 1 + 2j).add_all())

    counter = NumberInterview([12, 14, 16])
    print(counter.total())
    print(counter.average())

    lengths = NumberIndustry({"Chr1": 5000, "Chr2": 4000})
    print(lengths.total_length())
    print(lengths.is_within_range("Chr1", 1000, 6000))
