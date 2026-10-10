"""
TOPIC: zip()

MAIN POINTS
- zip() combines corresponding elements from multiple iterables.
- It returns a lazy iterator of tuples.
- By default, iteration stops when the shortest iterable is exhausted.
- Use strict=True in Python 3.10+ when equal iterable lengths are required.
- zip() is useful for associating gene IDs with expression values or sample IDs with measurements.
- Incorrect ordering or mismatched lengths can produce incorrect scientific analyses.
"""

# Example 1: Associate gene IDs with expression values.
gene_ids = ["BRCA1", "TP53", "EGFR", "MYC"]
expression_values = [24.6, 18.2, 42.8, 35.1]

gene_expression = zip(
    gene_ids,
    expression_values
)

print("Gene expression records:")
for gene, expression in gene_expression:
    print(f"{gene}: {expression}")


# Example 2: Build a dictionary from two lists.
gene_ids = ["BRCA1", "TP53", "EGFR"]
expression_values = [24.6, 18.2, 42.8]

expression_dictionary = dict(
    zip(gene_ids, expression_values)
)

print("\nExpression dictionary:")
print(expression_dictionary)


# Example 3: Compare control and treatment measurements.
control = [10.0, 20.0, 30.0]
treatment = [15.0, 18.0, 45.0]

comparisons = zip(control, treatment)

print("\nControl versus treatment:")
for control_value, treatment_value in comparisons:
    difference = treatment_value - control_value

    print(
        f"Control={control_value}, "
        f"Treatment={treatment_value}, "
        f"Difference={difference}"
    )


# Example 4: Combine three experimental columns.
sample_ids = ["S001", "S002", "S003"]
dna_concentrations = [42.5, 58.1, 36.4]
purity_ratios = [1.87, 1.92, 1.75]

for sample_id, concentration, purity in zip(
    sample_ids,
    dna_concentrations,
    purity_ratios,
    strict=True
):
    print(
        sample_id,
        concentration,
        purity
    )


# Example 5: Understand unequal lengths.
gene_ids = ["BRCA1", "TP53", "EGFR"]
expression_values = [24.6, 18.2]

# Default zip() silently stops at the shortest iterable.
print("\nDefault zip:")
print(list(zip(gene_ids, expression_values)))

# Uncomment to raise ValueError for unequal lengths.
# print(list(zip(gene_ids, expression_values, strict=True)))