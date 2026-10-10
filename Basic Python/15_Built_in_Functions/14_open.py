"""
TOPIC: open()

MAIN POINTS
- open() opens a file and returns a file object.
- Common modes include r (read), w (write), a (append), and x (create exclusively).
- Text encoding should be specified when appropriate.
- Use newline="" when working with CSV files.
- Prefer with open() so that the file is closed automatically.
- File paths can be absolute or relative.
"""

import csv
import json
from pathlib import Path

# Example 1: Write a DNA sequence.
with open(
    "dna_sequence.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("ATGCGTACGTAG\n")

# Example 2: Read the sequence.
with open(
    "dna_sequence.txt",
    "r",
    encoding="utf-8"
) as file:
    sequence = file.read().strip()

print("DNA sequence:", sequence)
print("Length:", len(sequence))

# Example 3: Append another record.
with open(
    "dna_sequence.txt",
    "a",
    encoding="utf-8"
) as file:
    file.write("TTAGGCAT\n")

# Example 4: Write structured CSV data.
with open(
    "gene_expression.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:
    writer = csv.writer(file)

    writer.writerow(["gene", "expression"])
    writer.writerow(["BRCA1", 24.6])
    writer.writerow(["TP53", 18.2])

# Example 5: Read CSV data.
with open(
    "gene_expression.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:
    reader = csv.DictReader(file)

    for record in reader:
        print(record["gene"], float(record["expression"]))

# Example 6: Write JSON metadata.
metadata = {
    "sample_id": "S001",
    "organism": "Homo sapiens",
    "sequence_length": len(sequence)
}

with open(
    "sample_metadata.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(metadata, file, indent=4)

# Example 7: Inspect the generated path.
print("File exists:", Path("sample_metadata.json").exists())