
"""
TOPIC: Errors vs Exceptions

MAIN POINTS
- Errors indicate problems that prevent code from working as intended.
- Syntax errors occur when Python cannot parse the code.
- Exceptions occur during execution, such as ZeroDivisionError.
- Exceptions can often be handled using try and except.
- Not every error can or should be handled.
"""

# SyntaxError example — uncomment to see the error:
# print("DNA sequence is not closed)

# Runtime exception example:
cell_count = 100
sample_count = 0

try:
    cells_per_sample = cell_count / sample_count
except ZeroDivisionError:
    print("Cannot divide cell count by zero.")

# Normal execution:
dna_sequence = "ATGCGT"
print("DNA sequence:", dna_sequence)
