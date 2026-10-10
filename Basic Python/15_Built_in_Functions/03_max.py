"""
TOPIC: max()

MAIN POINTS
- max() returns the largest item or value.
- It can accept multiple positional arguments or one iterable.
- key= determines the comparison value.
- default= supplies a fallback when an iterable is empty.
- max() is useful for finding the highest expression measurement or longest sequence.
- The largest numerical measurement is not automatically the most biologically significant result.
"""

# Example 1: Highest gene-expression measurement.
expression_values = [24.6, 18.2, 42.8, 35.1]

print("Maximum expression:", max(expression_values))

# Example 2: Longest DNA sequence.
dna_sequences = ["ATGC", "ATGCGTAC", "GCTA", "GGCCATTA"]

longest_sequence = max(dna_sequences, key=len)

print("Longest sequence:", longest_sequence)
print("Length:", len(longest_sequence))

# Example 3: Gene with the highest expression.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8,
    "MYC": 35.1
}

highest_gene = max(
    gene_expression,
    key=gene_expression.get
)

print("Highest-expression gene:", highest_gene)
print("Expression:", gene_expression[highest_gene])

# Example 4: Highest concentration in a sample dataset.
samples = [
    {"sample_id": "S001", "concentration": 42.5},
    {"sample_id": "S002", "concentration": 58.1},
    {"sample_id": "S003", "concentration": 36.4}
]

highest_sample = max(
    samples,
    key=lambda sample: sample["concentration"]
)

print("Highest-concentration sample:", highest_sample)

# Example 5: Handle an empty iterable.
sequences = []

longest = max(sequences, key=len, default=None)

print("Longest sequence:", longest)