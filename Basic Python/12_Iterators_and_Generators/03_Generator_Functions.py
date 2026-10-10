"""
TOPIC: Generator Functions

MAIN POINTS
- A generator function is a function that contains yield.
- Calling a generator function returns a generator object.
- Its body does not execute fully when the generator is created.
- The body executes as values are requested.
- A generator remembers its execution state between requests.
- Generators can produce values incrementally instead of storing every result in a list.
- They are useful for streaming FASTA records, processing large files, and analyzing genomic datasets.
"""

def generate_dna_sequences():
    """Generate DNA sequences one at a time."""

    print("Preparing the first sequence...")
    yield "ATGCGTAC"

    print("Preparing the second sequence...")
    yield "TTAGGCAT"

    print("Preparing the third sequence...")
    yield "CGATCGAT"


# Calling the function creates a generator object.
sequence_generator = generate_dna_sequences()

print("Generator created:")
print(sequence_generator)

# The function body begins when a value is requested.
print("\nFirst request:")
print(next(sequence_generator))

print("\nSecond request:")
print(next(sequence_generator))

print("\nThird request:")
print(next(sequence_generator))

# The generator is exhausted after its final yield.
# Uncomment to observe StopIteration.
# print(next(sequence_generator))


# A generator can also be consumed using a for loop.
def generate_gene_records():
    genes = [
        ("BRCA1", 24.6),
        ("TP53", 18.2),
        ("EGFR", 42.8),
        ("MYC", 35.1)
    ]

    for gene, expression in genes:
        yield {
            "gene": gene,
            "expression": expression
        }


print("\nGenerated gene records:")

for record in generate_gene_records():
    print(record)


# Generate synthetic DNA sequences with a chosen length.
def generate_repeated_dna(base_sequence, repetitions):
    """Yield repeated DNA sequences one at a time."""

    if repetitions < 0:
        raise ValueError("Repetitions cannot be negative.")

    for index in range(repetitions):
        yield f"Sequence_{index + 1}", base_sequence


print("\nGenerated sequences:")

for sequence_id, sequence in generate_repeated_dna("ATGC", 5):
    print(sequence_id, sequence)