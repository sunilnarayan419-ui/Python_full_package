
"""
02. Parameters

Main points
- Parameters are names listed in a function definition.
- Arguments are the actual values supplied when calling a function.
- Functions can accept zero, one, or multiple parameters.
- Each parameter receives a corresponding argument according to
  the calling convention.
- Parameters allow the same function to process different data.
- Descriptive parameter names improve readability.
"""

# Example 1: Calculate the total reagent volume.
def calculate_total_volume(volume_per_reaction, reaction_count):
    return volume_per_reaction * reaction_count


total_volume = calculate_total_volume(0.025, 96)

print("Total reagent volume:", total_volume, "mL")

# volume_per_reaction and reaction_count are parameters.
# 0.025 and 96 are arguments.

# Example 2: Calculate fold change.
def calculate_fold_change(treated_expression, control_expression):
    return treated_expression / control_expression


fold_change = calculate_fold_change(24.0, 8.0)
print("Fold change:", fold_change)

# Example 3: A function with three parameters.
def describe_sample(sample_id, organism, tissue):
    return (
        f"Sample {sample_id}: {organism}, "
        f"tissue = {tissue}"
    )


description = describe_sample(
    "S002",
    "Arabidopsis thaliana",
    "leaf"
)

print(description)

# Example 4: Parameters can represent different data types.
def create_sample_record(sample_id, concentration, passed_qc):
    return {
        "sample_id": sample_id,
        "concentration": concentration,
        "passed_qc": passed_qc
    }


record = create_sample_record("S003", 35.5, True)
print(record)
