"""Demonstrates the math module through plant-science and molecular examples."""

import math


class UniversityMath:
    """Introduces core math functions using plant growth measurements."""

    def __init__(self, heights_cm: list[float]) -> None:
        self.heights_cm = heights_cm

    def calculate_average_height(self) -> float:
        return sum(self.heights_cm) / len(self.heights_cm)

    def calculate_growth_area(self, radius_cm: float) -> float:
        """Area of a circular leaf canopy: pi * r^2."""
        return math.pi * math.pow(radius_cm, 2)

    def round_to_whole_cm(self, value: float) -> tuple[int, int]:
        """Return (floor, ceil) bounds for a measurement, useful for reporting ranges."""
        return math.floor(value), math.ceil(value)

    @staticmethod
    def run() -> None:
        heights_cm = [28.5, 31.2, 26.8, 30.1]
        processor = UniversityMath(heights_cm)

        average = processor.calculate_average_height()
        canopy_area = processor.calculate_growth_area(radius_cm=12.5)
        floor_val, ceil_val = processor.round_to_whole_cm(average)

        print(f"Average plant height: {average:.2f} cm")
        print(f"Canopy area (r=12.5cm): {canopy_area:.2f} sq cm")
        print(f"Reporting bounds for average height: [{floor_val}, {ceil_val}]")


class InterviewMath:
    """Solves a pH calculation problem: pH = -log10([H+]), with edge-case handling."""

    def __init__(self, hydrogen_ion_concentrations: list[float]) -> None:
        self.hydrogen_ion_concentrations = hydrogen_ion_concentrations

    def calculate_ph(self, concentration: float) -> float:
        """Calculate pH from hydrogen ion molar concentration.

        Raises ValueError for non-positive concentrations, since log is undefined
        for zero or negative values.
        """
        if concentration <= 0:
            raise ValueError("Hydrogen ion concentration must be positive.")
        return -math.log10(concentration)

    def classify_solution(self, ph_value: float) -> str:
        if math.isclose(ph_value, 7.0, abs_tol=0.05):
            return "neutral"
        return "acidic" if ph_value < 7.0 else "basic"

    def summarize_samples(self) -> list[dict[str, float | str]]:
        results: list[dict[str, float | str]] = []
        for concentration in self.hydrogen_ion_concentrations:
            try:
                ph_value = self.calculate_ph(concentration)
                results.append(
                    {
                        "concentration": concentration,
                        "ph": round(ph_value, 2),
                        "classification": self.classify_solution(ph_value),
                    }
                )
            except ValueError as error:
                results.append({"concentration": concentration, "error": str(error)})
        return results

    @staticmethod
    def run() -> None:
        # Valid concentrations plus an invalid (zero) sample to test edge-case handling.
        samples = [1e-7, 1e-3, 1e-10, 0.0]
        solver = InterviewMath(samples)

        for entry in solver.summarize_samples():
            print(entry)


class IndustryMath:
    """Reusable numerical utility for scientific growth-model calculations."""

    def __init__(self, tolerance: float = 1e-6) -> None:
        self.tolerance = tolerance

    def exponential_growth(self, initial: float, rate: float, time_hours: float) -> float:
        """Model bacterial or cell-culture growth: N(t) = N0 * e^(rate * t)."""
        if initial <= 0:
            raise ValueError("Initial population must be positive.")
        return initial * math.exp(rate * time_hours)

    def decay_half_life(self, initial: float, half_life_hours: float, time_hours: float) -> float:
        """Model radioactive tracer or drug decay using exponential decay."""
        if half_life_hours <= 0:
            raise ValueError("Half-life must be positive.")
        decay_constant = math.log(2) / half_life_hours
        return initial * math.exp(-decay_constant * time_hours)

    def values_agree(self, measured: float, expected: float) -> bool:
        """Compare measured vs expected experimental values within tolerance."""
        return math.isclose(measured, expected, rel_tol=self.tolerance)

    def vector_magnitude(self, components: tuple[float, ...]) -> float:
        """Euclidean magnitude, e.g. for 3D microscopy displacement vectors."""
        return math.sqrt(sum(math.pow(component, 2) for component in components))

    @staticmethod
    def run() -> None:
        calculator = IndustryMath(tolerance=1e-3)

        population = calculator.exponential_growth(initial=500.0, rate=0.35, time_hours=6.0)
        print(f"Projected cell population after 6h: {population:.1f}")

        remaining = calculator.decay_half_life(initial=100.0, half_life_hours=8.0, time_hours=4.0)
        print(f"Tracer remaining after 4h: {remaining:.2f}")

        agrees = calculator.values_agree(measured=population, expected=population * 1.0005)
        print(f"Measured value within tolerance of expected: {agrees}")

        displacement = calculator.vector_magnitude((1.2, -0.8, 0.4))
        print(f"Cell displacement magnitude: {displacement:.3f} micrometers")


if __name__ == "__main__":
    UniversityMath.run()
    InterviewMath.run()
    IndustryMath.run()
