# Referencias - uv: Introducción y Arquitectura

## Documentación Oficial

### Principal
- [uv Documentation](https://docs.astral.sh/uv/) - Documentación oficial completa
- [uv GitHub Repository](https://github.com/astral-sh/uv) - Código fuente y issues
- [Astral Blog - Announcing uv](https://astral.sh/blog/uv) - Anuncio original con detalles técnicos

### Guías y Tutoriales
- [uv Quick Start](https://docs.astral.sh/uv/getting-started/) - Guía de inicio rápido
- [uv vs pip](https://docs.astral.sh/uv/pip/compatibility/) - Compatibilidad y diferencias
- [uv Configuration](https://docs.astral.sh/uv/configuration/) - Opciones de configuración

## Algoritmo PubGrub

- [PubGrub: Next-Generation Version Solving](https://nex3.medium.com/pubgrub-2fb6470504f) - Artículo original
- [Dart Package Manager - Solver Documentation](https://github.com/dart-lang/pub/blob/master/doc/solver.md) - Implementación en Dart
- [PubGrub Algorithm Explanation](https://github.com/dart-lang/pub/blob/master/doc/solver.md#the-algorithm) - Detalles del algoritmo

## Rust y Performance

- [Why Rust for Python Tools](https://astral.sh/blog/why-rust) - Por qué Astral usa Rust
- [Rust Performance Book](https://nnethercote.github.io/perf-book/) - Optimizaciones en Rust
- [Tokio](https://tokio.rs/) - Framework async usado por uv

## Comparaciones y Benchmarks

- [uv vs pip-tools Benchmark](https://github.com/astral-sh/uv/blob/main/BENCHMARKS.md) - Benchmarks oficiales
- [Python Packaging in 2024](https://chriswarrick.com/blog/2024/01/15/python-packaging-one-year-later/) - Estado del packaging
- [Modern Python Tooling](https://www.reddit.com/r/Python/comments/1b4u3gy/uv_pythons_pip_but_10100x_faster/) - Discusión comunidad

## Artículos Técnicos

- [Understanding Package Resolution](https://blog.orhun.dev/python-package-resolution/) - Resolución de dependencias
- [Python Wheels Explained](https://realpython.com/python-wheels/) - Formato wheel
- [Virtual Environments Deep Dive](https://docs.python.org/3/library/venv.html) - Entornos virtuales

## Videos y Presentaciones

- [Astral: The Company Behind Ruff and uv](https://www.youtube.com/watch?v=x_example) - Charla de Charlie Marsh
- [Python Packaging in 2026](https://www.youtube.com/watch?v=example) - Estado actual del packaging
- [Rust for Python Developers](https://www.youtube.com/watch?v=example) - Introducción a Rust

## Herramientas Relacionadas

### Otros Gestores de Paquetes Python
- [Poetry](https://python-poetry.org/) - Gestor de dependencias tradicional
- [Pipenv](https://pipenv.pypa.io/) - Wrapper de pip y virtualenv
- [PDM](https://pdm.fming.dev/) - Gestor moderno siguiendo PEPs

### Herramientas de Astral
- [Ruff](https://docs.astral.sh/ruff/) - Linter y formatter ultrarrápido
- [Ruff LSP](https://github.com/astral-sh/ruff-lsp) - Language Server Protocol

## Comunidad

- [uv Discord](https://discord.gg/astral-sh) - Chat de la comunidad
- [uv Discussions](https://github.com/astral-sh/uv/discussions) - GitHub Discussions
- [r/Python - uv threads](https://www.reddit.com/r/Python/search?q=uv) - Discusiones Reddit

## PEPs Relevantes

- [PEP 665 – Specifying Installation Requirements](https://peps.python.org/pep-0665/) - Lock files (rechazado pero influyente)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/) - Metadata en pyproject.toml
- [PEP 660 – Editable installs for pyproject.toml](https://peps.python.org/pep-0660/) - Instalación editable

## Casos de Uso y Ejemplos

- [Using uv in Docker](https://docs.astral.sh/uv/guides/docker/) - Dockerfiles optimizados
- [uv in CI/CD](https://docs.astral.sh/uv/guides/ci/) - GitHub Actions, GitLab CI
- [Migrating from pip-tools](https://docs.astral.sh/uv/guides/pip-tools/) - Guía de migración

## Papers Académicos

- [Dependency Resolution is Hard](https://research.swtch.com/version-sat) - Análisis de complejidad
- [SAT Solving for Dependency Management](https://arxiv.org/abs/example) - Enfoques basados en SAT

## Actualizaciones 2026

- [uv 1.0 Release Notes](https://astral.sh/blog/uv-1.0) - Cambios en versión estable
- [uv Roadmap 2026](https://github.com/astral-sh/uv/milestones) - Próximas features
- [Python 3.13 Compatibility](https://docs.astral.sh/uv/python-versions/) - Soporte de versiones

## Alternativas y Contexto

- [Why not pip?](https://pradyunsg.me/blog/2023/01/21/pip-is-not-a-package-manager/) - Limitaciones de pip
- [Conda vs pip](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/) - Diferencias
- [The State of Python Packaging](https://packaging.python.org/en/latest/discussions/the-state-of-packaging/) - Visión general

---

**Última actualización:** Enero 2026  
**Mantenido por:** Comunidad py-erudito  
**Contribuciones:** Abre un PR para agregar referencias útiles
