"""Integer operations in plant/genomic data."""


class IntegerUniversity:
    def __init__(self, count: int) -> None:
        self.count = count

    def double(self) -> int:
        return self.count * 2


class IntegerInterview:
    def __init__(self, reads: list[int]) -> None:
        self.reads = reads

    def count_above(self, threshold: int) -> int:
        return sum(1 for r in self.reads if r > threshold)


class IntegerIndustry:
    def __init__(self, total_reads: int) -> None:
        self.total_reads = total_reads

    def allocate(self, lanes: int) -> int:
        if lanes <= 0:
            raise ValueError("lanes must be positive")
        return self.total_reads // lanes

    def remainder(self, lanes: int) -> int:
        return self.total_reads % lanes


if __name__ == "__main__":
    print(IntegerUniversity(21).double())

    print(IntegerInterview([100, 200, 300]).count_above(150))

    alloc = IntegerIndustry(1000)
    print(alloc.allocate(7))
    print(alloc.remainder(7))
