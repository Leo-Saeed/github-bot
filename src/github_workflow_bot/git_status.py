from __future__ import annotations

import subprocess
from pathlib import Path

from .models import FileChange


class GitError(Exception):
    """Raised when git commands cannot be executed successfully."""


def get_status_changes(repo_path: Path) -> list[FileChange]:
    """Return changed files from `git status --short`."""

    completed = run_git(["status", "--short"], repo_path)
    changes: list[FileChange] = []

    for line in completed.stdout.splitlines():
        if not line.strip():
            continue

        status = line[:2].strip() or "?"
        path_text = line[3:].strip()

        # Rename output looks like: old/path -> new/path. The new path is what matters.
        if " -> " in path_text:
            path_text = path_text.split(" -> ", maxsplit=1)[1]

        changes.append(FileChange(status=status, path=Path(path_text)))

    return changes


def run_git(args: list[str], repo_path: Path) -> subprocess.CompletedProcess[str]:
    """Run git safely and raise a friendly exception on failure."""

    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise GitError("Git is not installed or is not available on PATH.") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or "Unknown git error."
        raise GitError(message) from exc

    return completed
