from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from resources import InstrumentLock, TransactionManager, scratch_workspace
from resources.instrument_lock import InstrumentBusyError


@pytest.fixture()
def connection() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE samples (id TEXT PRIMARY KEY)")
    conn.commit()
    return conn


def test_transaction_commits_on_success(connection: sqlite3.Connection) -> None:
    with TransactionManager(connection) as conn:
        conn.execute("INSERT INTO samples VALUES ('S1')")
    rows = connection.execute("SELECT id FROM samples").fetchall()
    assert rows == [("S1",)]


def test_transaction_rolls_back_on_exception(connection: sqlite3.Connection) -> None:
    with pytest.raises(ValueError):
        with TransactionManager(connection) as conn:
            conn.execute("INSERT INTO samples VALUES ('S2')")
            raise ValueError("simulated failure")
    rows = connection.execute("SELECT id FROM samples").fetchall()
    assert rows == []


def test_nested_savepoint_rolls_back_independently(connection: sqlite3.Connection) -> None:
    tx = TransactionManager(connection)
    with tx as conn:
        conn.execute("INSERT INTO samples VALUES ('OUTER')")
        try:
            with tx as inner_conn:
                inner_conn.execute("INSERT INTO samples VALUES ('INNER')")
                raise RuntimeError("inner failure")
        except RuntimeError:
            pass
    rows = {row[0] for row in connection.execute("SELECT id FROM samples")}
    assert rows == {"OUTER"}


def test_scratch_workspace_cleans_up_even_on_error() -> None:
    captured_path: Path | None = None
    with pytest.raises(RuntimeError):
        with scratch_workspace() as workspace:
            captured_path = workspace
            (workspace / "intermediate.dat").write_bytes(b"data")
            raise RuntimeError("pipeline stage failed")
    assert captured_path is not None
    assert not captured_path.exists()


def test_instrument_lock_prevents_concurrent_acquisition(tmp_path: Path) -> None:
    lock = InstrumentLock(tmp_path, "sequencer-1", timeout_seconds=0.2)
    with lock.acquire():
        second_lock = InstrumentLock(tmp_path, "sequencer-1", timeout_seconds=0.2)
        with pytest.raises(InstrumentBusyError):
            with second_lock.acquire():
                pass


@pytest.mark.asyncio
async def test_async_scratch_workspace_cleans_up() -> None:
    from resources import async_scratch_workspace

    captured_path: Path | None = None
    async with async_scratch_workspace() as workspace:
        captured_path = workspace
        assert workspace.exists()
    assert captured_path is not None
    assert not captured_path.exists()
