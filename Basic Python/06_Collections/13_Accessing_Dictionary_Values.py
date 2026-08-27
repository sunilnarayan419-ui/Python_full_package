"""13_Accessing_Dictionary_Values.py — Accessing dictionary values safely."""
from __future__ import annotations


class PlantTraitAccessorUniversity:
    """University level: simple value retrieval with direct access and get()."""

    def __init__(self, traits: dict[str, str | float | int]) -> None:
        self.traits = traits

    def display(self) -> None:
        print("University — Plant traits:")
        print(f"  Direct access species: {self.traits['species']}")
        print(f"  Safe get height_cm:    {self.traits.get('height_cm')}")
        print(f"  Safe get missing:      {self.traits.get('root_length', 'N/A')}")

    @staticmethod
    def run() -> None:
        traits = {"species": "Maize", "height_cm": 25.8, "leaf_count": 10}
        demo = PlantTraitAccessorUniversity(traits)
        demo.display()


class GenomicMetadataAccessorInterview:
    """Interview level: safely retrieve genomic metadata."""

    def __init__(self, records: dict[str, dict[str, str | float | int]]) -> None:
        self.records = records

    def get_expression(self, gene_id: str) -> float | None:
        rec = self.records.get(gene_id)
        if rec is None:
            return None
        expr = rec.get("expression")
        return float(expr) if isinstance(expr, (int, float)) else None

    @staticmethod
    def run() -> None:
        records: dict[str, dict[str, str | float | int]] = {
            "AT1G01010": {"species": "Arabidopsis", "expression": 12.5},
            "AT1G01020": {"species": "Arabidopsis", "expression": 8.3},
        }
        demo = GenomicMetadataAccessorInterview(records)
        print("Interview — Safe genomic metadata access:")
        print(f"  AT1G01010 expression: {demo.get_expression('AT1G01010')}")
        print(f"  AT1G01099 expression: {demo.get_expression('AT1G01099')}")


class SampleMetadataAccessorIndustry:
    """Industry level: metadata-access component with predictable behavior."""

    def __init__(self, samples: dict[str, dict[str, str | float | int]]) -> None:
        self.samples = samples

    def retrieve(self, sample_id: str, field: str) -> str | float | int | None:
        sample = self.samples.get(sample_id)
        if sample is None:
            return None
        return sample.get(field)

    def require(self, sample_id: str, field: str) -> str | float | int:
        sample = self.samples.get(sample_id)
        if sample is None:
            raise KeyError(f"sample {sample_id} not found")
        if field not in sample:
            raise KeyError(f"field {field} not found in {sample_id}")
        return sample[field]

    @staticmethod
    def run() -> None:
        samples: dict[str, dict[str, str | float | int]] = {
            "WHT-001": {"species": "Wheat", "height_cm": 28.5},
            "WHT-002": {"species": "Wheat", "height_cm": 32.1},
        }
        accessor = SampleMetadataAccessorIndustry(samples)
        print("Industry — Metadata accessor:")
        print(f"  WHT-001 height (safe):   {accessor.retrieve('WHT-001', 'height_cm')}")
        print(f"  WHT-001 missing (safe):  {accessor.retrieve('WHT-001', 'weight_g')}")
        print(f"  WHT-001 height (req):    {accessor.require('WHT-001', 'height_cm')}")


if __name__ == "__main__":
    PlantTraitAccessorUniversity.run()
    print()
    GenomicMetadataAccessorInterview.run()
    print()
    SampleMetadataAccessorIndustry.run()