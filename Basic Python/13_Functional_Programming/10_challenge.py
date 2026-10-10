"""
PROJECT: Gene Expression Ranking Pipeline

OBJECTIVES
- Pair gene IDs with measurements using zip().
- Filter genes using filter().
- Transform values using map().
- Validate measurements using all().
- Detect threshold-crossing genes using any().
- Rank genes using sorted() and key functions.
- Calculate a summary using sum() and a generator expression.
"""

gene_ids = [
    "BRCA1",
    "TP53",
    "EGFR",
    "MYC",
    "GAPDH",
    "BRAF"
]

expression_values = [
    24.6,
    18.2,
    42.8,
    35.1,
    8.4,
    51.7
]

# Step 1: Pair identifiers and measurements.
records = [
    {"gene": gene, "expression": float(expression)}
    for gene, expression in zip(
        gene_ids,
        expression_values,
        strict=True
    )
]

# Step 2: Validate the measurements.
all_non_negative = all(
    record["expression"] >= 0
    for record in records
)

if not all_non_negative:
    raise ValueError("Negative expression measurement found.")

# Step 3: Filter genes with expression >= 20.
selected_genes = filter(
    lambda record: record["expression"] >= 20,
    records
)

selected_genes = list(selected_genes)

# Step 4: Rank selected genes by expression.
ranked_genes = sorted(
    selected_genes,
    key=lambda record: record["expression"],
    reverse=True
)

# Step 5: Print the ranked report.
print("GENE EXPRESSION RANKING")
print("-" * 35)

for rank, record in enumerate(ranked_genes, start=1):
    print(
        f"{rank}. {record['gene']}: "
        f"{record['expression']}"
    )

# Step 6: Calculate the mean expression among selected genes.
mean_expression = (
    sum(
        record["expression"]
        for record in ranked_genes
    ) / len(ranked_genes)
    if ranked_genes
    else 0.0
)

print("-" * 35)
print("Selected gene count:", len(ranked_genes))
print("Mean selected expression:", round(mean_expression, 2))

# Step 7: Check whether any selected gene exceeds 40.
has_high_expression = any(
    record["expression"] > 40
    for record in ranked_genes
)

print("Any selected gene > 40:", has_high_expression)