"""
TOPIC: sorted()

MAIN POINTS
- sorted() returns a new list containing items in sorted order.
- The original iterable remains unchanged.
- reverse=True sorts in descending order.
- key= determines the value used for comparisons.
- Sorting is stable when multiple items have equal keys.
- sorted() is useful for ranking genes, samples, and sequences.
"""

# Example 1: Sort numerical measurements.
expression_values = [24.6, 18.2, 42.8, 35.1]

print("Ascending:", sorted(expression_values))
print("Descending:", sorted(expression_values, reverse=True))

# Example 2: Sort DNA sequences by length.
dna_sequences = ["ATGC", "ATGCGTAC", "GCTA", "GGCCATTA"]

print(
    "Sequences by length:",
    sorted(dna_sequences, key=len)
)

# Example 3: Rank genes by expression.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8,
    "MYC": 35.1
}

ranked_genes = sorted(
    gene_expression.items(),
    key=lambda item: item[1],
    reverse=True
)

for rank, (gene, expression) in enumerate(ranked_genes, start=1):
    print(f"{rank}. {gene}: {expression}")

# Example 4: Sort samples using multiple criteria.
samples = [
    {"sample_id": "S001", "purity": 1.91, "concentration": 42.5},
    {"sample_id": "S002", "purity": 1.91, "concentration": 58.1},
    {"sample_id": "S003", "purity": 1.86, "concentration": 36.4}
]

ranked_samples = sorted(
    samples,
    key=lambda sample: (
        sample["purity"],
        sample["concentration"]
    ),
    reverse=True
)

print("\nRanked samples:")
for sample in ranked_samples:
    print(sample)

# Example 5: Sorting does not modify the original list.
original = [3, 1, 2]
result = sorted(original)

print("Original:", original)
print("Sorted copy:", result)