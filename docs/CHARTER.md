# NaNLABS Lab Charter v1

> Single source of truth for the structure, conventions, and quality bar of every NaNLABS learning lab.

## Adopting labs

- `nanlabs/nan-python-engineering-labs`
- `nanlabs/nan-ai-engineering-labs`
- `nanlabs/nan-data-engineering-labs`
- `nanlabs/nan-ai-native-engineering-labs`

## 1. Repository naming

- Module directories: `NN_short_slug/` — two-digit number + snake_case.
- Topic directories (when used): `topic_NN_short_slug/` — same pattern with `topic_` prefix.

## 2. Mandatory root files

| File | Purpose |
|---|---|
| `README.md` | Hub (sections in §5) |
| `AGENTS.md` | Agent contract; references this Charter |
| `GETTING_STARTED.md` | Onboarding |
| `STATUS.md` | Progress; contains `<!-- PROGRESS:START -->`/`<!-- PROGRESS:END -->` markers |
| `CONTRIBUTING.md` | Contribution norms |
| `LICENSE` | MIT |
| `pyproject.toml` (or `Makefile` if non-Python) | Reproducible commands |
| `.devcontainer/devcontainer.json` + `post-create.sh` | DevContainer-first |
| `.pre-commit-config.yaml` | ruff + markdownlint + language-guard |
| `.markdownlint.json` | Shared lint config |
| `.github/workflows/validate-all-modules.yml` | CI gate |
| `.github/workflows/link-check.yml` | Weekly link freshness |
| `.github/skills/lab-module-sync/SKILL.md` | Content rules companion |
| `.github/ISSUE_TEMPLATE/{bug_report,new_topic,content_improvement}.yml` | Standard templates |
| `.github/pull_request_template.md` | With validation checklist |

## 3. Canonical module structure (superset)

```text
NN_module_slug/
├── README.md           # >=17 H2/H3 headings, English only
├── theory.md           # 200-400 word concept primer
├── examples/
│   ├── example_basic.<ext>
│   └── adapters/                # AI-native lab only
├── exercise/exercise_01.<ext>
├── evaluation/
│   ├── rubric.md
│   └── eval_cases.yaml
├── tests/test_basic.<ext>
├── references/links.md          # >=3 real https URLs
└── my_solution/.gitkeep
```

Per-track allowed deviations:

- python-labs: `tests/` content as `pytest` files (mandatory).
- data-labs: may keep `infrastructure/` or `data/` extras where the topic warrants.
- ai-labs: may keep `mini-project/` for capstone-style topics.
- ai-native-labs: must include `examples/adapters/` (Claude+Copilot mandatory).

## 4. Language policy

- All committed assets are English (`.md`, `.py`, `.yaml`, identifiers).
- User-facing chat may use the user's language; commits do not.

## 5. README hub schema

1. Title + one-line tagline
2. Quick Navigation Guide
3. Learning Roadmap (Hub) — ASCII diagram
4. Program Structure (Hub) — folder tree
5. Module Summary (Hub) — table
6. Quick Start (Hub) — DevContainer + local
7. Full Documentation (Hub) — links to `docs/`
8. Sibling Labs — cross-link the other adopting labs
9. License

## 6. Emoji policy

Strict: no emojis in committed Markdown.

## 7. Badge policy

Standard set:

- `License: MIT`
- `CI: Validate All Modules` (live status)
- `Modules: NN`
- Optional: a Track badge

Forbidden: marketing badges that don't map to validated values; language badges that contradict the actual content.

## 8. GitHub repo metadata

- Repo description: required, single-sentence.
- Topic tags: 5–8 tags relevant to the track.
- Optional: social preview image; pinned roadmap issue; Discussions enabled.

## 9. Validation contract

Topic-level checks every lab must enforce (CI):

| Check | Rule |
|---|---|
| L1 Language | English-only across `.md`/`.py`/`.yaml` |
| S1 Structure | All canonical files present |
| R1 References | `references/links.md` has >=3 real `https://` URLs |
| X1 Examples | `examples/example_basic.*` exists, non-empty |
| E1 Exercise | No `TODO`/`FIXME` placeholders; contains `## Acceptance Criteria` |
| M1 README | Topic README has >=17 markdown headings |
| A1 Adapters | (ai-native only) `claude.md` + `copilot.md` in `adapters/` |
| EV1 Evaluation | `rubric.md` has required sections; `eval_cases.yaml` >=3 cases |
| PH1 Phase | Module declared in `docs/LEARNING_MODEL.md` |

CI gate: all applicable checks must exit 0.

## 10. DevContainer

Base image: `mcr.microsoft.com/devcontainers/python:1-3.13-bookworm`.

## 11. Skeleton vs gold

Skeleton topics pass structural CI but contain placeholder text. Gold-quality topics have substantive prose, real examples, topic-specific evaluations, and authoritative references. Each lab must declare which modules are gold-required (CI fails on placeholders in those).

## 12. Validator distribution

Single shared validator (`validate_all_modules.py` from `nan-ai-native-engineering-labs`) is the reference. Each lab vendors a copy via the `lab-module-sync` skill. Future: extract to `nanlabs/labs-charter` repo or PyPI.

## 13. PR + branch policy

- Charter adoption work ships as **PRs to `main`**, never direct pushes.
- One PR per repo titled `feat: adopt NaNLABS Lab Charter v1`.
- PRs may be draft until validated.
