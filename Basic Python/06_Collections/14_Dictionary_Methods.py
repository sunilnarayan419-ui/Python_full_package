"""14_Dictionary_Methods.py — Python dictionary methods through plant science and genomics."""
from __future__ import annotations


class PlantTraitMethodsUniversity:
    """University level: basic dictionary manipulation with keys, values, items, update, pop, copy."""

    def __init__(self) -> None:
        self.traits: dict[str, str | float | int] = {"species": "Barley", "height_cm": 30.0}

    def demonstrate(self) -> None:
        print(f"Keys:   {list(self.traits.keys())}")
        print(f"Values: {list(self.traits.values())}")
        self.traits.update({"leaf_count": 14, "stem_diameter_mm": 4.2})
        print(f"After update: {self.traits}")
        popped = self.traits.pop("stem_diameter_mm")
        print(f"After pop('stem_diameter_mm') -> {popped}: {self.traits}")
        copied = self.traits.copy()
        copied.clear()
        print(f"Copied and cleared: {copied}")

    @staticmethod
    def run() -> None:
        demo = PlantTraitMethodsUniversity()
        demo.demonstrate()


class GenomicRecordProcessorInterview:
    """Interview level: process plant/genomic metadata with dictionary methods."""

    def __init__(self, records: dict[str, dict[str, str | float | int]]) -> None:
        self.records = records

    def merge_annotations(self, gene_id: str, annotations: dict[str, str | float | int]) -> None:
        rec = self.records.get(gene_id)
        if rec is None:
            self.records[gene_id] = annotations.copy()
        else:
            rec.update(annotations)

    def remove_record(self, gene_id: str) -> dict[str, str | float | int] | None:
        return self.records.pop(gene_id, None)

    def list_gene_ids(self) -> list[str]:
        return list(self.records.keys())

    @staticmethod
    def run() -> None:
        records: dict[str, dict[str, str | float | int]] = {
            "AT1G01010": {"expression": 12.5, "tissue": "leaf"},
            "AT1G01020": {"expression": 8.3, "tissue": "root"},
        }
        processor = GenomicRecordProcessorInterview(records)
        processor.merge_annotations("AT1G01010", {"go_term": "photosynthesis"})
        processor.merge_annotations("AT1G01030", {"expression": 5.0, "tissue": "stem"})
        removed = processor.remove_record("AT1G01020")
        print("Interview — Processed records:")
        print(f"  Gene IDs: {processor.list_gene_ids()}")
        print(f"  Removed:  {removed}")
        print(f"  Records:  {processor.records}")


class PhenotypeDatabaseIndustry:
    """Industry level: scientific metadata-management component."""

    def __init__(self) -> None:
        self.entries: dict[str, dict[str, str | float | int]] = {}

    def insert(self, sample_id: str, data: dict[str, str | float | int]) -> None:
        if sample_id in self.entries:
            raise ValueError(f"{sample_id} already exists")
        self.entries[sample_id] = data.copy()

    def upsert(self, sample_id: str, data: dict[str, str | float | int]) -> None:
        if sample_id in self.entries:
            self.entries[sample_id].update(data)
        else:
            self.entries[sample_id] = data.copy()

    def popitem_safe(self) -> tuple[str, dict[str, str | float | int]] | None:
        if not self.entries:
            return None
        return self.entries.popitem()

    def setdefault_field(self, sample_id: str, field: str, default: str | float | int) -> str | float | int:
        rec = self.entries.setdefault(sample_id, {})
        if not isinstance(rec, dict):
            raise TypeError("expected dict entry")
        return rec.setdefault(field, default)

    @staticmethod
    def run() -> None:
        db = PhenotypeDatabaseIndustry()
        db.insert("WHT-001", {"species": "Wheat", "height_cm": 28.5})
        db.upsert("WHT-001", {"leaf_count": 12})
        db.setdefault_field("WHT-002", "species", "Wheat")
        db.setdefault_field("WHT-002", "height_cm", 32.1)
        print("Industry — Phenotype database:")
        for sid, data in db.entries.items():
            print(f"  {sid}: {data}")


if __name__ == "__main__":
    PlantTraitMethodsUniversity.run()
    print()
    GenomicRecordProcessorInterview.run()
    print()
    PhenotypeDatabaseIndustry.run()