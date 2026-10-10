"""
TOPIC: filter()

MAIN POINTS
- filter() selects items from an iterable based on a function.
- Syntax: filter(function, iterable).
- The function should return a truthy or falsy result.
- filter() returns a lazy iterator in Python 3.
- filter(None, iterable) retains truthy elements.
- It is useful for selecting genes, DNA sequences, and samples that satisfy criteria.
"""

# Example 1: Select DNA sequences containing a start codon.
dna_sequences = [
    "ATGCGTAC",
    "TTAGGCAT",
    "ATGCCGTA",
    "CGATCGAT"
]

def contains_start_codon(sequence):
    return sequence.startswith("ATG")


coding_candidates = filter(
    contains_start_codon,
    dna_sequences
)

print("Sequences beginning with ATG:")
print(list(coding_candidates))


# Example 2: Select genes with high expression.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8,
    "MYC": 35.1,
    "GAPDH": 8.4
}

high_expression_genes = filter(
    lambda item: item[1] >= 30,
    gene_expression.items()
)

print("\nGenes with expression >= 30:")
print(list(high_expression_genes))


# Example 3: Select samples passing a quality threshold.
samples = [
    {"sample_id": "S001", "purity": 1.91},
    {"sample_id": "S002", "purity": 1.52},
    {"sample_id": "S003", "purity": 1.86},
    {"sample_id": "S004", "purity": 2.10}
]

def passes_purity_threshold(sample):
    return 1.8 <= sample["purity"] <= 2.0


qualified_samples = filter(
    passes_purity_threshold,
    samples
)

print("\nSamples within the illustrative purity range:")
for sample in qualified_samples:
    print(sample)


# Example 4: Remove empty sequence records.
sequences = [
    "ATGC",
    "",
    "GCTA",
    "",
    "CCGG"
]

non_empty_sequences = filter(None, sequences)

print("\nNon-empty sequences:")
print(list(non_empty_sequences))


# Example 5: Filter and then transform.
dna_sequences = [
    "ATGCGT",
    "TTAGGC",
    "ATGCCG",
    "CGATCG"
]

selected_lengths = map(
    len,
    filter(contains_start_codon, dna_sequences)
)

print("\nLengths of selected sequences:")
print(list(selected_lengths))