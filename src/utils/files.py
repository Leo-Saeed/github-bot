from __future__ import annotations

from pathlib import Path


def write_text_file(path: Path, content: str, overwrite: bool = False) -> bool:
    """Write a UTF-8 file and return True when the file was created or updated."""

    if path.exists() and not overwrite:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def sanitize_package_name(name: str) -> str:
    """Convert a project name into a safe Python package name."""

    cleaned = "".join(character if character.isalnum() else "_" for character in name)
    cleaned = "_".join(part for part in cleaned.lower().split("_") if part)

    if not cleaned:
        return "app"
    if cleaned[0].isdigit():
        return f"app_{cleaned}"
    return cleaned
