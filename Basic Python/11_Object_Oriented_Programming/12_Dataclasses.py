"""
TOPIC: Dataclasses

MAIN POINTS
- Dataclasses simplify classes that primarily store structured data.
- The @dataclass decorator can generate __init__(), __repr__(), and __eq__() automatically.
- Type annotations document the expected attribute types but do not enforce runtime validation.
- Default values can be provided for optional fields.
- Use field(default_factory=...) for mutable attributes such as lists and dictionaries.
- frozen=True prevents ordinary attribute reassignment after initialization.
- Dataclasses are useful for representing experimental records, biological metadata, and analysis results.
- Custom methods can be added when a data class needs behavior beyond storing values.
"""

from dataclasses import dataclass, field


@dataclass
class BiologicalSample:
    """Store structured metadata for a biological sample."""

    sample_id: str
    organism: str
    tissue: str
    condition: str
    collection_day: int = 1

    # Each object receives its own list.
    tags: list[str] = field(default_factory=list)

    # Each object receives its own dictionary.
    measurements: dict[str, float] = field(default_factory=dict)

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

    def record_measurement(
        self,
        measurement_name: str,
        value: float
    ) -> None:
        if value < 0:
            raise ValueError("Measurement cannot be negative.")

        self.measurements[measurement_name] = value

    def describe(self) -> None:
        print(f"Sample ID: {self.sample_id}")
        print(f"Organism: {self.organism}")
        print(f"Tissue: {self.tissue}")
        print(f"Condition: {self.condition}")
        print(f"Collection day: {self.collection_day}")
        print(f"Tags: {self.tags}")
        print(f"Measurements: {self.measurements}")


# Create a biological sample without writing a custom __init__().
sample_1 = BiologicalSample(
    sample_id="SAMPLE_001",
    organism="Homo sapiens",
    tissue="Blood",
    condition="Control",
    collection_day=1
)

sample_2 = BiologicalSample(
    sample_id="SAMPLE_002",
    organism="Mus musculus",
    tissue="Liver",
    condition="Treatment",
    collection_day=7
)

sample_1.add_tag("DNA_extraction")
sample_1.add_tag("Baseline")

sample_1.record_measurement("DNA_concentration_ng_uL", 45.2)
sample_1.record_measurement("A260_A280_ratio", 1.87)

sample_2.add_tag("Drug_response")
sample_2.record_measurement("DNA_concentration_ng_uL", 62.8)

sample_1.describe()

print()

sample_2.describe()

# Dataclasses generate a useful representation.
print(sample_1)

# Dataclasses generate equality based on their declared fields.
sample_3 = BiologicalSample(
    sample_id="SAMPLE_001",
    organism="Homo sapiens",
    tissue="Blood",
    condition="Control",
    collection_day=1
)

print("Same data:", sample_1 == sample_3)

# Mutable fields are independent between objects.
print("Sample 1 tags:", sample_1.tags)
print("Sample 2 tags:", sample_2.tags)

# Convert a dataclass instance into a dictionary.
from dataclasses import asdict

sample_record = asdict(sample_1)

print("Dictionary representation:")
print(sample_record)


# A separate immutable-style record.
@dataclass(frozen=True)
class GeneRecord:
    gene_id: str
    organism: str
    chromosome: str
    start_position: int
    end_position: int

    def gene_length(self) -> int:
        return self.end_position - self.start_position + 1


gene = GeneRecord(
    gene_id="BRCA1",
    organism="Homo sapiens",
    chromosome="17",
    start_position=43044295,
    end_position=43125482
)

print(gene)
print("Genomic interval length:", gene.gene_length())

# This would raise an error because the dataclass is frozen.
# gene.gene_id = "TP53"