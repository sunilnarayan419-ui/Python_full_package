"""
TOPIC: input()

MAIN POINTS
- input() reads text entered by the user.
- It always returns a string.
- Convert the result to int() or float() when numerical input is required.
- Validate user input before using it in calculations.
- input() is useful for interactive scientific scripts and simple data-entry tools.
"""

# Example 1: Collect sample metadata.
sample_id = input("Enter sample ID: ")
organism = input("Enter organism: ")
tissue = input("Enter tissue type: ")

print("\nSample information:")
print("Sample ID:", sample_id)
print("Organism:", organism)
print("Tissue:", tissue)

# Example 2: Collect a DNA concentration.
try:
    concentration = float(
        input("Enter DNA concentration in ng/uL: ")
    )

    if concentration < 0:
        raise ValueError("Concentration cannot be negative.")

    print("Recorded concentration:", concentration, "ng/uL")

except ValueError as error:
    print("Invalid concentration:", error)

# Example 3: Collect a sequence and calculate its length.
dna_sequence = input("Enter a DNA sequence: ").strip().upper()

valid_bases = {"A", "T", "G", "C"}

if not dna_sequence:
    print("The sequence cannot be empty.")
elif set(dna_sequence) - valid_bases:
    print("The sequence contains invalid DNA characters.")
else:
    print("Sequence length:", len(dna_sequence))