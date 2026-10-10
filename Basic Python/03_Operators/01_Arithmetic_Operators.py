
"""
01. Arithmetic Operators

Main points
- Arithmetic operators perform mathematical calculations.
- + : Addition
- - : Subtraction
- * : Multiplication
- / : Division; returns a float.
- // : Floor division; rounds the quotient down.
- % : Modulus; returns the remainder.
- ** : Exponentiation.
- Parentheses can control the order of calculations.
- Be careful with units when performing scientific calculations.
"""

# Example 1: Calculate the total number of DNA samples
samples_from_lab_a = 48
samples_from_lab_b = 36

total_samples = samples_from_lab_a + samples_from_lab_b
print("Total DNA samples:", total_samples)

# Example 2: Calculate remaining samples after quality control
initial_samples = 120
failed_samples = 15

valid_samples = initial_samples - failed_samples
print("Valid samples:", valid_samples)

# Example 3: Calculate total reagent volume
volume_per_reaction_ml = 0.025
number_of_reactions = 96

total_volume_ml = volume_per_reaction_ml * number_of_reactions
print("Total reagent volume:", total_volume_ml, "mL")

# Example 4: Calculate the mean concentration
concentrations = [12.5, 14.0, 13.5, 16.0]
mean_concentration = sum(concentrations) / len(concentrations)

print("Mean concentration:", mean_concentration, "ng/uL")

# Example 5: Calculate the number of complete plates
total_wells = 250
wells_per_plate = 96

complete_plates = total_wells // wells_per_plate
remaining_wells = total_wells % wells_per_plate

print("Complete plates:", complete_plates)
print("Remaining wells:", remaining_wells)

# Example 6: Calculate the theoretical number of DNA copies
# after successive ideal doubling cycles.
initial_copies = 100
cycles = 5

final_copies = initial_copies * (2 ** cycles)
print("Theoretical DNA copies:", final_copies)

# Important: Ideal doubling assumes 100% amplification efficiency.
