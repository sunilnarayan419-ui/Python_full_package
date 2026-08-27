"""Comparison operators in scientific data validation."""


class HeightThreshold:
    def __init__(self, height_cm: float, min_cm: float, max_cm: float) -> None:
        self.height_cm = height_cm
        self.min_cm = min_cm
        self.max_cm = max_cm

    def is_within(self) -> bool:
        return self.min_cm <= self.height_cm <= self.max_cm


class ExpressionComparator:
    def __init__(self, values: list[float], threshold: float) -> None:
        self.values = values
        self.threshold = threshold

    def above_threshold(self) -> list[float]:
        return [v for v in self.values if v > self.threshold]

    def is_significant(self, value: float) -> bool:
        return value != self.threshold and value >= self.threshold * 2


class QualityControlFilter:
    def __init__(self, min_quality: float, min_length: int) -> None:
        self.min_quality = min_quality
        self.min_length = min_length

    def passes(self, quality: float, length: int) -> bool:
        return quality >= self.min_quality and length >= self.min_length


if __name__ == "__main__":
    print(HeightThreshold(45.0, 30.0, 60.0).is_within())

    c = ExpressionComparator([1.2, 3.5, 0.4], threshold=1.0)
    print(c.above_threshold())

    qc = QualityControlFilter(min_quality=30.0, min_length=100)
    print(qc.passes(quality=35.0, length=150))
