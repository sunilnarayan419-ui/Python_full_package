
"""
07. *args

Main points
- *args collects extra positional arguments into a tuple.
- The name args is conventional; the asterisk is what matters.
- It allows a function to accept a variable number of positional arguments.
- The collected tuple can be iterated over or used in calculations.
- *args can be combined with ordinary parameters.
- It is useful when the number of measurements or datasets varies.
"""

# Example 1: Calculate the mean of any number of measurements.
def calculate_mean(*measurements):
    if not measurements:
        return None

    return sum(measurements) / len(measurements)


print(calculate_mean(10.0, 12.0, 14.0))
print(calculate_mean(5.5, 7.5, 9.5, 11.5))
print(calculate_mean())

# Example 2: Summarize multiple gene-expression measurements.
def summarize_expression(gene_name, *measurements):
    print("Gene:", gene_name)
    print("Measurements:", measurements)

    if measurements:
        mean = sum(measurements) / len(measurements)
        print("Mean expression:", mean)


summarize_expression("TP53", 12.5, 15.0, 18.5)
summarize_expression("BRCA1", 8.2, 9.1)

# Example 3: Pass existing values using unpacking.
expression_values = [10.0, 20.0, 30.0]

mean = calculate_mean(*expression_values)
print("Mean from a list:", mean)

# The * in a function definition collects arguments.
# The * in a function call unpacks an iterable into positional arguments.
