
"""
02. if-else Statement

Main points
- if executes a block when the condition is True.
- else executes when the if condition is False.
- The two branches are mutually exclusive.
- Both branches must use consistent indentation.
- if-else is useful for binary decisions such as pass/fail or detected/not detected.
- The else branch does not require a condition.
"""

# Example 1: DNA sample quality assessment.
dna_concentration = 18.5
minimum_concentration = 20.0

if dna_concentration >= minimum_concentration:
    print("PASS: Concentration meets the selected threshold.")
else:
    print("FAIL: Concentration is below the selected threshold.")

# Example 2: Check whether a target sequence was detected.
target_gene_detected = False

if target_gene_detected:
    print("Target gene detected.")
else:
    print("Target gene not detected.")

# Example 3: Determine whether a dataset has usable observations.
expression_data = []

if expression_data:
    print("Dataset contains observations.")
else:
    print("Dataset is empty.")

# Example 4: Check a laboratory temperature range.
temperature_celsius = 37.0

if 35.0 <= temperature_celsius <= 39.0:
    print("Temperature is within the selected range.")
else:
    print("Temperature is outside the selected range.")

# These thresholds are illustrative.
# Real laboratory acceptance criteria depend on the assay and protocol.
