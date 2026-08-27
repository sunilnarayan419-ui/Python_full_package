from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Protocol

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

DEFAULT_USER_AGENT = "ResearchCatalogBot/1.0 (+https://example.com/bot-info)"
DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_MIN_REQUEST_INTERVAL_SECONDS = 1.0


class ScraperError(Exception):
    """Base error for scraping failures."""


class FetchError(ScraperError):
    """Raised when a page cannot be retrieved."""


class ParseError(ScraperError):
    """Raised when expected content cannot be extracted from HTML."""


@dataclass(frozen=True, slots=True)
class PublicationRecord:
    title: str
    authors: str
    year: str


class HtmlFetcher(Protocol):
    """Abstraction over HTML retrieval so the parser can be tested offline."""

    def fetch(self, url: str) -> str: ...


class HttpHtmlFetcher:
    """Fetches HTML over the network with a configured client and rate limiting.

    Respects a minimum interval between requests and identifies itself with a
    descriptive User-Agent. Callers are responsible for confirming that target
    pages permit automated access before fetching.
    """

    def __init__(
        self,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        user_agent: str = DEFAULT_USER_AGENT,
        min_request_interval: float = DEFAULT_MIN_REQUEST_INTERVAL_SECONDS,
    ) -> None:
        self._client = httpx.Client(timeout=timeout, headers={"User-Agent": user_agent})
        self._min_request_interval = min_request_interval
        self._last_request_time: float | None = None

    def fetch(self, url: str) -> str:
        self._respect_rate_limit()
        try:
            response = self._client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise FetchError(f"Request to {url} returned status {exc.response.status_code}.") from exc
        except httpx.TransportError as exc:
            raise FetchError(f"Network error while fetching {url}.") from exc
        finally:
            self._last_request_time = time.monotonic()
        return response.text

    def _respect_rate_limit(self) -> None:
        if self._last_request_time is None:
            return
        elapsed = time.monotonic() - self._last_request_time
        remaining = self._min_request_interval - elapsed
        if remaining > 0:
            time.sleep(remaining)

    def close(self) -> None:
        self._client.close()


class OfflineHtmlFetcher:
    """Returns fixed HTML content, used for offline demonstration and unit tests."""

    def __init__(self, fixture_by_url: dict[str, str]) -> None:
        self._fixture_by_url = fixture_by_url

    def fetch(self, url: str) -> str:
        html = self._fixture_by_url.get(url)
        if html is None:
            raise FetchError(f"No offline fixture registered for {url}.")
        return html


class PublicationHtmlParser:
    """Extracts structured publication records from catalog HTML.

    Designed to be tested independently of any network fetching.
    """

    def parse(self, html: str) -> list[PublicationRecord]:
        soup = BeautifulSoup(html, "html.parser")
        entries = soup.select(".publication-entry")
        if not entries:
            raise ParseError("No publication entries found in the provided HTML.")

        records: list[PublicationRecord] = []
        for entry in entries:
            title_tag = entry.select_one(".title")
            authors_tag = entry.select_one(".authors")
            year_tag = entry.select_one(".year")
            if title_tag is None or authors_tag is None or year_tag is None:
                logger.warning("Skipping incomplete publication entry.")
                continue
            records.append(
                PublicationRecord(
                    title=title_tag.get_text(strip=True),
                    authors=authors_tag.get_text(strip=True),
                    year=year_tag.get_text(strip=True),
                )
            )
        return records


class PublicationScraperService:
    """Coordinates fetching and parsing to produce structured publication data."""

    def __init__(self, fetcher: HtmlFetcher, parser: PublicationHtmlParser | None = None) -> None:
        self._fetcher = fetcher
        self._parser = parser or PublicationHtmlParser()

    def scrape(self, url: str) -> list[PublicationRecord]:
        html = self._fetcher.fetch(url)
        return self._parser.parse(html)


def _sample_fixture_html() -> str:
    return """
    <html>
      <body>
        <div class="publication-entry">
          <span class="title">Drought Tolerance Mechanisms in Zea mays</span>
          <span class="authors">Chen, L.; Okafor, N.</span>
          <span class="year">2023</span>
        </div>
        <div class="publication-entry">
          <span class="title">Nitrogen Use Efficiency in Glycine max</span>
          <span class="authors">Patel, R.; Novak, S.</span>
          <span class="year">2022</span>
        </div>
      </body>
    </html>
    """


def run() -> list[PublicationRecord]:
    """Runs the scraper against an offline HTML fixture, avoiding live network access."""
    fixture_url = "https://example-research-catalog.test/publications"
    fetcher = OfflineHtmlFetcher({fixture_url: _sample_fixture_html()})
    service = PublicationScraperService(fetcher)

    records = service.scrape(fixture_url)
    for record in records:
        logger.info("Publication: %s (%s, %s)", record.title, record.authors, record.year)

    return records


if __name__ == "__main__":
    run()
