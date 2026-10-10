
"""
03. if-elif-else Statement

Main points
- elif means "else if" and tests another condition.
- Python evaluates conditions from top to bottom.
- The first condition that evaluates to True has its block executed.
- Remaining branches are skipped once a matching branch is found.
- else executes if none of the preceding conditions is True.
- Branch ordering matters when conditions overlap.
- This structure is useful for classification and multi-level decisions.
"""

# Example 1: Classify DNA concentration.
dna_concentration = 45.0  # ng/uL

if dna_concentration < 10.0:
    print("Very low DNA concentration.")
elif dna_concentration < 20.0:
    print("Low DNA concentration.")
elif dna_concentration < 50.0:
    print("Moderate DNA concentration.")
else:
    print("High DNA concentration.")

# Example 2: Classify sequencing read depth.
read_count = 2_500_000

if read_count < 100_000:
    print("Very low read count.")
elif read_count < 1_000_000:
    print("Low read count.")
elif read_count < 5_000_000:
    print("Moderate read count.")
else:
    print("High read count.")

# Example 3: Classify a gene expression change.
fold_change = 2.4

if fold_change < 1.0:
    print("Expression is lower than the reference.")
elif fold_change == 1.0:
    print("Expression is unchanged.")
else:
    print("Expression is higher than the reference.")

# Example 4: Classify a simplified quality-control result.
purity_ratio = 1.85

if purity_ratio < 1.6:
    print("Purity ratio is below the illustrative range.")
elif purity_ratio <= 2.0:
    print("Purity ratio is within the illustrative range.")
else:
    print("Purity ratio is above the illustrative range.")

# Important:
# A fold change alone does not establish statistical significance.
# Thresholds must be appropriate for the specific experiment.
