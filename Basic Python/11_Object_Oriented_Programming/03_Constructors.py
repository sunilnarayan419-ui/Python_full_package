"""
TOPIC: Constructors

MAIN POINTS
- __init__() initializes an object after it has been created.
- self refers to the current instance.
- Constructor parameters allow objects to receive data during creation.
- Constructors help ensure that objects start with the required attributes.
- Default parameter values can represent optional information.
- Type checks and validation can prevent invalid scientific data from entering the system.
- Python technically creates objects through __new__(); __init__() initializes them.
"""

class BiologicalSample:
    """Represent a biological sample with initialized attributes."""

    def __init__(
        self,
        sample_id,
        organism,
        tissue,
        condition,
        collection_day=1
    ):
        self.sample_id = sample_id
        self.organism = organism
        self.tissue = tissue
        self.condition = condition
        self.collection_day = collection_day

    def describe(self):
        print(f"Sample ID: {self.sample_id}")
        print(f"Organism: {self.organism}")
        print(f"Tissue: {self.tissue}")
        print(f"Condition: {self.condition}")
        print(f"Collection day: {self.collection_day}")


# Create an object by passing data to the constructor.
sample_1 = BiologicalSample(
    "SAMPLE_001",
    "Homo sapiens",
    "Liver",
    "Control"
)

# Create another object with a different collection day.
sample_2 = BiologicalSample(
    "SAMPLE_002",
    "Mus musculus",
    "Brain",
    "Treatment",
    collection_day=7
)

sample_1.describe()

print()

sample_2.describe()

# Access individual attributes.
print("Sample ID:", sample_1.sample_id)
print("Collection day:", sample_2.collection_day)

# Constructor arguments can also be passed by keyword.
sample_3 = BiologicalSample(
    sample_id="SAMPLE_003",
    organism="Arabidopsis thaliana",
    tissue="Root",
    condition="Drought",
    collection_day=5
)

sample_3.describe()