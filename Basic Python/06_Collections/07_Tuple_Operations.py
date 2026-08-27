"""07_Tuple_Operations.py — Python tuple operations through plant science and genomics."""
from __future__ import annotations


class PlantTraitOperationsUniversity:
    """University level: simple tuple operations."""

    def __init__(self) -> None:
        self.traits_a: tuple[str, ...] = ("height", "leaf_count", "stem_diameter")
        self.traits_b: tuple[str, ...] = ("root_length", "flower_color")

    def demonstrate(self) -> None:
        combined = self.traits_a + self.traits_b
        repeated = self.traits_a * 2
        print(f"University — Combined traits: {combined}")
        print(f"Repeated traits: {repeated}")
        print(f"'height' in traits_a: {'height' in self.traits_a}")
        print(f"Index of 'leaf_count': {self.traits_a.index('leaf_count')}")
        print(f"Slice [1:3]: {self.traits_a[1:3]}")

    @staticmethod
    def run() -> None:
        demo = PlantTraitOperationsUniversity()
        demo.demonstrate()


class GenomicMetadataInspectorInterview:
    """Interview level: combine and inspect fixed scientific metadata."""

    def __init__(self, run_metadata: tuple[str, ...], sample_metadata: tuple[str, ...]) -> None:
        self.run_metadata = run_metadata
        self.sample_metadata = sample_metadata

    def all_fields(self) -> tuple[str, ...]:
        return self.run_metadata + self.sample_metadata

    def has_field(self, field: str) -> bool:
        return field in self.all_fields()

    def compare_runs(self, other: tuple[str, ...]) -> bool:
        return self.run_metadata == other

    @staticmethod
    def run() -> None:
        run_a = ("run_id", "sequencer", "flowcell", "date")
        sample_a = ("sample_id", "species", "tissue")
        inspector = GenomicMetadataInspectorInterview(run_a, sample_a)
        print("Interview — Metadata operations:")
        print(f"  All fields: {inspector.all_fields()}")
        print(f"  Has 'species': {inspector.has_field('species')}")
        print(f"  Equals run_b: {inspector.compare_runs(('run_id', 'sequencer', 'flowcell', 'date'))}")


class ChromosomeSetProcessorIndustry:
    """Industry level: tuple operations in a realistic scientific processing component."""

    def __init__(self, reference_chroms: tuple[str, ...]) -> None:
        self.reference_chroms = reference_chroms

    def validate_sample_chromosomes(self, sample_chroms: tuple[str, ...]) -> tuple[str, ...]:
        missing = tuple(c for c in self.reference_chroms if c not in sample_chroms)
        return missing

    def create_ploidy_set(self, ploidy: int) -> tuple[str, ...]:
        return self.reference_chroms * ploidy

    @staticmethod
    def run() -> None:
        arabidopsis = ("Chr1", "Chr2", "Chr3", "Chr4", "Chr5")
        sample = ("Chr1", "Chr2", "Chr3", "Chr5")
        processor = ChromosomeSetProcessorIndustry(arabidopsis)
        missing = processor.validate_sample_chromosomes(sample)
        diploid = processor.create_ploidy_set(2)
        print("Industry — Chromosome set operations:")
        print(f"  Missing chromosomes: {missing}")
        print(f"  Diploid set: {diploid}")
        print(f"  Sample is subset: {set(sample) <= set(arabidopsis)}")


if __name__ == "__main__":
    PlantTraitOperationsUniversity.run()
    print()
    GenomicMetadataInspectorInterview.run()
    print()
    ChromosomeSetProcessorIndustry.run()