"""
TOPIC: reduce()

MAIN POINTS
- reduce() repeatedly combines items to produce one accumulated result.
- It is available from the functools module.
- Syntax: reduce(function, iterable, initial_value).
- The function receives an accumulated value and the next item.
- Without an initial value, the first item becomes the initial accumulator.
- An empty iterable without an initial value raises TypeError.
- sum(), min(), max(), and other built-ins are usually preferable for common operations.
- reduce() is useful when a custom cumulative operation is required.
"""

from functools import reduce


# Example 1: Calculate total nucleotide count across sequences.
dna_sequences = [
    "ATGC",
    "GCTA",
    "CCGG",
    "TTAA"
]

total_nucleotides = reduce(
    lambda total, sequence: total + len(sequence),
    dna_sequences,
    0
)

print("Total nucleotides:", total_nucleotides)


# Example 2: Combine nucleotide counts.
def count_nucleotides(counts, sequence):
    for nucleotide in sequence:
        if nucleotide in counts:
            counts[nucleotide] += 1

    return counts


dna_sequences = [
    "ATGC",
    "GGCC",
    "ATAT"
]

initial_counts = {
    "A": 0,
    "T": 0,
    "G": 0,
    "C": 0
}

nucleotide_counts = reduce(
    count_nucleotides,
    dna_sequences,
    initial_counts
)

print("\nNucleotide counts:")
print(nucleotide_counts)


# Example 3: Calculate the product of relative fold changes.
fold_changes = [1.5, 2.0, 0.5]

combined_fold_change = reduce(
    lambda accumulated, value: accumulated * value,
    fold_changes,
    1.0
)

print("\nCombined multiplicative factor:")
print(combined_fold_change)


# Example 4: Find the maximum expression value using reduce().
expression_values = [24.6, 18.2, 42.8, 35.1]

maximum_expression = reduce(
    lambda current_max, value: (
        value if value > current_max else current_max
    ),
    expression_values
)

print("\nMaximum expression:", maximum_expression)


# Example 5: Merge gene expression dictionaries.
expression_batch_1 = {
    "BRCA1": 24.6,
    "TP53": 18.2
}

expression_batch_2 = {
    "EGFR": 42.8,
    "MYC": 35.1
}

merged_expression = reduce(
    lambda combined, current: combined | current,
    [expression_batch_1, expression_batch_2],
    {}
)

print("\nMerged expression records:")
print(merged_expression)


# Prefer a built-in when the operation is already supported.
print("\nTotal expression:", sum(expression_values))
print("Maximum expression:", max(expression_values))