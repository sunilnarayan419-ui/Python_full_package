"""01_Lists.py — Python lists through plant science and genomics."""
from __future__ import annotations


class PlantSpeciesListUniversity:
    """University level: fundamental list creation and usage."""

    def __init__(self) -> None:
        self.species: list[str] = []

    def create_and_display(self) -> None:
        self.species = ["Triticum aestivum", "Oryza sativa", "Zea mays", "Arabidopsis thaliana"]
        print("University — Plant species list:")
        for sp in self.species:
            print(f"  - {sp}")
        print(f"Total species: {len(self.species)}")

    @staticmethod
    def run() -> None:
        demo = PlantSpeciesListUniversity()
        demo.create_and_display()


class GenomicRecordListInterview:
    """Interview level: process a list of genomic records with validation."""

    def __init__(self, records: list[dict[str, str | float]]) -> None:
        self.records = records

    def filter_by_gene_length(self, min_length: int) -> list[dict[str, str | float]]:
        result: list[dict[str, str | float]] = []
        for rec in self.records:
            length = rec.get("gene_length_bp")
            if isinstance(length, (int, float)) and length >= min_length:
                result.append(rec)
        return result

    @staticmethod
    def run() -> None:
        records: list[dict[str, str | float]] = [
            {"gene_id": "AT1G01010", "species": "Arabidopsis", "gene_length_bp": 1200},
            {"gene_id": "AT1G01020", "species": "Arabidopsis", "gene_length_bp": 850},
            {"gene_id": "Zm00001eb000010", "species": "Maize", "gene_length_bp": 2100},
        ]
        demo = GenomicRecordListInterview(records)
        filtered = demo.filter_by_gene_length(min_length=1000)
        print("Interview — Genes >= 1000 bp:")
        for rec in filtered:
            print(f"  {rec['gene_id']}: {rec['gene_length_bp']} bp")


class PhenotypeDataCollectorIndustry:
    """Industry level: a small scientific data component using lists."""

    def __init__(self) -> None:
        self.measurements: list[dict[str, str | float | int]] = []

    def add_measurement(self, sample_id: str, height_cm: float, leaf_count: int) -> None:
        if height_cm <= 0:
            raise ValueError("height_cm must be positive")
        if leaf_count < 0:
            raise ValueError("leaf_count must be non-negative")
        self.measurements.append({
            "sample_id": sample_id,
            "height_cm": height_cm,
            "leaf_count": leaf_count,
        })

    def get_average_height(self) -> float:
        if not self.measurements:
            return 0.0
        return sum(m["height_cm"] for m in self.measurements) / len(self.measurements)

    @staticmethod
    def run() -> None:
        collector = PhenotypeDataCollectorIndustry()
        collector.add_measurement("WHT-001", 28.5, 12)
        collector.add_measurement("WHT-002", 32.1, 15)
        collector.add_measurement("WHT-003", 25.8, 10)
        print("Industry — Phenotype measurements:")
        for m in collector.measurements:
            print(f"  {m['sample_id']}: {m['height_cm']} cm, {m['leaf_count']} leaves")
        print(f"Average height: {collector.get_average_height():.2f} cm")


if __name__ == "__main__":
    PlantSpeciesListUniversity.run()
    print()
    GenomicRecordListInterview.run()
    print()
    PhenotypeDataCollectorIndustry.run()