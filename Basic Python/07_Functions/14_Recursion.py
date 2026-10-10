
"""
14. Recursion

Main points
- Recursion occurs when a function calls itself.
- A recursive function needs a base case that stops further recursion.
- Each recursive call should move toward a base case.
- Missing or incorrect base cases can cause RecursionError.
- Recursive calls consume call-stack space.
- Recursion is useful for tree traversal, divide-and-conquer algorithms,
  and some mathematical problems.
- Iteration is often simpler and more memory-efficient for straightforward
  repeated calculations in Python.
"""

# Example 1: Calculate factorial recursively.
def factorial(n):
    if n < 0:
        raise ValueError("n must be non-negative")

    # Base case
    if n == 0:
        return 1

    # Recursive case
    return n * factorial(n - 1)


print("Factorial of 5:", factorial(5))

# Example 2: Count DNA nucleotides recursively.
def count_nucleotide(sequence, nucleotide):
    if not sequence:
        return 0

    current_match = 1 if sequence[0] == nucleotide else 0

    return current_match + count_nucleotide(
        sequence[1:],
        nucleotide
    )


dna_sequence = "ATGCGTAA"

print("A count:", count_nucleotide(dna_sequence, "A"))
print("G count:", count_nucleotide(dna_sequence, "G"))

# Example 3: Sum expression measurements recursively.
def recursive_sum(values):
    if not values:
        return 0

    return values[0] + recursive_sum(values[1:])


measurements = [2.5, 3.0, 4.5]

print("Total measurement:", recursive_sum(measurements))

# Important:
# These simple examples illustrate recursion, not optimal implementations
# for long biological sequences. Repeated slicing and recursive calls add
# overhead. Built-in functions and iteration are generally preferable
# for straightforward sequence counting and summation.
