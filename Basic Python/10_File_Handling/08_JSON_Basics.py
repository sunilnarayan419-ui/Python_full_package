"""
TOPIC: JSON Basics

MAIN POINTS
- JSON stands for JavaScript Object Notation.
- JSON stores structured data using objects, arrays, strings, numbers, booleans, and null values.
- Python's json module provides json.dump(), json.load(), json.dumps(), and json.loads().
- json.dump() writes Python data structures to a file.
- json.load() reads JSON data from a file.
- JSON objects become Python dictionaries, and JSON arrays become Python lists.
- JSON is useful for storing structured biological metadata, experimental configurations, and analysis results.
"""

import json

# Structured metadata for a hypothetical protein study.
protein_data = {
    "protein_id": "P04637",
    "protein_name": "Tumor protein p53",
    "organism": "Homo sapiens",
    "sequence": "MEEPQSDPSV",
    "sequence_length": 10,
    "experimental_conditions": {
        "temperature_celsius": 37,
        "pH": 7.4
    },
    "validated": True,
    "related_genes": ["MDM2", "ATM", "CHEK2"]
}

# Save the structured data as JSON.
with open("protein_metadata.json", "w", encoding="utf-8") as file:
    json.dump(protein_data, file, indent=4)

# Load the JSON data into Python.
with open("protein_metadata.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)

print("Protein:", loaded_data["protein_name"])
print("Protein ID:", loaded_data["protein_id"])
print("Organism:", loaded_data["organism"])
print("Sequence:", loaded_data["sequence"])
print("Sequence length:", loaded_data["sequence_length"])
print(
    "Experimental temperature:",
    loaded_data["experimental_conditions"]["temperature_celsius"]
)
print("Related genes:", loaded_data["related_genes"])

# Convert a Python dictionary into a JSON string.
json_string = json.dumps(loaded_data, indent=4)

print("JSON representation:")
print(json_string)