
"""
08. Packing and Unpacking

Main points
- Packing groups multiple values into a tuple.
- Unpacking assigns iterable elements to multiple variables.
- The number of assigned variables must match the number of elements,
  unless starred unpacking is used.
- *variable captures remaining elements into a list.
- _ is conventionally used for an intentionally ignored value.
- Unpacking is useful for experimental records and multiple return values.
"""

# Example 1: Tuple packing
sample_record = "S001", "TP53", 12.5

print("Packed record:", sample_record)
print("Record type:", type(sample_record))

# Example 2: Unpack sample metadata
sample_id, gene_name, expression = sample_record

print("Sample:", sample_id)
print("Gene:", gene_name)
print("Expression:", expression)

# Example 3: Swap two variables
control_expression = 10.0
treated_expression = 18.0

control_expression, treated_expression = (
    treated_expression,
    control_expression
)

print("First value after swap:", control_expression)
print("Second value after swap:", treated_expression)

# Example 4: Starred unpacking
measurements = (12.5, 14.2, 16.8, 19.1, 20.0)

first, *middle, last = measurements

print("First:", first)
print("Middle:", middle)
print("Last:", last)

# Example 5: Ignore an unneeded field
sample_id, _, concentration = ("S002", "unused", 35.0)

print("Sample:", sample_id)
print("Concentration:", concentration)

# Example 6: A function returning multiple values
def summarize_expression(values):
    return min(values), max(values), sum(values) / len(values)

minimum, maximum, mean = summarize_expression([5.0, 10.0, 15.0])

print("Minimum:", minimum)
print("Maximum:", maximum)
print("Mean:", mean)
