______________________________________________________________________

## name: lab-module-sync description: "Use when creating or updating topic labs inside nan-python-engineering-labs: enforce canonical structure, validate English-only content, run checks, and prepare scoped commits. Triggers: module update, topic standardization, lab workflow, examples validation, structure check."

# Lab Module Sync

## Purpose

Standardize and validate Python lab topics inside this repository only.

The workflow ensures:

- Canonical topic structure in every module
- English-only documentation and code comments
- Runnable examples and passing topic tests
- Consistent README heading schema
- Scoped, reviewable changes

## Canonical Topic Structure

Each topic must include:

- `README.md`
- `examples/example_basic.py`
- `exercise/exercise_01.py`
- `tests/test_basic.py`
- `references/links.md`
- `my_solution/.gitkeep`

## Required Workflow

1. Discover context

- Read `README.md`, `GETTING_STARTED.md`, and `STATUS.md`.
- Confirm module and topic naming conventions.

1. Normalize structure

- Ensure the canonical topic structure exists.
- Create missing paths with minimal edits.

1. Validate language and quality

- Keep docs, comments, and user-facing text in English.
- Remove placeholder content (`TODO`, empty stubs, template markers).

1. Validate execution

- Run module validators and tests.
- Fix failures before finalizing.

1. Commit hygiene

- Keep changes scoped to requested modules/topics.
- Use English commit messages.

## Validation Commands

Use the project venv:

```bash
source .venv/bin/activate
python scripts/validate_all_modules.py
python scripts/run_topic_tests.py
```

Or using `uv run`:

```bash
uv run scripts/validate_all_modules.py
uv run scripts/run_topic_tests.py
```

## Quality Gates (must pass)

- Topic structure is canonical.
- README headings match repository expectations.
- Examples run without runtime errors.
- Tests pass for touched topics.
- English-only content in touched files.
- No unrelated file changes.

## Output Format

When done, return:

- Module/topic processed
- Files created/updated summary
- Validation result summary
- Any residual risks or manual follow-up

## Safety Rules

- Do not delete user-authored learner work in `my_solution/`.
- Do not revert unrelated user changes.
- Do not run destructive git commands.
