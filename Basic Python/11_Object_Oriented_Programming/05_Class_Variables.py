"""
TOPIC: Class Variables

MAIN POINTS
- Class variables are defined directly inside the class body.
- They are shared through the class unless an individual instance overrides the attribute.
- They are useful for constants and information common to all objects.
- Instance variables store object-specific information.
- Access class variables using ClassName.variable_name when you want to reference the class-level value explicitly.
- Mutable class variables, such as lists and dictionaries, can accidentally share changing data between instances.
- Use class variables carefully when managing laboratory-wide settings or sample categories.
"""

class BiologicalSample:
    """Represent a biological sample in a shared research project."""

    laboratory_name = "Molecular Biology Laboratory"
    project_code = "BIO_PROJECT_2026"
    total_samples_created = 0

    def __init__(self, sample_id, organism, tissue):
        self.sample_id = sample_id
        self.organism = organism
        self.tissue = tissue

        # Update the shared class-level counter.
        BiologicalSample.total_samples_created += 1

    def describe(self):
        print(f"Laboratory: {self.laboratory_name}")
        print(f"Project: {self.project_code}")
        print(f"Sample ID: {self.sample_id}")
        print(f"Organism: {self.organism}")
        print(f"Tissue: {self.tissue}")


sample_1 = BiologicalSample(
    "SAMPLE_001",
    "Homo sapiens",
    "Blood"
)

sample_2 = BiologicalSample(
    "SAMPLE_002",
    "Mus musculus",
    "Liver"
)

sample_3 = BiologicalSample(
    "SAMPLE_003",
    "Arabidopsis thaliana",
    "Root"
)

sample_1.describe()

print()

sample_2.describe()

print()
print("Total samples created:", BiologicalSample.total_samples_created)

# Change the shared class attribute.
BiologicalSample.laboratory_name = "Genomics Research Laboratory"

print(sample_1.laboratory_name)
print(sample_2.laboratory_name)

# An instance assignment creates an instance-level override.
sample_1.laboratory_name = "Independent Research Unit"

print(sample_1.laboratory_name)
print(sample_2.laboratory_name)
print(BiologicalSample.laboratory_name)