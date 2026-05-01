from __future__ import annotations

from pathlib import Path

from src.utils.files import sanitize_package_name, write_text_file

from .models import SkeletonResult


def generate_project_skeleton(
    project_name: str,
    destination: Path,
    overwrite: bool = False,
) -> SkeletonResult:
    """Generate a small professional Python project skeleton."""

    root = destination / project_name
    package_name = sanitize_package_name(project_name)
    files = build_skeleton_files(project_name, package_name)
    result = SkeletonResult(root=root)

    for relative_path, content in files.items():
        target = root / relative_path
        was_written = write_text_file(target, content, overwrite=overwrite)

        if was_written:
            result.created.append(target)
        else:
            result.skipped.append(target)

    return result


def build_skeleton_files(project_name: str, package_name: str) -> dict[Path, str]:
    """Return the template files for a generated Python project."""

    return {
        Path("README.md"): f"""# {project_name}

A clean Python project generated with GitHub Workflow Bot.

## Installation

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```
""",
        Path(".gitignore"): """__pycache__/
*.py[cod]
.venv/
venv/
.env
.pytest_cache/
""",
        Path("requirements.txt"): "# Add project dependencies here.\n",
        Path("main.py"): f"""from src.{package_name}.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
""",
        Path("src") / "__init__.py": "",
        Path("src") / package_name / "__init__.py": f'"""Application package for {project_name}."""\n',
        Path("src") / package_name / "cli.py": '''def main() -> int:
    """Run the application."""

    print("Hello from your generated Python project.")
    return 0
''',
        Path("tests") / ".gitkeep": "",
    }
