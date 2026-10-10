"""
TOPIC: Unpacking

MAIN POINTS
- Unpacking extracts elements from an iterable into variables.
- The number of targets must match the number of elements unless starred unpacking is used.
- The * operator captures remaining elements into a list.
- The ** operator unpacks dictionary entries as keyword arguments.
- Iterable unpacking is useful for processing sequence records and structured measurements.
- Dictionary unpacking is useful for combining metadata dictionaries.
"""

# Example 1: Unpack a biological record.
sample_record = (
    "S001",
    "Homo sapiens",
    "Blood",
    45.2
)

sample_id, organism, tissue, concentration = sample_record

print("Sample ID:", sample_id)
print("Organism:", organism)
print("Tissue:", tissue)
print("DNA concentration:", concentration)


# Example 2: Starred unpacking.
measurements = (
    "S001",
    45.2,
    1.87,
    20.0,
    "Control"
)

sample_id, *numeric_values, condition = measurements

print("\nSample ID:", sample_id)
print("Numeric values:", numeric_values)
print("Condition:", condition)


# Example 3: Unpack the first and last elements.
gene_expression = [
    24.6,
    18.2,
    42.8,
    35.1,
    29.7
]

first_expression, *middle_expression, last_expression = gene_expression

print("\nFirst expression:", first_expression)
print("Middle values:", middle_expression)
print("Last expression:", last_expression)


# Example 4: Unpack a dictionary into function arguments.
def register_sample(sample_id, organism, tissue):
    return (
        f"{sample_id}: {organism}, "
        f"{tissue}"
    )


sample_metadata = {
    "sample_id": "S002",
    "organism": "Mus musculus",
    "tissue": "Liver"
}

print("\nRegistered sample:")
print(register_sample(**sample_metadata))


# Example 5: Merge dictionaries using unpacking.
identity = {
    "sample_id": "S003",
    "organism": "Homo sapiens"
}

measurements = {
    "dna_concentration": 58.1,
    "purity_ratio": 1.92
}

complete_record = {
    **identity,
    **measurements
}

print("\nComplete sample record:")
print(complete_record)


# Example 6: Unpack sequences in a loop.
gene_records = [
    ("BRCA1", 24.6),
    ("TP53", 18.2),
    ("EGFR", 42.8)
]

for gene, expression in gene_records:
    print(f"{gene}: {expression}")


# Example 7: Unpack the remainder of a DNA sequence.
dna_sequence = "ATGCGTAC"

first_base, *remaining_bases = dna_sequence

print("\nFirst nucleotide:", first_base)
print("Remaining nucleotides:", remaining_bases)