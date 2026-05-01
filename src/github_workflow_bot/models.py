from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class FileChange:
    """A normalized file change from git status output."""

    status: str
    path: Path


@dataclass(frozen=True)
class CommitSuggestion:
    """A suggested commit message with a short explanation."""

    message: str
    reason: str


@dataclass
class SkeletonResult:
    """Tracks files created and skipped during project generation."""

    root: Path
    created: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)

    @property
    def created_count(self) -> int:
        return len(self.created)

    @property
    def skipped_count(self) -> int:
        return len(self.skipped)
