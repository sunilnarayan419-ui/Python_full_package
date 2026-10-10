
"""
04. List Methods

Main points
- append(x) adds one element to the end.
- extend(iterable) adds multiple elements.
- insert(index, x) inserts an element at a position.
- remove(x) removes the first matching value.
- pop(index) removes and returns an element.
- sort() sorts the list in place.
- reverse() reverses the list in place.
- count(x) counts occurrences.
- index(x) returns the first matching index.
- clear() removes all elements.
- Most mutating list methods modify the existing list and return None.
"""

gene_names = ["TP53", "BRCA1", "EGFR"]

# Append one gene
gene_names.append("MYC")
print("After append:", gene_names)

# Extend with multiple genes
gene_names.extend(["APOE", "CFTR"])
print("After extend:", gene_names)

# Insert a gene at an index
gene_names.insert(1, "GAPDH")
print("After insert:", gene_names)

# Count occurrences
gene_names.append("TP53")
print("TP53 occurrences:", gene_names.count("TP53"))

# Find an index
print("BRCA1 index:", gene_names.index("BRCA1"))

# Remove the first matching value
gene_names.remove("TP53")
print("After remove:", gene_names)

# Remove and return the last element
removed_gene = gene_names.pop()
print("Removed gene:", removed_gene)
print("Remaining genes:", gene_names)

# Sort alphabetically in place
gene_names.sort()
print("Sorted genes:", gene_names)

# Reverse in place
gene_names.reverse()
print("Reversed genes:", gene_names)

# Clear all elements
gene_names.clear()
print("After clear:", gene_names)
