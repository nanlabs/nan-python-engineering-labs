______________________________________________________________________

## name: lab-module-sync description: "Use when creating or updating a lab module across training-py and nan-python-engineering-labs: copy module structure, translate docs to English, keep examples identical in both repos, validate all examples run, and prepare commits. Triggers: module migration, translate module, sync examples, lab workflow, copy+translate+validate."

# Lab Module Sync

## Purpose

Standardize the workflow for Python lab modules across both repositories:

- `training-py` (original/source)
- `nan-python-engineering-labs` (target NaNLABS)

The workflow ensures:

- English directory names and references
- Language split by repository:
  - `training-py`: Spanish documentation
  - `nan-python-engineering-labs`: English documentation
- Identical `examples/example_basic.py` content in both repos
- Executable examples with validation evidence
- A homogeneous topic structure even when source modules are inconsistent
- Pattern/topic-appropriate examples (no name-only template cloning)

## Repository Policy Matrix

The table below is the **authoritative source** for language and content rules per file type and repo. When in doubt, refer here first.

| File / Asset                | `training-py`                                    | `nan-python-engineering-labs`                     |
| --------------------------- | ------------------------------------------------ | ------------------------------------------------- |
| `README.md`                 | **Spanish** content + 17-heading schema          | **English** content + 17-heading schema           |
| `exercise/exercise_01.py`   | **English** instructions, goal, comments         | **English** instructions, goal, comments          |
| `references/links.md`       | Spanish section headers OK; real `https://` URLs | **English** section headers; real `https://` URLs |
| `examples/example_basic.py` | **English** comments, docstrings, output         | **English** comments, docstrings, output          |
| `tests/test_basic.py`       | **English** docstrings and comments              | **English** docstrings and comments               |
| Directory / file names      | **English** slugs                                | **English** slugs                                 |

> **Key rule**: Only `README.md` files in `training-py` are written in Spanish. Every other asset (exercises, examples, tests, references) uses English in **both** repos. This is because technical instructions and code are universally English; only the pedagogical narrative stays in Spanish for `training-py` learners.

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
  - `exercise/`
  - `tests/`
  - `references/`
  - `my_solution/`
- Ensure `my_solution/.gitkeep` exists.
- If the source layout is inconsistent, fix it first so both repos end with the same standard structure.

3. Copy structure

- Create target module in NaNLABS repo with standard lab layout per topic:
  - `README.md`
  - `examples/example_basic.py`
  - `exercise/exercise_01.py`
  - `tests/test_basic.py`
  - `references/links.md`
  - `my_solution/.gitkeep`

4. Translate and normalize (Repository language policy)

- Apply language policy by repository:
  - `training-py`: keep or translate documentation to Spanish.
  - `nan-python-engineering-labs`: keep or translate documentation to English.
- For NaN repo, translate ALL files to English (not just README, but also exercises, references, tests):
  - `README.md` (module and all topic READMEs)
  - `exercise/exercise_01.py` (instructions and comments)
  - `references/links.md` (documentation and descriptions)
  - `tests/test_basic.py` (docstrings and comments)
  - Any other markdown or documentation files
- Validation:
  - In `training-py`, enforce Spanish documentation style in README content.
  - In `nan-python-engineering-labs`, scan all files for Spanish keywords (Módulo, Descripción, Objetivo, Ejercicio, Referencias, Instrucciones, etc.) and translate before proceeding.
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
- For `training-py`, preserve pedagogical depth and enforce Spanish language in topic READMEs.
- For `nan-python-engineering-labs`, preserve pedagogical depth and enforce English-only content.
- If any section is missing, create it before continuing.

4.2 README heading schema lock (NEW - strict)

