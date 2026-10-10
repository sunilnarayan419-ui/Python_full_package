"""
TOPIC: Multiple Assignment

MAIN POINTS
- Python can assign multiple variables in one statement.
- Multiple assignment can unpack values from an iterable.
- Chained assignment assigns the same object or value to multiple names.
- Tuple unpacking requires the expected number of elements unless starred unpacking is used.
- Multiple assignment is useful for measurements, counters, and sequence statistics.
- Be careful with mutable objects when using chained assignment.
"""

# Example 1: Assign biological metadata.
sample_id, organism, tissue = (
    "S001",
    "Homo sapiens",
    "Blood"
)

print(sample_id)
print(organism)
print(tissue)


# Example 2: Assign multiple measurements.
dna_concentration, purity_ratio, sample_volume = (
    45.2,
    1.87,
    20.0
)

print("\nDNA concentration:", dna_concentration)
print("Purity ratio:", purity_ratio)
print("Sample volume:", sample_volume)


# Example 3: Swap two values.
control_expression = 20.0
treatment_expression = 35.0

control_expression, treatment_expression = (
    treatment_expression,
    control_expression
)

print("\nAfter swapping:")
print("Control variable:", control_expression)
print("Treatment variable:", treatment_expression)


# Example 4: Update multiple counters.
adenine = thymine = guanine = cytosine = 0

dna_sequence = "ATGCGTAC"

adenine = dna_sequence.count("A")
thymine = dna_sequence.count("T")
guanine = dna_sequence.count("G")
cytosine = dna_sequence.count("C")

print("\nNucleotide counts:")
print(adenine, thymine, guanine, cytosine)


# Example 5: Chained assignment with immutable values.
threshold_a = threshold_b = threshold_c = 30

print("\nThresholds:")
print(threshold_a, threshold_b, threshold_c)


# Example 6: Avoid accidental sharing of mutable objects.
# This assigns the same list object to both variables.
sample_A = sample_B = []

sample_A.append("DNA_001")

print("\nShared list:")
print("Sample A:", sample_A)
print("Sample B:", sample_B)

# Use separate assignments when independent lists are required.
sample_A = []
sample_B = []

sample_A.append("DNA_002")

print("\nIndependent lists:")
print("Sample A:", sample_A)
print("Sample B:", sample_B)


# Example 7: Assign a function's multiple return values.
def calculate_sequence_statistics(sequence):
    length = len(sequence)
    gc_count = sequence.count("G") + sequence.count("C")

    gc_percentage = (
        gc_count / length * 100
        if length
        else 0.0
    )

    return length, gc_count, gc_percentage


length, gc_count, gc_percentage = calculate_sequence_statistics(
    "ATGCGCGT"
)

print("\nSequence statistics:")
print(length, gc_count, gc_percentage)