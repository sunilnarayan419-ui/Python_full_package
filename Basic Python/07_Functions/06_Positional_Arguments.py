
"""
06. Positional Arguments

Main points
- Positional arguments are matched to parameters by their order.
- The first positional argument goes to the first parameter, and so on.
- Required positional parameters generally must receive values.
- Too few or too many arguments can raise TypeError.
- Positional arguments are concise when the parameter order is obvious.
- Use keyword arguments when the meaning of values might be unclear.
"""

# Example 1: Calculate a dilution factor.
def calculate_dilution_factor(initial_concentration, final_concentration):
    return initial_concentration / final_concentration


dilution_factor = calculate_dilution_factor(100.0, 10.0)
print("Dilution factor:", dilution_factor)

# The first argument is initial_concentration.
# The second argument is final_concentration.

# Example 2: Calculate fold change.
def calculate_fold_change(treated, control):
    return treated / control


fold_change = calculate_fold_change(20.0, 5.0)
print("Fold change:", fold_change)

# Reversing the order changes the result.
reverse_fold_change = calculate_fold_change(5.0, 20.0)
print("Reversed calculation:", reverse_fold_change)

# Example 3: Process sample identifiers.
def compare_samples(sample_a, sample_b):
    print("First sample:", sample_a)
    print("Second sample:", sample_b)


compare_samples("CONTROL_01", "TREATMENT_01")

# For complex scientific calculations, choose parameter names carefully
# and document the expected units.
