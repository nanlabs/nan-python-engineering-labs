---
name: lab-module-sync
description: "Use when creating or updating a lab module across training-py and nan-python-engineering-labs: copy module structure, translate docs to English, keep examples identical in both repos, validate all examples run, and prepare commits. Triggers: module migration, translate module, sync examples, lab workflow, copy+translate+validate."
---

# Lab Module Sync

## Purpose

Standardize the workflow for Python lab modules across both repositories:
- `training-py` (original/source)
- `nan-python-engineering-labs` (target NaNLABS)

The workflow ensures:
- English directory names and references
- English docs and examples
- Identical `examples/example_basic.py` content in both repos
- Executable examples with validation evidence

## Inputs

- Module number and source path (for example: `03_basic_intermediate_oop`)
- Target module path in NaNLABS repo
- Whether to commit and push

## Workflow

1. Discover context
- Read root `README.md`, `GETTING_STARTED.md`, `STATUS.md` in both repos.
- Confirm naming conventions currently in use.
- Confirm module/topic slug mapping.

2. Copy structure
- Create target module in NaNLABS repo with standard lab layout per topic:
  - `README.md`
  - `examples/example_basic.py`
  - `exercises/exercise_01.py`
  - `tests/test_basic.py`
  - `references/links.md`
  - `my_solution/.gitkeep`

3. Translate and normalize
- Translate module and topic docs to English.
- Keep technical terms consistent across files.
- Ensure folder names are English slugs.
- Update all markdown/internal references after renames.

4. Complete examples
- Replace placeholder examples with runnable Python code.
- Keep examples practical and beginner-friendly for that module level.
- Ensure examples in both repos are identical (same code, same language).

5. Sync to original repo
- Copy generated/approved examples from NaNLABS module to matching module in `training-py`.
- Preserve topic slug mapping exactly.

6. Validate
- Run every `*/examples/example_basic.py` in both repos for the module.
- Report pass/fail counts and list failing files with traceback if any.
- Fix failures before finishing.

7. Commit hygiene
- Show `git status --short` for both repos.
- Use English commit messages.
- Commit separately per repo.
- Push only when requested (or when already agreed in session).

## Quality Gates (must pass)

- All topic directories are in English.
- No broken internal links in module readmes/references.
- `examples/example_basic.py` files are identical in both repos.
- Validation result is 100% passing for the target module.
- No unrelated file changes included in commits.

## Output Format

When done, return:
- Module processed
- Files created/updated summary
- Validation results for both repos (`X/Y OK`)
- Commit SHAs (and push status if applicable)
- Any residual risks or manual follow-up

## Safety Rules

- Do not delete learner work in `my_solution/`.
- Do not revert unrelated user changes.
- Avoid destructive git commands.
- Keep changes minimal and scoped to the requested module.
