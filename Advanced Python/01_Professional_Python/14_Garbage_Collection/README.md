# 14_Garbage_Collection

Demonstrates a realistic reference-cycle hazard in an observer-pattern
pipeline (`observer_graph.py`) resolved with `weakref` rather than
relying on the cyclic collector, plus a `weakref.finalize`-based
resource-leak detector (`resource_tracker.py`) with a narrowly scoped,
justified use of explicit `gc.collect()` for diagnostics — not routine
production cleanup.

Run: `pytest tests/`
