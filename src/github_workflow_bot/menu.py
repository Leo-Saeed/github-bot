from __future__ import annotations

from pathlib import Path

from src.utils.console import print_list, print_section

from .commit_suggester import suggest_commit_messages
from .git_commands import build_git_command_plan
from .git_status import GitError
from .skeleton import generate_project_skeleton


def run_menu() -> int:
    """Run a small interactive CLI menu for common developer tasks."""

    while True:
        print_section("GitHub Workflow Bot")
        print("1. Generate project skeleton")
        print("2. Suggest commit messages")
        print("3. Show git publish commands")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            handle_generate_skeleton()
        elif choice == "2":
            handle_suggest_commits()
        elif choice == "3":
            handle_git_commands()
        elif choice == "4":
            print("Goodbye.")
            return 0
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


def handle_generate_skeleton() -> None:
    project_name = input("Project name: ").strip()
    destination_text = input("Destination folder [.]: ").strip() or "."

    if not project_name:
        print("Project name is required.")
        return

    result = generate_project_skeleton(project_name, Path(destination_text))
    print_section("Skeleton Created")
    print(f"Root: {result.root}")
    print(f"Created files: {result.created_count}")
    print(f"Skipped files: {result.skipped_count}")


def handle_suggest_commits() -> None:
    repo_text = input("Repository path [.]: ").strip() or "."

    try:
        suggestions = suggest_commit_messages(Path(repo_text))
    except GitError as exc:
        print(f"Error: {exc}")
        return

    print_section("Commit Suggestions")
    print_list(
        [f'{item.message} - {item.reason}' for item in suggestions],
        "No suggestions available.",
    )


def handle_git_commands() -> None:
    message = input("Commit message [feat: add initial project]: ").strip()
    remote = input("Remote URL [https://github.com/<username>/<repository>.git]: ").strip()
    branch = input("Branch [main]: ").strip() or "main"

    commands = build_git_command_plan(
        commit_message=message or "feat: add initial project",
        branch=branch,
        remote_url=remote or "https://github.com/<username>/<repository>.git",
    )

    print_section("Git Commands")
    for command in commands:
        print(command)
