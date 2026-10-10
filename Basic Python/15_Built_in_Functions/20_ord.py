"""
TOPIC: ord()

MAIN POINTS
- ord() returns the Unicode code point of a single character.
- It is the conceptual inverse of chr() for valid individual characters.
- ord() accepts a string containing exactly one character.
- It is useful for exploring text encoding and character-level data.
- Biological sequence analysis normally works with nucleotide symbols directly rather than their integer code points.
"""

# Example 1: Inspect nucleotide code points.
for nucleotide in "ATGC":
    print(nucleotide, ord(nucleotide))

# Example 2: Convert a character to an integer and back.
nucleotide = "G"

code_point = ord(nucleotide)
recovered_character = chr(code_point)

print("Original:", nucleotide)
print("Code point:", code_point)
print("Recovered:", recovered_character)

# Example 3: Inspect a gene identifier.
gene_id = "BRCA1"

for character in gene_id:
    print(character, ord(character))

# Example 4: Unicode characters.
print("Alpha:", ord("α"))
print("Beta:", ord("β"))

# Example 5: ord() requires exactly one character.
try:
    print(ord("ATG"))
except TypeError as error:
    print("Invalid input:", error)