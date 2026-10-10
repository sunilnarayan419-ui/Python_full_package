"""
TOPIC: Generator Expressions

MAIN POINTS
- Generator expressions create generators using compact comprehension-like syntax.
- Their syntax is (expression for item in iterable).
- Unlike list comprehensions, generator expressions do not construct a list containing every result.
- Values are computed as the generator is consumed.
- Generator expressions are useful with sum(), any(), all(), min(), and max().
- They can reduce memory usage when processing large collections.
- They are particularly useful for sequence statistics, gene expression summaries, and filtering biological records.
- A generator expression is typically consumed only once.
"""

dna_sequences = [
    "ATGCGCGT",
    "TTAGGCAT",
    "CGATCGAT",
    "GGCCATTA"
]

# A list comprehension calculates and stores all lengths.
sequence_lengths = [
    len(sequence)
    for sequence in dna_sequences
]

print("Sequence lengths:", sequence_lengths)

# A generator expression calculates lengths as needed.
length_generator = (
    len(sequence)
    for sequence in dna_sequences
)

print("Generator object:", length_generator)

print("First sequence length:", next(length_generator))
print("Second sequence length:", next(length_generator))

# Consume the remaining values.
print("Remaining lengths:", list(length_generator))


# Calculate the total number of nucleotides without
# constructing a separate list of lengths.
total_nucleotides = sum(
    len(sequence)
    for sequence in dna_sequences
)

print("Total nucleotides:", total_nucleotides)


# Calculate the total number of G and C nucleotides.
total_gc_count = sum(
    sequence.count("G") + sequence.count("C")
    for sequence in dna_sequences
)

print("Total GC nucleotides:", total_gc_count)


# Calculate the average GC percentage across all sequences.
gc_percentages = (
    (
        sequence.count("G") + sequence.count("C")
    ) / len(sequence) * 100
    for sequence in dna_sequences
    if sequence
)

gc_values = list(gc_percentages)

mean_gc_percentage = sum(gc_values) / len(gc_values)

print("Individual GC percentages:", gc_values)
print("Mean GC percentage:", round(mean_gc_percentage, 2))


# Filter sequences lazily by length.
long_sequences = (
    sequence
    for sequence in dna_sequences
    if len(sequence) >= 8
)

print("Sequences with length >= 8:")

for sequence in long_sequences:
    print(sequence)


# Check whether any sequence contains a start codon.
contains_start_codon = any(
    sequence.startswith("ATG")
    for sequence in dna_sequences
)

print("Any sequence starts with ATG:", contains_start_codon)


# Check whether all sequences contain only valid DNA bases.
valid_bases = {"A", "T", "G", "C"}

all_valid = all(
    set(sequence.upper()) <= valid_bases
    for sequence in dna_sequences
)

print("All sequences contain valid DNA bases:", all_valid)