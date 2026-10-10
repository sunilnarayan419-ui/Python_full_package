
"""
10. Variable Scope

Main points
- Scope determines where a variable name can be accessed.
- Python commonly resolves names using the LEGB rule:
  Local, Enclosing, Global, Built-in.
- Local names belong to a function's local scope.
- Enclosing names belong to an outer function.
- Global names belong to the module's global scope.
- Built-in names include functions such as len(), sum(), and print().
- A variable's scope is different from the lifetime of the object it references.
"""

# Global scope
organism = "Arabidopsis thaliana"


def analyze_sample():
    # Local scope
    sample_id = "S001"

    # The function can read a global variable.
    print("Sample:", sample_id)
    print("Organism:", organism)


analyze_sample()

# Built-in name
sequence = "ATGC"
print("Sequence length:", len(sequence))

# A local variable is not accessible outside the function.
# Uncomment to observe NameError:
# print(sample_id)

# Example: local names can have the same spelling as global names.
expression_level = 100


def report_expression():
    expression_level = 25
    print("Local expression:", expression_level)


report_expression()
print("Global expression:", expression_level)

# The local assignment does not modify the global variable.
