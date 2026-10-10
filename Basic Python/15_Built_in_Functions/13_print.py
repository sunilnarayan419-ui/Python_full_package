"""
TOPIC: print()

MAIN POINTS
- print() displays objects as text.
- Multiple objects can be printed in one call.
- sep= controls the separator between objects.
- end= controls what is printed at the end.
- f-strings provide readable formatting for scientific reports.
- file= allows print() to write to an open file.
"""

# Example 1: Display DNA information.
dna_sequence = "ATGCGCGT"

print("DNA sequence:", dna_sequence)
print("Sequence length:", len(dna_sequence))

# Example 2: Control separators.
print("BRCA1", 24.6, "TP53", 18.2, sep=" | ")

# Example 3: Control the ending.
print("Analyzing sample...", end=" ")
print("Complete!")

# Example 4: Format scientific measurements.
concentration = 42.56789
gc_percentage = 62.5

print(f"Concentration: {concentration:.2f} ng/uL")
print(f"GC percentage: {gc_percentage:.1f}%")

# Example 5: Print a table.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8
}

print("\nGENE EXPRESSION REPORT")
print("-" * 35)
print(f"{'Gene':<12}{'Expression':>12}")
print("-" * 35)

for gene, expression in gene_expression.items():
    print(f"{gene:<12}{expression:>12.2f}")

# Example 6: Write printed output to a file.
with open("analysis_output.txt", "w", encoding="utf-8") as file:
    print("DNA analysis completed.", file=file)
    print(f"Sequence: {dna_sequence}", file=file)

print("Report written to analysis_output.txt")