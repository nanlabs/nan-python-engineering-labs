# Module 11: Modern Tooling 2026

This module covers the modern Python tooling ecosystem in 2026, focused on the fastest and most efficient tools written in Rust and current best practices.

## 🎯 Module Objectives

- Master **uv** as an ultra-fast package and environment manager
- Use **Ruff** as an all-in-one linter, formatter, and import sorter
- Implement modern type checking with **mypy, Pyright, and pylyzer**
- Configure quality workflows with **pre-commit**
- Apply advanced testing with **pytest, hypothesis, and mutmut**
- Use modern profiling tools: **py-spy, memray, viztracer**

## 📚 Module Structure

### Group 1: uv - Ultra-Fast Package Manager (9 topics)
1. [uv: Introduction and architecture](01_uv_introduction_architecture/)
2. [uv: installation and initial configuration](02_uv_installation_configuration/)
3. [uv pip: ultra-fast package installation](03_uv_pip_package_installation/)
4. [uv venv: Virtual environment management](04_uv_venv_virtual_environments/)
5. [uv tool: Global tools](05_uv_tool_global_tools/)
6. [uv in pyproject.toml](06_uv_pyproject_toml/)
7. [Lock files with uv (uv.lock)](07_uv_lock_files/)
8. [Workspaces and monorepos with uv](08_uv_workspaces_monorepos/)
9. [Scripts and entry points](09_uv_scripts_entry_points/)

### Group 2: Ruff - Ultra-Fast Linter and Formatter (8 topics)
10. [Ruff: Introduction and speed](10_ruff_introduction_speed/)
11. [Ruff as linter: available rules](11_ruff_linter_rules/)
12. [Ruff as formatter (Black replacement)](12_ruff_formatter_black/)
13. [Ruff as import sorter (isort replacement)](13_ruff_import_sorter_isort/)
14. [Configuration in pyproject.toml](14_ruff_pyproject_configuration/)
15. [Strict rules for production code](15_ruff_strict_rules/)
16. [Performance benchmarks](16_ruff_performance_benchmarks/)
17. [Workflow integration (pre-commit, CI/CD)](17_ruff_workflow_integration/)

### Group 3: Modern Type Checkers (6 topics)
18. [mypy: Current state in 2026](18_mypy_current_state_2026/)
19. [Pyright and BasedPyright](19_pyright_basedpyright/)
20. [Pylyzer: Type checker in Rust](20_pylyzer_type_checker_rust/)
21. [Comparison: mypy vs pyright vs pylyzer](21_comparacion_type_checkers/)
22. [Strict typing configuration](22_configuracion_tipado_estricto/)
23. [Type narrowing and advanced type guards](23_type_narrowing_guards_avanzados/)

### Group 4: Pre-commit and Hooks (3 topics)
24. [Pre-commit: Configuration and essential hooks](24_precommit_configuracion_hooks/)
25. [Security hooks: detect-secrets and bandit](25_precommit_hooks_seguridad/)
26. [Hook performance and caching](26_precommit_performance_caching/)

### Group 5: Modern Testing (5 topics)
27. [Advanced pytest: fixtures and parametrize](27_pytest_avanzado_fixtures/)
28. [pytest-cov and coverage analysis](28_pytest_cov_coverage/)
29. [pytest-xdist: test parallelization](29_pytest_xdist_paralelizacion/)
30. [Hypothesis: property-based testing](30_hypothesis_property_testing/)
31. [Mutation testing with mutmut](31_mutation_testing_mutmut/)

### Group 6: Modern Debugging and Profiling (4 topics)
32. [py-spy: profiling without overhead](32_pyspy_profiling_sin_overhead/)
33. [memray: modern memory profiling](33_memray_memory_profiling/)
34. [viztracer: visual tracing](34_viztracer_tracing_visual/)
35. [debugpy and remote debugging](35_debugpy_remote_debugging/)

## 🚀 Highlighted Tools 2026

### uv - The New Standard
- **10-100x faster** than pip and pip-tools
- Written in Rust by Astral (creators of Ruff)
- Compatible with pip but with modern architecture
- Unified management of packages, environments, and tools

### Ruff - The Universal Linter
- **10-100x faster** than pylint, flake8, black, isort
- Replaces multiple tools in one
- 800+ rules compatible with flake8, pylint, pycodestyle
- Perfect integration with editors and CI/CD

### Next-Generation Type Checkers
- **Pyright/BasedPyright**: Fast, precise, Microsoft/community
- **pylyzer**: Type checker in Rust, extremely fast
- **mypy**: Mature and stable, but slower

### Profiling Without Overhead
- **py-spy**: Sampling profiler without modifying code
- **memray**: Memory profiler with rich visualizations
- **viztracer**: Tracing with interactive visual timeline

## 📖 Learning Methodology

Each topic includes:
- **README.md**: Theory and concepts (200-300 words)
- **examples/**: Functional code and real use cases
- **exercises/**: Progressive exercises with clear instructions
- **my_solution/**: Space for your solutions
- **tests/**: Automated tests with pytest
- **references/**: Links to official 2026 documentation

## 🔗 Main References

- [uv Documentation](https://docs.astral.sh/uv/) - Astral
- [Ruff Documentation](https://docs.astral.sh/ruff/) - Astral
- [Pyright Documentation](https://microsoft.github.io/pyright/)
- [BasedPyright](https://docs.basedpyright.com/)
- [py-spy](https://github.com/benfred/py-spy)
- [memray](https://bloomberg.github.io/memray/)

## 💡 Why These Tools in 2026

The Python ecosystem has experienced a revolution with tools written in Rust that are **orders of magnitude faster** than their Python predecessors. This module focuses on the tools that have become the de facto standard in 2026:

- **uv** is replacing pip, pip-tools, poetry, virtualenv
- **Ruff** has replaced black, isort, flake8, pylint for many teams
- **Modern profilers** allow production analysis without impact
- **Type checking** is now instantaneous even in large projects

---

**Module updated January 2026** - State-of-the-art tools and practices.
