# GitHub Workflow Bot

GitHub Workflow Bot is a clean Python CLI project that helps developers start and publish small projects faster. It can generate a professional Python project skeleton, suggest commit messages from current Git changes, and print the exact Git commands needed to initialize, commit, and push a repository.

The project is intentionally simple, modular, and portfolio-ready.

## Features

- Generate a clean Python project skeleton with `src/`, `tests/`, `README.md`, `.gitignore`, and `requirements.txt`.
- Suggest practical Conventional Commit messages from `git status --short`.
- Show copy-ready Git commands for `add`, `commit`, remote setup, and push.
- Provide both direct CLI commands and a simple interactive menu.
- Use only the Python standard library.

## Project Structure

```text
.
├── src/
│   ├── github_workflow_bot/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── commit_suggester.py
│   │   ├── git_commands.py
│   │   ├── git_status.py
│   │   ├── menu.py
│   │   ├── models.py
│   │   └── skeleton.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── console.py
│   │   └── files.py
│   └── __init__.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository.

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>
```

2. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

This project currently uses only the Python standard library.

## Usage

Open the interactive menu:

```bash
python main.py menu
```

Generate a new Python project skeleton:

```bash
python main.py init-project my-python-app
```

Generate a skeleton in a specific destination:

```bash
python main.py init-project my-python-app --destination projects
```

Suggest commit messages from the current repository:

```bash
python main.py suggest-commit --path .
```

Show Git commands for publishing:

```bash
python main.py git-commands --message "feat: add GitHub workflow helper bot" --remote-url https://github.com/<username>/<repository>.git
```

## Example Output

```text
Suggested Commit Messages
-------------------------
- feat: add GitHub workflow helper bot - Detected a new app-style structure with source and README files.
- feat: update project structure - Best fit based on changed file types and git statuses.
- chore: update project workflow files - Good general-purpose option for setup or maintenance changes.
```

## Git Commands

Run these commands from the project root after creating a GitHub repository:

```bash
git init
git branch -M main
git add .
git commit -m "feat: add GitHub workflow helper bot"
git remote add origin https://github.com/<username>/<repository>.git
git push -u origin main
```

Replace `<username>` and `<repository>` with your GitHub username and repository name.

## Notes

- The bot prints Git commands instead of running destructive publish operations automatically.
- Existing files are skipped during skeleton generation unless `--force` is used.
- Commit suggestions are rule-based, transparent, and easy to extend.
