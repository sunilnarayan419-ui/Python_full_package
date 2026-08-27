"""Arithmetic operators applied to plant/genomic data."""


class PlantMeasurementCalculator:
    def __init__(self, height_cm: float, leaf_count: int, biomass_g: float) -> None:
        self.height_cm = height_cm
        self.leaf_count = leaf_count
        self.biomass_g = biomass_g

    def total_height_and_biomass(self) -> float:
        return self.height_cm + self.biomass_g

    def leaf_density(self) -> float:
        return self.leaf_count / self.height_cm if self.height_cm else 0.0

    def squared_height(self) -> float:
        return self.height_cm ** 2


class GrowthRateAnalyzer:
    def __init__(self, initial: float, final: float, days: int) -> None:
        self.initial = initial
        self.final = final
        self.days = days

    def absolute_growth(self) -> float:
        return self.final - self.initial

    def relative_growth(self) -> float:
        return (self.final - self.initial) / self.initial if self.initial else 0.0

    def average_daily_growth(self) -> float:
        return (self.final - self.initial) // self.days if self.days else 0


class PhenotypeMetricsBatch:
    def __init__(self, heights: list[float]) -> None:
        self.heights = heights

    def mean(self) -> float:
        return sum(self.heights) / len(self.heights) if self.heights else 0.0

    def height_range(self) -> float:
        if not self.heights:
            return 0.0
        return max(self.heights) - min(self.heights)

    def fold_change(self, baseline: float) -> float:
        m = self.mean()
        return m / baseline if baseline else 0.0


if __name__ == "__main__":
    uni = PlantMeasurementCalculator(height_cm=45.0, leaf_count=12, biomass_g=3.4)
    print(uni.total_height_and_biomass())
    print(uni.leaf_density())
    print(uni.squared_height())

    inter = GrowthRateAnalyzer(initial=10.0, final=25.0, days=5)
    print(inter.average_daily_growth())

    ind = PhenotypeMetricsBatch(heights=[40.0, 42.0, 45.0])
    print(ind.height_range())
    print(ind.fold_change(baseline=10.0))
