
"""
07. String Slicing

Main points
- Slicing extracts a portion of a sequence.
- Syntax: sequence[start:stop:step].
- The start index is included; the stop index is excluded.
- If omitted, start and stop use their default boundaries.
- A negative step can reverse a sequence.
- Slicing beyond the sequence boundaries generally does not raise IndexError.
- Slicing creates a new string.
"""

sequence = "ATGCGTAC"

# Basic slicing
print("First three:", sequence[0:3])
print("Characters 2 to 5:", sequence[2:6])

# Omitted boundaries
print("From beginning:", sequence[:4])
print("To the end:", sequence[4:])
print("Entire sequence:", sequence[:])

# Step
print("Every second character:", sequence[::2])

# Negative indexing in slices
print("Last three characters:", sequence[-3:])

# Reverse a string
print("Reversed:", sequence[::-1])

# Biological example: extract a subsequence
dna_sequence = "ATGAAATAG"
coding_region = dna_sequence[0:6]

print("DNA sequence:", dna_sequence)
print("Extracted region:", coding_region)

# Slices do not include the stop index
print("First five characters:", sequence[:5])
