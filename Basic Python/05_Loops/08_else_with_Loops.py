"""for/while loop else clause in scientific search."""


class PatternSearcher:
    def __init__(self, sequence: str, pattern: str) -> None:
        self.sequence = sequence.upper()
        self.pattern = pattern.upper()

    def find(self) -> str:
        for i in range(len(self.sequence) - len(self.pattern) + 1):
            if self.sequence[i:i + len(self.pattern)] == self.pattern:
                return f"found at {i}"
        else:
            return "not found"


class SampleLookup:
    def __init__(self, sample_ids: list[str], target: str) -> None:
        self.sample_ids = sample_ids
        self.target = target

    def locate(self) -> str:
        for s in self.sample_ids:
            if s == self.target:
                return f"located {s}"
            if len(s) > len(self.target):
                break
        else:
            return "missing from batch"
        return "search terminated early"


class QualityBatchValidator:
    def __init__(self, qualities: list[float], min_quality: float) -> None:
        self.qualities = qualities
        self.min_quality = min_quality

    def validate(self) -> str:
        for q in self.qualities:
            if q < self.min_quality:
                break
        else:
            return "all_passed"
        return "rejected"


if __name__ == "__main__":
    print(PatternSearcher("ATGCAT", "GC").find())

    print(SampleLookup(["S1", "S2"], "S3").locate())

    print(QualityBatchValidator([35.0, 32.0, 30.0], 30.0).validate())
    print(QualityBatchValidator([35.0, 25.0], 30.0).validate())
