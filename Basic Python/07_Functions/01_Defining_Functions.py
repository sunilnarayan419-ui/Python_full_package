
"""
01. Defining Functions

Main points
- A function is a reusable block of code designed to perform a task.
- Define a function using the def keyword.
- A function name should describe its purpose.
- Parentheses contain parameters; a colon starts the function body.
- Indentation defines the function body.
- A function executes when it is called.
- Functions help reduce repetition and organize scientific workflows.
- A function can accept inputs, perform operations, and return results.
"""

# Example 1: Calculate the GC percentage of a DNA sequence.
def calculate_gc_percentage(sequence):
    sequence = sequence.upper()
    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100


dna_sequence = "ATGCGCGT"
gc_percentage = calculate_gc_percentage(dna_sequence)

print("DNA sequence:", dna_sequence)
print("GC percentage:", gc_percentage)

# Example 2: Display sample information.
def display_sample(sample_id, organism):
    print("Sample ID:", sample_id)
    print("Organism:", organism)


display_sample("S001", "Arabidopsis thaliana")

# Example 3: Reuse a function for multiple sequences.
sequences = ["ATGC", "GGCC", "ATAT"]

for sequence in sequences:
    print(sequence, calculate_gc_percentage(sequence))

# Note:
# This introductory example assumes a non-empty sequence containing
# only A, T, G, and C. Robust validation can be added later.
