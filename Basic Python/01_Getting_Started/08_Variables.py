"""
08. Variables
Main points
- A variable name refers to an object in Python.
- Assignment uses =.
- Python is dynamically typed; a name can later refer to an object of a different type.
- Common built-in types include int, float, str, bool, list, tuple, dict, and set.
- Python is case-sensitive: sample and Sample are different names.
- Use type() to inspect an object's type.
"""


# Integer
sample_count = 10

# Floating-point number
ph_value = 7.4

# String
organism = "Arabidopsis thaliana"

# Boolean
is_sample_processed = True

# List
gene_expression = [2.1, 3.4, 1.8]

# Dictionary
sample = {
    "id": "S001",
    "temperature": 25.0
}

# Display values and their types
print(sample_count, type(sample_count))
print(ph_value, type(ph_value))
print(organism, type(organism))
print(is_sample_processed, type(is_sample_processed))
print(gene_expression, type(gene_expression))
print(sample, type(sample))

# Reassign a name to a different type of object
result = 100
print(result, type(result))

result = "Completed"
print(result, type(result))
