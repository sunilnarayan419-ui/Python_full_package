
"""
09. Sets

Main points
- A set is a collection of unique elements.
- Sets are created using {} or set().
- An empty set must be created using set(), not {}.
- Duplicate elements are automatically removed.
- Sets are unordered and do not support positional indexing.
- Sets support fast membership testing in typical cases.
- Set elements must be hashable.
- Sets are useful for unique gene identifiers and sample deduplication.
"""

# Gene identifiers from an experiment
gene_ids = {"TP53", "BRCA1", "EGFR", "TP53", "MYC"}

print("Unique genes:", gene_ids)
print("Number of unique genes:", len(gene_ids))

# Create an empty set
unique_samples = set()
unique_samples.add("S001")
unique_samples.add("S002")
unique_samples.add("S001")

print("Unique samples:", unique_samples)

# Membership testing
print("TP53 present:", "TP53" in gene_ids)
print("ALK present:", "ALK" in gene_ids)

# Remove a known element
gene_ids.remove("EGFR")
print("After removal:", gene_ids)

# Discard does not raise KeyError if the element is absent
gene_ids.discard("NOT_A_GENE")
print("After discard:", gene_ids)

# Convert a list to a set to remove duplicates
sample_ids = ["S001", "S002", "S001", "S003", "S002"]
unique_sample_ids = set(sample_ids)

print("Unique sample IDs:", unique_sample_ids)

# Sets do not preserve the original list order.
