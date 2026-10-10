
"""
03. List Slicing

Main points
- Slicing extracts a portion of a list.
- Syntax: list[start:stop:step].
- The start index is included; the stop index is excluded.
- Omitted boundaries use default values.
- Negative indices count from the end.
- A negative step can reverse the order.
- Slicing creates a new outer list; nested objects are not deep-copied.
"""

gene_names = ["BRCA1", "TP53", "EGFR", "MYC", "APOE", "CFTR"]

# Select a subset
print("First three:", gene_names[0:3])
print("Middle genes:", gene_names[2:5])

# Omitted boundaries
print("First four:", gene_names[:4])
print("From index 3:", gene_names[3:])
print("Entire list:", gene_names[:])

# Step
print("Every second gene:", gene_names[::2])

# Negative slicing
print("Last three genes:", gene_names[-3:])

# Reverse the list order
print("Reversed:", gene_names[::-1])

# Create a sliced list and modify it
selected_genes = gene_names[:3]
selected_genes[0] = "ACTB"

print("Selected genes:", selected_genes)
print("Original genes:", gene_names)
