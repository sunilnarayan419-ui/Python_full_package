from __future__ import annotations

import multiprocessing as mp
import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def _score_sequence_pair(pair: tuple[str, str]) -> int:
    """Worker function: CPU-bound Hamming-style mismatch scoring for a sequence pair."""
    sequence_a, sequence_b = pair
    length = min(len(sequence_a), len(sequence_b))
    score = 0
    for index in range(length):
        if sequence_a[index] == sequence_b[index]:
            score += 2
        else:
            score -= 1
    return score


class ParallelSequenceScoringWorkflow:
    """Compares serial vs multiprocessing execution for CPU-bound sequence scoring.

    Workload: scoring many pairs of DNA reads against a reference read,
    representative of batch alignment-quality scoring in a sequencing pipeline.
    """

    def __init__(self, num_pairs: int, sequence_length: int, process_count: int | None = None, seed: int = 31) -> None:
        if num_pairs <= 0 or sequence_length <= 0:
            raise ValueError("num_pairs and sequence_length must be positive")
        self.num_pairs = num_pairs
        self.sequence_length = sequence_length
        self.process_count = process_count or min(4, mp.cpu_count())
        self.sequence_pairs = self._generate_pairs(num_pairs, sequence_length, seed)

    @staticmethod
    def _random_sequence(length: int, rng: random.Random) -> str:
        return "".join(rng.choice("ACGT") for _ in range(length))

    def _generate_pairs(self, num_pairs: int, sequence_length: int, seed: int) -> list[tuple[str, str]]:
        rng = random.Random(seed)
        reference = self._random_sequence(sequence_length, rng)
        pairs: list[tuple[str, str]] = []
        for _ in range(num_pairs):
            candidate = self._random_sequence(sequence_length, rng)
            pairs.append((reference, candidate))
        return pairs

    def score_serial(self) -> list[int]:
        return [_score_sequence_pair(pair) for pair in self.sequence_pairs]

    def score_parallel(self) -> list[int]:
        if self.num_pairs < 200:
            raise RuntimeError("workload too small to benefit from multiprocessing")
        chunk_size = max(1, self.num_pairs // (self.process_count * 4))
        with mp.Pool(processes=self.process_count) as pool:
            results = pool.map(_score_sequence_pair, self.sequence_pairs, chunksize=chunk_size)
        return results

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    @staticmethod
    def run() -> None:
        workflow = ParallelSequenceScoringWorkflow(num_pairs=1500, sequence_length=1200, seed=23)

        serial_result, serial_elapsed = workflow.benchmark(workflow.score_serial)
        print(f"serial: elapsed={serial_elapsed:.6f}s, total_score={sum(serial_result)}")

        parallel_result, parallel_elapsed = workflow.benchmark(workflow.score_parallel)
        print(f"parallel ({workflow.process_count} processes): elapsed={parallel_elapsed:.6f}s, total_score={sum(parallel_result)}")

        if serial_result != parallel_result:
            raise RuntimeError("Optimized implementation changed the numerical result.")

        speedup = serial_elapsed / parallel_elapsed if parallel_elapsed > 0 else float("inf")
        print(f"speedup: {speedup:.2f}x")


if __name__ == "__main__":
    ParallelSequenceScoringWorkflow.run()
