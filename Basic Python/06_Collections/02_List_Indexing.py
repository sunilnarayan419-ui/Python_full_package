"""02_List_Indexing.py — Python list indexing through plant science and genomics."""
from __future__ import annotations


class PlantSampleIndexerUniversity:
    """University level: positive and negative list indexing."""

    def __init__(self, samples: list[str]) -> None:
        self.samples = samples

    def show_first_and_last(self) -> None:
        print("University — Plant samples:")
        print(f"  First sample (index 0):  {self.samples[0]}")
        print(f"  Last sample (index -1):  {self.samples[-1]}")
        print(f"  Second sample (index 1): {self.samples[1]}")

    @staticmethod
    def run() -> None:
        samples = ["Wheat-Leaf-01", "Rice-Root-03", "Maize-Stem-07", "Barley-Seed-12"]
        demo = PlantSampleIndexerUniversity(samples)
        demo.show_first_and_last()


class GenomicMeasurementIndexerInterview:
    """Interview level: safe deterministic access to scientific records."""

    def __init__(self, measurements: list[float]) -> None:
        self.measurements = measurements

    def get_measurement(self, index: int) -> float | None:
        if not isinstance(index, int):
            return None
        if -len(self.measurements) <= index < len(self.measurements):
            return self.measurements[index]
        return None

    @staticmethod
    def run() -> None:
        heights = [28.5, 32.1, 25.8, 30.0, 27.3]
        demo = GenomicMeasurementIndexerInterview(heights)
        print("Interview — Plant height measurements (cm):")
        print(f"  Index 2:  {demo.get_measurement(2)}")
        print(f"  Index -2: {demo.get_measurement(-2)}")
        print(f"  Index 10: {demo.get_measurement(10)}")


class ChromosomeRecordAccessorIndustry:
    """Industry level: deterministic access to chromosome records with validation."""

    def __init__(self, records: list[dict[str, str | int]]) -> None:
        self.records = records

    def get_chromosome_by_index(self, index: int) -> dict[str, str | int]:
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not (-len(self.records) <= index < len(self.records)):
            raise IndexError(f"index {index} out of range for {len(self.records)} records")
        return self.records[index]

    @staticmethod
    def run() -> None:
        records: list[dict[str, str | int]] = [
            {"chromosome": "Chr1", "length_bp": 30_432_000, "organism": "Arabidopsis"},
            {"chromosome": "Chr2", "length_bp": 19_698_000, "organism": "Arabidopsis"},
            {"chromosome": "Chr3", "length_bp": 23_465_000, "organism": "Arabidopsis"},
            {"chromosome": "Chr4", "length_bp": 18_585_000, "organism": "Arabidopsis"},
            {"chromosome": "Chr5", "length_bp": 26_975_000, "organism": "Arabidopsis"},
        ]
        accessor = ChromosomeRecordAccessorIndustry(records)
        print("Industry — Chromosome records:")
        first = accessor.get_chromosome_by_index(0)
        last = accessor.get_chromosome_by_index(-1)
        print(f"  First: {first['chromosome']} — {first['length_bp']:,} bp")
        print(f"  Last:  {last['chromosome']} — {last['length_bp']:,} bp")


if __name__ == "__main__":
    PlantSampleIndexerUniversity.run()
    print()
    GenomicMeasurementIndexerInterview.run()
    print()
    ChromosomeRecordAccessorIndustry.run()