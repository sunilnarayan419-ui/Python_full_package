
"""
06. Tuples

Main points
- A tuple is an ordered collection that cannot be structurally modified.
- Tuples are created using parentheses, although parentheses may be optional.
- Tuples can contain duplicate values and different data types.
- A single-element tuple requires a trailing comma.
- Tuples support indexing, slicing, iteration, and len().
- Tuples are useful for fixed records and returning multiple values.
- A tuple containing a mutable object does not make that object immutable.
"""

# Store fixed sample metadata
sample_metadata = ("S001", "Arabidopsis thaliana", 25.0)

print("Sample metadata:", sample_metadata)
print("Sample ID:", sample_metadata[0])
print("Organism:", sample_metadata[1])
print("Temperature:", sample_metadata[2])

# A single-element tuple
single_gene = ("TP53",)
print("Single-gene tuple:", single_gene)

# A tuple can contain mixed types
measurement = ("S002", 18.5, True)
print("Measurement:", measurement)

# Iterate through a tuple
for item in sample_metadata:
    print(item)

# Tuples cannot be reassigned by index.
# Uncomment to observe TypeError:
# sample_metadata[0] = "S003"

# A tuple can contain a mutable list.
experiment = ("E001", ["control", "treatment"])
experiment[1].append("replicate")

print("Tuple containing a list:", experiment)
