
"""
04. Logical Operators

Main points
- and evaluates whether both operands are truthy.
- or evaluates whether at least one operand is truthy.
- not reverses the truth value of an expression.
- Logical operators short-circuit when the result is already determined.
- In Python, and and or return one of their operands, not necessarily bool.
- Use parentheses to make complex conditions easier to understand.
- Logical conditions can represent quality-control and eligibility rules.
"""

# Example 1: DNA sample quality control
dna_concentration = 35.0
purity_ratio = 1.85

concentration_ok = dna_concentration >= 20
purity_ok = 1.8 <= purity_ratio <= 2.0

sample_passes_qc = concentration_ok and purity_ok
print("Sample passes QC:", sample_passes_qc)

# Example 2: Accept a sample if either sequencing method succeeded
illumina_success = False
nanopore_success = True

sequencing_available = illumina_success or nanopore_success
print("Sequencing data available:", sequencing_available)

# Example 3: Identify samples that are not contaminated
contamination_detected = False

sample_is_clean = not contamination_detected
print("Sample is clean:", sample_is_clean)

# Example 4: Combine multiple biological conditions
temperature = 28
nutrient_available = True
light_available = True

growth_conditions_met = (
    20 <= temperature <= 35
    and nutrient_available
    and light_available
)

print("Growth conditions met:", growth_conditions_met)

# Example 5: Short-circuit evaluation
gene_expression = None

# The second condition is evaluated only if the first is True.
if gene_expression is not None and gene_expression > 10:
    print("High gene expression detected.")
else:
    print("Expression is missing or not above the threshold.")

# Important: Boolean conditions alone do not establish causality.
