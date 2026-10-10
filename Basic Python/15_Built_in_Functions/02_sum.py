"""
TOPIC: sum()

MAIN POINTS
- sum() calculates the total of numeric values in an iterable.
- Syntax: sum(iterable, start=0).
- The optional start value determines the initial accumulator.
- sum() works with integers, floats, and other compatible numeric types.
- It is useful for total nucleotide counts, experimental measurements, and gene-expression summaries.
- Use a suitable data type and meaningful units when combining measurements.
"""

# Example 1: Total DNA nucleotides.
sequence_lengths = [120, 250, 180, 400]

total_nucleotides = sum(sequence_lengths)

print("Total nucleotides:", total_nucleotides)

# Example 2: Total gene expression measurements.
expression_values = [24.6, 18.2, 42.8, 35.1]

print("Total expression:", sum(expression_values))

# Example 3: Calculate the mean expression.
mean_expression = sum(expression_values) / len(expression_values)

print("Mean expression:", round(mean_expression, 2))

# Example 4: Sum values from biological records.
samples = [
    {"sample_id": "S001", "dna_mass": 120.5},
    {"sample_id": "S002", "dna_mass": 95.0},
    {"sample_id": "S003", "dna_mass": 145.2}
]

total_dna_mass = sum(
    sample["dna_mass"]
    for sample in samples
)

print("Total DNA mass:", total_dna_mass)

# Example 5: Sum only measurements from treated samples.
measurements = [
    {"condition": "Control", "expression": 10.0},
    {"condition": "Treatment", "expression": 18.5},
    {"condition": "Treatment", "expression": 22.0}
]

treatment_total = sum(
    record["expression"]
    for record in measurements
    if record["condition"] == "Treatment"
)

print("Total treatment expression:", treatment_total)

# Example 6: Empty iterable.
print("Sum of an empty list:", sum([]))