# Retired Scripts

The `scripts/` directory previously contained one-shot authoring helpers
that were used to bootstrap the initial 16 modules and 379 topics. Those
scripts have been retired (issue #6) and removed because:

- They referenced internal generation contexts that no longer apply.
- None were imported by other scripts, workflows, or Makefile targets.
- They are not maintained tools — re-running them would not reproduce
  current content.

## What was retired

The following scripts were removed in the chore PR that closed #6:

- `complete_module_content.py`
- `complete_module_readmes.py`
- `fix_remaining_placeholders.py`
- `generate_modulo_14.py`
- `generate_modulo_16.py`
- `generate_patrones.py`
- `populate_content.py`
- `update_readmes.py`
- `update_references.py`

If you need to look at what they did, fetch the parent SHA of the chore
PR's first commit from git history.

## Canonical authoring flow today

To author or extend a topic, follow the workflow in `AGENTS.md` and
`docs/CHARTER.md`. The maintained tools in `scripts/` are:

- `progress.py` — read-only progress tracking
- `generate_structure.py` — create a new module/topic skeleton
- `validate_all_modules.py` — module structure validator (CI gate)
- `validate_ci_gate.py` — gold-quality validator
- `link_check.py` — external-link verification
