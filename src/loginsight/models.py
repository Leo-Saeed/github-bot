from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LogEntry:
    """A normalized log line parsed from a plain text application log."""

    timestamp: datetime | None
    level: str
    message: str
    source_line: int
    raw: str


@dataclass(frozen=True)
class AnalysisResult:
    """Aggregated metrics produced from parsed log entries."""

    total_entries: int
    invalid_lines: int
    level_counts: dict[str, int]
    top_messages: list[tuple[str, int]]
    first_timestamp: datetime | None
    last_timestamp: datetime | None
    busiest_minute: tuple[str, int] | None
    health_score: int
