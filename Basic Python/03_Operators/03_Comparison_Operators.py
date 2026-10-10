
"""
03. Comparison Operators

Main points
- Comparison operators evaluate relationships between values.
- == : Equal to.
- != : Not equal to.
- > : Greater than.
- < : Less than.
- >= : Greater than or equal to.
- <= : Less than or equal to.
- Comparisons generally return Boolean values: True or False.
- Chained comparisons such as 20 <= temperature <= 30 are valid.
- Comparisons are meaningful only when the values and units are appropriate.
"""

# Example 1: Check a laboratory temperature range
temperature_celsius = 25.0

print("Above 20 C:", temperature_celsius > 20)
print("Below 30 C:", temperature_celsius < 30)
print("Within range:", 20 <= temperature_celsius <= 30)

# Example 2: Compare gene expression values
control_expression = 12.5
treated_expression = 25.0

print("Expression increased:", treated_expression > control_expression)
print("Expression unchanged:", treated_expression == control_expression)
print("Expression differs:", treated_expression != control_expression)

# Example 3: Check sample quality
dna_concentration = 45.0
minimum_concentration = 20.0

is_concentration_sufficient = dna_concentration >= minimum_concentration
print("Concentration sufficient:", is_concentration_sufficient)

# Example 4: Compare sequencing read counts
sample_a_reads = 1_500_000
sample_b_reads = 1_200_000

print("A has more reads:", sample_a_reads > sample_b_reads)
print("Read counts are equal:", sample_a_reads == sample_b_reads)

# Example 5: Check an approximate laboratory target
measured_ph = 7.35
target_ph = 7.40
tolerance = 0.10

is_close_to_target = abs(measured_ph - target_ph) <= tolerance
print("pH is within tolerance:", is_close_to_target)

# A comparison does not establish biological significance.
# Statistical analysis and experimental context are separate requirements.
