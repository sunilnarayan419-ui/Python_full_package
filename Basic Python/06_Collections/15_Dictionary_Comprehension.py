
"""
15. Dictionary Comprehension

Main points
- Dictionary comprehensions create dictionaries using a concise expression.
- Basic syntax: {key_expression: value_expression for item in iterable}.
- Conditions can filter entries.
- Duplicate generated keys overwrite earlier values.
- Dictionary comprehensions are useful for transforming annotations,
  mapping identifiers, and filtering measurements.
- For complex transformations, a regular loop may be easier to read.
"""

# Example 1: Map genes to their expression values
genes = ["TP53", "BRCA1", "EGFR"]
expression_values = [12.5, 8.2, 18.4]

expression_map = {
    gene: value
    for gene, value in zip(genes, expression_values)
}

print("Expression map:", expression_map)

# Example 2: Convert expression values to a different scale
expression_map_scaled = {
    gene: value / 10
    for gene, value in expression_map.items()
}

print("Scaled expression:", expression_map_scaled)

# Example 3: Keep only genes above a threshold
high_expression_genes = {
    gene: value
    for gene, value in expression_map.items()
    if value > 10
}

print("High-expression genes:", high_expression_genes)

# Example 4: Generate sample identifiers
sample_numbers = range(1, 5)

sample_map = {
    number: f"S{number:03d}"
    for number in sample_numbers
}

print("Sample map:", sample_map)

# Example 5: Build nucleotide counts from a DNA sequence
dna_sequence = "ATGCGTAA"

nucleotide_counts = {
    nucleotide: dna_sequence.count(nucleotide)
    for nucleotide in set(dna_sequence)
}

print("Nucleotide counts:", nucleotide_counts)

# Example 6: Invert a mapping when values are unique
gene_to_id = {
    "TP53": "G001",
    "BRCA1": "G002",
    "EGFR": "G003"
}

id_to_gene = {
    identifier: gene
    for gene, identifier in gene_to_id.items()
}

print("ID-to-gene mapping:", id_to_gene)

# Important:
# If multiple genes share the same value in an inverted mapping,
# earlier entries can be overwritten. Check uniqueness before inverting.
