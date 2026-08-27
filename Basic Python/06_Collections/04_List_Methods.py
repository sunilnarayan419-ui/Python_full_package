"""04_List_Methods.py — Python list methods through plant science and genomics."""
from __future__ import annotations


class PlantHeightListMethodsUniversity:
    """University level: basic list manipulation with append, extend, insert, remove, pop, sort."""

    def __init__(self) -> None:
        self.heights: list[float] = []

    def demonstrate(self) -> None:
        self.heights.append(28.5)
        self.heights.extend([32.1, 25.8])
        self.heights.insert(1, 30.0)
        print(f"After append/extend/insert: {self.heights}")
        self.heights.remove(25.8)
        print(f"After remove(25.8):         {self.heights}")
        popped = self.heights.pop()
        print(f"After pop() -> {popped}:      {self.heights}")
        self.heights.sort()
        print(f"After sort():               {self.heights}")
        self.heights.reverse()
        print(f"After reverse():            {self.heights}")

    @staticmethod
    def run() -> None:
        demo = PlantHeightListMethodsUniversity()
        demo.demonstrate()


class GenomicRecordManagerInterview:
    """Interview level: manipulate plant/genomic records, handle missing values and duplicates."""

    def __init__(self, records: list[dict[str, str | float | None]]) -> None:
        self.records = records

    def clean_and_deduplicate(self) -> list[dict[str, str | float]]:
        cleaned: list[dict[str, str | float]] = []
        seen_ids: set[str] = set()
        for rec in self.records:
            gene_id = rec.get("gene_id")
            expr = rec.get("expression")
            if gene_id is None or expr is None:
                continue
            if isinstance(gene_id, str) and gene_id in seen_ids:
                continue
            if isinstance(expr, (int, float)) and expr >= 0:
                seen_ids.add(gene_id)
                cleaned.append({"gene_id": gene_id, "expression": expr})
        return cleaned

    def sort_by_expression(self, records: list[dict[str, str | float]]) -> None:
        records.sort(key=lambda r: r["expression"], reverse=True)

    @staticmethod
    def run() -> None:
        records: list[dict[str, str | float | None]] = [
            {"gene_id": "AT1G01010", "expression": 12.5},
            {"gene_id": "AT1G01020", "expression": None},
            {"gene_id": "AT1G01010", "expression": 12.5},
            {"gene_id": "AT1G01030", "expression": 8.3},
            {"gene_id": None, "expression": 5.0},
        ]
        manager = GenomicRecordManagerInterview(records)
        cleaned = manager.clean_and_deduplicate()
        manager.sort_by_expression(cleaned)
        print("Interview — Cleaned and sorted gene-expression records:")
        for rec in cleaned:
            print(f"  {rec['gene_id']}: {rec['expression']} FPKM")


class SampleCollectionManagerIndustry:
    """Industry level: scientific collection-management component."""

    def __init__(self) -> None:
        self.samples: list[dict[str, str | float | int]] = []

    def register_sample(self, sample: dict[str, str | float | int]) -> None:
        if "sample_id" not in sample:
            raise ValueError("sample must contain 'sample_id'")
        existing = [s for s in self.samples if s["sample_id"] == sample["sample_id"]]
        if existing:
            self.samples.remove(existing[0])
        self.samples.append(sample.copy())
        self.samples.sort(key=lambda s: s["sample_id"])

    def get_sample_index(self, sample_id: str) -> int:
        for idx, s in enumerate(self.samples):
            if s["sample_id"] == sample_id:
                return idx
        raise ValueError(f"sample_id {sample_id} not found")

    def clear_all(self) -> None:
        self.samples.clear()

    @staticmethod
    def run() -> None:
        manager = SampleCollectionManagerIndustry()
        manager.register_sample({"sample_id": "WHT-003", "species": "Wheat", "height_cm": 25.8})
        manager.register_sample({"sample_id": "WHT-001", "species": "Wheat", "height_cm": 28.5})
        manager.register_sample({"sample_id": "WHT-002", "species": "Wheat", "height_cm": 32.1})
        print("Industry — Registered samples (sorted by ID):")
        for s in manager.samples:
            print(f"  {s['sample_id']}: {s['height_cm']} cm")
        idx = manager.get_sample_index("WHT-002")
        print(f"Index of WHT-002: {idx}")


if __name__ == "__main__":
    PlantHeightListMethodsUniversity.run()
    print()
    GenomicRecordManagerInterview.run()
    print()
    SampleCollectionManagerIndustry.run()