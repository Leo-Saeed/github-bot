from __future__ import annotations

from collections import Counter

from .models import AnalysisResult, LogEntry


SEVERITY_WEIGHT = {
    "TRACE": 0,
    "DEBUG": 0,
    "INFO": 0,
    "WARNING": 2,
    "ERROR": 5,
    "CRITICAL": 9,
}


def analyze(entries: list[LogEntry], invalid_lines: int, top: int = 5) -> AnalysisResult:
    """Compute portfolio-friendly metrics from parsed log entries."""

    level_counts = Counter(entry.level for entry in entries)
    message_counts = Counter(normalize_message(entry.message) for entry in entries)
    timestamps = [entry.timestamp for entry in entries if entry.timestamp is not None]
    minute_counts = Counter(
        timestamp.strftime("%Y-%m-%d %H:%M") for timestamp in timestamps
    )

    busiest_minute = minute_counts.most_common(1)[0] if minute_counts else None

    return AnalysisResult(
        total_entries=len(entries),
        invalid_lines=invalid_lines,
        level_counts=dict(sorted(level_counts.items())),
        top_messages=message_counts.most_common(top),
        first_timestamp=min(timestamps) if timestamps else None,
        last_timestamp=max(timestamps) if timestamps else None,
        busiest_minute=busiest_minute,
        health_score=calculate_health_score(entries, invalid_lines),
    )


def normalize_message(message: str) -> str:
    """Reduce noisy IDs and numbers so repeated error patterns are grouped."""

    parts = []
    for token in message.split():
        if any(character.isdigit() for character in token):
            parts.append("<value>")
        else:
            parts.append(token)
    return " ".join(parts)


def calculate_health_score(entries: list[LogEntry], invalid_lines: int) -> int:
    """Return a simple 0-100 score based on severity and parse quality."""

    if not entries and invalid_lines == 0:
        return 100

    total_lines = len(entries) + invalid_lines
    severity_points = sum(SEVERITY_WEIGHT.get(entry.level, 0) for entry in entries)
    parse_penalty = invalid_lines * 3
    max_reasonable_penalty = max(total_lines * 5, 1)
    penalty_ratio = min((severity_points + parse_penalty) / max_reasonable_penalty, 1)

    return round(100 - (penalty_ratio * 100))