- All topic READMEs must have the exact same heading and subheading schema (same amount, same order) across all processed modules.
- Required heading/subheading sequence:
  1. `# <Topic Title>`
  1. `Estimated time: ...`
  1. `## 1. Definition`
  1. `### Key Characteristics`
  1. `## 2. Practical Application`
  1. `### Use Cases`
  1. `### Code Example`
  1. `## 3. Why Is It Important?`
  1. `### Problem It Solves`
  1. `### Solution and Benefits`
  1. `## 4. References`
  1. `## 5. Practice Task`
  1. `### Basic Level`
  1. `### Intermediate Level`
  1. `### Advanced Level`
  1. `### Success Criteria`
  1. `## 6. Summary`
  1. `## 7. Reflection Prompt`
- If a topic README deviates from this schema, rewrite it to match exactly.

5. Complete examples

- Replace placeholder examples with runnable Python code.
- Keep examples practical and beginner-friendly for that module level.
- Ensure examples in both repos are identical (same code, same language).
- Each topic/pattern must have logic specific to its own concept (not the same skeleton with renamed labels).

5.1 Example language + completeness lock (NEW - strict)

- Every `examples/example_basic.py` in `nan-python-engineering-labs` must be English-only in comments, docstrings, and printed messages.
- Disallow placeholders in examples:
  - No `TODO`
  - No template comments like "add specific example"
  - No empty demo placeholders intended to be completed later
- Each example must contain runnable concept-specific logic and meaningful output.
- Avoid trivial no-op stubs as final examples.

5.2 Exercise language + completeness lock (NEW - strict)

- Every `exercise/exercise_01.py` in **both repos** must be English-only in comments, docstrings, instructions, and task descriptions.
- This applies equally to `training-py` and `nan-python-engineering-labs`. Only `README.md` files stay in Spanish for `training-py`; exercises are English in both.
- Disallow placeholders in exercises:
  - No `TODO`
  - No template comments in Spanish (for example: "Implementa", "Añade", "Resuelve")
  - No incomplete scaffolding intended to be translated later
- Keep the exercise statement stable and learner-safe:
  - Include clear English goal and instructions
  - Preserve the "copy to `my_solution/`" workflow
  - Avoid deleting learner workspace content

5.3 References completeness lock (NEW - strict)

- Every `references/links.md` in both repos must be non-empty and contain at least 3 real `https://` URLs.
- Disallow placeholder-only references:
  - No `Add relevant documentation links here.`
  - No empty files
  - No files with a title-only header and no links
- Required structure:
  - A title heading (`# References: <Topic>` or `# Referencias: <Topic>`)
  - At least one `## Official Documentation` / `## Documentación Oficial` section
  - At least 2 links in the official section
  - At least 1 article/guide link
- Links must be topic-specific (not the same generic set for every topic in the module).

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
- **Language compliance check (NEW)**:
  - `training-py`: verify topic README structure is in Spanish (section headers/content language in Spanish).
  - `nan-python-engineering-labs`: scan ALL files for Spanish keywords:
  - If any Spanish content found in exercises, references, tests, or docs → FAIL gate and re-translate before committing
  - This ensures 100% English-only compliance for NaN repo
- **Example completeness + language check (NEW)**:
  - Scan every `examples/example_basic.py` in the processed module.
  - Fail if any example contains placeholder markers (`TODO`, template text, incomplete scaffolding).
  - Fail if any comments/docstrings/messages in examples are Spanish.
  - Execute every example and require zero runtime failures.
- **Exercise completeness + language check (NEW)**:
  - Scan every `exercise/exercise_01.py` in the processed module.
  - Fail if any exercise contains Spanish comments/docstrings/instructions.
  - Fail if any exercise contains placeholder markers (`TODO`, template scaffolding, untranslated helper comments).
  - Require all exercise files to exist and be syntactically valid Python.
- **References completeness check (NEW)**:
  - Scan every `references/links.md` in the processed module.
  - Fail if any file contains fewer than 3 `https://` URLs.
  - Fail if any file contains `Add relevant documentation links here.` placeholder text.
  - Fail if all references files are identical (indicates a copy-paste fallback instead of topic-specific content).
  - For NaN repo: fail if any references file contains Spanish-language section headers.

8. Commit hygiene

