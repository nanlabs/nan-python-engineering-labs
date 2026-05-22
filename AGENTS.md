# AGENTS

## Scope

This file defines agent behavior for this repository.

## Source of Truth

1. **Upstream contract**: [`docs/CHARTER.md`](docs/CHARTER.md) (NaNLABS Lab Charter v1).
1. Follow this file for agent-specific behavior within this repo.
1. Follow `.github/skills/lab-module-sync/SKILL.md` for module sync and validation rules.
1. If instructions conflict, prefer this file for agent behavior and the SKILL file for content rules.

## Sibling Labs

- [`nanlabs/nan-ai-engineering-labs`](https://github.com/nanlabs/nan-ai-engineering-labs)
- [`nanlabs/nan-data-engineering-labs`](https://github.com/nanlabs/nan-data-engineering-labs)
- [`nanlabs/nan-ai-native-engineering-labs`](https://github.com/nanlabs/nan-ai-native-engineering-labs)

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

Use the project virtual environment:

```bash
# Activate the project venv and run validators
source .venv/bin/activate
python scripts/validate_all_modules.py
python scripts/run_topic_tests.py
```

Or with `uv run` (does not require manual activation):

```bash
uv run scripts/validate_all_modules.py
uv run scripts/run_topic_tests.py
```

## Safety

- Do not run destructive git commands (`reset --hard`, `checkout --`) unless explicitly requested.
- Do not revert unrelated user changes.
- Keep changes minimal and scoped to the requested task.
