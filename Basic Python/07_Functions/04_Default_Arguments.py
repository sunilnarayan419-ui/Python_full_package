
"""
04. Default Arguments

Main points
- A default argument provides a value when the caller omits that argument.
- Parameters with defaults must follow parameters without defaults.
- The caller can override a default value.
- Default expressions are evaluated once when the function is defined.
- Avoid mutable defaults such as [] or {} when fresh state is intended.
- Use None as a default when a new mutable object should be created per call.
"""

# Example 1: Default temperature for a sample report.
def describe_temperature(temperature_celsius, unit="C"):
    return f"Temperature: {temperature_celsius} °{unit}"


print(describe_temperature(25))
print(describe_temperature(37, "C"))
print(describe_temperature(77, "F"))

# Example 2: Default threshold for a simple expression filter.
def is_high_expression(expression, threshold=10.0):
    return expression > threshold


print(is_high_expression(12.5))
print(is_high_expression(12.5, 15.0))

# Example 3: Avoid a mutable default argument.
def add_gene(gene, gene_list=None):
    if gene_list is None:
        gene_list = []

    gene_list.append(gene)
    return gene_list


first_list = add_gene("TP53")
second_list = add_gene("BRCA1")

print("First list:", first_list)
print("Second list:", second_list)

# Each call creates a separate list when gene_list is omitted.

# Example 4: A supplied list can still be reused intentionally.
existing_genes = ["EGFR"]

updated_genes = add_gene("MYC", existing_genes)

print("Updated existing list:", updated_genes)
print("Original reference:", existing_genes)
