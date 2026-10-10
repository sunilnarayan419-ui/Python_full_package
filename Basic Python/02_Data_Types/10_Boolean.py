
"""
10. Boolean

Main points
- bool represents logical truth values: True and False.
- Boolean values are commonly produced by comparisons.
- Comparison operators include ==, !=, >, <, >=, and <=.
- Logical operators include and, or, and not.
- bool is a subclass of int, where True behaves like 1 and False like 0.
- Truthiness determines whether an object behaves as true or false
  in a conditional context.
"""

temperature = 28
maximum_temperature = 30

# Boolean values
is_active = True
is_complete = False

print(is_active)
print(is_complete)

# Comparisons
print(temperature > maximum_temperature)
print(temperature <= maximum_temperature)
print(temperature == 28)
print(temperature != 25)

# Logical operators
has_data = True
is_valid = True

print("Both conditions:", has_data and is_valid)
print("At least one:", has_data or is_valid)
print("Negation:", not has_data)

# Conditional example
if temperature > maximum_temperature:
    print("Temperature is too high.")
else:
    print("Temperature is within the limit.")

# Truthiness examples
print(bool(0))
print(bool(1))
print(bool(""))
print(bool("Python"))
print(bool([]))

# Boolean and integer relationship
print(True + True)
print(type(True))
