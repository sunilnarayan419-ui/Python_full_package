"""
TOPIC: Instance Variables

MAIN POINTS
- Instance variables belong to individual objects.
- They are usually defined using self.variable_name inside __init__().
- Different objects can store different values for the same instance variable.
- Instance variables represent object-specific state.
- Biological sample IDs, tissue types, collection dates, and experimental measurements are natural instance variables.
- Changing an instance variable normally affects only that particular object.
"""

class BiologicalSample:
    """Store information specific to an individual biological sample."""

    def __init__(
        self,
        sample_id,
        organism,
        tissue,
        condition,
        dna_concentration
    ):
        self.sample_id = sample_id
        self.organism = organism
        self.tissue = tissue
        self.condition = condition
        self.dna_concentration = dna_concentration

    def update_dna_concentration(self, new_concentration):
        if new_concentration < 0:
            raise ValueError("DNA concentration cannot be negative.")

        self.dna_concentration = new_concentration

    def describe(self):
        print(
            f"{self.sample_id}: "
            f"{self.organism}, "
            f"{self.tissue}, "
            f"{self.condition}, "
            f"DNA concentration={self.dna_concentration} ng/µL"
        )


sample_1 = BiologicalSample(
    "DNA_001",
    "Homo sapiens",
    "Blood",
    "Control",
    42.5
)

sample_2 = BiologicalSample(
    "DNA_002",
    "Homo sapiens",
    "Blood",
    "Treatment",
    68.2
)

sample_1.describe()
sample_2.describe()

print()

# Modify only the first sample.
sample_1.update_dna_concentration(50.0)

print("After updating the first sample:")

sample_1.describe()
sample_2.describe()

# Inspect object-specific variables.
print("Sample 1 variables:", sample_1.__dict__)
print("Sample 2 variables:", sample_2.__dict__)