"""Floating-point values in plant measurements."""


class FloatUniversity:
    def __init__(self, height_cm: float) -> None:
        self.height_cm = height_cm

    def in_meters(self) -> float:
        return self.height_cm / 100.0


class FloatInterview:
    def __init__(self, ph: float) -> None:
        self.ph = ph

    def is_acidic(self) -> bool:
        return self.ph < 7.0


class FloatIndustry:
    def __init__(self, values: list[float], tolerance: float = 0.01) -> None:
        self.values = values
        self.tolerance = tolerance

    def mean(self) -> float:
        if not self.values:
            return 0.0
        return sum(self.values) / len(self.values)

    def is_consistent(self) -> bool:
        if not self.values:
            return True
        m = self.mean()
        return all(abs(v - m) <= self.tolerance for v in self.values)


if __name__ == "__main__":
    print(FloatUniversity(150.0).in_meters())

    print(FloatInterview(5.5).is_acidic())

    print(FloatIndustry([0.45, 0.46, 0.44]).is_consistent())
