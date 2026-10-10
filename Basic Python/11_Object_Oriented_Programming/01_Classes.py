"""
TOPIC: Classes

MAIN POINTS
- A class is a blueprint for creating objects.
- Classes group related data and behavior into one logical unit.
- Define a class using the class keyword.
- Attributes represent the data associated with an object.
- Methods represent the behaviors an object can perform.
- Class names conventionally use PascalCase.
- In biology, classes can represent biological samples, genes, proteins, cells, or experiments.
- A class helps organize scientific code when many related entities share the same structure.
"""

class BiologicalSample:
    """Represent a biological sample used in a research laboratory."""

    def describe(self):
        print("This is a biological sample.")
        print("It belongs to a biological research experiment.")


# Create a class definition, then instantiate an object from it.
sample = BiologicalSample()

# Call a method defined inside the class.
sample.describe()

# Inspect the object's type.
print(type(sample))

# Check whether the object belongs to BiologicalSample.
print(isinstance(sample, BiologicalSample))

# Create another object from the same class.
another_sample = BiologicalSample()

print(type(another_sample))

# Both objects share the same class but have separate identities.
print(sample is another_sample)