"""
TOPIC: List Comprehensions

MAIN POINTS
- List comprehensions create lists using concise syntax.
- Basic syntax: [expression for item in iterable].
- Conditions can filter items: [expression for item in iterable if condition].
- Multiple loops can be included in a comprehension.
- Comprehensions are useful for transforming and filtering biological datasets.
- Use ordinary loops when the logic becomes too complicated to read.
"""

# Example 1: Convert DNA sequences to uppercase.
dna_sequences = [
    "atgcgt",
    "ttaggc",
    "cgatcg"
]

uppercase_sequences = [
    sequence.upper()
    for sequence in dna_sequences
]

print("Uppercase DNA sequences:")
print(uppercase_sequences)


# Example 2: Calculate DNA sequence lengths.
dna_sequences = [
    "ATGC",
    "ATGCGTAC",
    "GCTA",
    "GGCCATTA"
]

sequence_lengths = [
    len(sequence)
    for sequence in dna_sequences
]

print("\nSequence lengths:")
print(sequence_lengths)


# Example 3: Filter sequences containing only valid DNA bases.
valid_bases = {"A", "T", "G", "C"}

dna_sequences = [
    "ATGC",
    "GCTA",
    "ATGX",
    "CCGG",
    ""
]

valid_sequences = [
    sequence
    for sequence in dna_sequences
    if sequence and set(sequence.upper()) <= valid_bases
]

print("\nValid DNA sequences:")
print(valid_sequences)


# Example 4: Calculate GC percentages.
def calculate_gc_percentage(sequence):
    sequence = sequence.upper()

    if not sequence:
        return 0.0

    gc_count = sequence.count("G") + sequence.count("C")

    return gc_count / len(sequence) * 100


gc_percentages = [
    calculate_gc_percentage(sequence)
    for sequence in valid_sequences
]

print("\nGC percentages:")
print(gc_percentages)


# Example 5: Filter and transform in one comprehension.
high_gc_sequences = [
    {
        "sequence": sequence,
        "gc_percentage": calculate_gc_percentage(sequence)
    }
    for sequence in valid_sequences
    if calculate_gc_percentage(sequence) >= 50
]

print("\nSequences with GC percentage >= 50:")
for record in high_gc_sequences:
    print(record)


# Example 6: Nested comprehensions.
# Flatten a collection of DNA sequences into individual nucleotides.
sequence_groups = [
    ["ATGC", "GCTA"],
    ["CCGG", "TTAA"]
]

all_nucleotides = [
    nucleotide
    for group in sequence_groups
    for sequence in group
    for nucleotide in sequence
]

print("\nFlattened nucleotides:")
print(all_nucleotides)