
"""
12. Dictionaries

Main points
- A dictionary stores key-value pairs.
- Dictionaries are created using {} or dict().
- Keys must be hashable and unique.
- Values can be objects of different types.
- Assigning an existing key replaces its value.
- Modern Python dictionaries preserve insertion order.
- Dictionaries are mutable.
- They are useful for sample metadata, gene annotations, and lookup tables.
"""

# Store biological sample metadata
sample = {
    "sample_id": "S001",
    "organism": "Arabidopsis thaliana",
    "tissue": "leaf",
    "temperature_celsius": 25.0
}

print("Sample metadata:", sample)

# Access a value using its key
print("Sample ID:", sample["sample_id"])
print("Organism:", sample["organism"])

# Add a new key-value pair
sample["treatment"] = "control"
print("Updated sample:", sample)

# Update an existing value
sample["temperature_celsius"] = 28.0
print("Updated temperature:", sample["temperature_celsius"])

# Store gene expression values
expression = {
    "TP53": 12.5,
    "BRCA1": 8.2,
    "EGFR": 18.4
}

print("TP53 expression:", expression["TP53"])

# Count occurrences using a dictionary
dna_sequence = "ATGCGTAA"
nucleotide_counts = {}

for nucleotide in dna_sequence:
    nucleotide_counts[nucleotide] = (
        nucleotide_counts.get(nucleotide, 0) + 1
    )

print("Nucleotide counts:", nucleotide_counts)
