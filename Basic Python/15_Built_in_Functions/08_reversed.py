"""
TOPIC: reversed()

MAIN POINTS
- reversed() returns an iterator that yields elements in reverse order.
- It does not automatically create a reversed list.
- It works with reversible objects such as lists, tuples, and strings.
- Convert the result to list() when you need a list.
- Reversing a DNA string changes its order, but does not calculate its reverse complement.
"""

# Example 1: Reverse a DNA sequence.
dna_sequence = "ATGCGTAC"

reversed_sequence = "".join(reversed(dna_sequence))

print("Original sequence:", dna_sequence)
print("Reversed sequence:", reversed_sequence)

# Example 2: Reverse the order of biological records.
samples = ["S001", "S002", "S003", "S004"]

for sample in reversed(samples):
    print(sample)

# Example 3: Convert a reversed iterator into a list.
expression_values = [24.6, 18.2, 42.8, 35.1]

print("Reversed values:", list(reversed(expression_values)))

# Example 4: Inspect a sequence from its final nucleotide.
for nucleotide in reversed("ATGC"):
    print(nucleotide)

# Example 5: Reverse-complement a DNA sequence.
# Reverse order and nucleotide complementation are separate operations.
def reverse_complement(sequence):
    sequence = sequence.upper()

    valid_bases = {"A", "T", "G", "C"}

    if set(sequence) - valid_bases:
        raise ValueError("Sequence contains invalid DNA bases.")

    complement = str.maketrans("ATGC", "TACG")

    return sequence.translate(complement)[::-1]


print("Reverse complement:", reverse_complement("ATGCGTAC"))