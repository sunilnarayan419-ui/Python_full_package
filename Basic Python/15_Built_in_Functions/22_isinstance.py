"""
TOPIC: isinstance()

MAIN POINTS
- isinstance() checks whether an object belongs to a class or its subclasses.
- It can also check against a tuple of types.
- It is usually preferable to type(value) is SomeType when subclasses should be accepted.
- bool is a subclass of int, so isinstance(True, int) returns True.
- isinstance() is useful for validating input types and biological data structures.
"""

# Example 1: Check a DNA sequence's type.
dna_sequence = "ATGCGTAC"

print(isinstance(dna_sequence, str))
print(isinstance(dna_sequence, list))

# Example 2: Accept integers and floats.
concentration = 42.5

if isinstance(concentration, (int, float)):
    print("Concentration is numeric.")
else:
    print("Invalid concentration type.")

# Example 3: Exclude booleans from numeric measurements.
concentration = True

if (
    isinstance(concentration, (int, float))
    and not isinstance(concentration, bool)
):
    print("Valid numeric type.")
else:
    print("Boolean is not an accepted concentration.")

# Example 4: Validate a biological record.
sample = {
    "sample_id": "S001",
    "organism": "Homo sapiens",
    "sequence": "ATGC"
}

if isinstance(sample, dict):
    print("Sample record is a dictionary.")

if isinstance(sample.get("sequence"), str):
    print("Sequence field is a string.")

# Example 5: Check class inheritance.
class BiologicalSample:
    pass


class DNA_Sample(BiologicalSample):
    pass


dna_sample = DNA_Sample()

print(isinstance(dna_sample, DNA_Sample))
print(isinstance(dna_sample, BiologicalSample))

# Example 6: Check against multiple accepted types.
value = ("BRCA1", 24.6)

print(isinstance(value, (list, tuple)))