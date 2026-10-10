
"""
04. Nested Loops

Main points
- A nested loop is a loop inside another loop.
- The inner loop runs for each iteration of the outer loop.
- With n outer iterations and m inner iterations, the body may execute
  n * m times.
- Nested loops are useful for comparing samples, sequences, and matrices.
- Large nested loops can be computationally expensive.
- Use clear variable names to distinguish outer and inner iterations.
"""

# Example 1: Compare every pair of biological samples.
sample_ids = ["S001", "S002", "S003"]

for sample_a in sample_ids:
    for sample_b in sample_ids:
        print("Comparing:", sample_a, "with", sample_b)

# Example 2: Generate a simple gene-by-sample expression table.
genes = ["GeneA", "GeneB", "GeneC"]
samples = ["Control", "Treatment"]

for gene in genes:
    for sample in samples:
        print(f"{gene} in {sample}")

# Example 3: Count nucleotides in multiple DNA sequences.
dna_sequences = [
    "ATGC",
    "AATT",
    "CCGG"
]

for sequence_number, sequence in enumerate(dna_sequences, start=1):
    print("Sequence", sequence_number)

    for nucleotide in sequence:
        print(" ", nucleotide)

# Example 4: Calculate pairwise differences between short sequences.
sequences = ["ATGC", "ATGT", "TTGC"]

for i in range(len(sequences)):
    for j in range(i + 1, len(sequences)):
        differences = sum(
            base_a != base_b
            for base_a, base_b in zip(sequences[i], sequences[j])
        )

        print(
            sequences[i],
            "vs",
            sequences[j],
            "differences:",
            differences
        )

# This simple comparison assumes equal-length sequences.
# Real sequence alignment may require gap handling and alignment algorithms.
