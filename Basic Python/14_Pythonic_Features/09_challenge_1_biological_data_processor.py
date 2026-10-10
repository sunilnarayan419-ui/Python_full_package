"""
PROJECT: Biological Sample Data Processor

OBJECTIVES
- Represent sample records using dictionaries.
- Use comprehensions to filter and transform records.
- Use unpacking to access structured data.
- Use the walrus operator to reuse calculations.
- Use a context manager to save a report.
"""

from pathlib import Path

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
        "sequence": ""
    }
]

valid_bases = {"A", "T", "G", "C"}

# Step 1: Keep non-empty sequences containing valid DNA bases.
valid_samples = [
    sample
    for sample in samples
    if sample["sequence"]
    and set(sample["sequence"].upper()) <= valid_bases
]

# Step 2: Create an analysis report for every valid sample.
analysis_results = [
    {
        "sample_id": sample_id,
        "organism": organism,
        "length": len(sequence),
        "gc_percentage": (
            gc_count / len(sequence) * 100
        ),
        "category": (
            "GC-rich"
            if gc_count / len(sequence) * 100 >= 50
            else "AT-rich"
        )
    }
    for sample in valid_samples
    for sample_id, organism, sequence in [
        (
            sample["sample_id"],
            sample["organism"],
            sample["sequence"].upper()
        )
    ]
    if (gc_count := sequence.count("G") + sequence.count("C")) >= 0
]

# Step 3: Convert results into a dictionary keyed by sample ID.
results_by_sample = {
    result["sample_id"]: result
    for result in analysis_results
}

# Step 4: Display the results.
for sample_id, result in results_by_sample.items():
    print(
        sample_id,
        result["organism"],
        result["length"],
        round(result["gc_percentage"], 2),
        result["category"]
    )

# Step 5: Save a report using a context manager.
report_path = Path("sample_analysis_report.txt")

with open(report_path, "w", encoding="utf-8") as report:
    report.write("BIOLOGICAL SAMPLE ANALYSIS\n")
    report.write("=" * 50 + "\n")

    for sample_id, result in results_by_sample.items():
        report.write(
            f"{sample_id}\t"
            f"{result['organism']}\t"
            f"{result['length']}\t"
            f"{result['gc_percentage']:.2f}\t"
            f"{result['category']}\n"
        )

print("\nReport saved to:", report_path)