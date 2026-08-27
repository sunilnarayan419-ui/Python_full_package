from __future__ import annotations

import pytest

from reporting import AsyncReportPublisher, build_summary
from reporting.async_reporting import PublishConfig


def test_build_summary_computes_completion_rate() -> None:
    summary = build_summary("TRIAL-001", enrolled_patients=100, completed_patients=80)
    assert summary.completion_rate == 0.8


def test_build_summary_applies_endpoint_transform() -> None:
    summary = build_summary(
        "TRIAL-002",
        enrolled_patients=50,
        completed_patients=50,
        secondary_endpoint_results=[("ORR", 0.4, 0.05)],
        endpoint_transform=lambda e: (e[0], round(e[1] * 100, 1), e[2]),
    )
    assert summary.secondary_endpoints == [("ORR", 40.0, 0.05)]


@pytest.mark.asyncio
async def test_publisher_retries_on_timeout() -> None:
    attempts = 0

    async def flaky_transport(url: str, summary) -> bool:  # noqa: ANN001
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise ConnectionError("simulated failure")
        return True

    publisher = AsyncReportPublisher(
        PublishConfig(endpoint_url="https://trials.example/report", retry_backoff_seconds=0.0),
        transport=flaky_transport,
    )
    summary = build_summary("TRIAL-003", enrolled_patients=10, completed_patients=10)
    assert await publisher.publish(summary) is True
    assert attempts == 2
