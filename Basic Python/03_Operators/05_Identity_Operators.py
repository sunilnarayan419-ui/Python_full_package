
"""
05. Identity Operators

Main points
- is checks whether two references point to the same object.
- is not checks whether they point to different objects.
- == checks value equality, not object identity.
- Use 'is None' to test whether a value is None.
- Two different lists can contain equal elements but be different objects.
- Python may reuse certain immutable objects, so identity should not be
  used as a substitute for numerical or string equality.
"""

# Example 1: Compare two gene lists
genes_a = ["BRCA1", "TP53"]
genes_b = ["BRCA1", "TP53"]

print("Same contents:", genes_a == genes_b)
print("Same object:", genes_a is genes_b)

# Example 2: Compare references to the same object
genes_c = genes_a

print("Same contents:", genes_a == genes_c)
print("Same object:", genes_a is genes_c)

# Example 3: Mutating a shared list
genes_c.append("EGFR")

print("Genes A:", genes_a)
print("Genes C:", genes_c)

# Both names refer to the same list.
print("Same object after mutation:", genes_a is genes_c)

# Example 4: Identity checks for missing experimental results
experimental_result = None

if experimental_result is None:
    print("Experimental result has not been recorded.")

# Example 5: is not
if experimental_result is not None:
    print("Result is available.")
else:
    print("Result is unavailable.")

# Example 6: Value equality versus identity
sample_id_a = 1000
sample_id_b = 1000

print("IDs equal:", sample_id_a == sample_id_b)

# Do not rely on the identity of numeric objects.
