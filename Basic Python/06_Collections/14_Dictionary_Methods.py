
"""
14. Dictionary Methods

Main points
- keys() returns a view of dictionary keys.
- values() returns a view of dictionary values.
- items() returns a view of key-value pairs.
- get() retrieves a value with an optional default.
- update() adds or updates key-value pairs.
- pop(key) removes a key and returns its value.
- popitem() removes and returns the most recently inserted pair.
- setdefault() returns an existing value or inserts a default.
- copy() creates a shallow copy.
- clear() removes all key-value pairs.
- View objects reflect changes to the dictionary.
"""

# Gene expression data
expression = {
    "TP53": 12.5,
    "BRCA1": 8.2,
    "EGFR": 18.4
}

# Retrieve keys, values, and items
print("Genes:", expression.keys())
print("Measurements:", expression.values())
print("Records:", expression.items())

# Safe retrieval
print("MYC expression:", expression.get("MYC", 0.0))

# Update one or more values
expression.update({
    "MYC": 14.3,
    "EGFR": 20.1
})

print("Updated expression:", expression)

# Insert a default only when a key is absent
expression.setdefault("APOE", 5.0)
expression.setdefault("TP53", 0.0)

print("After setdefault:", expression)

# Remove and retrieve a specific value
removed_value = expression.pop("BRCA1")
print("Removed BRCA1 expression:", removed_value)

# Remove the most recently inserted pair
removed_pair = expression.popitem()
print("Removed pair:", removed_pair)

# Create a shallow copy
expression_copy = expression.copy()
print("Copied dictionary:", expression_copy)

# Iterate through the data
for gene, value in expression.items():
    print(f"{gene}: {value}")

# Clear the copy without clearing the original
expression_copy.clear()

print("Cleared copy:", expression_copy)
print("Original remains:", expression)
