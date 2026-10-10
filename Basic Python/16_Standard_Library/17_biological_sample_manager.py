"""
PROJECT: Biological Sample Manager
MODULES: csv, json, re, statistics, collections, pathlib, datetime

MAIN POINTS:
- Read scientific data from CSV.
- Validate sample identifiers with regular expressions.
- Group samples using defaultdict.
- Calculate descriptive statistics.
- Export a structured JSON report.
"""

import csv
import json
import re
import statistics

from collections import defaultdict
from datetime import datetime
from pathlib import Path


# --------------------------------------------------
# 1. CREATE A DEMONSTRATION DATASET
# --------------------------------------------------

data_directory = Path("biological_data")
data_directory.mkdir(parents=True, exist_ok=True)

csv_file = data_directory / "samples.csv"
json_file = data_directory / "summary_report.json"

sample_data = [
    {"sample_id": "EXP001", "condition": "Control", "expression": 10.5},
    {"sample_id": "EXP002", "condition": "Control", "expression": 11.2},
    {"sample_id": "EXP003", "condition": "Control", "expression": 9.8},
    {"sample_id": "EXP004", "condition": "Treatment", "expression": 15.7},
    {"sample_id": "EXP005", "condition": "Treatment", "expression": 16.3},
    {"sample_id": "EXP006", "condition": "Treatment", "expression": 14.9},
]

with csv_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["sample_id", "condition", "expression"],
    )
    writer.writeheader()
    writer.writerows(sample_data)


# --------------------------------------------------
# 2. LOAD AND VALIDATE DATA
# --------------------------------------------------

valid_sample_pattern = re.compile(r"EXP\d{3}")
samples_by_condition = defaultdict(list)
valid_sample_count = 0

with csv_file.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        sample_id = row["sample_id"]

        if not valid_sample_pattern.fullmatch(sample_id):
            print("Invalid sample ID:", sample_id)
            continue

        expression = float(row["expression"])

        sample = {
            "sample_id": sample_id,
            "condition": row["condition"],
            "expression": expression,
        }

        samples_by_condition[row["condition"]].append(sample)
        valid_sample_count += 1


# --------------------------------------------------
# 3. CALCULATE SUMMARY STATISTICS
# --------------------------------------------------

summary = {}

for condition, samples in samples_by_condition.items():
    values = [sample["expression"] for sample in samples]

    summary[condition] = {
        "sample_count": len(values),
        "mean_expression": round(statistics.mean(values), 3),
        "median_expression": round(statistics.median(values), 3),
        "minimum_expression": min(values),
        "maximum_expression": max(values),
    }


# --------------------------------------------------
# 4. BUILD THE REPORT
# --------------------------------------------------

report = {
    "report_generated_at": datetime.now().isoformat(timespec="seconds"),
    "total_valid_samples": valid_sample_count,
    "conditions": summary,
}

with json_file.open("w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("\nBIOLOGICAL SAMPLE REPORT")
print("=" * 35)
print("Valid samples:", valid_sample_count)

for condition, result in summary.items():
    print(f"\nCondition: {condition}")
    print("Sample count:", result["sample_count"])
    print("Mean expression:", result["mean_expression"])
    print("Median expression:", result["median_expression"])

print("\nJSON report saved to:", json_file)