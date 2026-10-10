
"""
06. continue

Main points
- continue skips the remaining statements in the current iteration.
- The loop proceeds to its next iteration.
- In a for loop, the next item is processed.
- In a while loop, the condition is checked again.
- continue is useful for skipping missing, invalid, or irrelevant records.
- Ensure that while-loop state updates are not accidentally skipped,
  or the loop may never terminate.
"""

# Example 1: Skip samples with failed quality control.
sample_results = [
    ("S001", True),
    ("S002", False),
    ("S003", True),
    ("S004", False)
]

for sample_id, passed_qc in sample_results:
    if not passed_qc:
        print("Skipping failed sample:", sample_id)
        continue

    print("Analyzing sample:", sample_id)

# Example 2: Skip ambiguous nucleotides.
dna_sequence = "ATGNCTGA"

for nucleotide in dna_sequence:
    if nucleotide not in "ATGC":
        print("Skipping ambiguous symbol:", nucleotide)
        continue

    print("Processing nucleotide:", nucleotide)

# Example 3: Ignore missing expression measurements.
expression_values = [12.5, None, 18.0, None, 9.5]

for expression in expression_values:
    if expression is None:
        continue

    print("Valid expression measurement:", expression)

# Example 4: Skip even-numbered positions.
for position in range(1, 11):
    if position % 2 == 0:
        continue

    print("Odd position:", position)

# Note: Skipping data is not always scientifically appropriate.
# Missing or ambiguous data may need explicit quality-control handling.
