from __future__ import annotations

import sys
from collections.abc import Iterator


class UniversitySpaceComplexity:
    """Demonstrates auxiliary space vs. input space using small
    biological datasets (DNA base sequences)."""

    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def count_bases_in_place(self) -> dict[str, int]:
        """Count occurrences of each base using one small fixed-size dict.

        Input space: O(n) for the sequence itself (not counted as auxiliary)
        Auxiliary space: O(1) since only 4 possible DNA bases exist
        Time: O(n)
        """
        counts = {"A": 0, "C": 0, "G": 0, "T": 0}
        for base in self.sequence:
            if base in counts:
                counts[base] += 1
        return counts

    def reversed_copy(self) -> str:
        """Build a full reversed copy of the sequence.

        Auxiliary space: O(n) - a brand-new string is allocated
        Time: O(n)
        """
        return self.sequence[::-1]

    @staticmethod
    def run() -> None:
        seq = "ACGTACGGTTACG"
        demo = UniversitySpaceComplexity(seq)
        print("University: base counts (O(1) auxiliary) ->", demo.count_bases_in_place())
        print("University: reversed copy (O(n) auxiliary) ->", demo.reversed_copy())


class InterviewSpaceComplexity:
    """Compares a memory-heavy solution against a memory-efficient one
    for the same problem: detecting a repeated k-mer (DNA substring) in
    a long sequence.
    """

    @staticmethod
    def find_repeated_kmer_heavy(sequence: str, k: int) -> str | None:
        """Store every k-mer in a list before checking for duplicates.

        Time: O(n)
        Space: O(n) - stores all n-k+1 substrings twice over (list + set)
        """
        if not sequence or k <= 0 or k > len(sequence):
            return None
        all_kmers = [sequence[i:i + k] for i in range(len(sequence) - k + 1)]
        seen: set[str] = set()
        for kmer in all_kmers:
            if kmer in seen:
                return kmer
            seen.add(kmer)
        return None

    @staticmethod
    def find_repeated_kmer_efficient(sequence: str, k: int) -> str | None:
        """Stream k-mers with a sliding window, avoiding the intermediate list.

        Time: O(n)
        Space: O(n - k) for the seen set only, no intermediate list built
        """
        if not sequence or k <= 0 or k > len(sequence):
            return None
        seen: set[str] = set()
        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i + k]
            if kmer in seen:
                return kmer
            seen.add(kmer)
        return None

    @classmethod
    def compare(cls, sequence: str, k: int) -> dict[str, str | None]:
        """Time: O(n), Space: O(n) combined across both calls."""
        return {
            "heavy_result": cls.find_repeated_kmer_heavy(sequence, k),
            "efficient_result": cls.find_repeated_kmer_efficient(sequence, k),
        }

    @staticmethod
    def run() -> None:
        sequence = "ACGTTGCAACGTGGCTA"
        result = InterviewSpaceComplexity.compare(sequence, 3)
        print("Interview: heavy approach result ->", result["heavy_result"])
        print("Interview: efficient approach result ->", result["efficient_result"])
        print("Interview: efficient version avoids materializing the full k-mer list.")


class IndustrySpaceComplexity:
    """Demonstrates memory-aware processing strategies for large
    genomic FASTA-style datasets: streaming vs. loading entire files
    into memory.
    """

    @staticmethod
    def _generate_fasta_lines(record_count: int, bases_per_record: int) -> Iterator[str]:
        """Lazily yield synthetic FASTA records without materializing them all.

        Auxiliary space: O(1) per yielded line
        """
        base_cycle = "ACGT"
        for record_id in range(record_count):
            yield f">record_{record_id}"
            yield base_cycle * (bases_per_record // 4)

    def compute_gc_content_streaming(self, record_count: int, bases_per_record: int) -> float:
        """Compute overall GC content without holding the whole dataset in memory.

        Time: O(n) where n is total bases processed
        Space: O(1) auxiliary - only running counters are kept
        """
        gc_count = 0
        total_count = 0
        for line in self._generate_fasta_lines(record_count, bases_per_record):
            if line.startswith(">"):
                continue
            for base in line:
                total_count += 1
                if base in ("G", "C"):
                    gc_count += 1
        return gc_count / total_count if total_count else 0.0

    def compute_gc_content_in_memory(self, record_count: int, bases_per_record: int) -> float:
        """Load every base into one large list before computing GC content.

        Time: O(n)
        Space: O(n) auxiliary - all bases are retained simultaneously
        """
        all_bases: list[str] = []
        for line in self._generate_fasta_lines(record_count, bases_per_record):
            if line.startswith(">"):
                continue
            all_bases.extend(line)
        gc_count = sum(1 for base in all_bases if base in ("G", "C"))
        return gc_count / len(all_bases) if all_bases else 0.0

    @staticmethod
    def run() -> None:
        processor = IndustrySpaceComplexity()
        streaming_result = processor.compute_gc_content_streaming(500, 40)
        in_memory_result = processor.compute_gc_content_in_memory(500, 40)
        print(f"Industry: streaming GC content -> {streaming_result:.3f} (O(1) auxiliary space)")
        print(f"Industry: in-memory GC content -> {in_memory_result:.3f} (O(n) auxiliary space)")
        print("Industry: streaming is preferred for large-scale FASTA processing pipelines.")


if __name__ == "__main__":
    UniversitySpaceComplexity.run()
    InterviewSpaceComplexity.run()
    IndustrySpaceComplexity.run()
