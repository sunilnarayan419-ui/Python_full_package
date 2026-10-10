"""
TOPIC: Writing Files

MAIN POINTS
- Use open(file_path, "w") to write data to a file.
- The "w" mode creates a file if it does not exist.
- Opening an existing file in "w" mode overwrites its previous contents.
- Use write() to write strings to a file.
- Use \n to separate records into different lines.
- Writing files is useful for storing analysis results, gene sequences, and experimental summaries.
"""

# Gene expression measurements from a laboratory experiment.
gene_expression = {
    "BRCA1": 24.6,
    "TP53": 18.2,
    "EGFR": 42.8,
    "MYC": 35.1
}

# Write the measurements to a text file.
with open("gene_expression_report.txt", "w") as file:
    file.write("GENE EXPRESSION REPORT\n")
    file.write("Gene\tExpression_Level\n")

    for gene, expression in gene_expression.items():
        file.write(f"{gene}\t{expression}\n")

print("Gene expression report saved.")

# Read the generated report.
with open("gene_expression_report.txt", "r") as file:
    print(file.read())