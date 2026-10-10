
"""
08. Operator Precedence

Main points
- Operator precedence determines which operations are evaluated first.
- Parentheses can explicitly control the order of evaluation.
- Exponentiation has higher precedence than multiplication and addition.
- Multiplication and division have higher precedence than addition.
- Comparisons are evaluated after arithmetic expressions.
- 'not' has lower precedence than comparisons.
- 'and' has higher precedence than 'or'.
- Bitwise operators have their own precedence levels.
- When in doubt, use parentheses for clarity.
"""

# Example 1: Calculate the concentration after dilution
initial_concentration = 100.0
initial_volume = 2.0
final_volume = 10.0

# Multiplication and division occur before addition or subtraction.
final_concentration = (
    initial_concentration * initial_volume
) / final_volume

print("Final concentration:", final_concentration)

# Example 2: Parentheses change the result
result_a = 2 + 3 * 4
result_b = (2 + 3) * 4

print("Without parentheses:", result_a)
print("With parentheses:", result_b)

# Example 3: Exponentiation versus multiplication
copies_a = 2 * 3 ** 2
copies_b = (2 * 3) ** 2

print("First result:", copies_a)
print("Second result:", copies_b)

# Example 4: Compare a laboratory measurement
temperature = 28
ph_value = 7.2

# Comparisons are evaluated before the logical AND.
acceptable = 20 <= temperature <= 35 and 6.5 <= ph_value <= 8.0

print("Measurements acceptable:", acceptable)

# Example 5: and versus or
# Parentheses make the intended grouping explicit.
gene_detected = True
contamination_detected = False
control_passed = True

result = (
    gene_detected
    and control_passed
    or contamination_detected
)

print("Pipeline condition:", result)

# Explicit grouping is easier to review.
result_clear = (
    (gene_detected and control_passed)
    or contamination_detected
)

print("Explicitly grouped result:", result_clear)

# Example 6: Calculate ideal PCR amplification
initial_copies = 100
cycles = 10

expected_copies = initial_copies * (2 ** cycles)

print("Ideal theoretical copies:", expected_copies)

# This model assumes perfect doubling per cycle.
