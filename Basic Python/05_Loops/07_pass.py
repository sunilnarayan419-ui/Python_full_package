
"""
07. pass

Main points
- pass is a null statement that performs no operation.
- It allows a syntactically valid block where a statement is required.
- pass does not skip an iteration or terminate a loop.
- Unlike continue, pass does not change loop execution.
- It is useful for temporary placeholders during program development.
- Replace placeholders with meaningful logic when implementation is ready.
"""

# Example 1: Placeholder for future DNA quality-control logic.
dna_sequence = "ATGC"

for nucleotide in dna_sequence:
    if nucleotide == "N":
        pass  # TODO: Implement ambiguous-base handling.

    print("Current nucleotide:", nucleotide)

# Example 2: Placeholder for a future analysis function.
def analyze_protein_sequence(sequence):
    pass  # TODO: Add protein sequence analysis.

# Calling the function returns None because it has no return statement.
result = analyze_protein_sequence("MKWVTFIS")
print("Analysis result:", result)

# Example 3: Compare pass with continue.
for nucleotide in "ATGN":
    if nucleotide == "N":
        pass

    print("pass example:", nucleotide)

for nucleotide in "ATGN":
    if nucleotide == "N":
        continue

    print("continue example:", nucleotide)

# Example 4: A placeholder class method.
class GenomicsPipeline:
    def run_quality_control(self):
        pass  # TODO: Implement quality control.

pipeline = GenomicsPipeline()
pipeline.run_quality_control()

print("Placeholder method executed.")

# Remember:
# pass = do nothing here.
# continue = skip the rest of this iteration.
# break = terminate the nearest enclosing loop.
