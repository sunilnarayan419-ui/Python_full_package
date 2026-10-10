"""
TOPIC: itertools
MAIN POINTS:
- Combine iterables.
- Generate combinations and permutations.
- Group consecutive matching values.
- Use count() and islice() for controlled iteration.
"""

from itertools import chain, combinations, count, islice, groupby, permutations

# Combine sequences
dna_parts = ["ATG", "GCA", "TTA"]
combined_sequence = "".join(chain.from_iterable(dna_parts))
print("Combined DNA:", combined_sequence)

# Combinations: choose two nucleotides without regard to order
nucleotides = ["A", "T", "G", "C"]

print("Pairs:")
for pair in combinations(nucleotides, 2):
    print(pair)

# Permutations: order matters
print("Ordered pairs:")
for pair in permutations(["A", "T", "G"], 2):
    print(pair)

# Group consecutive equal values
measurements = [
    ("Control", 10),
    ("Control", 12),
    ("Treatment", 15),
    ("Treatment", 17),
]

for condition, group in groupby(measurements, key=lambda item: item[0]):
    values = [value for _, value in group]
    print(condition, values)

# count() produces an infinite sequence
sample_ids = islice(count(start=1), 5)
print("Generated sample numbers:", list(sample_ids))

# Important: groupby() groups consecutive runs, not all matching
# values throughout an unsorted collection.