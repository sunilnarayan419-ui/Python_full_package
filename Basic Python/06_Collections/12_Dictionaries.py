"""12_Dictionaries.py — Python dictionaries through plant science and genomics."""
from __future__ import annotations


class PlantSampleDictionaryUniversity:
    """University level: basic dictionary creation and usage."""

    def __init__(self) -> None:
        self.sample: dict[str, str | float] = {
            "sample_id": "P001",
            "species": "Wheat",
            "height_cm": 28.5,
        }

    def display(self) -> None:
        print("University — Plant sample record:")
        for key, value in self.sample.items():
            print(f"  {key}: {value}")

    @staticmethod
    def run() -> None:
        demo = PlantSampleDictionaryUniversity()
        demo.display()


class GenomicRecordDictionaryInterview:
    """Interview level: represent realistic plant/genomic records."""

    def __init__(self, records: list[dict[str, str | float | int]]) -> None:
        self.records = records

    def index_by_gene_id(self) -> dict[str, dict[str, str | float | int]]:
        indexed: dict[str, dict[str, str | float | int]] = {}
        for rec in self.records:
            gene_id = rec.get("gene_id")
            if isinstance(gene_id, str):
                indexed[gene_id] = rec
        return indexed

    @staticmethod
    def run() -> None:
        records: list[dict[str, str | float | int]] = [
            {"gene_id": "AT1G01010", "species": "Arabidopsis", "expression": 12.5},
            {"gene_id": "AT1G01020", "species": "Arabidopsis", "expression": 8.3},
            {"gene_id": "AT1G01030", "species": "Arabidopsis", "expression": 15.1},
        ]
        demo = GenomicRecordDictionaryInterview(records)
        indexed = demo.index_by_gene_id()
        print("Interview — Records indexed by gene_id:")
        for gid, rec in indexed.items():
            print(f"  {gid}: {rec}")


class PhenotypeMetadataStoreIndustry:
    """Industry level: clean scientific metadata structure using dictionaries."""

    def __init__(self) -> None:
        self.samples: dict[str, dict[str, str | float | int]] = {}

    def add_sample(self, sample_id: str, metadata: dict[str, str | float | int]) -> None:
        if not sample_id:
            raise ValueError("sample_id must not be empty")
        self.samples[sample_id] = metadata.copy()

    def get_sample(self, sample_id: str) -> dict[str, str | float | int] | None:
        return self.samples.get(sample_id)

    @staticmethod
    def run() -> None:
        store = PhenotypeMetadataStoreIndustry()
        store.add_sample("WHT-001", {"species": "Wheat", "height_cm": 28.5, "leaf_count": 12})
        store.add_sample("RCE-001", {"species": "Rice", "height_cm": 32.1, "leaf_count": 15})
        print("Industry — Phenotype metadata store:")
        for sid, meta in store.samples.items():
            print(f"  {sid}: {meta}")


if __name__ == "__main__":
    PlantSampleDictionaryUniversity.run()
    print()
    GenomicRecordDictionaryInterview.run()
    print()
    PhenotypeMetadataStoreIndustry.run()