
"""
11. Local Scope

Main points
- Variables assigned inside a function are generally local to that function,
  unless declared global or nonlocal.
- Local variables can be accessed within their function.
- Different function calls have their own local namespaces.
- Local variables help prevent accidental changes to unrelated state.
- A local variable cannot normally be accessed directly outside its function.
- If a name is assigned anywhere in a function, Python generally treats it
  as local throughout that function unless declared otherwise.
"""

# Example 1: Local measurements.
def calculate_mean(expression_values):
    total = sum(expression_values)
    count = len(expression_values)
    mean = total / count

    return mean


result = calculate_mean([10.0, 12.0, 14.0])
print("Mean expression:", result)

# total, count, and mean are local names.

# Example 2: Separate calls use separate local variables.
def calculate_sample_score(expression):
    score = expression * 2
    return score


score_a = calculate_sample_score(10)
score_b = calculate_sample_score(15)

print("Sample A score:", score_a)
print("Sample B score:", score_b)

# Example 3: Local assignments do not alter the global name.
sample_count = 100


def process_batch():
    sample_count = 20
    print("Batch sample count:", sample_count)


process_batch()
print("Global sample count:", sample_count)

# Local variables improve isolation and make functions easier to test.
