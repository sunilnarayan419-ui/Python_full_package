"""
TOPIC: enumerate()

MAIN POINTS
- enumerate() produces an index-value pair for each item.
- Syntax: enumerate(iterable, start=0).
- The default index begins at zero.
- Use start=1 for human-readable numbering.
- enumerate() is useful for tracking sequence positions and numbering records.
- Python string indices are zero-based, while many biological sequence positions are reported using one-based coordinates.
- Distinguish array indices from biological coordinates.
"""

# Example 1: Number biological samples.
samples = [
    "SAMPLE_001",
    "SAMPLE_002",
    "SAMPLE_003"
]

for index, sample in enumerate(samples):
    print(index, sample)


# Example 2: Number samples starting from one.
for number, sample in enumerate(samples, start=1):
    print(f"Sample {number}: {sample}")


# Example 3: Find the positions of guanine nucleotides.
dna_sequence = "ATGCGTACG"

print("\nGuanine positions:")

for index, nucleotide in enumerate(dna_sequence):
    if nucleotide == "G":
        print(
            f"Zero-based index: {index}, "
            f"one-based position: {index + 1}"
        )


# Example 4: Number gene expression records.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8,
    "MYC": 35.1
}

for number, (gene, expression) in enumerate(
    gene_expression.items(),
    start=1
):
    print(
        f"{number}. {gene}: {expression}"
    )


# Example 5: Identify the first sequence containing a start codon.
dna_sequences = [
    "TTAGGCAT",
    "CGATCGAT",
    "ATGCGTAC",
    "GGCCATTA"
]

for index, sequence in enumerate(dna_sequences):
    if sequence.startswith("ATG"):
        print(
            f"First matching sequence: {sequence}"
        )
        print("List index:", index)
        print("One-based record number:", index + 1)
        break