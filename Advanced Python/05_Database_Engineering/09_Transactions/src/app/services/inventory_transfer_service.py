from __future__ import annotations

import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("transactions.inventory_transfer")

SERIALIZATION_FAILURE_SQLSTATE = "40001"
DEADLOCK_DETECTED_SQLSTATE = "40P01"
RETRYABLE_SQLSTATES = {SERIALIZATION_FAILURE_SQLSTATE, DEADLOCK_DETECTED_SQLSTATE}


class InsufficientInventoryError(Exception):
    pass


class InventoryTransferService:
    """Moves compound sample volume between two lab freezers atomically.

    Demonstrates: explicit transaction boundary, SERIALIZABLE isolation for a
    correctness-critical transfer, a SAVEPOINT for a non-fatal sub-step, and a
    bounded retry loop for serialization failures / deadlocks. Errors are never
    swallowed -- after the retry budget is exhausted, the original exception propagates.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def transfer_with_retry(
        self,
        *,
        source_sample_id: int,
        target_sample_id: int,
        volume_ul: int,
        max_attempts: int = 3,
    ) -> None:
        attempt = 0
        while True:
            attempt += 1
            try:
                await self._transfer_once(
                    source_sample_id=source_sample_id,
                    target_sample_id=target_sample_id,
                    volume_ul=volume_ul,
                )
                return
            except DBAPIError as exc:
                sqlstate = getattr(getattr(exc, "orig", None), "sqlstate", None)
                await self._session.rollback()
                if sqlstate not in RETRYABLE_SQLSTATES or attempt >= max_attempts:
                    logger.error(
                        "transfer failed permanently after %d attempts: %s", attempt, exc
                    )
                    raise
                backoff_seconds = 0.05 * (2 ** (attempt - 1))
                logger.warning(
                    "retryable transaction failure (sqlstate=%s), attempt=%d, backing off %.2fs",
                    sqlstate,
                    attempt,
                    backoff_seconds,
                )
                await asyncio.sleep(backoff_seconds)

    async def _transfer_once(
        self, *, source_sample_id: int, target_sample_id: int, volume_ul: int
    ) -> None:
        await self._session.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))

        source_volume = await self._session.scalar(
            text("SELECT volume_ul FROM sample_aliquots WHERE sample_id = :sid FOR UPDATE"),
            {"sid": source_sample_id},
        )
        if source_volume is None or source_volume < volume_ul:
            raise InsufficientInventoryError(
                f"sample {source_sample_id} has insufficient volume for transfer"
            )

        await self._session.execute(
            text(
                "UPDATE sample_aliquots SET volume_ul = volume_ul - :vol WHERE sample_id = :sid"
            ),
            {"vol": volume_ul, "sid": source_sample_id},
        )

        # Savepoint around the target-side update: if the target row is somehow locked
        # in a conflicting way we want to attempt a fallback insert without aborting
        # the whole outer transaction.
        async with self._session.begin_nested():
            result = await self._session.execute(
                text(
                    "UPDATE sample_aliquots SET volume_ul = volume_ul + :vol WHERE sample_id = :sid"
                ),
                {"vol": volume_ul, "sid": target_sample_id},
            )
            if result.rowcount == 0:
                await self._session.execute(
                    text(
                        "INSERT INTO sample_aliquots (sample_id, volume_ul) VALUES (:sid, :vol)"
                    ),
                    {"sid": target_sample_id, "vol": volume_ul},
                )

        await self._session.commit()
        logger.info(
            "transferred %d uL from sample %s to sample %s",
            volume_ul,
            source_sample_id,
            target_sample_id,
        )
