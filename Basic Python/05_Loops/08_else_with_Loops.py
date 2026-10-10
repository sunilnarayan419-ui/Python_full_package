
"""
08. else With Loops

Main points
- Python allows else clauses on both for and while loops.
- A loop's else block executes if the loop finishes normally.
- The else block does not execute if the loop terminates through break.
- continue does not prevent the loop's else block from executing.
- A while loop's else executes when its condition becomes False.
- Loop-else is useful for search operations where no match is found.
- It differs from the else clause of an if statement.
"""

# Example 1: Search for a gene.
gene_list = ["ACTB", "GAPDH", "TP53", "BRCA1"]
target_gene = "TP53"

for gene in gene_list:
    print("Checking:", gene)

    if gene == target_gene:
        print("Target gene found:", gene)
        break
else:
    print("Target gene was not found.")

# Example 2: Search for a missing gene.
target_gene = "MYC"

for gene in gene_list:
    if gene == target_gene:
        print("Target gene found:", gene)
        break
else:
    print("Target gene was not found.")

# Example 3: Use continue without preventing loop-else.
expression_values = [None, None, 12.5, 18.0]

for expression in expression_values:
    if expression is None:
        continue

    print("Valid measurement:", expression)
else:
    print("All available records were processed.")

# Example 4: Use while-else for a bounded search.
target_copy_count = 100
current_copy_count = 1
maximum_cycles = 8
cycle = 0

while current_copy_count < target_copy_count and cycle < maximum_cycles:
    current_copy_count *= 2
    cycle += 1

    print("Cycle:", cycle, "Copies:", current_copy_count)
else:
    print("Loop ended without break.")

# Example 5: Show that break skips loop-else.
for attempt in range(1, 6):
    print("Attempt:", attempt)

    if attempt == 2:
        print("Stopping early.")
        break
else:
    print("All attempts completed without break.")

# Important:
# Loop-else means "no break occurred", not simply "the loop had no errors."
