# 15_Profiling

Before/after profiling story built on sequence-alignment edit
distance: an exponential naive implementation vs. an O(m*n)-time,
O(min(m,n))-memory iterative version. `profiler_utils.py` wraps
`cProfile`/`pstats` for call-graph profiling, `timeit`-style
microbenchmarking via `time.perf_counter`, and `tracemalloc`-based peak
memory measurement with top-allocation-site reporting.

Run: `pytest tests/`
