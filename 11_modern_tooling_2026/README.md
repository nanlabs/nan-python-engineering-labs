# Module 11: Modern Tooling 2026

This module covers the modern Python tooling ecosystem in 2026, focused on the fastest and most efficient tools written in Rust y las mejores prácticas actuales.

## 🎯 Module Objectives

- Master **uv** como ultra-fast package and environment manager
- Use **Ruff** como linter, formatter y import sorter todo-en-uno
- Implement type checking moderno con **mypy, Pyright y pylyzer**
- Configure workflows de calidad con **pre-commit**
- Apply testing avanzado con **pytest, hypothesis y mutmut**
- Use herramientas modernas de profiling: **py-spy, memray, viztracer**

## 📚 Module Structure

### Group 1: uv - Ultra-Fast Package Manager (9 topics)
1. [uv: Introducción y arquitectura](01_uv_introduction_architecture/)
2. [uv: Instalación y configuración inicial](02_uv_installation_configuration/)
3. [uv pip: Instalación de paquetes ultrarrápida](03_uv_pip_package_installation/)
4. [uv venv: Gestión de entornos virtuales](04_uv_venv_virtual_environments/)
5. [uv tool: Herramientas globales](05_uv_tool_global_tools/)
6. [uv en pyproject.toml](06_uv_pyproject_toml/)
7. [Lock files con uv (uv.lock)](07_uv_lock_files/)
8. [Workspaces y monorepos con uv](08_uv_workspaces_monorepos/)
9. [Scripts y entry points](09_uv_scripts_entry_points/)

### Group 2: Ruff - Ultra-Fast Linter and Formatter (8 topics)
10. [Ruff: Introducción y velocidad](10_ruff_introduction_speed/)
11. [Ruff como linter: reglas disponibles](11_ruff_linter_rules/)
12. [Ruff como formatter (Black replacement)](12_ruff_formatter_black/)
13. [Ruff como import sorter (isort replacement)](13_ruff_import_sorter_isort/)
14. [Configuración en pyproject.toml](14_ruff_pyproject_configuration/)
15. [Reglas estrictas para código de producción](15_ruff_strict_rules/)
16. [Performance benchmarks](16_ruff_performance_benchmarks/)
17. [Integración en workflow (pre-commit, CI/CD)](17_ruff_workflow_integration/)

### Group 3: Modern Type Checkers (6 topics)
18. [mypy: Estado actual en 2026](18_mypy_current_state_2026/)
19. [Pyright y BasedPyright](19_pyright_basedpyright/)
20. [Pylyzer: Type checker en Rust](20_pylyzer_type_checker_rust/)
21. [Comparación: mypy vs pyright vs pylyzer](21_comparacion_type_checkers/)
22. [Configuración de tipado estricto](22_configuracion_tipado_estricto/)
23. [Type narrowing y type guards avanzados](23_type_narrowing_guards_avanzados/)

### Group 4: Pre-commit and Hooks (3 topics)
24. [Pre-commit: Configuration and essential hooks](24_precommit_configuracion_hooks/)
25. [Security hooks (detect-secrets, bandit)](25_precommit_hooks_seguridad/)
26. [Hook performance and caching](26_precommit_performance_caching/)

### Group 5: Modern Testing (5 topics)
27. [pytest avanzado: fixtures y parametrize](27_pytest_avanzado_fixtures/)
28. [pytest-cov y análisis de coverage](28_pytest_cov_coverage/)
29. [pytest-xdist: paralelización de tests](29_pytest_xdist_paralelizacion/)
30. [Hypothesis: property-based testing](30_hypothesis_property_testing/)
31. [Mutation testing con mutmut](31_mutation_testing_mutmut/)

### Group 6: Modern Debugging and Profiling (4 topics)
32. [py-spy: profiling sin overhead](32_pyspy_profiling_sin_overhead/)
33. [memray: memory profiling moderno](33_memray_memory_profiling/)
34. [viztracer: tracing visual](34_viztracer_tracing_visual/)
35. [debugpy y remote debugging](35_debugpy_remote_debugging/)

## 🚀 Highlighted Tools 2026

### uv - El Nuevo Estándar
- **10-100x más rápido** que pip y pip-tools
- Escrito en Rust por Astral (creadores de Ruff)
- Compatible con pip pero con arquitectura moderna
- Gestión unificada de paquetes, entornos y herramientas

### Ruff - El Linter Universal
- **10-100x más rápido** que pylint, flake8, black, isort
- Reemplaza múltiples herramientas en una
- 800+ reglas compatibles con flake8, pylint, pycodestyle
- Integración perfecta con editores y CI/CD

### Type Checkers de Nueva Generación
- **Pyright/BasedPyright**: Rápido, preciso, Microsoft/comunidad
- **pylyzer**: Type checker en Rust, extremadamente rápido
- **mypy**: Maduro y estable, pero más lento

### Profiling Sin Overhead
- **py-spy**: Sampling profiler sin modificar código
- **memray**: Memory profiler con visualizaciones ricas
- **viztracer**: Tracing con timeline visual interactivo

## 📖 Metodología de Aprendizaje

Cada tema incluye:
- **README.md**: Teoría y conceptos (200-300 palabras)
- **examples/**: Código funcional y casos de uso reales
- **exercises/**: Ejercicios progresivos con instrucciones claras
- **my_solution/**: Espacio para tus soluciones
- **tests/**: Tests automatizados con pytest
- **references/**: Enlaces a documentación oficial 2026

## 🔗 Referencias Principales

- [uv Documentation](https://docs.astral.sh/uv/) - Astral
- [Ruff Documentation](https://docs.astral.sh/ruff/) - Astral
- [Pyright Documentation](https://microsoft.github.io/pyright/)
- [BasedPyright](https://docs.basedpyright.com/)
- [py-spy](https://github.com/benfred/py-spy)
- [memray](https://bloomberg.github.io/memray/)

## 💡 Por Qué Estas Herramientas en 2026

El ecosistema Python ha experimentado una revolución con herramientas escritas en Rust que son **órdenes de magnitud más rápidas** que sus predecesoras en Python. Este módulo se centra en las herramientas que se han convertido en el estándar de facto en 2026:

- **uv** está reemplazando pip, pip-tools, poetry, virtualenv
- **Ruff** ha reemplazado black, isort, flake8, pylint para muchos equipos
- **Profilers modernos** permiten analizar producción sin impacto
- **Type checking** es ahora instantáneo incluso en proyectos grandes

---

**Módulo actualizado a Enero 2026** - Herramientas y prácticas del estado del arte actual.
