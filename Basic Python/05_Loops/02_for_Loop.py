
"""
02. for Loop

Main points
- A for loop iterates over the items of an iterable.
- Iterables include lists, tuples, strings, sets, dictionaries, and ranges.
- The loop variable receives one item during each iteration.
- The loop ends when the iterable is exhausted or execution is interrupted.
- for is useful when processing known collections of data.
- Iteration order depends on the iterable; lists preserve their element order.
"""

# Example 1: Process a list of biological samples.
sample_ids = ["S001", "S002", "S003", "S004"]

for sample_id in sample_ids:
    print("Processing sample:", sample_id)

# Example 2: Inspect a DNA sequence one nucleotide at a time.
dna_sequence = "ATGCGTAC"

for nucleotide in dna_sequence:
    print("Nucleotide:", nucleotide)

# Example 3: Count nucleotides.
dna_sequence = "ATGCGTAC"
nucleotide_count = {}

for nucleotide in dna_sequence:
    nucleotide_count[nucleotide] = (
        nucleotide_count.get(nucleotide, 0) + 1
    )

print("Nucleotide counts:", nucleotide_count)

# Example 4: Process gene expression measurements.
expression_values = [12.5, 15.2, 8.7, 21.3]

for expression in expression_values:
    if expression > 15:
        print(expression, "is above the selected threshold.")

# Example 5: Iterate over a dictionary.
sample_metadata = {
    "organism": "Arabidopsis thaliana",
    "tissue": "leaf",
    "temperature_celsius": 25
}

for key, value in sample_metadata.items():
    print(key, ":", value)
