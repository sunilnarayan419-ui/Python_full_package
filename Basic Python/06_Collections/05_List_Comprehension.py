
"""
05. List Comprehension

Main points
- List comprehensions create lists from iterables.
- Basic syntax: [expression for item in iterable].
- Conditions can filter elements.
- Syntax with filtering: [expression for item in iterable if condition].
- Expressions can transform each element.
- Nested comprehensions are possible but can become difficult to read.
- Use comprehensions for concise transformations, not at the expense of clarity.
"""

# Example 1: Convert DNA sequences to uppercase
sequences = ["atgc", "ggta", "ccga"]

uppercase_sequences = [sequence.upper() for sequence in sequences]
print("Uppercase sequences:", uppercase_sequences)

# Example 2: Select high gene-expression measurements
expression_values = [2.1, 15.5, 8.4, 22.0, 17.2]

high_expression = [
    value for value in expression_values
    if value > 10
]

print("High expression:", high_expression)

# Example 3: Transform concentrations
concentrations_mg = [1.0, 2.5, 3.2, 4.8]

concentrations_g = [
    value / 1000 for value in concentrations_mg
]

print("Concentrations in grams:", concentrations_g)

# Example 4: Extract gene identifiers
gene_records = [
    {"gene": "TP53", "expression": 12.5},
    {"gene": "BRCA1", "expression": 8.2},
    {"gene": "EGFR", "expression": 18.4}
]

gene_names = [record["gene"] for record in gene_records]
print("Gene names:", gene_names)

# Example 5: Filter records and transform values
high_expression_genes = [
    record["gene"]
    for record in gene_records
    if record["expression"] > 10
]

print("High-expression genes:", high_expression_genes)

# Example 6: Generate squared values for a simple model
time_points = [1, 2, 3, 4]

squared_times = [time ** 2 for time in time_points]
print("Squared time points:", squared_times)
