"""functools.reduce: accumulating biological measurements into a single result."""

from functools import reduce


class UniversityReduce:
    def __init__(self, plant_heights_cm: list[float]) -> None:
        self.plant_heights_cm = plant_heights_cm

    def total_height(self) -> float:
        return reduce(lambda total, height: total + height, self.plant_heights_cm, 0.0)

    @staticmethod
    def run() -> None:
        heights_cm = [25.5, 31.2, 18.0, 42.8]

        processor = UniversityReduce(heights_cm)
        total = processor.total_height()

        print(f"Individual heights: {heights_cm}")
        print(f"Total combined height (cm): {total}")


class InterviewReduce:
    def __init__(self, readings: list[float]) -> None:
        self.readings = readings

    def find_max_reading(self) -> float | None:
        """Uses reduce with an explicit initial value to handle empty input safely."""
        if not self.readings:
            return None
        return reduce(
            lambda current_max, value: value if value > current_max else current_max,
            self.readings,
            self.readings[0],
        )

    def cumulative_dilution_factor(self) -> float:
        """Combines successive dilution factors into one overall factor."""
        return reduce(lambda acc, factor: acc * factor, self.readings, 1.0)

    @staticmethod
    def run() -> None:
        empty_readings: list[float] = []
        processor = InterviewReduce(empty_readings)
        print(f"Empty readings -> max: {processor.find_max_reading()}")

        readings = [12.5, 8.3, 19.7, 4.1]
        processor = InterviewReduce(readings)
        print(f"Readings {readings} -> max: {processor.find_max_reading()}")

        dilution_factors = [2.0, 5.0, 10.0]
        processor = InterviewReduce(dilution_factors)
        print(
            f"Dilution factors {dilution_factors} -> "
            f"cumulative: {processor.cumulative_dilution_factor()}"
        )


class IndustryReduce:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def total_expression_by_gene(self) -> dict[str, float]:
        """Aggregates expression levels per gene into a single accumulator dict.

        A clear case where reduce is appropriate: building one merged
        structure out of many records, rather than a simple numeric sum.
        """

        def accumulate(totals: dict[str, float], record: dict) -> dict[str, float]:
            gene = record.get("gene")
            level = record.get("expression_level", 0.0)
            if gene:
                totals[gene] = totals.get(gene, 0.0) + level
            return totals

        return reduce(accumulate, self.data, {})

    def process(self) -> dict[str, object]:
        totals = self.total_expression_by_gene()
        return {
            "total_records": len(self.data),
            "genes_tracked": len(totals),
            "expression_totals": totals,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"gene": "GA20ox", "expression_level": 12.4},
            {"gene": "GA20ox", "expression_level": 3.1},
            {"gene": "WUS1", "expression_level": 8.7},
        ]

        processor = IndustryReduce(sample_data)
        report = processor.process()
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityReduce.run()
    InterviewReduce.run()
    IndustryReduce.run()
