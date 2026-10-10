"""
TOPIC: eval()

MAIN POINTS
- eval() evaluates a Python expression supplied as a string.
- It can return the result of arithmetic and other expressions.
- Never pass untrusted user input to eval().
- Arbitrary expression evaluation can execute unintended code and create serious security vulnerabilities.
- For simple numerical input, use int(), float(), or a dedicated parser instead.
- eval() is rarely necessary in ordinary scientific application code.
"""

# Example 1: Evaluate a trusted mathematical expression.
expression = "12 * 5 + 3"

result = eval(expression)

print("Result:", result)

# Example 2: Calculate a trusted expression from known constants.
# The expression is authored by the program, not entered by a user.
dna_length = 100
gc_count = 45

gc_percentage = eval(
    "gc_count / dna_length * 100"
)

print("GC percentage:", gc_percentage)

# Example 3: Demonstrate the safer alternative for numerical input.
numeric_text = "42.5"

concentration = float(numeric_text)

print("Concentration:", concentration)

# Example 4: Parse a fixed set of allowed scientific operations.
# Explicit dispatch is safer than evaluating arbitrary expressions.
operations = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b
}

operation = "multiply"
result = operations[operation](12, 5)

print("Calculated result:", result)

# SECURITY RULE:
# Do not write:
# user_expression = input("Enter an expression: ")
# result = eval(user_expression)
#
# An attacker could supply an expression that performs
# unintended operations in the program's environment.