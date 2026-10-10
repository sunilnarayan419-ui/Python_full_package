
"""
05. Keyword Arguments

Main points
- Keyword arguments identify parameters by name during a function call.
- They improve readability when a function has several parameters.
- Keyword arguments can be supplied in a different order from the definition.
- A parameter cannot receive multiple values unintentionally.
- Positional arguments must precede keyword arguments in a function call.
- Keyword arguments are useful for scientific functions with many settings.
"""

# Example 1: Describe a biological sample.
def describe_sample(sample_id, organism, tissue, temperature):
    return (
        f"{sample_id}: {organism}, tissue={tissue}, "
        f"temperature={temperature} C"
    )


# Supply arguments by parameter name.
report = describe_sample(
    sample_id="S001",
    organism="Arabidopsis thaliana",
    tissue="leaf",
    temperature=25.0
)

print(report)

# Example 2: Keyword arguments can change the order.
report = describe_sample(
    temperature=28.0,
    tissue="root",
    organism="Arabidopsis thaliana",
    sample_id="S002"
)

print(report)

# Example 3: Combine positional and keyword arguments.
def calculate_reagent_volume(volume_per_reaction, reaction_count, extra_fraction=0.1):
    return volume_per_reaction * reaction_count * (1 + extra_fraction)


volume = calculate_reagent_volume(
    0.025,
    96,
    extra_fraction=0.15
)

print("Required volume:", volume, "mL")

# Positional arguments first, keyword arguments afterwards.
