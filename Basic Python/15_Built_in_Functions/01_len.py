"""
TOPIC: len()

MAIN POINTS
- len() returns the number of items in an object.
- It works with strings, lists, tuples, dictionaries, sets, and other sized objects.
- For a DNA string, len() returns the number of characters.
- For a dictionary, len() returns the number of keys.
- len() does not calculate the biological length of a complex object automatically.
"""

# Example 1: DNA sequence length.
dna_sequence = "ATGCGTACGTAG"

print("DNA length:", len(dna_sequence))

# Example 2: Number of biological samples.
samples = ["S001", "S002", "S003", "S004"]

print("Number of samples:", len(samples))

# Example 3: Number of genes in an expression dataset.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8
}

print("Number of genes:", len(gene_expression))

# Example 4: Count the nucleotides in a sequence.
for nucleotide in "ATGC":
    count = dna_sequence.count(nucleotide)
    print(f"{nucleotide}: {count}")

# Example 5: Length of a nested dataset.
sample_records = [
    {"sample_id": "S001", "genes": ["BRCA1", "TP53"]},
    {"sample_id": "S002", "genes": ["EGFR"]}
]

print("Number of sample records:", len(sample_records))
print("Genes in first sample:", len(sample_records[0]["genes"]))