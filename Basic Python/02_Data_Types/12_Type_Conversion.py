
"""
12. Type Conversion

Main points
- Type conversion changes a value from one type to another.
- Explicit conversion is also called type casting.
- Common conversion functions include int(), float(), str(), bool(),
  complex(), list(), tuple(), set(), and dict().
- int("25") converts a valid integer string to an integer.
- float("3.14") converts a valid numeric string to a float.
- Invalid conversions may raise ValueError or TypeError.
- Converting a float to int truncates the fractional part toward zero.
- Converting to bool follows Python's truthiness rules.
"""

# String to integer
count = int("25")
print(count, type(count))

# String to float
temperature = float("27.5")
print(temperature, type(temperature))

# Integer to float
measurement = float(10)
print(measurement, type(measurement))

# Number to string
sample_id = str(1001)
print(sample_id, type(sample_id))

# Float to integer: truncates toward zero
print(int(9.8))
print(int(-9.8))

# Convert to boolean
print(bool(0))
print(bool(1))
print(bool(""))
print(bool("False"))  # Non-empty string is True

# Convert between collections
letters = list("DNA")
print(letters)

unique_values = set([1, 2, 2, 3])
print(unique_values)

# Convert integer to complex
number = complex(5)
print(number, type(number))

# Uncomment to observe ValueError:
# invalid_number = int("hello")
