"""
TOPIC: any()

MAIN POINTS
- any() returns True if at least one item in an iterable is truthy.
- It returns False for an empty iterable.
- It short-circuits when it finds the first truthy item.
- any() is useful for checking whether at least one biological record satisfies a condition.
- Combined with generator expressions, it can test large datasets lazily.
"""

# Example 1: Check whether any sequence begins with ATG.
dna_sequences = [
    "TTAGGCAT",
    "CGATCGAT",
    "ATGCGTAC"
]

has_start_codon = any(
    sequence.startswith("ATG")
    for sequence in dna_sequences
)

print("Any sequence starts with ATG:", has_start_codon)


# Example 2: Check for high gene expression.
expression_values = [12.5, 18.2, 42.8, 15.6]

has_high_expression = any(
    expression >= 40
    for expression in expression_values
)

print("Any gene has expression >= 40:", has_high_expression)


# Example 3: Check whether any DNA sequence contains an invalid base.
valid_bases = {"A", "T", "G", "C"}

dna_sequences = [
    "ATGC",
    "GCTA",
    "ATGX"
]

has_invalid_sequence = any(
    bool(set(sequence.upper()) - valid_bases)
    for sequence in dna_sequences
)

print("Any invalid DNA sequence:", has_invalid_sequence)


# Example 4: Check whether any sample fails a quality threshold.
samples = [
    {"sample_id": "S001", "purity": 1.91},
    {"sample_id": "S002", "purity": 1.86},
    {"sample_id": "S003", "purity": 1.55}
]

has_failed_sample = any(
    not 1.8 <= sample["purity"] <= 2.0
    for sample in samples
)

print("Any sample outside the illustrative range:", has_failed_sample)


# Example 5: any() with an empty iterable.
print("Any values in an empty list:", any([]))