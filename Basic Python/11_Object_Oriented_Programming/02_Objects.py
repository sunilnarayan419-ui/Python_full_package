"""
TOPIC: Objects

MAIN POINTS
- An object is an instance of a class.
- Different objects created from the same class can represent different biological samples.
- Objects can have individual attributes.
- The dot operator accesses an object's attributes and methods.
- Each object has its own identity and can maintain its own state.
- Two objects can belong to the same class but contain different data.
- Objects make it easier to represent multiple samples in a research experiment.
"""

class BiologicalSample:
    """Represent an individual biological sample."""

    def describe(self):
        print(f"Sample ID: {self.sample_id}")
        print(f"Organism: {self.organism}")
        print(f"Tissue: {self.tissue}")
        print(f"Condition: {self.condition}")


# Create the first object.
sample_1 = BiologicalSample()

sample_1.sample_id = "SAMPLE_001"
sample_1.organism = "Homo sapiens"
sample_1.tissue = "Liver"
sample_1.condition = "Control"

# Create the second object.
sample_2 = BiologicalSample()

sample_2.sample_id = "SAMPLE_002"
sample_2.organism = "Mus musculus"
sample_2.tissue = "Brain"
sample_2.condition = "Treatment"

# Each object maintains its own attributes.
sample_1.describe()

print()

sample_2.describe()

# Inspect individual attributes.
print("First sample organism:", sample_1.organism)
print("Second sample organism:", sample_2.organism)

# Objects are separate instances.
print("Same object:", sample_1 is sample_2)

# Each object has its own instance dictionary.
print("First sample data:", sample_1.__dict__)
print("Second sample data:", sample_2.__dict__)