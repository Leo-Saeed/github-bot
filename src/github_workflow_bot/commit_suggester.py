from __future__ import annotations

from pathlib import Path

from .git_status import GitError, get_status_changes
from .models import CommitSuggestion, FileChange


DOC_EXTENSIONS = {".md", ".rst", ".txt"}
TEST_MARKERS = {"test", "tests"}
CONFIG_FILES = {
    ".gitignore",
    "requirements.txt",
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
}


def suggest_commit_messages(repo_path: Path) -> list[CommitSuggestion]:
    """Suggest practical Conventional Commit messages from current git changes."""

    changes = get_status_changes(repo_path)
    if not changes:
        return [
            CommitSuggestion(
                message="chore: no pending changes",
                reason="Git status is clean.",
            )
        ]

    primary_type = detect_commit_type(changes)
    summary = summarize_changes(changes)

    suggestions = [
        CommitSuggestion(
            message=f"{primary_type}: {summary}",
            reason="Best fit based on changed file types and git statuses.",
        ),
        CommitSuggestion(
            message=f"chore: update project workflow files",
            reason="Good general-purpose option for setup or maintenance changes.",
        ),
    ]

    if has_new_project_shape(changes):
        suggestions.insert(
            0,
            CommitSuggestion(
                message="feat: add GitHub workflow helper bot",
                reason="Detected a new app-style structure with source and README files.",
            ),
        )

    return dedupe_suggestions(suggestions)


def detect_commit_type(changes: list[FileChange]) -> str:
    paths = [change.path for change in changes]

    if has_new_project_shape(changes):
        return "feat"
    if all(path.suffix.lower() in DOC_EXTENSIONS for path in paths):
        return "docs"
    if any(part.lower() in TEST_MARKERS for path in paths for part in path.parts):
        return "test"
    if all(path.name in CONFIG_FILES for path in paths):
        return "chore"
    if any(change.status.startswith("D") for change in changes):
        return "refactor"
    if any(change.status.startswith("?") or "A" in change.status for change in changes):
        return "feat"

    return "fix"


def summarize_changes(changes: list[FileChange]) -> str:
    paths = [change.path.as_posix() for change in changes]

    if len(changes) >= 5:
        return "update project structure"
    if any(path.startswith("src/") for path in paths):
        return "update application code"
    if any(path.lower().endswith("readme.md") for path in paths):
        return "update documentation"
    if any(Path(path).name in CONFIG_FILES for path in paths):
        return "update project configuration"

    return "update project files"


def has_new_project_shape(changes: list[FileChange]) -> bool:
    paths = {change.path.as_posix().lower() for change in changes}
    return "readme.md" in paths and "main.py" in paths and any(
        path == "src" or path.startswith("src/") for path in paths
    )


def dedupe_suggestions(
    suggestions: list[CommitSuggestion],
) -> list[CommitSuggestion]:
    unique: list[CommitSuggestion] = []
    seen: set[str] = set()

    for suggestion in suggestions:
        if suggestion.message in seen:
            continue
        seen.add(suggestion.message)
        unique.append(suggestion)

    return unique
