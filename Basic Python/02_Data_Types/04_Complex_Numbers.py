
"""
04. Complex Numbers

Main points
- complex numbers contain real and imaginary components.
- Python uses j to represent the imaginary unit.
- Example: 3 + 4j has real part 3 and imaginary part 4.
- Use .real and .imag to access the components.
- Use abs() to calculate the magnitude.
- Use the conjugate() method to obtain the complex conjugate.
- Complex numbers are useful in signal processing, physics,
  electrical engineering, and mathematical modelling.
"""

# Create complex numbers
z1 = 3 + 4j
z2 = 2 + 1j

# Access components
print("Real part:", z1.real)
print("Imaginary part:", z1.imag)

# Arithmetic operations
print("Addition:", z1 + z2)
print("Subtraction:", z1 - z2)
print("Multiplication:", z1 * z2)
print("Division:", z1 / z2)

# Magnitude
print("Magnitude:", abs(z1))

# Complex conjugate
print("Conjugate:", z1.conjugate())

# Create a complex number using complex()
z3 = complex(5, 6)
print("Created complex number:", z3)

# Type inspection
print("Type:", type(z1))
