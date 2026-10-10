
"""
02. Assignment Operators

Main points
- = assigns an object to a variable name.
- += adds a value and reassigns the result.
- -= subtracts a value and reassigns the result.
- *= multiplies and reassigns the result.
- /= divides and reassigns the result.
- //= performs floor division and reassigns the result.
- %= stores the remainder after division.
- **= performs exponentiation and reassigns the result.
- Assignment does not necessarily copy an object.
- For mutable objects, augmented assignment may modify the same object.
"""

# Track DNA extraction samples
processed_samples = 0

processed_samples += 25
print("After batch 1:", processed_samples)

processed_samples += 30
print("After batch 2:", processed_samples)

processed_samples -= 5
print("After excluding failed samples:", processed_samples)

# Calculate reagent inventory
reagent_ml = 500

reagent_ml -= 75
print("Remaining reagent:", reagent_ml, "mL")

# Scale a concentration value
concentration = 2.5
dilution_factor = 4

concentration *= dilution_factor
print("Scaled concentration:", concentration)

# Calculate average measurements
total_expression = 240.0
sample_count = 12

total_expression /= sample_count
print("Mean expression value:", total_expression)

# Demonstrate other augmented operators
number = 17

number //= 5
print("Floor division result:", number)

number = 17
number %= 5
print("Remainder:", number)

number = 2
number **= 4
print("Exponentiation result:", number)

# Mutable object example
gene_list = ["BRCA1", "TP53"]
original_reference = gene_list

gene_list += ["EGFR"]

print("Updated genes:", gene_list)
print("Same list object:", gene_list is original_reference)
