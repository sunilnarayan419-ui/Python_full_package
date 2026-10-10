"""
PROJECT: Biological Sample Analyzer

OBJECTIVES
- Use len() to measure sequence lengths.
- Use sum(), min(), and max() to summarize sequence data.
- Use round() for readable output.
- Use sorted() to rank biological samples.
- Use enumerate() to number results.
- Use isinstance() to validate data types.
- Use all() and any() for quality checks.
- Use open() and print() to generate a report.
"""

samples = [
    {
        "sample_id": "S001",
        "organism": "Homo sapiens",
        "sequence": "ATGCGCGT"
    },
    {
        "sample_id": "S002",
        "organism": "Mus musculus",
        "sequence": "TTAGGCAT"
    },
    {
        "sample_id": "S003",
        "organism": "Arabidopsis thaliana",
        "sequence": "GGCCATTA"
    },
    {
        "sample_id": "S004",
        "organism": "Homo sapiens",
        "sequence": "ATATATAT"
    }
]

valid_bases = {"A", "T", "G", "C"}

# Step 1: Validate the records.
valid_samples = []

for sample in samples:
    sequence = sample.get("sequence")

    if not isinstance(sequence, str):
        continue

    sequence = sequence.upper()

    if sequence and set(sequence) <= valid_bases:
        valid_samples.append({
            **sample,
            "sequence": sequence
        })

# Step 2: Calculate sequence statistics.
results = []

for sample in valid_samples:
    sequence = sample["sequence"]

    length = len(sequence)
    gc_count = sequence.count("G") + sequence.count("C")
    gc_percentage = gc_count / length * 100

    results.append({
        "sample_id": sample["sample_id"],
        "organism": sample["organism"],
        "length": length,
        "gc_count": gc_count,
        "gc_percentage": gc_percentage
    })

# Step 3: Summarize the results.
lengths = [
    result["length"]
    for result in results
]

gc_percentages = [
    result["gc_percentage"]
    for result in results
]

total_nucleotides = sum(lengths)

mean_length = (
    total_nucleotides / len(lengths)
    if lengths
    else 0
)

minimum_length = min(lengths, default=0)
maximum_length = max(lengths, default=0)

# Step 4: Rank samples by GC percentage.
ranked_results = sorted(
    results,
    key=lambda result: result["gc_percentage"],
    reverse=True
)

# Step 5: Perform basic quality checks.
all_sequences_valid = all(
    set(sample["sequence"]) <= valid_bases
    for sample in valid_samples
)

has_gc_rich_sample = any(
    result["gc_percentage"] >= 60
    for result in results
)

# Step 6: Display the report.
print("BIOLOGICAL SAMPLE ANALYSIS")
print("=" * 55)

for rank, result in enumerate(ranked_results, start=1):
    print(
        f"{rank}. {result['sample_id']} | "
        f"{result['organism']} | "
        f"Length: {result['length']} | "
        f"GC: {result['gc_percentage']:.2f}%"
    )

print("=" * 55)
print("Valid samples:", len(results))
print("Total nucleotides:", total_nucleotides)
print("Mean sequence length:", round(mean_length, 2))
print("Minimum sequence length:", minimum_length)
print("Maximum sequence length:", maximum_length)
print("All sequences valid:", all_sequences_valid)
print("Any sample with GC >= 60%:", has_gc_rich_sample)

# Step 7: Save the report.
with open(
    "biological_sample_report.txt",
    "w",
    encoding="utf-8"
) as file:
    print("BIOLOGICAL SAMPLE ANALYSIS", file=file)

    for rank, result in enumerate(ranked_results, start=1):
        print(
            f"{rank}. {result['sample_id']} | "
            f"Length: {result['length']} | "
            f"GC: {result['gc_percentage']:.2f}%",
            file=file
        )

print("\nReport saved to biological_sample_report.txt")