"""Boolean logic in biological data validation."""


class BooleanUniversity:
    def __init__(self, gc_content: float) -> None:
        self.gc_content = gc_content

    def is_valid(self) -> bool:
        return self.gc_content >= 0 and self.gc_content <= 1


class BooleanInterview:
    def __init__(self, gc_content: float, min_gc: float, max_gc: float) -> None:
        self.gc_content = gc_content
        self.min_gc = min_gc
        self.max_gc = max_gc

    def is_valid(self) -> bool:
        return self.min_gc <= self.gc_content <= self.max_gc

    def is_acceptable_for_pcr(self) -> bool:
        return 0.4 <= self.gc_content <= 0.6


class BooleanIndustry:
    def __init__(self, sequence: str, min_gc: float, max_gc: float) -> None:
        self.sequence = sequence.upper()
        self.min_gc = min_gc
        self.max_gc = max_gc

    def _gc_content(self) -> float:
        if not self.sequence:
            return 0.0
        gc = sum(1 for b in self.sequence if b in "GC")
        return gc / len(self.sequence)

    def is_valid(self) -> bool:
        gc = self._gc_content()
        return self.min_gc <= gc <= self.max_gc


if __name__ == "__main__":
    BooleanUniversity(gc_content=0.45).is_valid()
    BooleanInterview(gc_content=0.5, min_gc=0.3, max_gc=0.7).is_valid()
    BooleanIndustry(sequence="ATGCGC", min_gc=0.4, max_gc=0.6).is_valid()
