"""
TOPIC: zip()

MAIN POINTS
- zip() combines elements from multiple iterables position by position.
- It returns an iterator of tuples.
- By default, it stops at the shortest iterable.
- strict=True raises ValueError if the iterables have different lengths.
- zip() is useful for pairing sample IDs with measurements.
- Matching list lengths does not guarantee correct biological alignment.
"""

# Example 1: Pair gene IDs with expression values.
gene_ids = ["BRCA1", "TP53", "EGFR"]
expression_values = [24.6, 18.2, 42.8]

for gene, expression in zip(
    gene_ids,
    expression_values,
    strict=True
):
    print(gene, expression)

# Example 2: Construct a dictionary.
expression_dictionary = dict(
    zip(gene_ids, expression_values, strict=True)
)

print(expression_dictionary)

# Example 3: Compare control and treatment measurements.
control = [10.0, 20.0, 30.0]
treatment = [15.0, 18.0, 45.0]

for control_value, treatment_value in zip(
    control,
    treatment,
    strict=True
):
    print("Difference:", treatment_value - control_value)

# Example 4: Combine three columns.
sample_ids = ["S001", "S002"]
concentrations = [42.5, 58.1]
purity_ratios = [1.87, 1.92]

for sample_id, concentration, purity in zip(
    sample_ids,
    concentrations,
    purity_ratios,
    strict=True
):
    print(sample_id, concentration, purity)

# Example 5: Default behavior with unequal lengths.
print(list(zip(["BRCA1", "TP53"], [24.6])))

# Uncomment to raise ValueError.
# print(list(zip(["BRCA1", "TP53"], [24.6], strict=True)))