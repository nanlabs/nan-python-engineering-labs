# Python Engineering Labs

> Modular advanced Python learning system updated to the most modern technologies of 2026

---

## Quick Navigation Guide

This README serves two purposes:
1) **Entry hub** (to quickly understand how the training is structured), and
2) **Detail document** (all original technical content, further below).

If this is your first time here, follow this order:
- Learning Roadmap (Hub)
- Program Structure (Hub)
- Module Summary (Hub)
- Quick Start (Hub)
- Full Documentation (Hub)

---

## Learning Roadmap (Hub)

```text
PHASE 1: Foundation (4-6 weeks)
01_python_fundamentals → 02_intermediate_python → 03_basic_intermediate_oop

PHASE 2: Technical Core (6-8 weeks)
04_cpython_internals_advanced → 05_modern_concurrency → 06_typing_metaprogramming

PHASE 3: Software Engineering (8-10 weeks)
07_design_patterns → 08_application_architecture → 09_testing_qa → 10_performance_optimization

PHASE 4: Modern Stack 2026 (8-12 weeks)
11_modern_tooling_2026 → 12_fastapi_complete → 13_backend_ecosystem → 14_advanced_python_2026 → 15_basic_data_science → 16_modern_security
```

**Total estimated time:** 7-10 months, adaptable to your own pace.

---

## Program Structure (Hub)

```text
nan-python-engineering-labs/
├── 01...16_*/         → curriculum modules
├── scripts/           → automation tools (includes progress tracking)
├── GETTING_STARTED.md → step-by-step setup
├── STATUS.md          → global program status
├── pyproject.toml     → tooling/dependencies
└── README.md          → general map + full detail
```

Suggested flow per topic:

```text
topic README → examples → exercise → tests → reflection
```

---

## Module Summary (Hub)

| Module | What you learn |
|---|---|
| [01_python_fundamentals](01_python_fundamentals/) | Solid language foundation |
| [02_intermediate_python](02_intermediate_python/) | Flow, files, exceptions, generators |
| [03_basic_intermediate_oop](03_basic_intermediate_oop/) | Applicable object-oriented design |
| [04_cpython_internals_advanced](04_cpython_internals_advanced/) | Internals, GIL/free-threading, subinterpreters |
| [05_modern_concurrency](05_modern_concurrency/) | Threading, multiprocessing, modern asyncio |
| [06_typing_metaprogramming](06_typing_metaprogramming/) | Advanced typing and metaprogramming |
| [07_design_patterns](07_design_patterns/) | Patterns for robust design |
| [08_application_architecture](08_application_architecture/) | Modular and scalable architecture |
| [09_testing_qa](09_testing_qa/) | Professional testing and quality |
| [10_performance_optimization](10_performance_optimization/) | Practical profiling and optimization |
| [11_modern_tooling_2026](11_modern_tooling_2026/) | uv, Ruff, modern type checking |
| [12_fastapi_complete](12_fastapi_complete/) | Modern production-ready APIs |
| [13_backend_ecosystem](13_backend_ecosystem/) | Backend and infrastructure integration |
| [14_advanced_python_2026](14_advanced_python_2026/) | PyO3 and AI-assisted development |
| [15_basic_data_science](15_basic_data_science/) | Python data science fundamentals |
| [16_modern_security](16_modern_security/) | Modern software and supply chain security |

---

## Quick Start (Hub)

### 1) Essential documentation
- [GETTING_STARTED.md](GETTING_STARTED.md)
- [STATUS.md](STATUS.md)
- [README.md](README.md)

