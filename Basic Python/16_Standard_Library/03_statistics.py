"""
TOPIC: statistics
MAIN POINTS:
- Calculate descriptive statistics.
- Compare mean and median.
- Measure variance and standard deviation.
"""

import statistics

# Example: gene expression measurements
expression_values = [12.5, 14.2, 13.8, 15.1, 14.4, 13.9]

print("Mean:", statistics.mean(expression_values))
print("Median:", statistics.median(expression_values))
print("Population variance:", statistics.pvariance(expression_values))
print("Sample variance:", statistics.variance(expression_values))
print("Population standard deviation:", statistics.pstdev(expression_values))
print("Sample standard deviation:", statistics.stdev(expression_values))

# Compare two groups
control = [10, 11, 12, 10, 11]
treatment = [14, 15, 13, 16, 14]

print("Control mean:", statistics.mean(control))
print("Treatment mean:", statistics.mean(treatment))

# A difference in means alone does not establish statistical significance.