
"""
07. Tuple Operations

Main points
- Tuples support indexing and slicing.
- The + operator concatenates tuples.
- The * operator repeats tuple elements.
- in and not in check membership.
- count() counts occurrences.
- index() returns the first matching position.
- len() returns the number of elements.
- Tuples are immutable, so their elements cannot be reassigned.
"""

gene_panel = ("TP53", "BRCA1", "EGFR", "MYC")

# Indexing
print("First gene:", gene_panel[0])
print("Last gene:", gene_panel[-1])

# Slicing
print("First two genes:", gene_panel[:2])

# Concatenation
additional_genes = ("APOE", "CFTR")
combined_panel = gene_panel + additional_genes

print("Combined panel:", combined_panel)

# Repetition
replicated_labels = ("control",) * 3
print("Labels:", replicated_labels)

# Membership
print("TP53 included:", "TP53" in gene_panel)
print("ALK excluded:", "ALK" not in gene_panel)

# Counting and finding
repeated_values = ("A", "T", "A", "G", "A")

print("Count of A:", repeated_values.count("A"))
print("First G index:", repeated_values.index("G"))

# Length
print("Panel size:", len(gene_panel))
