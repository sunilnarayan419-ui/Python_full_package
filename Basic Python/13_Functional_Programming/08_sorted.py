"""
TOPIC: sorted()

MAIN POINTS
- sorted() returns a new list containing items in sorted order.
- The original iterable is not modified.
- reverse=True sorts in descending order.
- key= specifies a function used to determine sorting order.
- sorted() can order genes by expression, samples by quality metrics, and sequences by length.
- Python sorting is stable: items with equal keys preserve their relative order.
- Sorting materializes the results into a list, unlike lazy map() and filter().
"""

# Example 1: Sort DNA sequences alphabetically.
dna_sequences = [
    "TTAGGCAT",
    "ATGCGTAC",
    "CGATCGAT",
    "GGCCATTA"
]

alphabetical_sequences = sorted(dna_sequences)

print("Alphabetically sorted sequences:")
print(alphabetical_sequences)

# The original list remains unchanged.
print("Original list:")
print(dna_sequences)


# Example 2: Sort gene expression values.
expression_values = [24.6, 18.2, 42.8, 35.1]

print("\nAscending expression:")
print(sorted(expression_values))

print("Descending expression:")
print(sorted(expression_values, reverse=True))


# Example 3: Sort sequences by length.
dna_sequences = [
    "ATGC",
    "ATGCGTAC",
    "GCTA",
    "ATGCGCGTAA"
]

sequences_by_length = sorted(
    dna_sequences,
    key=len
)

print("\nSequences sorted by length:")
print(sequences_by_length)


# Example 4: Sort gene records by expression.
gene_expression = [
    {"gene": "BRCA1", "expression": 24.6},
    {"gene": "TP53", "expression": 18.2},
    {"gene": "EGFR", "expression": 42.8},
    {"gene": "MYC", "expression": 35.1}
]

ranked_genes = sorted(
    gene_expression,
    key=lambda record: record["expression"],
    reverse=True
)

print("\nGenes ranked by expression:")

for rank, record in enumerate(ranked_genes, start=1):
    print(
        f"{rank}. {record['gene']}: "
        f"{record['expression']}"
    )


# Example 5: Sort sample records by multiple criteria.
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

print("\nSamples ranked by purity and concentration:")

for sample in ranked_samples:
    print(sample)