
"""
01. Lists

Main points
- A list is an ordered, mutable collection of objects.
- Lists are created using square brackets [].
- Lists can contain duplicate values and different data types.
- Indexing starts at 0.
- append() adds an item to the end.
- Lists can be modified after creation.
- Lists are useful for storing samples, measurements, and sequences.
"""

# Store DNA sequences
dna_sequences = ["ATGC", "GGTA", "CCGA"]

# Store gene expression measurements
expression_values = [12.5, 18.2, 9.7, 21.4]

# Lists can contain mixed data types
sample_record = ["S001", 25.5, True]

print("DNA sequences:", dna_sequences)
print("Expression values:", expression_values)
print("Sample record:", sample_record)

# Access an element
print("First DNA sequence:", dna_sequences[0])

# Add an item
dna_sequences.append("ATAT")
print("Updated sequences:", dna_sequences)

# Modify an item
dna_sequences[1] = "TTGC"
print("Modified sequences:", dna_sequences)

# Remove an item
dna_sequences.remove("CCGA")
print("After removal:", dna_sequences)

# Calculate a simple mean
mean_expression = sum(expression_values) / len(expression_values)
print("Mean expression:", mean_expression)

# Lists are mutable
print("List type:", type(dna_sequences))
