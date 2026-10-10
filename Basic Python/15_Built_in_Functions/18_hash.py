"""
TOPIC: hash()

MAIN POINTS
- hash() returns an integer hash value for a hashable object.
- Hashable objects can be used as dictionary keys and set elements.
- Immutable built-in types such as strings, integers, and tuples of hashable values are commonly hashable.
- Lists and dictionaries are unhashable.
- Equal objects must have equal hashes.
- Hash values are not guaranteed to be unique.
- String and bytes hashes may vary between Python processes.
- Do not use hash() as a cryptographic digest or permanent biological record identifier.
"""

# Example 1: Hash a gene identifier.
gene_id = "BRCA1"

print("Gene ID:", gene_id)
print("Hash:", hash(gene_id))

# Example 2: Use gene identifiers as dictionary keys.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8
}

print("BRCA1 expression:", gene_expression["BRCA1"])

# Example 3: Hash a tuple of biological metadata.
sample_key = ("S001", "Homo sapiens", "Blood")

print("Sample key hash:", hash(sample_key))

# Example 4: A list is unhashable.
try:
    print(hash(["BRCA1", "TP53"]))
except TypeError as error:
    print("Cannot hash a list:", error)

# Example 5: Equal values have equal hashes.
value_a = ("S001", 42)
value_b = ("S001", 42)

print("Equal:", value_a == value_b)
print("Equal hashes:", hash(value_a) == hash(value_b))

# Example 6: Hash collisions are possible.
# A hash value is not a unique identifier.
print("Different values can share a hash.")