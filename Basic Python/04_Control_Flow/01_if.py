
"""
01. if Statement

Main points
- The if statement executes a block when a condition evaluates to True.
- A condition is usually a comparison, logical expression, or Boolean value.
- A colon (:) introduces the conditional block.
- Indentation defines the block of code to execute.
- Python treats certain values as falsy, including False, None, 0, and empty collections.
- If the condition is False, the block is skipped.
- Use if when an action should occur only when a specific condition is met.
"""

# Example 1: Check whether DNA concentration is sufficient.
dna_concentration = 35.0  # ng/uL
minimum_concentration = 20.0  # ng/uL

if dna_concentration >= minimum_concentration:
    print("DNA concentration is sufficient for further evaluation.")

# Example 2: Detect a gene in a sample.
gene_detected = True

if gene_detected:
    print("Target gene detected.")

# Example 3: Check whether a sequencing dataset contains reads.
sequencing_reads = 1_500_000

if sequencing_reads > 0:
    print("Sequencing data is available.")

# Example 4: Check whether a gene expression value exceeds a threshold.
gene_expression = 12.5
expression_threshold = 10.0

if gene_expression > expression_threshold:
    print("Gene expression exceeds the selected threshold.")

# Example 5: Check whether a biological dataset is non-empty.
gene_list = ["BRCA1", "TP53", "EGFR"]

if gene_list:
    print("Genes available for analysis:", gene_list)

# Important:
# Passing one condition does not establish statistical significance
# or biological importance.
