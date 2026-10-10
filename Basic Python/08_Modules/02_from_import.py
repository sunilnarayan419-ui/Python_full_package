
"""
02. from ... import

Main points
- from module import name imports a specific name into the current namespace.
- The imported function can be used without the module prefix.
- Multiple names can be imported in one statement.
- Import only what is needed to keep code readable.
- Importing names directly can cause naming conflicts.
- Avoid using from module import * in ordinary project code because
  it makes the origin of names less clear.
"""

# Import specific functions.
from math import sqrt, log10

# Calculate standard deviation from a variance.
variance = 25.0
standard_deviation = sqrt(variance)

print("Standard deviation:", standard_deviation)

# Calculate a logarithmic measurement.
concentration = 0.0001
log_value = log10(concentration)

print("Log10 concentration:", log_value)

# Import specific statistical functions.
from statistics import mean, median

gene_expression = [5.2, 7.8, 9.1, 12.4, 15.0]

print("Mean:", mean(gene_expression))
print("Median:", median(gene_expression))

# Import multiple names from the same module.
from math import ceil, floor

sample_count = 10.7

print("Rounded upward:", ceil(sample_count))
print("Rounded downward:", floor(sample_count))

# Note:
# These functions are imported into the current namespace.
# Use module prefixes when you want to make their origin explicit.
