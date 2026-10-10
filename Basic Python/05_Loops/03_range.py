
"""
03. range()

Main points
- range() generates a sequence of integers.
- range(stop) starts at 0 and stops before stop.
- range(start, stop) starts at start and stops before stop.
- range(start, stop, step) specifies the increment.
- The stop value is excluded.
- The step can be positive or negative, but cannot be zero.
- range() is useful for controlled repetition and index-based iteration.
"""

# Example 1: Simulate five PCR cycles.
for cycle in range(1, 6):
    print("PCR cycle:", cycle)

# Example 2: Generate sample numbers from 0 to 4.
for sample_number in range(5):
    print("Sample index:", sample_number)

# Example 3: Iterate through a DNA sequence using indices.
dna_sequence = "ATGCGT"

for index in range(len(dna_sequence)):
    print(index, dna_sequence[index])

# Example 4: Process every second nucleotide position.
dna_sequence = "ATGCGTAC"

for index in range(0, len(dna_sequence), 2):
    print("Position:", index, "Nucleotide:", dna_sequence[index])

# Example 5: Count backwards through an experiment.
for minute in range(10, 0, -2):
    print("Minutes remaining:", minute)

# Example 6: Calculate ideal DNA amplification by cycle.
initial_copies = 100

for cycle in range(1, 6):
    copies = initial_copies * (2 ** cycle)
    print(f"Cycle {cycle}: {copies} theoretical copies")

# The amplification model assumes ideal doubling in every cycle.
