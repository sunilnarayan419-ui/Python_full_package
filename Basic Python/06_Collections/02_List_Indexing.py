
"""
02. List Indexing

Main points
- Indexing accesses an individual list element.
- Positive indexing starts at 0.
- Negative indexing starts at -1 from the end.
- Indexing beyond the valid range raises IndexError.
- Lists are mutable, so an element can be replaced using its index.
- len() returns the number of elements.
"""

gene_names = ["BRCA1", "TP53", "EGFR", "MYC", "APOE"]

# Positive indexing
print("First gene:", gene_names[0])
print("Third gene:", gene_names[2])

# Negative indexing
print("Last gene:", gene_names[-1])
print("Second-last gene:", gene_names[-2])

# Replace an element
gene_names[1] = "GAPDH"
print("Updated genes:", gene_names)

# Get the list length
print("Number of genes:", len(gene_names))

# Iterate through indices
for index in range(len(gene_names)):
    print(index, gene_names[index])

# Uncomment to observe IndexError:
# print(gene_names[100])
