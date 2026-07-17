# Contributing

Thank you for helping improve Python Engineering Labs. Keep contributions focused,
beginner-friendly, and written in English.

## Prerequisites

- [Git](https://git-scm.com/)
- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)

You can also use the repository's Dev Container. See
[Getting Started](GETTING_STARTED.md) for the complete setup options.

## Local setup

Fork the repository on GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/nan-python-engineering-labs.git
cd nan-python-engineering-labs
uv venv
```

Activate the virtual environment:

```bash
# macOS or Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install the development dependencies:

```bash
uv pip install -e ".[dev]"
pre-commit install
```

Install all optional dependencies with `uv pip install -e ".[all]"` when your
change needs the full curriculum validation used in CI.

## Validate your change

Run the checks that match your change from the repository root:

```bash
uv run scripts/validate_all_modules.py
uv run scripts/validate_ci_gate.py
uv run scripts/run_topic_tests.py 01_python_fundamentals/advanced_strings
```

Run all topic tests with `uv run scripts/run_topic_tests.py`. For documentation-only
changes, preview the rendered Markdown and state in the pull request when automated
tests do not apply.

## Submit a pull request

1. Create a short-lived branch from `main` for one logical change.
1. Use focused commits with English messages.
1. Push the branch to your fork and open a pull request against `main`.
1. Complete the pull request template with the related issue, validation evidence,
   and any risks or follow-up work.

Before submitting, review the repository conventions in [AGENTS.md](AGENTS.md) and
keep unrelated changes out of the pull request.
