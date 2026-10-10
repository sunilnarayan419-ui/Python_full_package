"""
TOPIC: help()

MAIN POINTS
- help() displays documentation for Python objects.
- help(function) explains a function's purpose, arguments, and behavior.
- help(class) displays information about a class and its methods.
- help() without arguments starts the interactive help system.
- Use help() to explore unfamiliar Python functions without leaving the interpreter.
"""

# Example 1: Inspect len().
help(len)

# Example 2: Inspect sum().
help(sum)

# Example 3: Inspect sorted().
help(sorted)

# Example 4: Inspect the string count() method.
help(str.count)

# Example 5: Inspect a scientific helper function.
def calculate_gc_percentage(sequence):
    """Calculate the GC percentage of a non-empty DNA sequence."""
    if not sequence:
        raise ValueError("Sequence cannot be empty.")

    gc_count = sequence.upper().count("G") + sequence.upper().count("C")

    return gc_count / len(sequence) * 100


help(calculate_gc_percentage)

# Example 6: Read a function's docstring directly.
print(calculate_gc_percentage.__doc__)