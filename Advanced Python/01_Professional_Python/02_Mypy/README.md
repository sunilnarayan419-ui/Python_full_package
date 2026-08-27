# 02_Mypy

Strictly typed variant-calling repository designed to pass `mypy --strict`
(see `mypy.ini`). Demonstrates Protocol-based repository abstraction,
`@overload`, `Optional` narrowing, and a deliberately isolated boundary
for an untyped third-party dependency (`third_party.py`) so `Any` never
leaks into the rest of the codebase.

Run: `mypy --config-file mypy.ini src` and `pytest tests/`
