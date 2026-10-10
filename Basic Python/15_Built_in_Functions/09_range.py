"""
TOPIC: range()

MAIN POINTS
- range() generates a sequence of integers.
- range(stop) starts at zero and excludes stop.
- range(start, stop, step) specifies a starting value and increment.
- range() is useful for indexing, repeated operations, and chunk processing.
- It is an iterable, not a list.
- Python indexing begins at zero, while biological sequence positions often begin at one.
"""

# Example 1: Generate indices for a DNA sequence.
dna_sequence = "ATGCGT"

for index in range(len(dna_sequence)):
    print(index, dna_sequence[index])

# Example 2: Report one-based nucleotide positions.
for index in range(len(dna_sequence)):
    print(index + 1, dna_sequence[index])

# Example 3: Iterate over every second nucleotide.
for index in range(0, len(dna_sequence), 2):
    print(index, dna_sequence[index])

# Example 4: Divide a sequence into chunks.
sequence = "ATGCGTACGTAG"
chunk_size = 4

for start in range(0, len(sequence), chunk_size):
    chunk = sequence[start:start + chunk_size]
    print(start, chunk)

# Example 5: Use range with a custom step.
for day in range(0, 15, 3):
    print(f"Experimental day: {day}")

# Example 6: Convert a range to a list for inspection.
print(list(range(5)))
print(list(range(2, 10, 2)))