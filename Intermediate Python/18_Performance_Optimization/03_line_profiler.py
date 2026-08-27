from __future__ import annotations

import random
import time
from typing import Callable, TypeVar

try:
    from line_profiler import LineProfiler
    _LINE_PROFILER_AVAILABLE = True
except ImportError:
    LineProfiler = None  # type: ignore[assignment]
    _LINE_PROFILER_AVAILABLE = False

T = TypeVar("T")


class SequenceAlignmentScorer:
    """Line-level profiling target: naive local alignment scoring.

    The scoring routine is intentionally structured so each line represents
    a distinct computational cost, making it a meaningful line-profiler
    target (matrix initialization, scoring recurrence, traceback scan).
    """

    def __init__(self, sequence_a: str, sequence_b: str, match: int = 2, mismatch: int = -1, gap: int = -2) -> None:
        if not sequence_a or not sequence_b:
            raise ValueError("sequence_a and sequence_b must be non-empty")
        self.sequence_a = sequence_a
        self.sequence_b = sequence_b
        self.match = match
        self.mismatch = mismatch
        self.gap = gap

    def score_alignment(self) -> int:
        rows = len(self.sequence_a) + 1
        cols = len(self.sequence_b) + 1
        matrix = [[0] * cols for _ in range(rows)]

        for row_index in range(1, rows):
            for col_index in range(1, cols):
                base_a = self.sequence_a[row_index - 1]
                base_b = self.sequence_b[col_index - 1]
                diagonal_score = matrix[row_index - 1][col_index - 1]
                diagonal_score += self.match if base_a == base_b else self.mismatch
                up_score = matrix[row_index - 1][col_index] + self.gap
                left_score = matrix[row_index][col_index - 1] + self.gap
                matrix[row_index][col_index] = max(0, diagonal_score, up_score, left_score)

        best_score = 0
        for row in matrix:
            row_max = max(row)
            if row_max > best_score:
                best_score = row_max
        return best_score

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    def profile_scoring(self) -> str:
        if not _LINE_PROFILER_AVAILABLE:
            raise RuntimeError(
                "line_profiler is not installed. Install it with 'pip install line_profiler' "
                "to enable line-by-line profiling of score_alignment()."
            )
        profiler = LineProfiler()
        wrapped = profiler(self.score_alignment)
        wrapped()
        stream_buffer: list[str] = []

        class _Writer:
            def write(self, text: str) -> None:
                stream_buffer.append(text)

            def flush(self) -> None:
                return None

        profiler.print_stats(stream=_Writer())  # type: ignore[arg-type]
        return "".join(stream_buffer)

    @staticmethod
    def _random_sequence(length: int, seed: int) -> str:
        rng = random.Random(seed)
        return "".join(rng.choice("ACGT") for _ in range(length))

    @staticmethod
    def run() -> None:
        sequence_a = SequenceAlignmentScorer._random_sequence(220, seed=1)
        sequence_b = SequenceAlignmentScorer._random_sequence(200, seed=2)
        scorer = SequenceAlignmentScorer(sequence_a, sequence_b)

        result, elapsed = scorer.benchmark(scorer.score_alignment)
        print(f"alignment_score={result}, elapsed={elapsed:.6f}s")

        if _LINE_PROFILER_AVAILABLE:
            report = scorer.profile_scoring()
            print("Line-level profiling report:")
            print(report)
        else:
            print(
                "line_profiler not installed; skipping line-level report. "
                "Install with 'pip install line_profiler' to enable it."
            )


if __name__ == "__main__":
    SequenceAlignmentScorer.run()