### 2) Quick setup
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
uv pip install -e ".[dev,profiling,ai,pyo3,security,data]"
pre-commit install
uv run scripts/progress.py
```

### 3) First module
```bash
cd 01_python_fundamentals
cat README.md
```

---

## Full Documentation (Hub)

- [GETTING_STARTED.md](GETTING_STARTED.md): installation and setup
- [STATUS.md](STATUS.md): progress tracking
- [scripts/progress.py](scripts/progress.py): automatic progress report
- [pyproject.toml](pyproject.toml): environment and tooling configuration

---

## Full Program Details

## Description

**Python Engineering Labs** is a structured self-learning project covering Python from fundamentals to advanced topics, including the latest 2026 innovations: free-threading without GIL (PEP 703), Rust-based tooling (uv, Ruff), PyO3 extensions, AI-assisted development, and modern security architecture.

### Features

- **200+ topics organized in 16 thematic modules** — independent and self-contained
- **No fixed calendar**: learn at your own pace
- **Pre-populated templates** with curated content
- **Progressive exercises** (basic → intermediate → advanced) with tests
- **88 design patterns** fully documented
- **Modern infrastructure**: DevContainers, pre-commit hooks, automatic tracking
- **Rust ecosystem**: uv, Ruff, PyO3
- **Python 3.13+**: free-threading, subinterpreters

## My Learning Progress

| Module | Completed | Total | Progress | Percentage |
|--------|-----------|-------|----------|------------|
| Python Fundamentals | 0 | 12 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Intermediate Python | 0 | 15 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Basic Intermediate OOP | 0 | 12 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| CPython Internals Advanced | 0 | 5 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Modern Concurrency | 0 | 25 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Typing Metaprogramming | 0 | 22 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Design Patterns | 0 | 88 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Application Architecture | 0 | 18 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Testing QA | 0 | 16 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Performance Optimization | 0 | 14 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Modern Tooling 2026 | 0 | 9 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| FastAPI Complete | 0 | 28 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Backend Ecosystem | 0 | 20 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Advanced Python 2026 | 0 | 45 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Basic Data Science | 0 | 10 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
| Modern Security | 0 | 40 | ░░░░░░░░░░░░░░░░░░░░ | 0.0% |
|--------|-----------|-------|----------|------------|
| **TOTAL** | **0** | **379** | ░░░░░░░░░░░░░░░░░░░░ | **0.0%** |

*Last updated: nan-python-engineering-labs*


## Module Structure

### Basic Level (Optional for those who already know Python)

#### [01 - Python Fundamentals](01_python_fundamentals/)
Variables, data types, control structures, built-in data structures, basic functions, comprehensions. Topics marked as `(optional)` for experienced programmers.

**Topics**: 12 | **Estimated time**: 15-20 hours

#### [02 - Intermediate Python](02_intermediate_python/)
Basic decorators, file handling, exceptions, iterators, generators, important standard modules.

**Topics**: 15 | **Estimated time**: 20-25 hours

#### [03 - Basic and Intermediate OOP](03_basic_intermediate_oop/)
Classes, inheritance, polymorphism, special methods, properties, descriptors, composition vs inheritance.

**Topics**: 12 | **Estimated time**: 18-22 hours

---

### Intermediate-Advanced Level

#### [04 - CPython Internals Advanced](04_cpython_internals_advanced/)
History of the GIL, **PEP 703 free-threading**, **PEP 684 subinterpreters**, thread-safety without GIL, object model, reference counting, migration strategies.

**Topics**: 27 | **Estimated time**: 40-50 hours

**Highlighted topics**:
- Free-threading Python 3.13+ (`--disable-gil` mode)
- Subinterpreters with per-interpreter GIL
- Thread-safety in modern Python code
- Biased reference counting
- Immortal objects (PEP 683)

#### [05 - Modern Concurrency and Parallelism](05_modern_concurrency/)
Threading with/without GIL, subinterpreters for isolation, multiprocessing with shared memory, advanced asyncio, concurrency patterns, concurrent testing.

**Topics**: 25 | **Estimated time**: 35-50 hours

#### [06 - Typing and Metaprogramming](06_typing_metaprogramming/)
Advanced type hints, Protocols, TypeVar, ParamSpec, metaclasses, descriptors, AST manipulation, import hooks.

**Topics**: 22 | **Estimated time**: 30-40 hours

---

### Patterns and Architecture

#### [07 - Design Patterns](07_design_patterns/)
88 design patterns organized in 8 subcategories: GoF basics, Pythonic, advanced GoF, architectural, distributed systems, concurrency, messaging, object management.

**Patterns**: 88 | **Estimated time**: 60-80 hours

#### [08 - Application Architecture](08_application_architecture/)
SOLID, DDD, hexagonal architecture, CQRS, Event-Driven, clean architecture with practical Python examples.

**Topics**: 18 | **Estimated time**: 25-35 hours

#### [09 - Testing and QA](09_testing_qa/)
pytest advanced, fixtures, mocking, hypothesis (property-based testing), mutation testing, performance testing.

**Topics**: 16 | **Estimated time**: 20-30 hours

#### [10 - Performance and Optimization](10_performance_optimization/)
Profiling (py-spy, memray, viztracer), algorithmic optimization, Cython, NumPy vectorization, strategic caching.

**Topics**: 14 | **Estimated time**: 20-28 hours

---

### Modern Stack 2026

#### [11 - Modern Tooling 2026](11_modern_tooling_2026/)
uv (Rust-based package manager), Ruff (linter/formatter), BasedPyright/Pylyzer, pre-commit automation, advanced pytest configuration.

**Topics**: 35 | **Estimated time**: 25-35 hours

#### [12 - FastAPI Complete](12_fastapi_complete/)
Complete FastAPI framework, JWT authentication, WebSockets, background tasks, deployment on Railway/Fly.io.

**Topics**: 28 | **Estimated time**: 40-56 hours

#### [13 - Backend Ecosystem](13_backend_ecosystem/)
SQLAlchemy 2.0, Redis, RabbitMQ, Kafka, gRPC, distributed observability, service mesh.

**Topics**: 20 | **Estimated time**: 28-40 hours

#### [14 - Advanced Python 2026](14_advanced_python_2026/)
PyO3 (Rust extensions) — 22 topics. AI-Assisted Development — 23 topics. LangChain, LangGraph, autonomous agents.

**Topics**: 45 | **Estimated time**: 45-60 hours

#### [15 - Basic Data Science](15_basic_data_science/)
NumPy, Pandas, Matplotlib, Polars, practical statistics for data engineering.

**Topics**: 10 | **Estimated time**: 15-20 hours

#### [16 - Modern Security](16_modern_security/)
Supply chain security, SBOM, Sigstore (keyless signing), SOPS/Vault (secrets management), runtime hardening.

**Topics**: 40 | **Estimated time**: 30-45 hours
