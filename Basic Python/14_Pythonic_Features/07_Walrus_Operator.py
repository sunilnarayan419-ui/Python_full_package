"""
TOPIC: Walrus Operator

MAIN POINTS
- The walrus operator := assigns a value inside an expression.
- It was introduced in Python 3.8.
- It is useful when a calculated value is needed both in a condition and later in the same expression or block.
- Parentheses are often needed for clarity.
- It can reduce repeated calculations in loops and comprehensions.
- Do not use it merely to make code shorter; readability is more important.
"""

# Example 1: Calculate a DNA sequence length once.
dna_sequence = "ATGCGTAC"

if (sequence_length := len(dna_sequence)) >= 8:
    print("Sequence length:", sequence_length)
    print("Sequence meets the length threshold.")


# Example 2: Filter sequences while reusing a calculated length.
dna_sequences = [
    "ATGC",
    "ATGCGTAC",
    "GCTA",
    "ATGCGCGTAA"
]

long_sequences = [
    (sequence, length)
    for sequence in dna_sequences
    if (length := len(sequence)) >= 8
]

print("\nLong sequences:")
print(long_sequences)


# Example 3: Calculate GC percentage and reuse it.
def calculate_gc_percentage(sequence):
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

for sequence in dna_sequences:
    if (gc := calculate_gc_percentage(sequence)) >= 50:
        print(f"{sequence}: GC={gc:.2f}%")


# Example 4: Read records until no more lines are available.
from io import StringIO

fasta_text = """>Gene_A
ATGC
>Gene_B
GCTA
"""

file = StringIO(fasta_text)

while (line := file.readline()):
    print("Read line:", line.strip())


# Example 5: Reuse a calculated expression in a comprehension.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8,
    "MYC": 35.1
}

high_expression = [
    (gene, value)
    for gene, expression in gene_expression.items()
    if (value := float(expression)) >= 30
]

print("\nHigh-expression genes:")
print(high_expression)


# Example 6: Compare with ordinary code.
# Both versions are valid.

results = []

for sequence in dna_sequences:
    gc = calculate_gc_percentage(sequence)

    if gc >= 50:
        results.append((sequence, gc))

print("\nResults using an ordinary loop:")
print(results)