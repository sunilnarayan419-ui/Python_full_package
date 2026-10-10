
"""
05. break

Main points
- break immediately terminates the nearest enclosing loop.
- Execution continues with the first statement after that loop.
- break is useful when a target is found or a stopping condition is met.
- In nested loops, break exits only the innermost loop.
- break can be used in both for and while loops.
"""

# Example 1: Stop searching when a target gene is found.
gene_list = ["ACTB", "GAPDH", "TP53", "BRCA1", "EGFR"]
target_gene = "TP53"

for gene in gene_list:
    print("Checking:", gene)

    if gene == target_gene:
        print("Target gene found.")
        break

# Example 2: Stop processing when a failed sample is detected.
sample_results = [
    ("S001", True),
    ("S002", True),
    ("S003", False),
    ("S004", True)
]

for sample_id, passed_qc in sample_results:
    if not passed_qc:
        print("QC failure detected in:", sample_id)
        break

    print("QC passed:", sample_id)

# Example 3: Stop a retry loop after success.
attempt = 0
maximum_attempts = 5

while attempt < maximum_attempts:
    attempt += 1
    print("Attempt:", attempt)

    if attempt == 3:
        print("Simulated pipeline success.")
        break

print("Retry loop finished.")

# Important:
# In nested loops, break exits only the nearest enclosing loop.
