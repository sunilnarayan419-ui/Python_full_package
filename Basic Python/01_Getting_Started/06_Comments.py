"""
06. Comments
Main points
- Comments explain code to human readers.
- Single-line comments begin with #.
- Python has no dedicated multiline-comment syntax. Multiple # lines are the conventional approach.
- Triple-quoted strings are often used for docstrings, not as a special comment syntax.
- Comments should explain purpose or reasoning rather than repeat obvious code.
"""


# This is a single-line comment.

# Store the temperature measured in a laboratory.
temperature_celsius = 25.5

# Convert Celsius to Fahrenheit.
temperature_fahrenheit = (
    temperature_celsius * 9 / 5
) + 32

print("Celsius:", temperature_celsius)
print("Fahrenheit:", temperature_fahrenheit)

# A block comment can span several lines:
# 1. Collect the measurement.
# 2. Convert the unit.
# 3. Display the result.


def calculate_area(length, width):
    """Calculate the area of a rectangle."""
    return length * width


print("Area:", calculate_area(5, 4))
