"""
TOPIC: Inheritance

MAIN POINTS
- Inheritance allows one class to reuse and extend another class.
- The parent class is also called the base class or superclass.
- The child class is also called the derived class or subclass.
- A child class inherits accessible attributes and methods from its parent.
- Use super() to invoke parent-class behavior.
- A child class can override inherited methods to customize behavior.
- Inheritance is useful when biological sample types share common attributes but require specialized behavior.
"""

class BiologicalSample:
    """Base class for all biological samples."""

    def __init__(
        self,
        sample_id,
        organism,
        collection_date
    ):
        self.sample_id = sample_id
        self.organism = organism
        self.collection_date = collection_date

    def describe(self):
        print(f"Sample ID: {self.sample_id}")
        print(f"Organism: {self.organism}")
        print(f"Collection date: {self.collection_date}")

    def sample_type(self):
        return "General biological sample"


class DNA_Sample(BiologicalSample):
    """Represent a sample intended for DNA analysis."""

    def __init__(
        self,
        sample_id,
        organism,
        collection_date,
        dna_concentration,
        purity_ratio
    ):
        super().__init__(
            sample_id,
            organism,
            collection_date
        )

        self.dna_concentration = dna_concentration
        self.purity_ratio = purity_ratio

    def sample_type(self):
        return "DNA sample"

    def calculate_dna_mass(self, volume_microliters):
        if volume_microliters < 0:
            raise ValueError("Volume cannot be negative.")

        return self.dna_concentration * volume_microliters

    def describe(self):
        # Reuse the parent's description.
        super().describe()

        print("Sample type:", self.sample_type())
        print("DNA concentration:", self.dna_concentration, "ng/µL")
        print("Purity ratio:", self.purity_ratio)


class RNA_Sample(BiologicalSample):
    """Represent a sample intended for RNA analysis."""

    def __init__(
        self,
        sample_id,
        organism,
        collection_date,
        rna_concentration
    ):
        super().__init__(
            sample_id,
            organism,
            collection_date
        )

        self.rna_concentration = rna_concentration

    def sample_type(self):
        return "RNA sample"

    def describe(self):
        super().describe()

        print("Sample type:", self.sample_type())
        print("RNA concentration:", self.rna_concentration, "ng/µL")


dna_sample = DNA_Sample(
    "DNA_001",
    "Homo sapiens",
    "2026-10-01",
    45.0,
    1.87
)

rna_sample = RNA_Sample(
    "RNA_001",
    "Mus musculus",
    "2026-10-02",
    32.0
)

dna_sample.describe()

print()

rna_sample.describe()

print()
print("DNA mass in 5 µL:", dna_sample.calculate_dna_mass(5))

# Check the inheritance relationships.
print(isinstance(dna_sample, DNA_Sample))
print(isinstance(dna_sample, BiologicalSample))
print(issubclass(DNA_Sample, BiologicalSample))