- Show `git status --short` for both repos.
- Use English commit messages.
- Commit separately per repo.
- Push only when requested (or when already agreed in session).

## Validation Commands

Use these exact commands to run validation checks. Always use the project venv:

```bash
PYTHON=/media/nquiroga/SSDedo/Documents/projects/NanLabs/labs/.venv/bin/python

# ── NaN repo (from nan-python-engineering-labs/) ──────────────────────────────
# Full cross-module audit (C1 Spanish content, C2 filenames, C3 dirs, C4 dups, C5 canonical)
$PYTHON scripts/audit_nan_modules.py

# Language scan for a specific module
$PYTHON scripts/validate_nan_language.py --module 11_modern_tooling_2026

# Unified validation: all checks (L1, S1, R1, X1, E1, M1) across all modules
$PYTHON scripts/validate_all_modules.py

# Single module
$PYTHON scripts/validate_all_modules.py --module 14_advanced_python_2026

# ── training-py (from training-py/) ──────────────────────────────────────────
# Unified validation: all checks (SP1, S1, R1, X1, E1, M1) across modules 01-14
$PYTHON scripts/validate_all_modules.py

# Single module
$PYTHON scripts/validate_all_modules.py --module 14_advanced_python_2026

# Legacy module-14-only script (still usable)
$PYTHON 14_advanced_python_2026/validate_module14.py
```

**Expected output when all gates pass:**

```
Module 01_python_fundamentals  S1✅ R1✅ X1✅ E1✅ M1✅ L1✅
Module 02_intermediate_python  S1✅ R1✅ X1✅ E1✅ M1✅ L1✅
...
SUMMARY: 14/14 modules — all checks passed
```

## Quality Gates (must pass)

- All topic directories are in English.
- All topics in both repos share the standard lab subfolder structure.
- **README completeness**: Every topic README contains the full pedagogical structure with "Use Cases" and practice levels.
- **README schema consistency**: Every topic README follows the exact same heading/subheading count and order.
- **training-py Spanish compliance**: Topic READMEs are in Spanish with the required schema.
- **100% English-only compliance for NaN repo**: No Spanish content in NaN files (README, exercises, references, tests, code comments):
  - No "Módulo:", "Descripción", "Objetivo", "Ejercicio", "Referencias", "Instrucciones", etc.
  - All documentation files translated to English
  - All exercise and reference files in English
  - All comments and docstrings in code are English
- **Example quality gate (NEW)**:
  - Every `examples/example_basic.py` is English-only and free of placeholders.
  - No `TODO` markers in examples.
  - Examples execute successfully in module validation.
- **Exercise quality gate (NEW)**:
  - Every `exercise/exercise_01.py` is English-only and free of placeholders — **in both repos**.
  - No `TODO` markers in exercises.
  - Exercise statements are complete and usable without translation follow-up.
  - *Known technical debt*: exercises in `training-py` modules 01–13 may still contain Spanish docstrings from before this policy was enforced. Treat as tech debt; fix incrementally per module.
- **References quality gate (NEW)**:
  - Every `references/links.md` contains at least 3 real `https://` URLs.
  - No placeholder-only references files (e.g., `Add relevant documentation links here.` stubs).
  - Links must be topic-specific (not the same generic fallback for all topics).
  - NaN repo references must be in English; training-py references may use Spanish headers.
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
- All `examples/example_basic.py` files (comments/docstrings/print messages)
- All `exercise/exercise_01.py` files for placeholder markers (`TODO`, Spanish scaffolding text)
- Any `.md` or `.py` files in topics

**Action if Spanish found**:

1. Halt the commit workflow
1. Translate all Spanish content to English
1. Re-validate (scan again)
1. Only proceed with commit when 100% English-only confirmed

**Output**: Before final commit, show:

- ✓ training-py language check: Spanish README structure verified
- ✓ NaN language scan: 0 Spanish keywords found
- ✓ README structure scan: all required sections present
- ✓ README heading-schema scan: all topic READMEs match exactly
- ✓ All files: language policy compliance verified
- Ready for commit
