"""Using f-strings for formatted scientific/genomic output."""


class FStringUniversity:
    def __init__(self, name: str, value: float) -> None:
        self.name = name
        self.value = value

    def get_label(self) -> str:
        return f"{self.name}={self.value}"


class FStringInterview:
    def __init__(self, name: str, values: list[float]) -> None:
        self.name = name
        self.values = values

    def summarize(self) -> str:
        if not self.values:
            return f"No {self.name} values"
        mean = sum(self.values) / len(self.values)
        return f"{self.name}: n={len(self.values)}, mean={mean:.2f}"


class FStringIndustry:
    def __init__(self, sample_id: str, species: str, gc: float, length: int) -> None:
        self.sample_id = sample_id
        self.species = species
        self.gc = gc
        self.length = length

    def report(self) -> str:
        return (
            f"[{self.sample_id}] {self.species:<10} "
            f"len={self.length:>6,} GC={self.gc:.2%}"
        )


if __name__ == "__main__":
    u = FStringUniversity(name="Height_cm", value=12.5)
    print(u.get_label())

    i = FStringInterview(name="Height", values=[10.0, 11.5, 12.0])
    print(i.summarize())

    ind = FStringIndustry(sample_id="S001", species="Wheat", gc=0.45, length=1234)
    print(ind.report())
