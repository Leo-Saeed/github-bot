# Log Insight CLI

A clean, production-ready Python mini project that analyzes application log files and produces a concise health report. It is designed as a practical GitHub portfolio project with modular code, clear error handling, and a small standout feature: repeated messages are normalized so noisy IDs do not hide real patterns.

## Features

- Parse timestamped application logs with levels such as `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.
- Summarize log level counts, invalid lines, time range, and busiest minute.
- Detect repeated message patterns by normalizing IDs, durations, and other numeric values.
- Calculate a simple `0-100` health score based on severity and parse quality.
- Export a polished Markdown report for sharing or documentation.

## Project Structure

```text
.
├── examples/
│   └── sample.log
├── src/
│   ├── __init__.py
│   └── loginsight/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── cli.py
│       ├── models.py
│       ├── parser.py
│       └── reporter.py
├── main.py
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository.

```bash
git clone <your-repository-url>
cd <your-repository-folder>
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

The project currently uses only the Python standard library, so installation is intentionally lightweight.

## Usage

Analyze the included sample log:

```bash
python main.py examples/sample.log
```

Export a Markdown report:

```bash
python main.py examples/sample.log --export reports/sample-report.md
```

Limit repeated message patterns:

```bash
python main.py examples/sample.log --top 3
```

## Expected Log Format

Each valid log line should follow this format:

```text
YYYY-MM-DD HH:MM:SS LEVEL Message text
```

Example:

```text
2026-05-01 09:01:12 ERROR Payment failed order_id=1024 gateway=stripe
```

Supported levels are `TRACE`, `DEBUG`, `INFO`, `WARNING`, `WARN`, `ERROR`, `CRITICAL`, and `FATAL`.

## Example Output

```text
Log Insight Report
==================
Health score: 47/100
Total parsed entries: 8
Invalid lines skipped: 1

Levels:
- CRITICAL: 1
- ERROR: 2
- INFO: 4
- WARNING: 1
```

## Best Practices Included

- Modular package structure under `src/`.
- Dataclasses for structured analysis data.
- Clear CLI argument validation.
- Custom exception for readable parse errors.
- Small, focused functions that are easy to test and extend.
