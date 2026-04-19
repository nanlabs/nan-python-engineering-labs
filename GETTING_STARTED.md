# Getting Started — Python Engineering Labs

## What Has Been Created

### Complete Structure
- **16 thematic modules** organized and numbered
- **379 topics** in total with complete structure
- **88 design patterns** in a dedicated module
- **Modern infrastructure** ready to use

### Project Infrastructure

```
nan-python-engineering-labs/
├── .devcontainer/                    # DevContainer configuration
│   ├── devcontainer.json            # VS Code Dev Container setup
│   └── post-create.sh               # Automatic installation
├── .pre-commit-config.yaml          # Quality hooks (Ruff, BasedPyright)
├── .gitignore                       # Ignore unnecessary files
├── pyproject.toml                   # uv, Ruff, pytest configuration
├── README.md                        # Main documentation
└── scripts/
    ├── progress.py                  # Automatic progress tracking
    ├── generate_structure.py       # Basic module generator
    ├── generate_patrones.py        # 88 patterns generator
    ├── generate_modulo_14.py       # PyO3/AI module generator
    └── generate_modulo_16.py       # Security module generator
```

### Modules Created (16 modules, 379 topics)

#### Basic/Intermediate Level
1. **01_python_fundamentals** (12 topics) — Variables, control, structures, functions
2. **02_intermediate_python** (15 topics) — Decorators, files, iterators, modules
3. **03_basic_intermediate_oop** (12 topics) — Classes, inheritance, properties, descriptors

#### Advanced Level — Core Python
4. **04_cpython_internals_advanced** (27 topics) — GIL, PEP 703 free-threading, subinterpreters
5. **05_modern_concurrency** (25 topics) — Threading without GIL, asyncio, multiprocessing
6. **06_typing_metaprogramming** (22 topics) — Type hints, metaclasses, AST

#### Patterns and Architecture
7. **07_design_patterns** (88 patterns in 8 subcategories)
   - 01_basic_gof (11 patterns)
   - 02_pythonic (14 patterns)
   - 03_advanced_gof (12 patterns)
   - 04_architectural (13 patterns)
   - 05_distributed_systems (12 patterns)
   - 06_concurrency (14 patterns)
   - 07_messaging (4 patterns)
   - 08_object_management (8 patterns)

8. **08_application_architecture** (18 topics) — SOLID, DDD, hexagonal, CQRS
9. **09_testing_qa** (16 topics) — pytest, hypothesis, mutation testing
10. **10_performance_optimization** (14 topics) — Profiling, Cython, NumPy

#### Modern Technologies 2026
11. **11_modern_tooling_2026** (35 topics)
    - uv (Rust package manager)
    - Ruff (linter/formatter)
    - BasedPyright/Pylyzer
    - Pre-commit, pytest, profiling

12. **12_fastapi_complete** (28 topics) — Full framework, auth, WebSockets, deployment
13. **13_backend_ecosystem** (20 topics) — SQLAlchemy, Redis, Kafka, gRPC, observability
14. **14_advanced_python_2026** (45 topics)
    - PyO3 (Rust extensions) — 22 topics
    - AI-Assisted Development — 23 topics
    - LangChain, LangGraph, autonomous agents

15. **15_basic_data_science** (10 topics) — NumPy, Pandas, visualization
16. **16_modern_security** (40 topics)
    - Supply chain security
    - SBOM (Software Bill of Materials)
    - Sigstore (keyless signing)
    - SOPS, Vault (secrets management)

---

## How to Use This Project

### Option 1: With DevContainer (Recommended)

1. Open VS Code
2. Install the "Dev Containers" extension
3. `Cmd/Ctrl + Shift + P` → "Dev Containers: Reopen in Container"
4. Wait 3-5 minutes for automatic setup
5. Done! You will have:
   - Python 3.13
   - uv installed
   - Ruff, BasedPyright
   - All VS Code extensions
   - Pre-commit hooks configured

### Option 2: Local Installation

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Create virtual environment
uv venv

# 3. Activate environment
source .venv/bin/activate  # Linux/Mac

# 4. Install dependencies
uv pip install -e ".[dev,profiling,ai,pyo3,security,data]"

# 5. Install pre-commit hooks
pre-commit install

# 6. Verify installation
python scripts/progress.py
```

### Recommended Study Workflow

For each topic:

1. **Read README.md** → Understand definition, application, motivation
2. **Study examples/** → Run demonstration code
3. **Attempt exercise/** → Implement the topic solution in `exercise/exercise_01.py`
4. **Validate with tests** → Run the topic test file against your exercise
6. **Reflect** → Complete the "My Personal Analysis" section
7. **Commit** → Pre-commit hook updates progress automatically

```bash
# View current progress
python scripts/progress.py

# Run tests for a single topic (recommended)
python scripts/run_topic_tests.py 11_modern_tooling_2026/01_uv_introduction

# Run tests for a whole module
python scripts/run_topic_tests.py 16_modern_security

# Run all topic tests sequentially
python scripts/run_topic_tests.py

# Direct pytest for one topic only
python -m pytest -o addopts='' 11_modern_tooling_2026/01_uv_introduction/tests/test_basic.py

# Commit (updates progress automatically)
git add .
git commit -m "Completed: uv introduction"
# → Pre-commit runs Ruff, BasedPyright, progress.py
```

### Manual Test Execution Notes

- Use `python scripts/run_topic_tests.py ...` when you want a stable manual runner.
- The helper executes one `tests/test_basic.py` at a time, which avoids collisions caused by many files sharing the same name.
- If you call pytest directly, run a single file and override repo addopts with `-o addopts=''`.
- The generated tests validate `exercise/exercise_01.py`, so failures usually mean the exercise still has TODOs, import errors, or no user-defined API yet.

---

## Recommended Next Steps

### Immediate (First Hours)

1. **Review main README** → Already updated with progress
2. **Explore structure** → Navigate through the 16 modules
3. **Start with priority content**:
   - Module 11 (Tooling): uv, Ruff
   - Module 04 (CPython): Internals topics
   - Module 14 (PyO3): Introduction to PyO3

### Short Term (First Week)

1. **Choose a learning path** from the main README
2. **Start with the module that fits your level**:
   - Beginner → 01, 02, 03
   - Intermediate → 11, 04, 05
   - Expert → 14, 16, 07
3. **Complete the first topic** from start to finish
4. **Practice the workflow**: examples → exercises → solution → tests → commit

### Medium Term (First Month)

1. **Populate content** for topics you study:
   - Copy/adapt from official documentation
   - Add useful references you find
   - Write your personal analysis
2. **Create your own additional examples**
3. **Share feedback** if you find improvements
