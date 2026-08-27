from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reporting_views import AssayHitCountView


class ReportingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_assay_hit_counts(self, assay_id: int) -> AssayHitCountView | None:
        stmt = select(AssayHitCountView).where(AssayHitCountView.assay_id == assay_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def refresh_dashboard_view(self) -> None:
        """Invokes the scheduled refresh function rather than issuing REFRESH directly,
        so retry/alerting logic lives in one place (the SQL function)."""
        await self._session.execute(text("SELECT refresh_assay_hit_counts()"))
        await self._session.commit()
