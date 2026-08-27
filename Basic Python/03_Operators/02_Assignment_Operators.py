"""Assignment operators for updating scientific measurements."""


class GrowthAccumulator:
    def __init__(self, height_cm: float) -> None:
        self.height_cm = height_cm

    def add_growth(self, growth: float) -> float:
        self.height_cm += growth
        return self.height_cm

    def reset(self) -> None:
        self.height_cm = 0.0


class SequencingReadCounter:
    def __init__(self, total: int) -> None:
        self.total = total

    def add_batch(self, reads: int) -> None:
        self.total += reads

    def discard(self, reads: int) -> None:
        self.total -= reads

    def scale(self, factor: int) -> None:
        self.total *= factor


class ExpressionTotalUpdater:
    def __init__(self, expression: float) -> None:
        self.expression = expression

    def add_replicate(self, value: float) -> None:
        self.expression += value

    def normalize(self, factor: float) -> None:
        if factor == 0:
            return
        self.expression /= factor

    def power(self, exponent: int) -> None:
        self.expression **= exponent


if __name__ == "__main__":
    g = GrowthAccumulator(height_cm=10.0)
    print(g.add_growth(2.5))

    s = SequencingReadCounter(total=1000)
    s.add_batch(500)
    s.discard(200)
    print(s.total)

    e = ExpressionTotalUpdater(expression=2.0)
    e.add_replicate(1.5)
    e.normalize(2)
    print(e.expression)
