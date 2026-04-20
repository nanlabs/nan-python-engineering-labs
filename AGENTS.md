# AGENTS

## Scope

This file defines agent behavior for this repository.

## Source of Truth

1. Follow this file first.
1. Follow `.github/skills/lab-module-sync/SKILL.md` for module sync and validation rules.
1. If instructions conflict, prefer this file for agent behavior and the SKILL file for content rules.

## Repository Conventions

- Canonical topic structure:
  - `README.md`
  - `examples/example_basic.py`
  - `exercise/exercise_01.py`
  - `tests/test_basic.py`
  - `references/links.md`
  - `my_solution/.gitkeep`
- Language policy:
  - All repository documentation and code comments must be English.
- Exercise policy:
  - `exercise/exercise_01.py` must be English-only and must not contain TODO placeholders.
- README policy:
  - Topic README schema is validated with a minimum of 17 markdown headings.

## Validation Commands

Use project venv explicitly:

```bash
PYTHON=/media/nquiroga/SSDedo/Documents/projects/NanLabs/labs/.venv/bin/python
$PYTHON scripts/validate_all_modules.py
$PYTHON scripts/run_topic_tests.py
```

## Safety

- Do not run destructive git commands (`reset --hard`, `checkout --`) unless explicitly requested.
- Do not revert unrelated user changes.
- Keep changes minimal and scoped to the requested task.
