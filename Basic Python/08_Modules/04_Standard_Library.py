
"""
04. Standard Library

Main points
- The Python standard library is distributed with Python.
- It provides modules for mathematics, statistics, dates, files,
  JSON, CSV, random numbers, operating-system interfaces, and more.
- Standard-library modules usually require no separate pip installation.
- External packages such as NumPy, pandas, SciPy, and Biopython are
  not part of the standard library.
- Prefer standard-library tools when they adequately solve the problem.
- Some modules interact with the operating system and may behave differently
  across platforms.
"""

# Mathematics
import math

print("Square root:", math.sqrt(81))
print("Natural logarithm:", math.log(10))
print("Pi:", math.pi)

# Statistics
import statistics

measurements = [12.0, 15.0, 14.0, 18.0, 16.0]

print("Mean:", statistics.mean(measurements))
print("Median:", statistics.median(measurements))
print("Sample standard deviation:", statistics.stdev(measurements))

# Random numbers
import random

# Demonstration only: simulate a random measurement.
simulated_value = random.uniform(20.0, 30.0)
print("Simulated value:", simulated_value)

# Date and time
from datetime import date, datetime

today = date.today()
analysis_timestamp = datetime.now()

print("Date:", today)
print("Analysis timestamp:", analysis_timestamp)

# Count nucleotides using a standard-library collection.
from collections import Counter

dna_sequence = "ATGCGTAA"

nucleotide_counts = Counter(dna_sequence)
print("Nucleotide counts:", nucleotide_counts)

# Work with JSON-compatible biological metadata.
import json

sample = {
    "sample_id": "S001",
    "organism": "Arabidopsis thaliana",
    "temperature_celsius": 25.0
}

json_text = json.dumps(sample, indent=4)
print(json_text)

# The standard library helps build useful scientific tools
# before introducing external scientific-computing packages.
