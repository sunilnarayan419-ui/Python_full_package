
"""
02. Integers

Main points
- int represents whole numbers without a fractional component.
- Python integers support positive, negative, and zero values.
- Python integers have arbitrary precision, limited by available memory.
- The int() function converts suitable values to integers.
- Division using / returns a float, while // performs floor division.
- Boolean values are technically a subclass of int in Python.
"""

# Integer values
positive_number = 100
negative_number = -25
zero = 0
large_number = 123456789012345678901234567890

# Arithmetic operations
print("Addition:", 10 + 20)
print("Multiplication:", 5 * 4)
print("Floor division:", 17 // 5)
print("Remainder:", 17 % 5)

# Division versus floor division
print("Normal division:", 17 / 5)
print("Floor division:", 17 // 5)

# Convert a string to an integer
sample_count = int("250")
print("Sample count:", sample_count, type(sample_count))

# Boolean and integer relationship
print("True as integer:", int(True))
print("Is bool a subclass of int?", issubclass(bool, int))

# Inspect integer types
print(type(positive_number))
print(type(negative_number))
print(type(large_number))
