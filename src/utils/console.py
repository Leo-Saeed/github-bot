from __future__ import annotations


def print_section(title: str) -> None:
    """Print a consistent section header for CLI output."""

    print(f"\n{title}")
    print("-" * len(title))


def print_list(items: list[str], empty_message: str) -> None:
    """Print a simple list with a fallback message."""

    if not items:
        print(empty_message)
        return

    for item in items:
        print(f"- {item}")
