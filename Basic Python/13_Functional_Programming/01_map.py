"""
TOPIC: map()

MAIN POINTS
- map() applies a function to every item in an iterable.
- Syntax: map(function, iterable).
- It returns a lazy map iterator in Python 3.
- Convert it to list() when you need all results immediately.
- map() is useful for transforming biological measurements and sequences.
- Multiple iterables can be passed if the function accepts corresponding arguments.
"""

# Example 1: Convert DNA sequences to uppercase.
dna_sequences = [
    "atgcgt",
    "ttaggc",
    "cgatcg"
]

uppercase_sequences = map(str.upper, dna_sequences)

print("Uppercase DNA sequences:")
print(list(uppercase_sequences))


# Example 2: Convert gene expression values to floats.
expression_values = ["24.6", "18.2", "42.8", "35.1"]

expression_values = map(float, expression_values)

print("\nNumeric expression values:")
print(list(expression_values))


# Example 3: Calculate DNA sequence lengths.
dna_sequences = [
    "ATGCGTAC",
    "TTAGGCAT",
    "CGATCGAT"
]

sequence_lengths = map(len, dna_sequences)

print("\nDNA sequence lengths:")
print(list(sequence_lengths))


# Example 4: Calculate GC percentages.
def calculate_gc_percentage(sequence):
    sequence = sequence.upper()

    if not sequence:
        return 0.0

    gc_count = sequence.count("G") + sequence.count("C")

    return gc_count / len(sequence) * 100


dna_sequences = [
    "ATGC",
    "GGCC",
    "ATAT",
    "GCGC"
]

gc_percentages = map(
    calculate_gc_percentage,
    dna_sequences
)

print("\nGC percentages:")
print(list(gc_percentages))


# Example 5: Apply a function to multiple iterables.
# Calculate the difference between treated and control expression.
control_expression = [10.0, 20.0, 30.0]
treated_expression = [15.0, 18.0, 45.0]

differences = map(
    lambda treated, control: treated - control,
    treated_expression,
    control_expression
)

print("\nTreatment minus control:")
print(list(differences))