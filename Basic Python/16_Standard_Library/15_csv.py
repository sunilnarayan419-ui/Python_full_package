"""
TOPIC: csv
MAIN POINTS:
- Read CSV files row by row.
- Write rows to a CSV file.
- Work with named columns using dictionaries.
- Use newline="" when opening CSV files.
"""

import csv
from pathlib import Path

csv_file = Path("gene_expression.csv")

# Example scientific dataset
samples = [
    {"sample_id": "S001", "condition": "Control", "expression": 10.5},
    {"sample_id": "S002", "condition": "Control", "expression": 11.2},
    {"sample_id": "S003", "condition": "Treatment", "expression": 15.7},
]

fieldnames = ["sample_id", "condition", "expression"]

# Write CSV
with csv_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(samples)

# Read CSV
with csv_file.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # CSV values are strings by default.
        expression = float(row["expression"])

        print(
            row["sample_id"],
            row["condition"],
            expression,
        )

# Calculate the mean expression for the treatment group
treatment_values = [
    float(row["expression"])
    for row in csv.DictReader(
        csv_file.open("r", newline="", encoding="utf-8")
    )
    if row["condition"] == "Treatment"
]

if treatment_values:
    mean_expression = sum(treatment_values) / len(treatment_values)
    print("Treatment mean:", mean_expression)


# alternative 

import csv
from pathlib import Path

csv_file = Path("gene_expression.csv")
treatment_values = []

with csv_file.open("r", newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        if row["condition"] == "Treatment":
            treatment_values.append(float(row["expression"]))

if treatment_values:
    print("Treatment mean:", sum(treatment_values) / len(treatment_values))