
"""
13. type() Function

Main points
- type(object) returns the object's type.
- It is useful for inspecting data during learning and debugging.
- Common results include int, float, str, bool, list, dict, and NoneType.
- type() can be used to compare exact types.
- For checking whether an object belongs to a type or subclass,
  isinstance() is usually preferred.
"""

# Values of different types
count = 10
temperature = 25.5
organism = "Arabidopsis"
is_valid = True
genes = ["geneA", "geneB"]
sample = {"id": "S001"}
result = None

# Inspect their types
print(type(count))
print(type(temperature))
print(type(organism))
print(type(is_valid))
print(type(genes))
print(type(sample))
print(type(result))

# Store a type in a variable
value_type = type(count)
print("Stored type:", value_type)

# Exact type comparison
print(type(count) is int)
print(type(temperature) is float)
print(type(organism) is str)

# Boolean is a subclass of int, but its exact type is bool
print(type(True) is bool)
print(type(True) is int)

# Inspect a calculated result
total = 10 / 2
print("Total:", total)
print("Total type:", type(total))
