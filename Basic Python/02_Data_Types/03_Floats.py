
"""
03. Floats

Main points
- float represents floating-point numbers.
- Floats can represent fractional, positive, negative, and scientific
  notation values.
- Floating-point arithmetic has finite precision.
- Some decimal fractions cannot be represented exactly in binary.
- Use round() to round a value for display or a specific calculation.
- Avoid direct equality comparisons for many floating-point calculations.
"""

# Floating-point values
temperature = 25.5
negative_value = -12.75
scientific_value = 1.5e3

print(temperature)
print(negative_value)
print("Scientific notation:", scientific_value)

# Floating-point arithmetic
print("Addition:", 0.1 + 0.2)
print("Rounded result:", round(0.1 + 0.2, 2))

# Demonstrate floating-point precision
print("Direct equality:", 0.1 + 0.2 == 0.3)

# Compare floats with a tolerance
tolerance = 1e-9
difference = abs((0.1 + 0.2) - 0.3)

print("Approximately equal:", difference < tolerance)

# Convert a string to float
ph_value = float("7.4")
print("pH:", ph_value, type(ph_value))

# Scientific example: convert milligrams to grams
mass_mg = 250.0
mass_g = mass_mg / 1000

print(f"Mass in grams: {mass_g:.3f} g")
