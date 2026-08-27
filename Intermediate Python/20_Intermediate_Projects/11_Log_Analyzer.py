from __future__ import annotations

import logging
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

LOG_LINE_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"\| (?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) "
    r"\| (?P<source>[\w.\-]+) "
    r"\| (?P<message>.*)$"
)

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass(frozen=True, slots=True)
class LogEntry:
    timestamp: datetime
    level: str
    source: str
    message: str


@dataclass(frozen=True, slots=True)
class LogAnalysisReport:
    total_entries: int
    malformed_line_count: int
    error_count: int
    warning_count: int
    unique_sources: int
    level_counts: dict[str, int]
    top_errors: tuple[tuple[str, int], ...]
    entries_per_source: dict[str, int]


class LogParser:
    """Parses structured log lines, tolerating malformed entries."""

    def __init__(self, pattern: re.Pattern[str] = LOG_LINE_PATTERN) -> None:
        self._pattern = pattern

    def parse_lines(self, lines: list[str]) -> tuple[list[LogEntry], int]:
        entries: list[LogEntry] = []
        malformed_count = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            entry = self._parse_line(stripped)
            if entry is None:
                malformed_count += 1
                continue
            entries.append(entry)

        return entries, malformed_count

    def _parse_line(self, line: str) -> LogEntry | None:
        match = self._pattern.match(line)
        if match is None:
            return None
        try:
            timestamp = datetime.strptime(match.group("timestamp"), TIMESTAMP_FORMAT)
        except ValueError:
            return None
        return LogEntry(
            timestamp=timestamp,
            level=match.group("level"),
            source=match.group("source"),
            message=match.group("message"),
        )


class LogAnalyzer:
    """Computes frequency and classification statistics over parsed log entries."""

    def analyze(self, entries: list[LogEntry], malformed_count: int, top_n: int = 5) -> LogAnalysisReport:
        level_counter = Counter(entry.level for entry in entries)
        source_counter = Counter(entry.source for entry in entries)
        error_messages = Counter(
            entry.message for entry in entries if entry.level in ("ERROR", "CRITICAL")
        )

        return LogAnalysisReport(
            total_entries=len(entries),
            malformed_line_count=malformed_count,
            error_count=level_counter.get("ERROR", 0) + level_counter.get("CRITICAL", 0),
            warning_count=level_counter.get("WARNING", 0),
            unique_sources=len(source_counter),
            level_counts=dict(level_counter),
            top_errors=tuple(error_messages.most_common(top_n)),
            entries_per_source=dict(source_counter),
        )


class LogAnalyzerService:
    """Coordinates parsing and analysis of raw log content."""

    def __init__(self, parser: LogParser | None = None, analyzer: LogAnalyzer | None = None) -> None:
        self._parser = parser or LogParser()
        self._analyzer = analyzer or LogAnalyzer()

    def analyze_text(self, log_text: str) -> LogAnalysisReport:
        lines = log_text.splitlines()
        entries, malformed_count = self._parser.parse_lines(lines)
        if malformed_count:
            logger.warning("Skipped %d malformed log lines.", malformed_count)
        return self._analyzer.analyze(entries, malformed_count)


def _build_sample_log() -> str:
    return "\n".join(
        [
            "2024-06-01 08:12:03 | INFO | data_pipeline.ingest | Ingested 500 records.",
            "2024-06-01 08:12:05 | WARNING | data_pipeline.validate | 3 records missing soil_ph.",
            "2024-06-01 08:12:07 | ERROR | data_pipeline.clean | Failed to parse biomass_g for row 42.",
            "2024-06-01 08:12:09 | INFO | api.server | Request received for /experiments/EXP-001",
            "this line is not a valid log entry",
            "2024-06-01 08:13:00 | ERROR | data_pipeline.clean | Failed to parse biomass_g for row 87.",
            "2024-06-01 08:13:05 | CRITICAL | db.connection | Lost connection to database.",
            "2024-06-01 08:13:10 | INFO | api.server | Request received for /experiments/EXP-002",
            "2024-06-01 08:13:12 | DEBUG | api.server | Cache hit for /experiments/EXP-002",
        ]
    )


def run() -> LogAnalysisReport:
    """Runs the log analyzer against a controlled sample log."""
    service = LogAnalyzerService()
    report = service.analyze_text(_build_sample_log())

    logger.info("Total entries: %d (malformed: %d)", report.total_entries, report.malformed_line_count)
    logger.info("Errors: %d, Warnings: %d", report.error_count, report.warning_count)
    logger.info("Unique sources: %d", report.unique_sources)
    logger.info("Level counts: %s", report.level_counts)
    logger.info("Top errors: %s", report.top_errors)

    return report


if __name__ == "__main__":
    run()
