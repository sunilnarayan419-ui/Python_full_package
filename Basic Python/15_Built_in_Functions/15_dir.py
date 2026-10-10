"""
TOPIC: dir()

MAIN POINTS
- dir() lists names associated with an object or the current scope.
- dir(object) is useful for exploring attributes and methods.
- dir() without arguments lists names in the current local scope.
- Many returned names beginning and ending with double underscores are special methods.
- dir() is an exploration tool, not complete documentation.
"""

# Example 1: Explore a string.
dna_sequence = "ATGC"

print("String methods and attributes:")
print(dir(dna_sequence))

# Example 2: Explore a list.
samples = ["S001", "S002"]

print("\nList methods and attributes:")
print(dir(samples))

# Example 3: Explore a dictionary.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2
}

print("\nDictionary methods and attributes:")
print(dir(gene_expression))

# Example 4: Explore a custom biological class.
class BiologicalSample:
    def __init__(self, sample_id, organism):
        self.sample_id = sample_id
        self.organism = organism

    def describe(self):
        return f"{self.sample_id}: {self.organism}"


sample = BiologicalSample("S001", "Homo sapiens")

print("\nClass attributes and methods:")
print(dir(BiologicalSample))

print("\nObject attributes and methods:")
print(dir(sample))

# Example 5: Inspect selected attributes.
print("Sample ID:", sample.sample_id)
print("Description:", sample.describe())