
"""
05. Creating Modules

Main points
- Any Python file can act as a module.
- A module allows functions and variables to be reused across files.
- Keep related functionality together in one module.
- Import a module using its filename without the .py extension.
- The if __name__ == "__main__": guard distinguishes direct execution
  from importing a module.
- When a file runs directly, its __name__ is "__main__".
- When imported normally, its __name__ is usually the module name.
- The importing file must be able to locate the module.
"""

# ------------------------------------------------------------
# FILE 1: dna_tools.py
# Save the following code in a separate file named dna_tools.py.
# ------------------------------------------------------------

"""
def calculate_gc_percentage(sequence):
    sequence = sequence.upper()

    if not sequence:
        raise ValueError("DNA sequence cannot be empty.")

    invalid_bases = set(sequence) - set("ATGC")

    if invalid_bases:
        raise ValueError(
            f"Invalid DNA bases: {invalid_bases}"
        )

    gc_count = sequence.count("G") + sequence.count("C")
    return gc_count / len(sequence) * 100


def count_nucleotides(sequence):
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


if __name__ == "__main__":
    dna = "ATGCGCGT"
    print("GC percentage:", calculate_gc_percentage(dna))
    print("Nucleotide counts:", count_nucleotides(dna))
"""

# ------------------------------------------------------------
# FILE 2: main.py
# Save the following code in another file named main.py.
# Place both files in the same directory.
# ------------------------------------------------------------

"""
from dna_tools import calculate_gc_percentage, count_nucleotides

sequence = "ATGCGTAA"

gc_percentage = calculate_gc_percentage(sequence)
nucleotide_counts = count_nucleotides(sequence)

print("Sequence:", sequence)
print("GC percentage:", gc_percentage)
print("Nucleotide counts:", nucleotide_counts)
"""

# ------------------------------------------------------------
# HOW TO RUN
# ------------------------------------------------------------

"""
Your folder should look like this:

python_project/
    dna_tools.py
    main.py

Open a terminal in python_project and run:

python main.py

To run the module's demonstration directly:

python dna_tools.py

Important:
The two quoted code sections above are examples of separate files.
Copy each section into its own actual .py file before running.
"""

# This file documents the pattern; it does not create the two files.
