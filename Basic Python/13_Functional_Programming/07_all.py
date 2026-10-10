"""
TOPIC: all()

MAIN POINTS
- all() returns True if every item in an iterable is truthy.
- It returns False as soon as it encounters a falsy item.
- all() returns True for an empty iterable.
- This behavior for empty iterables is called vacuous truth.
- all() is useful for validating whether every record satisfies a condition.
- Combined with generator expressions, it supports efficient validation pipelines.
"""

# Example 1: Check whether every DNA sequence contains valid bases.
dna_sequences = [
    "ATGC",
    "GCTA",
    "CCGG"
]

valid_bases = {"A", "T", "G", "C"}

all_valid = all(
    bool(sequence)
    and set(sequence.upper()) <= valid_bases
    for sequence in dna_sequences
)

print("All sequences valid:", all_valid)


# Example 2: Validate gene expression measurements.
expression_values = [24.6, 18.2, 42.8, 35.1]

all_non_negative = all(
    expression >= 0
    for expression in expression_values
)

print("All expression values non-negative:", all_non_negative)


# Example 3: Check whether every sample has required fields.
samples = [
    {"sample_id": "S001", "organism": "Human"},
    {"sample_id": "S002", "organism": "Mouse"},
    {"sample_id": "S003", "organism": "Human"}
]

required_fields = {"sample_id", "organism"}

all_records_complete = all(
    required_fields <= sample.keys()
    for sample in samples
)

print("All records complete:", all_records_complete)


# Example 4: Validate sequence lengths.
dna_sequences = [
    "ATGC",
    "GCTA",
    "CCGG"
]

all_sequences_long_enough = all(
    len(sequence) >= 4
    for sequence in dna_sequences
)

print("All sequences have at least 4 bases:",
      all_sequences_long_enough)


# Example 5: Understand the empty iterable case.
print("All items in an empty list:", all([]))

# An explicit check may be necessary if at least one record is required.
records = []

valid_dataset = bool(records) and all(
    len(record) > 0
    for record in records
)

print("Dataset is non-empty and valid:", valid_dataset)