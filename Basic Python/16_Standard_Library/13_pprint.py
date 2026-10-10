"""
TOPIC: pprint
MAIN POINTS:
- Display nested data in a readable format.
- Control indentation and line width.
- Improve debugging of complex data structures.
"""

from pprint import pprint, pformat

experiment = {
    "experiment_id": "EXP001",
    "organism": "Arabidopsis thaliana",
    "conditions": {
        "temperature_c": 25,
        "light_hours": 16,
    },
    "measurements": {
        "gene_A": [12.4, 13.1, 11.9],
        "gene_B": [7.2, 8.1, 7.8],
    },
    "quality_control": {
        "passed": True,
        "warnings": [],
    },
}

# Print nested data in a readable format
pprint(experiment, indent=4, width=60)

# Convert the formatted output into a string
formatted_text = pformat(experiment, indent=2, width=50)
print("Formatted string:")
print(formatted_text)

# pprint is helpful for debugging Python objects.
# JSON serialization is more appropriate when you need
# to exchange structured data with another application.