"""
TOPIC: The with Statement

MAIN POINTS
- The with statement manages resources using a context manager.
- When used with open(), it automatically closes the file after the block finishes.
- It closes the file even if an exception occurs inside the block.
- It improves readability and reduces resource-management errors.
- Prefer with open() over manually calling close().
- Reliable file handling is important when processing large biological datasets.
"""

# Simulated protein sequence stored in a file.
with open("protein_sequence.txt", "w") as file:
    file.write("MKWVTFISLLFLFSSAYS")

# Open the protein sequence safely.
with open("protein_sequence.txt", "r") as file:
    protein = file.read().strip()
    print("Protein sequence:", protein)
    print("Amino acid count:", len(protein))

# The file is automatically closed after leaving the with block.
print("Is file closed:", file.closed)

# Multiple files can also be opened in one with statement.
with open("protein_sequence.txt", "r") as input_file, 
     open("protein_length.txt", "w") as output_file:

    sequence = input_file.read().strip()
    output_file.write(f"Protein length: {len(sequence)} amino acids\n")

with open("protein_length.txt", "r") as file:
    print(file.read())