
"""
09. f-Strings

Main points
- f-strings format expressions directly inside string literals.
- Prefix a string with f or F.
- Expressions are enclosed in curly braces: {}.
- Formatting specifications follow a colon inside the braces.
- :.2f formats a floating-point number to two decimal places.
- Commas can be used as thousands separators.
- f-strings support calculations and function calls inside expressions.
"""

name = "Sunil"
sample_count = 1250
temperature = 25.6789
ph_value = 7.4

# Basic interpolation
print(f"Student: {name}")
print(f"Sample count: {sample_count}")

# Format decimal places
print(f"Temperature: {temperature:.2f} °C")
print(f"pH: {ph_value:.1f}")

# Thousands separator
print(f"Processed samples: {sample_count:,}")

# Expressions inside f-strings
length = 10
width = 5

print(f"Area: {length * width}")

# Alignment
print(f"{'Sample':<15}{'Mass':>10}")
print(f"{'S001':<15}{12.5:>10.2f}")
print(f"{'S002':<15}{8.75:>10.2f}")

# Percentage formatting
completion = 0.875
print(f"Completion: {completion:.1%}")

# Scientific notation
concentration = 0.0000125
print(f"Concentration: {concentration:.2e}")
