"""Class-based context manager implementing transaction-like semantics
with commit/rollback and exception-safe cleanup, plus support for
nested (savepoint-style) transactions.
"""
from __future__ import annotations

import sqlite3
from types import TracebackType


class TransactionManager:
    """Wraps a `sqlite3.Connection` so a block either fully commits or
    fully rolls back, including on exceptions. Nested usage creates
    SAVEPOINTs so an inner failure doesn't necessarily abort the outer
    transaction.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._depth = 0
        self._savepoint_name: str | None = None

    def __enter__(self) -> sqlite3.Connection:
        self._depth += 1
        if self._depth == 1:
            self._connection.execute("BEGIN")
        else:
            self._savepoint_name = f"sp_{self._depth}"
            self._connection.execute(f"SAVEPOINT {self._savepoint_name}")
        return self._connection

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        if self._depth > 1:
            if exc_type is None:
                self._connection.execute(f"RELEASE SAVEPOINT {self._savepoint_name}")
            else:
                self._connection.execute(f"ROLLBACK TO SAVEPOINT {self._savepoint_name}")
            self._depth -= 1
            return False

        try:
            if exc_type is None:
                self._connection.commit()
            else:
                self._connection.rollback()
        finally:
            self._depth -= 1
        return False
