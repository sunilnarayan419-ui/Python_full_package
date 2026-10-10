"""
TOPIC: re
MAIN POINTS:
- Search text using regular expressions.
- Extract matching patterns.
- Replace text with sub().
- Find every match with findall().
"""

import re

# Example: simple FASTA record
fasta_text = """>gene_001
ATGCGTACGTAA
>gene_002
ATGAAACCCGGG
"""

# Find all FASTA headers
headers = re.findall(r"^>(.+)$", fasta_text, flags=re.MULTILINE)
print("FASTA headers:", headers)

# Extract DNA sequences from the example
sequences = re.findall(
    r"^[ACGT]+$",
    fasta_text,
    flags=re.MULTILINE
)
print("DNA sequences:", sequences)

# Search for a start codon
sequence = "CCCATGAAATTT"
match = re.search(r"ATG", sequence)

if match:
    print("Start codon found at index:", match.start())

# Replace repeated whitespace with one space
text = "Gene   expression    analysis"
cleaned_text = re.sub(r"\s+", " ", text)
print("Cleaned text:", cleaned_text)

# Validate a simple sample ID format, such as EXP123
sample_id = "EXP123"
is_valid = re.fullmatch(r"EXP\d{3}", sample_id) is not None

print("Valid sample ID:", is_valid)

# These are illustrative text checks, not biological validation.
# For complex biological formats, use a suitable parser and
# validate against the relevant format specification.