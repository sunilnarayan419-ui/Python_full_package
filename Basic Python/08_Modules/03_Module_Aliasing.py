"""
03_Module_Aliasing.py

Topic: Module aliasing with `import module as alias`.

Demonstrates readable, purposeful aliases in scientific/bioinformatics
contexts, and warns against confusing aliases.
"""

import statistics as stats
import datetime as dt
import collections as coll


class UniversityModuleAliasing:
    """Introduces `import module as alias` with a readable alias."""

    @staticmethod
    def run() -> None:
        soil_ph_readings: list[float] = [6.4, 6.7, 6.5, 6.9, 6.6]

        mean_ph = stats.mean(soil_ph_readings)
        median_ph = stats.median(soil_ph_readings)

        print("University: import module as alias")
        print(f"  Soil pH readings: {soil_ph_readings}")
        print(f"  Mean pH: {mean_ph:.2f}")
        print(f"  Median pH: {median_ph:.2f}")


class InterviewModuleAliasing:
    """Uses aliased modules to solve a realistic experiment-logging problem."""

    @staticmethod
    def run() -> None:
        crop_yield_kg_per_plot: list[float] = [18.2, 19.5, 17.8, 20.1, 18.9, 19.0]

        harvest_time = dt.datetime.now()
        yield_summary = {
            "mean": stats.mean(crop_yield_kg_per_plot),
            "stdev": stats.stdev(crop_yield_kg_per_plot),
        }

        print("Interview: import module as alias")
        print(f"  Harvest recorded: {harvest_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Yield summary: {yield_summary}")


class IndustryModuleAliasing:
    """Demonstrates disciplined aliasing conventions in maintainable code."""

    def __init__(self, plot_id: str, mutation_counts: list[int]) -> None:
        if not plot_id:
            raise ValueError("plot_id must be a non-empty string.")
        if not mutation_counts:
            raise ValueError("mutation_counts must contain at least one value.")

        self._plot_id = plot_id
        self._mutation_counts = mutation_counts
        self._logged_at = dt.datetime.now()

    def frequency_table(self) -> coll.Counter:
        return coll.Counter(self._mutation_counts)

    def average_mutation_count(self) -> float:
        return stats.mean(self._mutation_counts)

    def report(self) -> str:
        return (
            f"Plot {self._plot_id} | "
            f"avg_mutations={self.average_mutation_count():.2f} | "
            f"logged={self._logged_at.isoformat(timespec='seconds')}"
        )

    @staticmethod
    def run() -> None:
        observed_mutation_counts: list[int] = [2, 3, 2, 4, 3, 2, 5]

        analyzer = IndustryModuleAliasing("PLOT-B7", observed_mutation_counts)
        print("Industry: import module as alias")
        print(f"  {analyzer.report()}")
        print(f"  Frequency table: {dict(analyzer.frequency_table())}")


if __name__ == "__main__":
    UniversityModuleAliasing.run()
    InterviewModuleAliasing.run()
    IndustryModuleAliasing.run()
