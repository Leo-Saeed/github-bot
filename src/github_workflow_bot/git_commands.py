from __future__ import annotations


def build_git_command_plan(
    commit_message: str,
    branch: str = "main",
    remote_url: str = "https://github.com/<username>/<repository>.git",
) -> list[str]:
    """Return the git commands a developer can run to publish the project."""

    safe_message = commit_message.replace('"', '\\"')

    return [
        "git init",
        "git branch -M main",
        "git add .",
        f'git commit -m "{safe_message}"',
        f"git remote add origin {remote_url}",
        f"git push -u origin {branch}",
    ]
