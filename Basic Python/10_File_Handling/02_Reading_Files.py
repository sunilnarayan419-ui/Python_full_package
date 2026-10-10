"""
TOPIC: Reading Files

MAIN POINTS
- read() reads the entire file or a specified number of characters.
- readline() reads one line at a time.
- readlines() returns all lines as a list.
- Use strip() to remove surrounding whitespace and newline characters.
- Choose the reading method based on the dataset size and structure.
- Reading files is essential for analyzing DNA sequences, gene expression data, and laboratory records.
"""

# Sample FASTA file containing DNA sequences.
with open("genes.fasta", "w") as file:
    file.write(">Gene_1\nATGCGTAC\n")
    file.write(">Gene_2\nTTAGGCAT\n")

# Method 1: Read the complete file.
with open("genes.fasta", "r") as file:
    content = file.read()
    print("Complete FASTA file:")
    print(content)

# Method 2: Read one line.
with open("genes.fasta", "r") as file:
    first_line = file.readline()
    print("First line:", first_line.strip())

# Method 3: Read all lines into a list.
with open("genes.fasta", "r") as file:
    lines = file.readlines()
    print("All lines:", lines)

# Extract only DNA sequences, excluding FASTA headers.
sequences = [
    line.strip()
    for line in lines
    if not line.startswith(">")
]

print("DNA sequences:", sequences)