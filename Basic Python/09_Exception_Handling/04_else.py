
"""
TOPIC: else WITH try-except

MAIN POINTS
- The else block runs only when the try block raises no exception.
- It does not run if a matching exception is handled.
- Use else for operations that should happen after successful execution.
- Keep exception-prone operations inside try.
"""

dna_sequence = "ATGCGTAA"

try:
    sequence_length = len(dna_sequence)
except TypeError:
    print("The DNA sequence must be a valid sequence.")
else:
    print("Sequence processed successfully.")
    print("Number of nucleotides:", sequence_length)
