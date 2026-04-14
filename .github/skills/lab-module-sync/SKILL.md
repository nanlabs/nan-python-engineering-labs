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
- A homogeneous topic structure even when source modules are inconsistent
- Pattern/topic-appropriate examples (no name-only template cloning)

## Inputs

- Module number and source path (for example: `03_basic_intermediate_oop`)
- Target module path in NaNLABS repo
- Whether to commit and push

## Workflow

1. Discover context
- Read root `README.md`, `GETTING_STARTED.md`, `STATUS.md` in both repos.
- Confirm naming conventions currently in use.
- Confirm module/topic slug mapping.

2. Normalize structure
- Inspect every topic directory in the source module.
- If any topic is missing standard lab folders, create or restore them before proceeding:
  - `examples/`
  - `exercises/`
  - `tests/`
  - `references/`
  - `my_solution/`
- Ensure `my_solution/.gitkeep` exists.
- If the source layout is inconsistent, fix it first so both repos end with the same standard structure.

3. Copy structure
- Create target module in NaNLABS repo with standard lab layout per topic:
  - `README.md`
  - `examples/example_basic.py`
  - `exercises/exercise_01.py`
  - `tests/test_basic.py`
  - `references/links.md`
  - `my_solution/.gitkeep`

4. Translate and normalize
- Translate module and topic docs to English.
- Keep technical terms consistent across files.
- Ensure folder names are English slugs.
- Update all markdown/internal references after renames.

5. Complete examples
- Replace placeholder examples with runnable Python code.
- Keep examples practical and beginner-friendly for that module level.
- Ensure examples in both repos are identical (same code, same language).
- Each topic/pattern must have logic specific to its own concept (not the same skeleton with renamed labels).

6. Sync to original repo
- Copy generated/approved examples from NaNLABS module to matching module in `training-py`.
- Preserve topic slug mapping exactly.

7. Validate
- Run every `*/examples/example_basic.py` in both repos for the module.
- Report pass/fail counts and list failing files with traceback if any.
- Fix failures before finishing.
- Run a structural duplication audit for the module examples. If the module uses near-identical structures for most topics, fail the gate and regenerate examples with concept-specific logic.
- If a module has nested topics (e.g., `category/topic/examples/example_basic.py`), include that layout in both execution and duplication audits.

8. Commit hygiene
- Show `git status --short` for both repos.
- Use English commit messages.
- Commit separately per repo.
- Push only when requested (or when already agreed in session).

## Quality Gates (must pass)

- All topic directories are in English.
- All topics in both repos share the standard lab subfolder structure.
- No broken internal links in module readmes/references.
- `examples/example_basic.py` files are identical in both repos.
- Validation result is 100% passing for the target module.
- Examples are concept-specific: no bulk copy/paste template where only names/labels change.
- Structural clone audit passes (high diversity expected for conceptual modules like design patterns).
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
