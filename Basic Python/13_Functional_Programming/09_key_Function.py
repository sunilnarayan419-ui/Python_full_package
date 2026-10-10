"""
TOPIC: Key Functions

MAIN POINTS
- The key parameter accepts a function that determines how values are compared.
- It is commonly used with sorted(), min(), and max().
- The key function receives one item and returns its comparison value.
- lambda expressions are useful for short key functions.
- Named functions are clearer when the comparison logic is complex.
- A key function can extract nested dictionary values or calculate derived properties.
- Key functions help rank biological records according to scientific measurements.
"""

# Example 1: Find the longest DNA sequence.
dna_sequences = [
    "ATGC",
    "ATGCGTAC",
    "GCTA",
    "ATGCGCGTAA"
]

longest_sequence = max(
    dna_sequences,
    key=len
)

print("Longest DNA sequence:", longest_sequence)
print("Length:", len(longest_sequence))


# Example 2: Find the shortest sequence.
shortest_sequence = min(
    dna_sequences,
    key=len
)

print("\nShortest DNA sequence:", shortest_sequence)
print("Length:", len(shortest_sequence))


# Example 3: Rank genes by expression.
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

for record in ranked_genes:
    print(record["gene"], record["expression"])


# Example 4: Use a named function for a more readable key.
def gc_percentage(sequence):
    if not sequence:
        return 0.0

    sequence = sequence.upper()

    gc_count = sequence.count("G") + sequence.count("C")

    return gc_count / len(sequence) * 100


dna_sequences = [
    "ATATAT",
    "GCGCGC",
    "ATGCGT",
    "GGCCATTA"
]

ranked_by_gc = sorted(
    dna_sequences,
    key=gc_percentage,
    reverse=True
)

print("\nSequences ranked by GC percentage:")

for sequence in ranked_by_gc:
    print(
        sequence,
        round(gc_percentage(sequence), 2)
    )


# Example 5: Rank samples by quality and then concentration.
samples = [
    {"sample_id": "S001", "purity": 1.91, "concentration": 42.5},
    {"sample_id": "S002", "purity": 1.91, "concentration": 58.1},
    {"sample_id": "S003", "purity": 1.86, "concentration": 36.4},
    {"sample_id": "S004", "purity": 1.98, "concentration": 31.2}
]

def sample_ranking_key(sample):
    return (
        sample["purity"],
        sample["concentration"]
    )


ranked_samples = sorted(
    samples,
    key=sample_ranking_key,
    reverse=True
)

print("\nRanked samples:")

for sample in ranked_samples:
    print(
        sample["sample_id"],
        sample_ranking_key(sample)
    )


# Example 6: Use a key function with min() and max().
highest_expression_gene = max(
    gene_expression,
    key=lambda record: record["expression"]
)

lowest_expression_gene = min(
    gene_expression,
    key=lambda record: record["expression"]
)

print("\nHighest expression gene:", highest_expression_gene["gene"])
print("Lowest expression gene:", lowest_expression_gene["gene"])