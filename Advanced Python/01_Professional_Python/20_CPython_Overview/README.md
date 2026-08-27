# 20_CPython_Overview

Practical CPython-level engineering: `dis`-based bytecode inspection
used to justify a set-vs-list membership optimization
(`bytecode_inspection.py`), reference-counting verified via
`sys.getrefcount` to confirm closures share one underlying lookup
table rather than copying it (`refcounting.py`), and string interning
applied to build memory-cheap batch keys — always paired with
equality-based (not identity-based) grouping logic for correctness
(`interning.py`).

Run: `pytest tests/`
