
"""
04. Nested if Statements

Main points
- A nested if is an if statement inside another conditional block.
- The inner condition is evaluated only if execution reaches it.
- Nested conditions represent decisions that depend on earlier decisions.
- Indentation determines which condition controls each block.
- Excessive nesting can reduce readability; logical operators or early returns
  may provide a simpler alternative.
- Nested if statements are useful for sequential quality-control decisions.
"""

# Example 1: Evaluate a DNA sample through sequential QC checks.
dna_concentration = 35.0  # ng/uL
purity_ratio = 1.85
contamination_detected = False

if dna_concentration >= 20.0:
    print("Concentration check passed.")

    if 1.8 <= purity_ratio <= 2.0:
        print("Purity check passed.")

        if not contamination_detected:
            print("Sample passed these illustrative QC checks.")
        else:
            print("Sample requires contamination investigation.")

    else:
        print("Purity check failed.")

else:
    print("Concentration check failed.")

# Example 2: A simplified bioinformatics pipeline.
dataset_available = True
reference_genome_available = True

if dataset_available:
    print("Input dataset found.")

    if reference_genome_available:
        print("Reference genome found.")
        print("Alignment can be considered for execution.")
    else:
        print("Cannot proceed: reference genome is unavailable.")

else:
    print("Cannot proceed: input dataset is unavailable.")

# Important:
# Passing these example checks is not equivalent to validating an assay
# or certifying that a bioinformatics pipeline is scientifically correct.
