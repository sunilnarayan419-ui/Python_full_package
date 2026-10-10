"""
TOPIC: id()

MAIN POINTS
- id() returns an integer representing an object's identity during its lifetime.
- Two names referring to the same object have the same identity.
- Two separate objects may contain equal values but have different identities.
- Identity is different from equality.
- The exact numeric value of id() is implementation-dependent.
- Use is to test object identity; use == to test value equality.
"""

# Example 1: Two names refer to the same list.
samples_a = ["S001", "S002"]
samples_b = samples_a

print("ID of samples_a:", id(samples_a))
print("ID of samples_b:", id(samples_b))

print("Same object:", samples_a is samples_b)
print("Equal values:", samples_a == samples_b)

# Example 2: Two different lists with equal values.
samples_c = ["S001", "S002"]

print("\nID of samples_c:", id(samples_c))
print("Same object:", samples_a is samples_c)
print("Equal values:", samples_a == samples_c)

# Example 3: Modify an aliased list.
samples_b.append("S003")

print("\nSamples A:", samples_a)
print("Samples B:", samples_b)

# Example 4: Explore object identity with biological records.
record_a = {"gene": "BRCA1", "expression": 24.6}
record_b = record_a
record_c = {"gene": "BRCA1", "expression": 24.6}

print("\nA and B are identical:", record_a is record_b)
print("A and C are identical:", record_a is record_c)
print("A and C have equal values:", record_a == record_c)