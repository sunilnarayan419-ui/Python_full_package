from __future__ import annotations

import asyncio
import logging

from app.database.connection import close_pool, init_pool
from app.repositories.screening_repository import ScreeningRepository

logger = logging.getLogger("drug_discovery.sql")
logging.basicConfig(level=logging.INFO)


async def run_reporting_snapshot() -> None:
    await init_pool()
    try:
        repo = ScreeningRepository()
        top_hits = await repo.top_potency_by_target(limit=50)
        logger.info("top_potency_rows=%d", len(top_hits))

        hit_rates = await repo.hit_rate_by_assay(min_results=10)
        for assay in hit_rates:
            logger.info(
                "assay_id=%s name=%s hit_rate_pct=%s",
                assay.assay_id,
                assay.assay_name,
                assay.hit_rate_pct,
            )
    finally:
        await close_pool()


if __name__ == "__main__":
    asyncio.run(run_reporting_snapshot())
