"""Complex numbers in scientific computing."""


class ComplexUniversity:
    def __init__(self, z: complex) -> None:
        self.z = z

    def conjugate(self) -> complex:
        return self.z.conjugate()


class ComplexInterview:
    @staticmethod
    def from_polar(r: float, theta: float) -> complex:
        import math
        return complex(r * math.cos(theta), r * math.sin(theta))


class ComplexIndustry:
    def __init__(self, signal: list[complex]) -> None:
        self.signal = signal

    def magnitude_spectrum(self) -> list[float]:
        return [abs(c) for c in self.signal]

    def mean_magnitude(self) -> float:
        if not self.signal:
            return 0.0
        return sum(abs(c) for c in self.signal) / len(self.signal)


if __name__ == "__main__":
    print(ComplexUniversity(1 + 2j).conjugate())

    print(ComplexInterview.from_polar(1.0, 0.0))

    print(ComplexIndustry([1 + 0j, 0 + 1j, 1 + 1j]).mean_magnitude())
