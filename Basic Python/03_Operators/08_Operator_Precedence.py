"""Operator precedence in scientific calculations."""


class ExpressionPrecedence:
    def __init__(self, a: int, b: int, c: int) -> None:
        self.a = a
        self.b = b
        self.c = c

    def ambiguous(self) -> int:
        return self.a + self.b * self.c

    def explicit(self) -> int:
        return self.a + (self.b * self.c)

    def with_parens(self) -> int:
        return (self.a + self.b) * self.c


class GenomicThresholdCheck:
    def __init__(self, value: float, baseline: float, tolerance: float) -> None:
        self.value = value
        self.baseline = baseline
        self.tolerance = tolerance

    def within_range_no_parens(self) -> bool:
        return self.baseline - self.tolerance < self.value < self.baseline + self.tolerance

    def within_range_explicit(self) -> bool:
        low = (self.baseline - self.tolerance)
        high = (self.baseline + self.tolerance)
        return low < self.value < high


class PhenotypeQC:
    def __init__(self, height: float, leaves: int, threshold: float) -> None:
        self.height = height
        self.leaves = leaves
        self.threshold = threshold

    def score(self) -> float:
        height_score = self.height / self.threshold
        leaf_score = self.leaves * 1.0
        return (height_score + leaf_score) / 2


if __name__ == "__main__":
    e = ExpressionPrecedence(2, 3, 4)
    print(e.ambiguous())
    print(e.explicit())
    print(e.with_parens())

    qc = GenomicThresholdCheck(value=10.5, baseline=10.0, tolerance=0.6)
    print(qc.within_range_explicit())

    p = PhenotypeQC(height=45.0, leaves=12, threshold=30.0)
    print(p.score())
