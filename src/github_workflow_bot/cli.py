from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.console import print_list, print_section

from . import __version__
from .commit_suggester import suggest_commit_messages
from .git_commands import build_git_command_plan
from .git_status import GitError
from .menu import run_menu
from .skeleton import generate_project_skeleton


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="github-workflow-bot",
        description="Automate simple project setup and GitHub workflow helpers.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser(
        "init-project",
        help="Generate a clean Python project skeleton.",
    )
    init_parser.add_argument("name", help="Name of the project folder to create.")
    init_parser.add_argument(
        "--destination",
        type=Path,
        default=Path("."),
        help="Folder where the project should be created. Default: current folder.",
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files when they already exist.",
    )

    suggest_parser = subparsers.add_parser(
        "suggest-commit",
        help="Suggest commit messages from git status.",
    )
    suggest_parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Path to the git repository. Default: current folder.",
    )

    commands_parser = subparsers.add_parser(
        "git-commands",
        help="Show git commands for publishing a project.",
    )
    commands_parser.add_argument(
        "--message",
        default="feat: add initial project",
        help="Commit message to use in the generated commands.",
    )
    commands_parser.add_argument(
        "--remote-url",
        default="https://github.com/<username>/<repository>.git",
        help="GitHub remote URL.",
    )
    commands_parser.add_argument(
        "--branch",
        default="main",
        help="Branch to push. Default: main.",
    )

    subparsers.add_parser("menu", help="Open the interactive CLI menu.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Application entry point."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None or args.command == "menu":
        return run_menu()

    if args.command == "init-project":
        result = generate_project_skeleton(
            project_name=args.name,
            destination=args.destination,
            overwrite=args.force,
        )
        print_section("Project Skeleton")
        print(f"Root: {result.root}")
        print(f"Created files: {result.created_count}")
        print(f"Skipped files: {result.skipped_count}")
        return 0

    if args.command == "suggest-commit":
        try:
            suggestions = suggest_commit_messages(args.path)
        except GitError as exc:
            print(f"Error: {exc}")
            return 1

        print_section("Suggested Commit Messages")
        print_list(
            [f'{item.message} - {item.reason}' for item in suggestions],
            "No suggestions available.",
        )
        return 0

    if args.command == "git-commands":
        commands = build_git_command_plan(
            commit_message=args.message,
            branch=args.branch,
            remote_url=args.remote_url,
        )
        print_section("Git Commands")
        for command in commands:
            print(command)
        return 0

    parser.error("Unknown command.")
    return 2
