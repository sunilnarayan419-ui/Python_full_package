
"""
11. Set Methods

Main points
- add(x) adds one element.
- update(iterable) adds multiple elements.
- remove(x) removes an element and raises KeyError if it is absent.
- discard(x) removes an element without raising KeyError if absent.
- pop() removes and returns an arbitrary element.
- clear() removes all elements.
- intersection_update() retains only common elements.
- difference_update() removes elements found in another collection.
- symmetric_difference_update() retains elements found in exactly one set.
- Mutating set methods generally return None.
"""

detected_genes = {"TP53", "BRCA1", "EGFR"}

# Add one gene
detected_genes.add("MYC")
print("After add:", detected_genes)

# Add multiple genes
detected_genes.update(["APOE", "CFTR", "MYC"])
print("After update:", detected_genes)

# Remove a known gene
detected_genes.remove("EGFR")
print("After remove:", detected_genes)

# Discard an absent gene safely
detected_genes.discard("UNKNOWN")
print("After discard:", detected_genes)

# Retain only genes found in a reference panel
reference_panel = {"TP53", "BRCA1", "MYC"}

filtered_genes = detected_genes.copy()
filtered_genes.intersection_update(reference_panel)

print("Reference-panel overlap:", filtered_genes)

# Remove genes belonging to a reference set
genes_to_exclude = {"BRCA1"}

remaining_genes = detected_genes.copy()
remaining_genes.difference_update(genes_to_exclude)

print("After exclusion:", remaining_genes)

# Symmetric difference update
set_a = {"TP53", "BRCA1"}
set_b = {"BRCA1", "EGFR"}

set_a.symmetric_difference_update(set_b)
print("Symmetric difference:", set_a)

# Pop removes an arbitrary element; its identity is not guaranteed.
temporary_set = {"S001", "S002", "S003"}
removed_item = temporary_set.pop()

print("Removed item:", removed_item)
print("Remaining items:", temporary_set)

# Clear all elements
temporary_set.clear()
print("Cleared set:", temporary_set)
