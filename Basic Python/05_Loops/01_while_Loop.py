
"""
01. while Loop

Main points
- A while loop repeats a block while its condition is True.
- The condition is evaluated before each iteration.
- The loop may execute zero times if the initial condition is False.
- Update the relevant variable to avoid an unintended infinite loop.
- while is useful when the number of iterations is not known beforehand.
- Common applications include retries, convergence checks, and monitoring.
"""

# Example 1: Simulate DNA sample processing.
samples_remaining = 5

while samples_remaining > 0:
    print("Processing DNA sample:", samples_remaining)
    samples_remaining -= 1

print("All samples processed.")

# Example 2: Continue analysis until a target is reached.
gene_expression = 10.0
target_expression = 20.0
iterations = 0

while gene_expression < target_expression:
    gene_expression *= 1.5
    iterations += 1

print("Final expression estimate:", gene_expression)
print("Iterations required:", iterations)

# Example 3: Simulate retries for a sequencing pipeline.
attempt = 0
maximum_attempts = 3
pipeline_success = False

while attempt < maximum_attempts and not pipeline_success:
    attempt += 1
    print("Pipeline attempt:", attempt)

    # Simulated success on the third attempt.
    if attempt == 3:
        pipeline_success = True

if pipeline_success:
    print("Pipeline completed successfully.")
else:
    print("Pipeline failed after all attempts.")

# These are illustrative simulations, not actual laboratory measurements.
