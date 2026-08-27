from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import DBAPIError

from app.services.inventory_transfer_service import (
    DEADLOCK_DETECTED_SQLSTATE,
    InsufficientInventoryError,
    InventoryTransferService,
)


def _dbapi_error(sqlstate: str) -> DBAPIError:
    orig = SimpleNamespace(sqlstate=sqlstate)
    return DBAPIError("stmt", {}, orig)


@pytest.mark.asyncio
async def test_transfer_raises_when_source_has_insufficient_volume() -> None:
    session = AsyncMock()
    session.scalar.return_value = 10
    service = InventoryTransferService(session)

    with pytest.raises(InsufficientInventoryError):
        await service._transfer_once(source_sample_id=1, target_sample_id=2, volume_ul=50)


@pytest.mark.asyncio
async def test_transfer_with_retry_retries_on_deadlock_then_succeeds() -> None:
    service = InventoryTransferService(AsyncMock())
    call_count = {"n": 0}

    async def flaky_transfer(**kwargs):
        call_count["n"] += 1
        if call_count["n"] < 2:
            raise _dbapi_error(DEADLOCK_DETECTED_SQLSTATE)
        return None

    service._transfer_once = flaky_transfer  # type: ignore[method-assign]
    service._session.rollback = AsyncMock()

    await service.transfer_with_retry(
        source_sample_id=1, target_sample_id=2, volume_ul=10, max_attempts=3
    )

    assert call_count["n"] == 2
    assert service._session.rollback.await_count == 1


@pytest.mark.asyncio
async def test_transfer_with_retry_gives_up_after_max_attempts() -> None:
    service = InventoryTransferService(AsyncMock())
    service._session.rollback = AsyncMock()

    async def always_deadlocks(**kwargs):
        raise _dbapi_error(DEADLOCK_DETECTED_SQLSTATE)

    service._transfer_once = always_deadlocks  # type: ignore[method-assign]

    with pytest.raises(DBAPIError):
        await service.transfer_with_retry(
            source_sample_id=1, target_sample_id=2, volume_ul=10, max_attempts=3
        )
    assert service._session.rollback.await_count == 3


@pytest.mark.asyncio
async def test_transfer_with_retry_does_not_retry_non_retryable_errors() -> None:
    service = InventoryTransferService(AsyncMock())
    service._session.rollback = AsyncMock()

    async def non_retryable(**kwargs):
        raise _dbapi_error("23505")  # unique_violation, not retryable

    service._transfer_once = non_retryable  # type: ignore[method-assign]

    with pytest.raises(DBAPIError):
        await service.transfer_with_retry(
            source_sample_id=1, target_sample_id=2, volume_ul=10, max_attempts=5
        )
    assert service._session.rollback.await_count == 1
