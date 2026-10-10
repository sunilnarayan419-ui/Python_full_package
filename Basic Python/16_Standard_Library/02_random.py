"""
TOPIC: random
MAIN POINTS:
- Generate random numbers.
- Select random items and samples.
- Shuffle sequences.
- Use seeds for reproducible demonstrations.
"""

import random

# Reproducible results for this demonstration
random.seed(42)

# Random numbers
print("Random decimal:", random.random())
print("Random integer:", random.randint(1, 100))

# Random selection
nucleotides = ["A", "T", "G", "C"]
print("Random nucleotide:", random.choice(nucleotides))

# Select multiple items without replacement
print("Random sample:", random.sample(nucleotides, k=2))

# Shuffle a list in place
samples = ["Sample_A", "Sample_B", "Sample_C", "Sample_D"]
random.shuffle(samples)
print("Shuffled samples:", samples)

# Simulate a simple sequence
random_sequence = "".join(
    random.choice(nucleotides) for _ in range(20)
)
print("Random DNA sequence:", random_sequence)

# Note: random is not suitable for cryptographic security.