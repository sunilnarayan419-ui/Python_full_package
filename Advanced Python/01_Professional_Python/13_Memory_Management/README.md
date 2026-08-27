# 13_Memory_Management

Memory-conscious data structures for large-scale genomics workloads:
`__slots__`-based `GenomicInterval` (no per-instance `__dict__`
overhead at multi-million-object scale), a chromosome-bucketed
`IntervalStore` with lazy, early-terminating overlap queries, and an
LRU `ReadAlignmentCache` combining bounded strong-reference caching
with a `WeakValueDictionary` so evicted entries don't keep large
source alignment objects alive.

Run: `pytest tests/`
