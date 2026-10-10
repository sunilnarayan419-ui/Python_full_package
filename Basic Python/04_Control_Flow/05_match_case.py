
"""
05. match-case Statement

Main points
- match-case was introduced in Python 3.10.
- It performs structural pattern matching.
- match evaluates a subject against case patterns in order.
- The first matching case is selected.
- case _ acts as a catch-all fallback pattern.
- Patterns can match literal values, sequences, mappings, and class structures.
- A guard using if can add a condition to a case.
- match-case is useful when handling discrete commands or known categories.
- It is not a direct replacement for every if-elif chain.
"""

# Example 1: Choose a bioinformatics analysis operation.
analysis_type = "alignment"

match analysis_type:
    case "quality_control":
        print("Running sequencing quality-control analysis.")

    case "alignment":
        print("Aligning reads to a reference genome.")

    case "variant_calling":
        print("Identifying candidate genetic variants.")

    case "gene_expression":
        print("Quantifying gene expression.")

    case _:
        print("Unknown analysis type.")

# Example 2: Interpret a simplified laboratory status code.
sample_status = 2

match sample_status:
    case 0:
        print("Sample registered.")

    case 1:
        print("Sample processing.")

    case 2:
        print("Sample analysis completed.")

    case 3:
        print("Sample requires review.")

    case _:
        print("Unrecognized sample status.")

# Example 3: Match a tuple describing an experiment.
experiment = ("RNA-seq", "human")

match experiment:
    case ("RNA-seq", "human"):
        print("Human RNA sequencing workflow selected.")

    case ("RNA-seq", "plant"):
        print("Plant RNA sequencing workflow selected.")

    case ("WGS", organism):
        print(f"Whole-genome sequencing workflow: {organism}")

    case _:
        print("Workflow not configured.")

# Example 4: Use a guard condition.
read_count = 2_000_000

match read_count:
    case count if count < 100_000:
        print("Low sequencing depth.")

    case count if count < 5_000_000:
        print("Intermediate sequencing depth.")

    case _:
        print("High sequencing depth.")

# Python 3.10 or later is required for match-case.
# The categories and thresholds above are illustrative.
