"""
TOPIC: Iterators

MAIN POINTS
- An iterator produces elements one at a time.
- iter(iterable) obtains an iterator from an iterable.
- next(iterator) retrieves the next available element.
- When no elements remain, next() raises StopIteration.
- Iterators maintain their current position.
- An exhausted iterator generally cannot be restarted; obtain a new iterator to begin again.
- A list is iterable, but it is not itself an iterator.
- Iterators are useful for sequentially processing large biological datasets.
"""

# Simulated genomic records.
dna_sequences = [
    "ATGCGTAC",
    "TTAGGCAT",
    "CGATCGAT",
    "GGCCATTA"
]

# Convert the list into an iterator.
sequence_iterator = iter(dna_sequences)

print("First sequence:", next(sequence_iterator))
print("Second sequence:", next(sequence_iterator))

# The iterator remembers its current position.
print("Third sequence:", next(sequence_iterator))

# Continue processing the remaining records.
print("\nRemaining sequences:")

for sequence in sequence_iterator:
    print(sequence)

# The iterator is now exhausted.
# Uncomment the following line to observe StopIteration.
# print(next(sequence_iterator))

# A new iterator starts from the beginning.
new_iterator = iter(dna_sequences)

print("\nFirst sequence from the new iterator:")
print(next(new_iterator))


# Build a simple custom iterator for DNA sequences.
class DNASequenceIterator:
    """Iterate through the nucleotides of a DNA sequence."""

    def __init__(self, sequence):
        self.sequence = sequence
        self.position = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.position >= len(self.sequence):
            raise StopIteration

        nucleotide = self.sequence[self.position]
        self.position += 1

        return nucleotide


dna = "ATGCGT"

nucleotide_iterator = DNASequenceIterator(dna)

print("\nNucleotides from the custom iterator:")

for nucleotide in nucleotide_iterator:
    print(nucleotide)

# An iterator can also be used with next().
nucleotide_iterator = DNASequenceIterator("GCTA")

print("\nManual iteration:")
print(next(nucleotide_iterator))
print(next(nucleotide_iterator))
print(next(nucleotide_iterator))
print(next(nucleotide_iterator))