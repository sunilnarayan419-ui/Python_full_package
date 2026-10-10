"""
TOPIC: json
MAIN POINTS:
- Convert Python objects to JSON strings.
- Convert JSON strings to Python objects.
- Read and write JSON files.
- Handle data types that JSON does not directly support.
"""

import json
from pathlib import Path

experiment = {
    "sample_id": "EXP001",
    "organism": "Arabidopsis thaliana",
    "temperature_c": 25,
    "gene_expression": [12.5, 13.2, 11.8],
    "quality_control_passed": True,
}

# Python dictionary -> JSON string
json_text = json.dumps(experiment, indent=4)
print(json_text)

# JSON string -> Python dictionary
restored_experiment = json.loads(json_text)
print("Sample ID:", restored_experiment["sample_id"])

# Save JSON to a file
json_file = Path("experiment.json")

with json_file.open("w", encoding="utf-8") as file:
    json.dump(experiment, file, indent=4)

# Load JSON from a file
with json_file.open("r", encoding="utf-8") as file:
    loaded_experiment = json.load(file)

print("Loaded organism:", loaded_experiment["organism"])

# JSON supports objects, arrays, strings, numbers, booleans, and null.
# Python tuples become JSON arrays; custom objects and some other
# Python types require explicit conversion.