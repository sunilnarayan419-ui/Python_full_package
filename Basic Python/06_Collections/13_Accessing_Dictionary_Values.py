
"""
13. Accessing Dictionary Values

Main points
- dictionary[key] retrieves a value and raises KeyError if the key is absent.
- get(key) retrieves a value or returns None by default.
- get(key, default) returns the supplied default when the key is absent.
- The in operator checks dictionary keys.
- Nested dictionaries can represent structured biological records.
- Chained indexing can raise KeyError when an intermediate key is missing.
- Use explicit checks or get() when missing keys are expected.
"""

# Gene annotation database
gene_database = {
    "TP53": {
        "organism": "Homo sapiens",
        "chromosome": 17,
        "function": "Tumor suppressor"
    },
    "BRCA1": {
        "organism": "Homo sapiens",
        "chromosome": 17,
        "function": "DNA repair"
    }
}

# Direct access
print("TP53 annotation:", gene_database["TP53"])

# Access a nested value
print("TP53 chromosome:", gene_database["TP53"]["chromosome"])

# Safe access using get()
print("EGFR annotation:", gene_database.get("EGFR"))

# Supply a default value
print(
    "EGFR annotation:",
    gene_database.get("EGFR", "Annotation unavailable")
)

# Check whether a key exists
if "BRCA1" in gene_database:
    print("BRCA1 annotation is available.")

# Safely access an optional field
tp53_function = gene_database.get("TP53", {}).get(
    "function",
    "Unknown"
)

print("TP53 function:", tp53_function)

# Iterate over key-value pairs
for gene, annotation in gene_database.items():
    print(gene, "->", annotation["function"])

# Important:
# A missing annotation is not proof that a gene lacks a biological function.
