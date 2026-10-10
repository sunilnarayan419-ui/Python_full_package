"""
TOPIC: enumerate()

MAIN POINTS
- enumerate() yields index-value pairs.
- Its default starting index is zero.
- Use start=1 for one-based numbering.
- It returns an iterator, so values are generated as needed.
- It is useful for numbering biological records and identifying sequence positions.
"""

# Example 1: Number gene records.
genes = ["BRCA1", "TP53", "EGFR", "MYC"]

for index, gene in enumerate(genes):
    print(index, gene)

# Example 2: Use one-based numbering.
for number, gene in enumerate(genes, start=1):
    print(f"Gene {number}: {gene}")

# Example 3: Find guanine positions in DNA.
dna_sequence = "ATGCGTAC"

for index, nucleotide in enumerate(dna_sequence):
    if nucleotide == "G":
        print(
            "Zero-based index:", index,
            "One-based position:", index + 1
        )

# Example 4: Number expression records.
expression_values = [24.6, 18.2, 42.8]

for sample_number, expression in enumerate(expression_values, start=1):
    print(f"Sample {sample_number}: {expression}")

# Example 5: Find the first sequence of sufficient length.
sequences = ["ATGC", "ATGCGTAC", "GCTA"]

for number, sequence in enumerate(sequences, start=1):
    if len(sequence) >= 8:
        print("First qualifying record:", number, sequence)
        break