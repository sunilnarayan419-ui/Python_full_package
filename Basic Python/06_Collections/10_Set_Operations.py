
"""
10. Set Operations

Main points
- Union (|) combines elements from both sets.
- Intersection (&) returns elements common to both sets.
- Difference (-) returns elements present in the first set but not the second.
- Symmetric difference (^) returns elements present in exactly one set.
- issubset() checks whether one set is contained in another.
- issuperset() checks whether a set contains another set.
- isdisjoint() checks whether two sets have no common elements.
- These operations are useful for comparing gene panels and experimental groups.
"""

# Genes identified in two experimental conditions
control_genes = {"TP53", "BRCA1", "EGFR", "MYC"}
treated_genes = {"TP53", "EGFR", "APOE", "CFTR"}

# Union: genes found in either group
all_genes = control_genes | treated_genes
print("All genes:", all_genes)

# Intersection: shared genes
shared_genes = control_genes & treated_genes
print("Shared genes:", shared_genes)

# Difference: genes found only in the control set
control_only = control_genes - treated_genes
print("Control-only genes:", control_only)

# Difference: genes found only in the treated set
treated_only = treated_genes - control_genes
print("Treated-only genes:", treated_only)

# Symmetric difference: genes unique to either group
unique_to_one_group = control_genes ^ treated_genes
print("Genes unique to one group:", unique_to_one_group)

# Subset and superset checks
core_genes = {"TP53", "EGFR"}

print("Core genes are a subset:", core_genes.issubset(all_genes))
print("All genes contain core genes:", all_genes.issuperset(core_genes))

# Disjointness
housekeeping_genes = {"ACTB", "GAPDH"}
print("Disjoint gene sets:", housekeeping_genes.isdisjoint(core_genes))

# Important:
# Different detection lists do not automatically imply differential
# expression or biological significance.
