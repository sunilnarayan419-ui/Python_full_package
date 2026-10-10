
"""
09. Lambda Functions

Main points
- A lambda creates a small anonymous function.
- Syntax: lambda parameters: expression.
- A lambda contains one expression, not a block of statements.
- The expression's result is returned automatically.
- Lambdas are useful for short transformations and sorting keys.
- Use def when a function requires multiple statements, documentation,
  or substantial logic.
"""

# Example 1: Convert a temperature measurement.
celsius_to_fahrenheit = lambda celsius: (celsius * 9 / 5) + 32

print("Temperature:", celsius_to_fahrenheit(25), "F")

# Example 2: Calculate a simple fold change.
fold_change = lambda treated, control: treated / control

print("Fold change:", fold_change(20.0, 5.0))

# Example 3: Sort genes by expression level.
expression_data = [
    ("TP53", 12.5),
    ("BRCA1", 8.2),
    ("EGFR", 18.4)
]

sorted_genes = sorted(
    expression_data,
    key=lambda record: record[1]
)

print("Genes sorted by expression:", sorted_genes)

# Example 4: Sort from highest to lowest expression.
sorted_genes_descending = sorted(
    expression_data,
    key=lambda record: record[1],
    reverse=True
)

print("Descending order:", sorted_genes_descending)

# Example 5: Apply a lambda to each measurement.
measurements = [2.0, 4.0, 6.0, 8.0]

scaled_measurements = list(
    map(lambda value: value * 1000, measurements)
)

print("Scaled measurements:", scaled_measurements)

# Note: Division by zero must be handled if control expression can be zero.
