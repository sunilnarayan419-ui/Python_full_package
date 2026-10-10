"""
TOPIC: Opening Files

MAIN POINTS
- Use the open() function to open a file.
- The syntax is open(file_path, mode).
- Common modes include "r" for reading, "w" for writing, and "a" for appending.
- The "r" mode raises FileNotFoundError if the file does not exist.
- Always understand the selected mode before opening a file.
- File objects allow Python to access biological datasets stored on disk.
"""

# Create a sample DNA sequence file.
with open("dna_sequence.txt", "w") as file:
    file.write("ATGCGTACGTAG")

# Open the file in reading mode.
file = open("dna_sequence.txt", "r")

print(file.read())

file.close()