from __future__ import annotations

import importlib
import importlib.util
import os
import random
import subprocess
import sys
import tempfile
import time
from typing import Callable, TypeVar

T = TypeVar("T")

_PYX_SOURCE = """
# cython: language_level=3
# cython: boundscheck=False, wraparound=False

cpdef dict count_kmers_cython(str sequence, int k):
    cdef int n = len(sequence)
    cdef int i
    cdef str kmer
    cdef dict counts = {}
    if k <= 0 or k > n:
        raise ValueError("k must be positive and <= sequence length")
    for i in range(n - k + 1):
        kmer = sequence[i:i + k]
        if kmer in counts:
            counts[kmer] += 1
        else:
            counts[kmer] = 1
    return counts
"""

_SETUP_SOURCE = """
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("kmer_cython.pyx", language_level=3),
    zip_safe=False,
)
"""


def _count_kmers_python(sequence: str, k: int) -> dict[str, int]:
    """Pure-Python baseline k-mer counter, functionally equivalent to the Cython version."""
    if k <= 0 or k > len(sequence):
        raise ValueError("k must be positive and <= sequence length")
    counts: dict[str, int] = {}
    for index in range(len(sequence) - k + 1):
        kmer = sequence[index:index + k]
        counts[kmer] = counts.get(kmer, 0) + 1
    return counts


class CythonKmerBuildAndBenchmark:
    """Builds a Cython extension for k-mer counting and benchmarks it against Python.

    The Cython source (.pyx) and setup script are written to a temporary
    build directory and compiled with 'python setup.py build_ext --inplace'.
    This mirrors a realistic engineering workflow: Cython code must be
    compiled into a native extension before it can be imported and used.
    """

    def __init__(self, sequence_length: int, kmer_size: int, seed: int = 21) -> None:
        if sequence_length <= 0:
            raise ValueError("sequence_length must be positive")
        if kmer_size <= 0 or kmer_size > sequence_length:
            raise ValueError("kmer_size must be positive and <= sequence_length")
        self.kmer_size = kmer_size
        rng = random.Random(seed)
        self.sequence = "".join(rng.choice("ACGT") for _ in range(sequence_length))
        self.build_dir = tempfile.mkdtemp(prefix="cython_kmer_build_")

    def _cython_available(self) -> bool:
        return importlib.util.find_spec("Cython") is not None

    def build_extension(self) -> Callable[[str, int], dict[str, int]]:
        if not self._cython_available():
            raise RuntimeError(
                "Cython is not installed. Install it with 'pip install Cython' and ensure "
                "a C compiler is available to build the k-mer counting extension."
            )

        pyx_path = os.path.join(self.build_dir, "kmer_cython.pyx")
        setup_path = os.path.join(self.build_dir, "setup.py")
        with open(pyx_path, "w", encoding="utf-8") as pyx_file:
            pyx_file.write(_PYX_SOURCE)
        with open(setup_path, "w", encoding="utf-8") as setup_file:
            setup_file.write(_SETUP_SOURCE)

        build_command = [sys.executable, "setup.py", "build_ext", "--inplace"]
        process = subprocess.run(
            build_command,
            cwd=self.build_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if process.returncode != 0:
            raise RuntimeError(
                "Cython extension build failed. A C compiler toolchain is required. "
                f"stdout={process.stdout}\nstderr={process.stderr}"
            )

        sys.path.insert(0, self.build_dir)
        module = importlib.import_module("kmer_cython")
        return module.count_kmers_cython  # type: ignore[no-any-return]

    def baseline_python(self) -> dict[str, int]:
        return _count_kmers_python(self.sequence, self.kmer_size)

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    @staticmethod
    def run() -> None:
        workflow = CythonKmerBuildAndBenchmark(sequence_length=120_000, kmer_size=8, seed=17)

        baseline_result, baseline_elapsed = workflow.benchmark(workflow.baseline_python)
        print(f"python baseline: {baseline_elapsed:.6f}s, unique_kmers={len(baseline_result)}")

        try:
            count_kmers_cython = workflow.build_extension()
        except RuntimeError as build_error:
            print(f"Cython benchmark skipped: {build_error}")
            return

        cython_result, cython_elapsed = workflow.benchmark(
            count_kmers_cython, workflow.sequence, workflow.kmer_size
        )
        print(f"cython optimized: {cython_elapsed:.6f}s, unique_kmers={len(cython_result)}")

        if baseline_result != cython_result:
            raise RuntimeError("Optimized implementation changed the numerical result.")

        speedup = baseline_elapsed / cython_elapsed if cython_elapsed > 0 else float("inf")
        print(f"speedup: {speedup:.2f}x")


if __name__ == "__main__":
    CythonKmerBuildAndBenchmark.run()
