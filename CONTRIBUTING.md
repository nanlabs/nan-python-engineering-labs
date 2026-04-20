# Contributing

## Branches

- Work from `main` using short-lived feature branches.
- Keep one logical change per branch.

## Commits

- Use English commit messages.
- Keep commits focused and small.
- Avoid mixing infra and content changes in the same commit when possible.

## Validation Before Commit

Run from repo root:

```bash
PYTHON=/media/nquiroga/SSDedo/Documents/projects/NanLabs/labs/.venv/bin/python
$PYTHON scripts/validate_all_modules.py
$PYTHON scripts/run_topic_tests.py 01_python_fundamentals/advanced_strings
```

## Pull Requests

- Use the PR template.
- Include scope, validation evidence, and risks.
- Do not include unrelated changes.
