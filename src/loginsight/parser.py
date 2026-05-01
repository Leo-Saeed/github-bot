from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .models import LogEntry


LOG_PATTERN = re.compile(
    r"^\s*(?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>TRACE|DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)\s+"
    r"(?P<message>.+?)\s*$",
    re.IGNORECASE,
)

LEVEL_ALIASES = {
    "WARN": "WARNING",
    "FATAL": "CRITICAL",
}


class LogParseError(Exception):
    """Raised when a log file cannot be loaded."""


def read_log_file(path: Path) -> list[str]:
    """Read a log file and return its lines with clear user-facing errors."""

    if not path.exists():
        raise LogParseError(f"File not found: {path}")
    if not path.is_file():
        raise LogParseError(f"Expected a file, got: {path}")

    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise LogParseError("Log file must be UTF-8 encoded.") from exc
    except OSError as exc:
        raise LogParseError(f"Could not read log file: {exc}") from exc


def parse_lines(lines: Iterable[str]) -> tuple[list[LogEntry], int]:
    """Parse log lines and return valid entries plus the invalid line count."""

    entries: list[LogEntry] = []
    invalid_lines = 0

    for line_number, raw_line in enumerate(lines, start=1):
        match = LOG_PATTERN.match(raw_line)
        if not match:
            invalid_lines += 1
            continue

        timestamp_text = match.group("timestamp").replace("T", " ")
        level = match.group("level").upper()
        level = LEVEL_ALIASES.get(level, level)

        entries.append(
            LogEntry(
                timestamp=datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S"),
                level=level,
                message=match.group("message").strip(),
                source_line=line_number,
                raw=raw_line,
            )
        )

    return entries, invalid_lines
