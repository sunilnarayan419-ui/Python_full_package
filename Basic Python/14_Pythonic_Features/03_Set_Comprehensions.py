"""
TOPIC: Set Comprehensions

MAIN POINTS
- Set comprehensions create sets using concise syntax.
- Basic syntax: {expression for item in iterable}.
- Sets store unique elements and remove duplicates.
- Sets are unordered; do not rely on their display order.
- Conditions can filter elements.
- Sets support union, intersection, and difference.
- They are useful for unique nucleotide types, gene IDs, and comparing datasets.
"""

# Example 1: Extract unique nucleotides.
dna_sequence = "ATGCGCGTAT"

unique_bases = {
    nucleotide
    for nucleotide in dna_sequence
}

print("Unique nucleotides:")
print(unique_bases)


# Example 2: Extract unique GC bases from multiple sequences.
dna_sequences = [
    "ATGC",
    "GGCC",
    "ATAT",
    "GCGC"
]

unique_gc_bases = {
    nucleotide
    for sequence in dna_sequences
    for nucleotide in sequence
    if nucleotide in {"G", "C"}
}

print("\nUnique GC bases:")
print(unique_gc_bases)


# Example 3: Extract unique gene identifiers.
gene_records = [
    {"gene": "BRCA1", "expression": 24.6},
    {"gene": "TP53", "expression": 18.2},
    {"gene": "BRCA1", "expression": 26.1},
    {"gene": "EGFR", "expression": 42.8}
]

unique_gene_ids = {
    record["gene"]
    for record in gene_records
}

print("\nUnique gene identifiers:")
print(unique_gene_ids)


# Example 4: Find genes shared between two experiments.
experiment_A = {
    "BRCA1",
    "TP53",
    "EGFR",
    "MYC"
}

experiment_B = {
    "TP53",
    "EGFR",
    "KRAS",
    "BRAF"
}

shared_genes = {
    gene
    for gene in experiment_A
    if gene in experiment_B
}

print("\nShared genes:")
print(shared_genes)


# Example 5: Find genes unique to experiment A.
unique_to_A = {
    gene
    for gene in experiment_A
    if gene not in experiment_B
}

print("\nGenes unique to experiment A:")
print(unique_to_A)


# Example 6: Set operations provide concise alternatives.
print("\nIntersection:", experiment_A & experiment_B)
print("Union:", experiment_A | experiment_B)
print("Difference:", experiment_A - experiment_B)