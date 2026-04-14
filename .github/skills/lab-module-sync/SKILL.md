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

4. Translate and normalize (Complete English-only compliance)
- Translate ALL files to English (not just README, but also exercises, references, tests):
  - `README.md` (module and all topic READMEs)
  - `exercises/exercise_01.py` (instructions and comments)
  - `references/links.md` (documentation and descriptions)
  - `tests/test_basic.py` (docstrings and comments)
  - Any other markdown or documentation files
- Validation: scan all files for Spanish keywords (Módulo, Descripción, Objetivo, Ejercicio, Referencias, Instrucciones, etc.) and translate before proceeding.
- Keep technical terms consistent across files.
- Ensure folder names are English slugs.
- Update all markdown/internal references after renames.
- Result: 100% English-only content in NaNLABS repo (no Spanish text remains).

4.1 README structure normalization (NEW - mandatory)
- Every topic `README.md` must follow a complete teaching structure (not a short/sparse variant).
- Required sections per topic README:
  - Title (`# Topic Name`)
  - Estimated time
  - Definition
  - Key characteristics
  - Practical application
  - Use cases (minimum 3 concrete cases)
  - Code example section pointing to `examples/example_basic.py`
  - Why it matters
  - Problem it solves
  - Solution and benefits
  - References section (linked to `references/links.md`)
  - Practice task with levels (basic, intermediate, advanced) and explicit success criteria
  - Summary
  - Reflection prompt
- For `training-py`, preserve the pedagogical depth and structure even if source language is Spanish.
- For `nan-python-engineering-labs`, keep the same pedagogical depth but enforce English-only content.
- If any section is missing, create it before continuing.

4.2 README heading schema lock (NEW - strict)
- All topic READMEs must have the exact same heading and subheading schema (same amount, same order) across all processed modules.
- Required heading/subheading sequence:
  1. `# <Topic Title>`
  2. `Estimated time: ...`
  3. `## 1. Definition`
  4. `### Key Characteristics`
  5. `## 2. Practical Application`
  6. `### Use Cases`
  7. `### Code Example`
  8. `## 3. Why Is It Important?`
  9. `### Problem It Solves`
  10. `### Solution and Benefits`
  11. `## 4. References`
  12. `## 5. Practice Task`
  13. `### Basic Level`
  14. `### Intermediate Level`
  15. `### Advanced Level`
  16. `### Success Criteria`
  17. `## 6. Summary`
  18. `## 7. Reflection Prompt`
- If a topic README deviates from this schema, rewrite it to match exactly.

5. Complete examples
- Replace placeholder examples with runnable Python code.
- Keep examples practical and beginner-friendly for that module level.
- Ensure examples in both repos are identical (same code, same language).
- Each topic/pattern must have logic specific to its own concept (not the same skeleton with renamed labels).

6. Sync to original repo
- Copy generated/approved examples from NaNLABS module to matching module in `training-py`.
- Preserve topic slug mapping exactly.

7. Validate (Execution + Structure + Language)
- Run every `*/examples/example_basic.py` in both repos for the module.
- Report pass/fail counts and list failing files with traceback if any.
- Fix failures before finishing.
- Run a structural duplication audit for the module examples. If the module uses near-identical structures for most topics, fail the gate and regenerate examples with concept-specific logic.
- If a module has nested topics (e.g., `category/topic/examples/example_basic.py`), include that layout in both execution and duplication audits.
- **README structure compliance check (NEW)**:
  - Scan every topic `README.md` and verify all required sections exist.
  - Verify a "Use Cases" subsection exists with at least 3 items.
  - If structure is incomplete in any topic, fail the gate and complete the README before commit.
- **README heading-schema check (NEW)**:
  - Validate heading/subheading count and order against the locked schema.
  - If any topic README has extra/missing/reordered headings, fail the gate.
  - Normalize all non-compliant READMEs before commit.
- **Language compliance check (NEW)**: Scan ALL files in nan-python-engineering-labs repo for Spanish keywords:
  - If any Spanish content found in exercises, references, tests, or docs → FAIL gate and re-translate before committing
  - This ensures 100% English-only compliance for NaN repo

8. Commit hygiene
- Show `git status --short` for both repos.
- Use English commit messages.
- Commit separately per repo.
- Push only when requested (or when already agreed in session).

## Quality Gates (must pass)

- All topic directories are in English.
- All topics in both repos share the standard lab subfolder structure.
- **README completeness**: Every topic README contains the full pedagogical structure with "Use Cases" and practice levels.
- **README schema consistency**: Every topic README follows the exact same heading/subheading count and order.
- **100% English-only compliance**: No Spanish content in ANY file (README, exercises, references, tests, code comments):
  - No "Módulo:", "Descripción", "Objetivo", "Ejercicio", "Referencias", "Instrucciones", etc.
  - All documentation files translated to English
  - All exercise and reference files in English
  - All comments and docstrings in code are English
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

## Language Compliance Validation (NEW - Critical for NaN repo)

Implement a language check before final commit to NaN repo:

**Spanish content detection** - fail if ANY of these appear in NaN repo files:
- "Módulo:", "Descripción", "Objetivo", "Ejercicio", "Practica", "Instrucciones"
- "Referencias", "Enlaces", "Recursos", "Aprende", "Diseña", "Conceptos"
- "Debes", "Requisitos", "Hints", "Ejemplo", "Solución"

**Files to scan**:
- All `README.md` files (module + topics)
- All `exercises/exercise_*.py` files
- All `references/links.md` files
- All `tests/test_*.py` files (comments/docstrings)
- Any `.md` or `.py` files in topics

**Action if Spanish found**:
1. Halt the commit workflow
2. Translate all Spanish content to English
3. Re-validate (scan again)
4. Only proceed with commit when 100% English-only confirmed

**Output**: Before final commit, show:
- ✓ Language scan: 0 Spanish keywords found
- ✓ README structure scan: all required sections present
- ✓ README heading-schema scan: all topic READMEs match exactly
- ✓ All files: English-only compliance verified
- Ready for commit
