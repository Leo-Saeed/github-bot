from __future__ import annotations

from pathlib import Path

from .models import AnalysisResult


def format_console_report(result: AnalysisResult) -> str:
    """Create a readable text report for terminal output."""

    lines = [
        "Log Insight Report",
        "==================",
        f"Health score: {result.health_score}/100",
        f"Total parsed entries: {result.total_entries}",
        f"Invalid lines skipped: {result.invalid_lines}",
        "",
        "Levels:",
    ]

    if result.level_counts:
        lines.extend(
            f"- {level}: {count}" for level, count in result.level_counts.items()
        )
    else:
        lines.append("- No valid log levels found")

    lines.extend(["", "Time range:", f"- First: {format_timestamp(result.first_timestamp)}"])
    lines.append(f"- Last: {format_timestamp(result.last_timestamp)}")
    lines.append(
        f"- Busiest minute: {format_busiest_minute(result.busiest_minute)}"
    )

    lines.extend(["", "Top repeated messages:"])
    if result.top_messages:
        lines.extend(f"- {message} ({count})" for message, count in result.top_messages)
    else:
        lines.append("- No messages found")

    return "\n".join(lines)


def format_markdown_report(result: AnalysisResult) -> str:
    """Create a Markdown report that can be saved as a portfolio artifact."""

    level_rows = "\n".join(
        f"| {level} | {count} |" for level, count in result.level_counts.items()
    )
    message_rows = "\n".join(
        f"| {message} | {count} |" for message, count in result.top_messages
    )

    return "\n".join(
        [
            "# Log Insight Report",
            "",
            f"**Health score:** {result.health_score}/100",
            "",
            "## Summary",
            "",
            f"- Total parsed entries: {result.total_entries}",
            f"- Invalid lines skipped: {result.invalid_lines}",
            f"- First timestamp: {format_timestamp(result.first_timestamp)}",
            f"- Last timestamp: {format_timestamp(result.last_timestamp)}",
            f"- Busiest minute: {format_busiest_minute(result.busiest_minute)}",
            "",
            "## Levels",
            "",
            "| Level | Count |",
            "| --- | ---: |",
            level_rows or "| None | 0 |",
            "",
            "## Top Repeated Messages",
            "",
            "| Message Pattern | Count |",
            "| --- | ---: |",
            message_rows or "| None | 0 |",
            "",
        ]
    )


def write_report(path: Path, content: str) -> None:
    """Write a report to disk, creating parent folders when needed."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def format_timestamp(value) -> str:
    if value is None:
        return "N/A"
    return value.strftime("%Y-%m-%d %H:%M:%S")


def format_busiest_minute(value: tuple[str, int] | None) -> str:
    if value is None:
        return "N/A"
    minute, count = value
    return f"{minute} ({count} entries)"
