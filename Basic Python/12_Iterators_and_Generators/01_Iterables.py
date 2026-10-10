"""
TOPIC: Iterables

MAIN POINTS
- An iterable is an object that can return its elements one at a time.
- Common iterables include lists, tuples, strings, dictionaries, and sets.
- The iter() function obtains an iterator from an iterable.
- A for loop automatically obtains an iterator and retrieves its elements.
- Iterables can be traversed using loops, comprehensions, and other iteration tools.
- Lists store all their elements in memory, while some other iterables can generate data dynamically.
- In computational biology, iterables can represent DNA sequences, gene identifiers, protein sequences, and experimental measurements.
"""

# A DNA sequence is a string, and strings are iterable.
dna_sequence = "ATGCGTACGTAG"

print("DNA sequence:")
for nucleotide in dna_sequence:
    print(nucleotide)

# A list of DNA sequences is also iterable.
dna_sequences = [
    "ATGCGTAC",
    "TTAGGCAT",
    "CGATCGAT"
]

print("\nDNA sequences:")
for sequence in dna_sequences:
    print(sequence)

# A tuple can store gene identifiers.
gene_ids = ("BRCA1", "TP53", "EGFR", "MYC")

print("\nGene identifiers:")
for gene in gene_ids:
    print(gene)

# A dictionary is iterable over its keys by default.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8
}

print("\nGene expression:")
for gene in gene_expression:
    print(gene, gene_expression[gene])

# Use items() to iterate over keys and values together.
for gene, expression in gene_expression.items():
    print(f"{gene}: {expression}")

# Obtain an iterator explicitly.
sequence_iterator = iter(dna_sequences)

print("\nIterator object:")
print(sequence_iterator)

# Retrieve elements through the iterator.
print(next(sequence_iterator))
print(next(sequence_iterator))
print(next(sequence_iterator))

# A list is reusable: a new loop can traverse it again.
print("\nTraverse the list again:")
for sequence in dna_sequences:
    print(sequence)