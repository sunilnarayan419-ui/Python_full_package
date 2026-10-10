
"""
05. Strings

Main points
- str represents text in Python.
- Strings can be enclosed in single, double, or triple quotes.
- Strings are ordered sequences of Unicode code points.
- Strings are immutable: individual characters cannot be changed in place.
- The + operator concatenates strings.
- The * operator repeats strings.
- len() returns the number of characters in a string.
"""

# Create strings
organism = "Arabidopsis thaliana"
message = 'Python is useful for scientific computing.'
description = """Plant science combines
biology, chemistry, and computation."""

print(organism)
print(message)
print(description)

# Concatenation
first_name = "Sunil"
last_name = "Narayan"

full_name = first_name + " " + last_name
print("Full name:", full_name)

# Repetition
print("Python! " * 3)

# String length
print("Length:", len(organism))

# Strings are immutable
sequence = "ATGC"
print("Original sequence:", sequence)

# This creates a new string rather than modifying the original.
sequence = "C" + sequence[1:]
print("Updated sequence:", sequence)

# Type inspection
print(type(organism))
