"""
TOPIC: min()

MAIN POINTS
- min() returns the smallest item or value.
- key= allows comparison using a derived property.
- default= provides a fallback for an empty iterable.
- min() is useful for finding minimum expression values, shortest sequences, and lowest sample concentrations.
- A minimum value should be interpreted in the context of the measurement and its units.
"""

# Example 1: Minimum gene expression.
expression_values = [24.6, 18.2, 42.8, 35.1]

print("Minimum expression:", min(expression_values))

# Example 2: Shortest DNA sequence.
dna_sequences = ["ATGC", "ATGCGTAC", "GCTA", "GGCCATTA"]

shortest_sequence = min(dna_sequences, key=len)

print("Shortest sequence:", shortest_sequence)
print("Length:", len(shortest_sequence))

# Example 3: Gene with the lowest expression.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8,
    "MYC": 35.1
}

lowest_gene = min(
    gene_expression,
    key=gene_expression.get
)

print("Lowest-expression gene:", lowest_gene)
print("Expression:", gene_expression[lowest_gene])

# Example 4: Sample with the lowest concentration.
samples = [
    {"sample_id": "S001", "concentration": 42.5},
    {"sample_id": "S002", "concentration": 58.1},
    {"sample_id": "S003", "concentration": 36.4}
]

lowest_sample = min(
    samples,
    key=lambda sample: sample["concentration"]
)

print("Lowest-concentration sample:", lowest_sample)

# Example 5: Handle an empty iterable.
print("Minimum of empty list:", min([], default=None))