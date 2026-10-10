
"""
TOPIC: try

MAIN POINTS
- Put code that might raise an exception inside try.
- Python executes the try block first.
- If an exception occurs, execution moves to a matching except block.
- If no exception occurs, the try block completes normally.
- Keep the try block focused on the statements that may fail.
"""

dna_sequence = "ATGCGT"

try:
    nucleotide_count = len(dna_sequence)
    print("DNA sequence:", dna_sequence)
    print("Sequence length:", nucleotide_count)
except Exception:
    print("Something went wrong while processing the sequence.")
