from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .analyzer import analyze
from .parser import LogParseError, parse_lines, read_log_file
from .reporter import format_console_report, format_markdown_report, write_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log-insight",
        description="Analyze application logs and generate a clean health report.",
    )
    parser.add_argument("log_file", type=Path, help="Path to a UTF-8 log file.")
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of repeated message patterns to show. Default: 5.",
    )
    parser.add_argument(
        "--export",
        type=Path,
        help="Optional path for a Markdown report, for example reports/summary.md.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.top < 1:
        parser.error("--top must be greater than 0")

    try:
        lines = read_log_file(args.log_file)
        entries, invalid_lines = parse_lines(lines)
        result = analyze(entries, invalid_lines, top=args.top)

        print(format_console_report(result))

        if args.export:
            write_report(args.export, format_markdown_report(result))
            print(f"\nMarkdown report written to: {args.export}")

        return 0
    except LogParseError as exc:
        print(f"Error: {exc}")
        return 1
    except OSError as exc:
        print(f"Error: could not write report: {exc}")
        return 1
