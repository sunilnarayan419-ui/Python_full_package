
"""
03. Module Aliasing

Main points
- The as keyword assigns an alternative name to an imported module or object.
- Aliases can make long module names shorter.
- Aliasing does not create a new module or duplicate its functionality.
- Common scientific aliases include np for NumPy and pd for pandas.
- Standard aliases improve consistency when collaborating with others.
- Use meaningful aliases rather than arbitrary abbreviations.
"""

# Alias the mathematics module.
import math as m

print("Square root:", m.sqrt(144))
print("Pi:", m.pi)

# Alias the statistics module.
import statistics as stats

expression_values = [10.0, 12.5, 15.0, 17.5]

print("Mean expression:", stats.mean(expression_values))
print("Standard deviation:", stats.stdev(expression_values))

# Alias an imported function.
from math import factorial as fact

print("Factorial of 5:", fact(5))

# Scientific computing convention:
# NumPy and pandas are external packages, not part of the Python
# standard library. Install them in your environment before importing.

# import numpy as np
# import pandas as pd

# Example usage after installation:
# measurements = np.array([10.0, 12.0, 14.0])
# print(np.mean(measurements))
