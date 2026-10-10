"""
TOPIC: type()

MAIN POINTS
- type(object) returns the object's type.
- type() is useful for inspecting values during development.
- type(value) is often used to distinguish exact built-in types.
- isinstance() is usually better when inheritance and subclasses should be accepted.
- type() can also be used to create classes dynamically, although class statements are clearer for ordinary use.
"""

# Example 1: Inspect biological data types.
dna_sequence = "ATGCGTAC"
sequence_length = len(dna_sequence)
gc_percentage = 50.0

print(type(dna_sequence))
print(type(sequence_length))
print(type(gc_percentage))

# Example 2: Inspect collections.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2
}

samples = ["S001", "S002"]

print(type(gene_expression))
print(type(samples))

# Example 3: Compare type() with isinstance().
print(type(True))
print(isinstance(True, int))

# Example 4: Inspect a biological class.
class BiologicalSample:
    def __init__(self, sample_id, organism):
        self.sample_id = sample_id
        self.organism = organism


sample = BiologicalSample("S001", "Homo sapiens")

print(type(sample))
print(type(sample) is BiologicalSample)
print(isinstance(sample, BiologicalSample))

# Example 5: Demonstrate subclass behavior.
class DNA_Sample(BiologicalSample):
    pass


dna_sample = DNA_Sample("DNA001", "Homo sapiens")

print(type(dna_sample) is BiologicalSample)
print(isinstance(dna_sample, BiologicalSample))
print(isinstance(dna_sample, DNA_Sample))

# Example 6: Inspect a function's return type.
def calculate_gc_percentage(sequence):
    if not sequence:
        return 0.0

    gc_count = sequence.count("G") + sequence.count("C")

    return gc_count / len(sequence) * 100


result = calculate_gc_percentage("ATGCGC")

print("Result:", result)
print("Result type:", type(result))