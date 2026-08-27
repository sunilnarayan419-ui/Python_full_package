"""Two implementations of sequence edit distance (a core primitive in
read alignment / variant normalization): a naive recursive version
used to demonstrate a real bottleneck, and an optimized dynamic-
programming version with O(min(m, n)) memory, used to demonstrate a
concrete before/after profiling story.
"""
from __future__ import annotations

from functools import lru_cache


def naive_edit_distance(a: str, b: str) -> int:
    """Exponential-time recursive edit distance. Intentionally left
    unoptimized as the 'before' profiling target — do not use on
    real sequences beyond toy lengths.
    """

    @lru_cache(maxsize=None)
    def recurse(i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        if a[i - 1] == b[j - 1]:
            return recurse(i - 1, j - 1)
        return 1 + min(recurse(i - 1, j), recurse(i, j - 1), recurse(i - 1, j - 1))

    result = recurse(len(a), len(b))
    recurse.cache_clear()
    return result


def optimized_edit_distance(a: str, b: str) -> int:
    """Iterative DP with a rolling two-row buffer: O(len(a) * len(b))
    time, O(min(len(a), len(b))) memory — the 'after' profiling target.
    """
    if len(a) < len(b):
        a, b = b, a
    previous_row = list(range(len(b) + 1))
    for i, char_a in enumerate(a, start=1):
        current_row = [i] + [0] * len(b)
        for j, char_b in enumerate(b, start=1):
            cost = 0 if char_a == char_b else 1
            current_row[j] = min(
                previous_row[j] + 1,
                current_row[j - 1] + 1,
                previous_row[j - 1] + cost,
            )
        previous_row = current_row
    return previous_row[-1]
