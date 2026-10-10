
"""
06. Packages

Main points
- A package organizes related Python modules into a directory structure.
- A regular package commonly contains an __init__.py file.
- Subpackages organize functionality into additional directories.
- Packages help prevent large projects from becoming a single collection
  of unrelated Python files.
- Import paths use dots to identify modules inside packages.
- A package can separate sequence analysis, statistics, data handling,
  and reporting into distinct components.
- __init__.py can be empty or contain package initialization code.
- Python also supports namespace packages, which do not require __init__.py.
"""

# ------------------------------------------------------------
# EXAMPLE PROJECT STRUCTURE
# ------------------------------------------------------------

"""
biotech_project/
    main.py
    biotech_tools/
        __init__.py
        sequences.py
        statistics_tools.py
"""

# ------------------------------------------------------------
# FILE 1: biotech_tools/sequences.py
# ------------------------------------------------------------

"""
def count_bases(sequence):
    sequence = sequence.upper()

    invalid_bases = set(sequence) - set("ATGC")

    if invalid_bases:
        raise ValueError(
            f"Invalid DNA bases: {invalid_bases}"
        )

    return {
        base: sequence.count(base)
        for base in "ATGC"
    }


def gc_percentage(sequence):
    if not sequence:
        raise ValueError("Sequence cannot be empty.")

    counts = count_bases(sequence)
    total_bases = sum(counts.values())

    return (counts["G"] + counts["C"]) / total_bases * 100
"""

# ------------------------------------------------------------
# FILE 2: biotech_tools/statistics_tools.py
# ------------------------------------------------------------

"""
def calculate_mean(values):
    if not values:
        raise ValueError("Values cannot be empty.")

    return sum(values) / len(values)


def find_maximum(values):
    if not values:
        raise ValueError("Values cannot be empty.")

    return max(values)
"""

# ------------------------------------------------------------
# FILE 3: biotech_tools/__init__.py
# ------------------------------------------------------------

"""
from .sequences import count_bases, gc_percentage
from .statistics_tools import calculate_mean, find_maximum

__all__ = [
    "count_bases",
    "gc_percentage",
    "calculate_mean",
    "find_maximum",
]
"""

# ------------------------------------------------------------
# FILE 4: main.py
# ------------------------------------------------------------

"""
from biotech_tools import (
    count_bases,
    gc_percentage,
    calculate_mean,
    find_maximum,
)

dna_sequence = "ATGCGTAA"
expression_values = [10.5, 12.0, 15.5, 18.0]

print("Base counts:", count_bases(dna_sequence))
print("GC percentage:", gc_percentage(dna_sequence))
print("Mean expression:", calculate_mean(expression_values))
print("Maximum expression:", find_maximum(expression_values))
"""

# ------------------------------------------------------------
# HOW TO RUN
# ------------------------------------------------------------

"""
Open a terminal in the biotech_project directory:

python main.py

The import paths assume the directory structure shown above.
The package directory is discoverable because the project root is
on Python's import path during this execution.
"""

# Important:
# The quoted sections represent separate files, not code that should
# all be pasted into one executable Python file.
