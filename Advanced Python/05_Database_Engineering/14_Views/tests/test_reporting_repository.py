from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.repositories.reporting_repository import ReportingRepository


@pytest.mark.asyncio
async def test_get_assay_hit_counts_returns_none_when_missing() -> None:
    session = AsyncMock()
    session.execute.return_value.scalar_one_or_none.return_value = None
    repo = ReportingRepository(session)

    result = await repo.get_assay_hit_counts(999)

    assert result is None


@pytest.mark.asyncio
async def test_refresh_dashboard_view_commits_after_calling_function() -> None:
    session = AsyncMock()
    repo = ReportingRepository(session)

    await repo.refresh_dashboard_view()

    session.execute.assert_awaited_once()
    call_args = session.execute.call_args.args[0]
    assert "refresh_assay_hit_counts" in str(call_args)
    session.commit.assert_awaited_once()
