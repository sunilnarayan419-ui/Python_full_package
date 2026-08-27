"""Async report publishing with nested awaits and complex configuration,
formatted deterministically by Black.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable

from .summary import ClinicalTrialSummary


@dataclass(slots=True)
class PublishConfig:
    endpoint_url: str
    timeout_seconds: float = 30.0
    max_retries: int = 3
    retry_backoff_seconds: float = 2.0


class AsyncReportPublisher:
    def __init__(
        self,
        config: PublishConfig,
        transport: Callable[[str, ClinicalTrialSummary], Awaitable[bool]],
    ) -> None:
        self._config = config
        self._transport = transport

    async def publish(self, summary: ClinicalTrialSummary) -> bool:
        last_error: Exception | None = None
        for attempt in range(1, self._config.max_retries + 1):
            try:
                return await asyncio.wait_for(
                    self._transport(self._config.endpoint_url, summary),
                    timeout=self._config.timeout_seconds,
                )
            except (asyncio.TimeoutError, ConnectionError) as exc:
                last_error = exc
                if attempt < self._config.max_retries:
                    await asyncio.sleep(self._config.retry_backoff_seconds * attempt)
        assert last_error is not None
        raise last_error
