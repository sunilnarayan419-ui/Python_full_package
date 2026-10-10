"""
TOPIC: yield

MAIN POINTS
- yield produces a value and pauses the generator.
- When the generator resumes, execution continues immediately after the previous yield.
- Local variables retain their values between yields.
- A generator can yield values inside loops and conditional statements.
- Multiple yield statements can produce a sequence of values.
- return ends a generator; a return value becomes the value carried by StopIteration rather than an ordinary yielded item.
- yield from delegates iteration to another iterable or generator.
- These features allow complex biological data-processing pipelines to operate incrementally.
"""

def analyze_dna_sequence(sequence):
    """Yield analysis results one at a time."""

    sequence = sequence.upper()

    yield f"Sequence: {sequence}"

    yield f"Length: {len(sequence)}"

    gc_count = sequence.count("G") + sequence.count("C")
    gc_percentage = gc_count / len(sequence) * 100 if sequence else 0

    yield f"GC percentage: {gc_percentage:.2f}%"

    yield f"A count: {sequence.count('A')}"
    yield f"T count: {sequence.count('T')"
    yield f"G count: {sequence.count('G')}"
    yield f"C count: {sequence.count('C')}"


dna = "ATGCGCGT"

print("DNA analysis results:")

for result in analyze_dna_sequence(dna):
    print(result)


# Demonstrate how generator state is preserved.
def gene_expression_generator():
    print("\nStarting gene expression analysis.")

    gene = "BRCA1"
    expression = 24.6

    yield gene, expression

    # Execution resumes here.
    expression = expression * 1.5

    yield gene, expression

    expression = expression * 2

    yield gene, expression


expression_generator = gene_expression_generator()

print("\nFirst value:")
print(next(expression_generator))

print("\nSecond value:")
print(next(expression_generator))

print("\nThird value:")
print(next(expression_generator))


# yield from delegates to another iterable.
def generate_all_sequences():
    yield from ["ATGC", "GCTA", "TTAA"]

    yield from generate_repeated_dna("CCGG", 2)


print("\nCombined sequence stream:")

for sequence in generate_all_sequences():
    print(sequence)