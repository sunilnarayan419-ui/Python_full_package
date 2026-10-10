"""
TOPIC: Ternary Operator

MAIN POINTS
- The conditional expression selects one of two values.
- Syntax: value_if_true if condition else value_if_false.
- It is useful for short, simple decisions.
- It can replace a small if-else block that assigns a value.
- Nested ternary expressions can become difficult to read.
- Use regular if-elif-else statements for complex scientific decision logic.
"""

# Example 1: Classify a DNA sequence by length.
sequence = "ATGCGTAC"

length_category = (
    "Long sequence"
    if len(sequence) >= 8
    else "Short sequence"
)

print("Length category:", length_category)


# Example 2: Calculate a GC percentage safely.
sequence = "ATGCGC"

gc_percentage = (
    (sequence.count("G") + sequence.count("C"))
    / len(sequence) * 100
    if sequence
    else 0.0
)

print("GC percentage:", gc_percentage)


# Example 3: Classify an illustrative purity ratio.
purity_ratio = 1.92

quality_status = (
    "Within illustrative range"
    if 1.8 <= purity_ratio <= 2.0
    else "Outside illustrative range"
)

print("Quality status:", quality_status)


# Example 4: Assign an expression category.
expression = 42.8

expression_category = (
    "High"
    if expression >= 40
    else "Moderate"
    if expression >= 20
    else "Low"
)

print("Expression category:", expression_category)


# Example 5: Process multiple genes.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8,
    "MYC": 35.1
}

for gene, expression in gene_expression.items():
    category = (
        "High"
        if expression >= 40
        else "Moderate"
        if expression >= 20
        else "Low"
    )

    print(f"{gene}: {expression} -> {category}")


# Example 6: Use ordinary if-elif-else for complex logic.
sample_purity = 1.92
sample_concentration = 45.0

if sample_concentration <= 0:
    status = "Invalid concentration"
elif not 1.8 <= sample_purity <= 2.0:
    status = "Review purity"
else:
    status = "Passes illustrative checks"

print("Sample status:", status)