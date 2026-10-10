"""
TOPIC: collections
MAIN POINTS:
- Count repeated items with Counter.
- Group values using defaultdict.
- Use deque for efficient operations at both ends.
- Store named fields with namedtuple.
"""

from collections import Counter, defaultdict, deque, namedtuple

# Count nucleotides
dna_sequence = "ATGCGATATCGG"
nucleotide_counts = Counter(dna_sequence)

print("Nucleotide counts:", nucleotide_counts)
print("Most common nucleotide:", nucleotide_counts.most_common(1))

# Group samples by experimental condition
samples = [
    ("Control", "Sample_A"),
    ("Treatment", "Sample_B"),
    ("Control", "Sample_C"),
    ("Treatment", "Sample_D"),
]

groups = defaultdict(list)

for condition, sample in samples:
    groups[condition].append(sample)

print("Grouped samples:", dict(groups))

# Deque: useful for adding/removing items at either end
recent_samples = deque(["Sample_A", "Sample_B"])
recent_samples.append("Sample_C")
recent_samples.appendleft("Sample_0")

print("Recent samples:", recent_samples)
print("Oldest entry removed:", recent_samples.popleft())

# Named tuple
Sample = namedtuple("Sample", ["sample_id", "condition", "value"])

sample = Sample("EXP001", "Control", 12.5)

print("Sample ID:", sample.sample_id)
print("Condition:", sample.condition)
print("Value:", sample.value)