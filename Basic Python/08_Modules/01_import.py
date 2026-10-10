
"""
01. import

Main points
- A module is a Python file containing reusable code.
- The import statement makes a module available in the current namespace.
- Use module_name.function_name() to access its functions.
- Modules can contain functions, classes, variables, and executable statements.
- Python's standard library provides modules for mathematics, statistics,
  file handling, dates, random numbers, and more.
- Importing a module normally executes its top-level code once per module
  instance in a Python process.
- Use descriptive module names to make code easier to understand.
"""

# Import the math module.
import math

# Calculate the square root of a scientific measurement.
variance = 16.0
standard_deviation = math.sqrt(variance)

print("Standard deviation:", standard_deviation)

# Calculate a logarithm.
concentration = 0.001
log_concentration = math.log10(concentration)

print("Log10 concentration:", log_concentration)

# Import the statistics module.
import statistics

expression_values = [12.5, 15.0, 18.5, 14.0, 20.0]

mean_expression = statistics.mean(expression_values)
median_expression = statistics.median(expression_values)

print("Mean expression:", mean_expression)
print("Median expression:", median_expression)

# Import the random module.
import random

# Simulate selecting a sample for a demonstration.
sample_ids = ["S001", "S002", "S003", "S004"]
selected_sample = random.choice(sample_ids)

print("Selected sample:", selected_sample)

# Random selection is for demonstration only, not experimental design.
