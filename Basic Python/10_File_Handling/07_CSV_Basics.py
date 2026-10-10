"""
TOPIC: CSV Basics

MAIN POINTS
- CSV stands for Comma-Separated Values.
- CSV files store tabular data as rows and columns.
- Python's csv module provides csv.reader(), csv.writer(), DictReader, and DictWriter.
- DictReader accesses each row using column names.
- Use newline="" when opening CSV files for writing.
- CSV files are widely used for gene expression measurements, clinical datasets, and experimental results.
- The csv module reads values as strings, so numerical conversion may be necessary.
"""

import csv

# Simulated gene expression dataset.
gene_data = [
    {"gene": "BRCA1", "expression": 24.6, "condition": "Control"},
    {"gene": "TP53", "expression": 18.2, "condition": "Treatment"},
    {"gene": "EGFR", "expression": 42.8, "condition": "Treatment"},
    {"gene": "MYC", "expression": 35.1, "condition": "Control"}
]

# Write the dataset to a CSV file.
with open("gene_expression.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["gene", "expression", "condition"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(gene_data)

# Read the CSV file using column names.
with open("gene_expression.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        gene = row["gene"]
        expression = float(row["expression"])
        condition = row["condition"]

        print(
            f"Gene: {gene}, "
            f"Expression: {expression}, "
            f"Condition: {condition}"
        )

# Calculate mean expression for the treatment group.
treatment_values = [
    float(row["expression"])
    for row in csv.DictReader(
        open("gene_expression.csv", newline="", encoding="utf-8")
    )
    if row["condition"] == "Treatment"
]

mean_expression = sum(treatment_values) / len(treatment_values)

print("Mean treatment expression:", round(mean_expression, 2))