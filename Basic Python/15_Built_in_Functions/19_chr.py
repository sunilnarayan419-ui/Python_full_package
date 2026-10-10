"""
TOPIC: chr()

MAIN POINTS
- chr() converts a valid Unicode code point into a string character.
- Valid code points range from 0 to 0x10FFFF.
- chr() raises ValueError when the integer is outside that range.
- It is useful for understanding character encoding and text processing.
- DNA letters are Unicode characters, but chr() is not a DNA-specific function.
"""

# Example 1: Convert integer code points into characters.
print(chr(65))
print(chr(71))
print(chr(84))
print(chr(67))

# Example 2: Construct a DNA string from character codes.
dna_codes = [65, 84, 71, 67]

dna_sequence = "".join(
    chr(code)
    for code in dna_codes
)

print("DNA sequence:", dna_sequence)

# Example 3: Convert ASCII codes for a gene identifier.
gene_codes = [66, 82, 67, 65, 49]

gene_id = "".join(chr(code) for code in gene_codes)

print("Gene ID:", gene_id)

# Example 4: Unicode works beyond ASCII.
print(chr(945))   # Greek lowercase alpha
print(chr(946))   # Greek lowercase beta

# Example 5: Reject an invalid code point.
try:
    print(chr(0x110000))
except ValueError as error:
    print("Invalid Unicode code point:", error)