# 09_Context_Managers

Production resource-management patterns: a nested-transaction SQL
context manager (SAVEPOINT-based), a file-lock-based exclusive
instrument-access manager built on `contextlib.contextmanager`, and
sync/async ephemeral scratch-workspace managers with guaranteed
exception-safe cleanup.

Run: `pytest tests/`
