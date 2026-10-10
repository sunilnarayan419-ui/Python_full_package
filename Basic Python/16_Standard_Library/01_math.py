"""
TOPIC: math
MAIN POINTS:
- Use mathematical functions and constants.
- Calculate powers, square roots, logarithms, and factorials.
- Apply math functions to scientific data.
"""

import math

# Basic calculations
print("Square root:", math.sqrt(144))
print("Power:", math.pow(2, 5))
print("Absolute ceiling:", math.ceil(4.2))
print("Floor:", math.floor(4.8))

# Constants
print("Pi:", math.pi)
print("Euler's number:", math.e)

# Logarithms
print("Log base 10:", math.log10(1000))
print("Natural log:", math.log(math.e))

# Factorial
print("Factorial of 5:", math.factorial(5))

# Scientific example: calculate pH from hydrogen ion concentration.
hydrogen_ion_concentration = 1e-7
ph = -math.log10(hydrogen_ion_concentration)

print("Calculated pH:", ph)