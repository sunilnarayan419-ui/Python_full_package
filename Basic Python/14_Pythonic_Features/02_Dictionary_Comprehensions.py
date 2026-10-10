"""
TOPIC: Dictionary Comprehensions

MAIN POINTS
- Dictionary comprehensions create dictionaries concisely.
- Basic syntax: {key: value for item in iterable}.
- Conditions can filter dictionary entries.
- Dictionary comprehensions are useful for constructing lookup tables.
- Keys must be unique; duplicate keys overwrite previous values.
- They are useful for gene-expression mappings, sequence metadata, and sample registries.
"""

# Example 1: Map gene IDs to expression measurements.
gene_ids = ["BRCA1", "TP53", "EGFR", "MYC"]

expression_values = [24.6, 18.2, 42.8, 35.1]

gene_expression = {
    gene: expression
    for gene, expression in zip(
        gene_ids,
        expression_values,
        strict=True
    )
}

print("Gene expression dictionary:")
print(gene_expression)


# Example 2: Calculate DNA sequence lengths.
dna_sequences = {
    "Gene_A": "ATGC",
    "Gene_B": "ATGCGTAC",
    "Gene_C": "GCTA"
}

sequence_lengths = {
    gene: len(sequence)
    for gene, sequence in dna_sequences.items()
}

print("\nSequence lengths:")
print(sequence_lengths)


# Example 3: Filter genes by expression.
high_expression_genes = {
    gene: expression
    for gene, expression in gene_expression.items()
    if expression >= 30
}

print("\nGenes with expression >= 30:")
print(high_expression_genes)


# Example 4: Calculate GC percentages for multiple sequences.
def gc_percentage(sequence):
    if not sequence:
        return 0.0

    sequence = sequence.upper()
    gc_count = sequence.count("G") + sequence.count("C")

    return gc_count / len(sequence) * 100


sequence_gc = {
    gene: gc_percentage(sequence)
    for gene, sequence in dna_sequences.items()
}

print("\nGC percentages:")
print(sequence_gc)


# Example 5: Construct a sample registry.
samples = [
    {
        "sample_id": "S001",
        "organism": "Homo sapiens",
        "tissue": "Blood"
    },
    {
        "sample_id": "S002",
        "organism": "Mus musculus",
        "tissue": "Liver"
    },
    {
        "sample_id": "S003",
        "organism": "Arabidopsis thaliana",
        "tissue": "Root"
    }
]

sample_registry = {
    sample["sample_id"]: sample
    for sample in samples
}

print("\nSample registry:")
print(sample_registry)

print("S002 organism:", sample_registry["S002"]["organism"])


# Example 6: Normalize expression relative to the maximum.
maximum_expression = max(gene_expression.values())

relative_expression = {
    gene: expression / maximum_expression
    for gene, expression in gene_expression.items()
}

print("\nRelative expression:")
print(relative_expression)