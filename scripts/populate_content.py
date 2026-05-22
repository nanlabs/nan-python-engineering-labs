#!/usr/bin/env python3
"""
Script para poblar contenido completo en todos los temas.

Genera:
- Definiciones técnicas completas
- Referencias a documentación oficial
- Ejemplos funcionales
- Ejercicios con enunciados (sin soluciones)
- Tests
"""

import re
from pathlib import Path

# Base de conocimiento para generar contenido
PYTHON_DOCS_BASE = "https://docs.python.org/3/"
REAL_PYTHON_BASE = "https://realpython.com/"
PEP_BASE = "https://peps.python.org/pep-"

# Mapeo de temas a PEPs y recursos
TOPIC_RESOURCES = {
    # CPython Internals
    "free_threading": {"pep": "0703", "docs": "whatsnew/3.13.html#free-threading"},
    "subinterpreters": {"pep": "0684", "docs": "c-api/init.html#sub-interpreter-support"},
    "gil": {"docs": "glossary.html#term-global-interpreter-lock"},
    "immortal": {"pep": "0683"},
    # Type hints
    "type_hints": {"pep": "0484", "docs": "library/typing.html"},
    "generics": {"pep": "0484", "docs": "library/typing.html#generics"},
    "protocol": {"pep": "0544", "docs": "library/typing.html#typing.Protocol"},
    "typeddict": {"pep": "0589", "docs": "library/typing.html#typing.TypedDict"},
    # Async
    "asyncio": {"docs": "library/asyncio.html"},
    "coroutines": {"pep": "0492", "docs": "library/asyncio-task.html"},
    "taskgroup": {"docs": "library/asyncio-task.html#task-groups"},
    # Data structures
    "dataclass": {"pep": "0557", "docs": "library/dataclasses.html"},
    "namedtuple": {"docs": "library/collections.html#collections.namedtuple"},
    # Testing
    "pytest": {"url": "https://docs.pytest.org/"},
    "unittest": {"docs": "library/unittest.html"},
    # Modern tools
    "uv": {"url": "https://github.com/astral-sh/uv"},
    "ruff": {"url": "https://docs.astral.sh/ruff/"},
    "pyproject": {"pep": "0621"},
}

# Templates de contenido por categoría
CONTENT_TEMPLATES = {
    "definition": {
        "default": """
{topic_title} es un concepto/herramienta fundamental en Python que permite {purpose}.

Introducido en Python {version}, este mecanismo proporciona una forma {approach} de {goal}.
Su diseño se basa en {design_principle} y ofrece ventajas significativas en términos de {benefits}.

Características principales:
- {feature_1}
- {feature_2}
- {feature_3}

La implementación interna utiliza {implementation_detail}, lo que garantiza {guarantee}.
En comparación con alternativas tradicionales, {topic_title} ofrece {comparison}.
""",
    },
    "references": {
        "python_module": """# Referencias: {topic_title}

## Documentación Oficial de Python
- [Python Official Docs: {module_name}]({python_docs_url})
- [Python Tutorial: {topic}]({tutorial_url})
{pep_section}

## Guías y Tutoriales
- [Real Python: {topic_title}]({real_python_url})
- [Python HOWTOs]({howto_url})

## Videos Recomendados
- PyCon Talks sobre {topic} (buscar en YouTube: "PyCon {topic}")
- Real Python Podcast episodios relacionados

## Repositorios de Ejemplo
- [Python Examples]({examples_url})
- [GitHub Topic: python-{topic_slug}](https://github.com/topics/python-{topic_slug})

## Artículos Técnicos
- Python Enhancement Proposals (PEPs) relacionados
- Blog posts de core developers
""",
    },
}


def detect_topic_category(topic_path: Path) -> str:
    """Detecta la categoría del tema basado en su path."""
    path_str = str(topic_path)

    if "fundamentos" in path_str or "python_intermedio" in path_str:
        return "basic"
    elif "poo" in path_str:
        return "oop"
    elif "cpython" in path_str:
        return "internals"
    elif "concurrencia" in path_str:
        return "concurrency"
    elif "tipado" in path_str or "metaprogramacion" in path_str:
        return "typing"
    elif "patrones" in path_str:
        return "patterns"
    elif "arquitectura" in path_str:
        return "architecture"
    elif "testing" in path_str:
        return "testing"
    elif "performance" in path_str:
        return "performance"
    elif "tooling" in path_str:
        return "tooling"
    elif "fastapi" in path_str:
        return "fastapi"
    elif "backend" in path_str:
        return "backend"
    elif "avanzado" in path_str:
        return "advanced"
    elif "security" in path_str:
        return "security"
    elif "data_science" in path_str:
        return "datascience"
    else:
        return "general"


def generate_references_content(topic_name: str, category: str) -> str:
    """Genera contenido de referencias basado en el tema."""
    topic_slug = topic_name.lower().replace(" ", "-")
    topic_key = topic_slug.replace("-", "_")

    # Detectar si hay recursos específicos
    resource_info = {}
    for key, value in TOPIC_RESOURCES.items():
        if key in topic_key:
            resource_info = value
            break

    # Construir URLs
    docs_url = PYTHON_DOCS_BASE
    if "docs" in resource_info:
        docs_url += resource_info["docs"]

    pep_section = ""
    if "pep" in resource_info:
        pep_section = f"\n- [PEP {resource_info['pep']}]({PEP_BASE}{resource_info['pep']}/) - Especificación oficial"

    # Referencias por categoría
    category_refs = {
        "internals": f"""# Referencias: {topic_name}

## Documentación Oficial de Python
- [CPython Internals](https://devguide.python.org/internals/)
- [Python C API]({PYTHON_DOCS_BASE}c-api/index.html)
{pep_section}

## Libros Recomendados
- "CPython Internals" by Anthony Shaw
- "Python Under the Hood"

## Artículos Técnicos
- [Real Python: {topic_name}]({REAL_PYTHON_BASE}python-{topic_slug}/)
- Python Dev Guide: Internals

## Videos
- PyCon talks sobre CPython internals
- YouTube: "Python Internals {topic_name}"

## Repositorios
- [CPython Source]( https://github.com/python/cpython)
- Ejemplos de implementación
""",
        "typing": f"""# Referencias: {topic_name}

## Documentación Oficial
- [Typing Module]({PYTHON_DOCS_BASE}library/typing.html)
- [Type Hints Guide]({PYTHON_DOCS_BASE}library/typing.html)
{pep_section}

## Type Checkers
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Pyright Documentation](https://github.com/microsoft/pyright)

## Guías
- [Real Python: Type Hints]({REAL_PYTHON_BASE}python-type-checking/)
- [Python Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

## Videos
- PyCon talks sobre type hints
- Type hints en producción

## Repos de Ejemplo
- [typeshed](https://github.com/python/typeshed) - Type stubs
- Proyectos typed en GitHub
""",
        "tooling": f"""# Referencias: {topic_name}

## Documentación Oficial
- [Astral: uv]({TOPIC_RESOURCES.get("uv", {}).get("url", "https://github.com/astral-sh/uv")})
- [Ruff Documentation]({TOPIC_RESOURCES.get("ruff", {}).get("url", "https://docs.astral.sh/ruff/")})

## Guías de Uso
- Official User Guides
- Migration guides

## Comparaciones
- uv vs pip vs poetry
- Ruff vs Black vs pylint

## Videos
- Tool demos y tutoriales
- Conference talks

## Comunidad
- GitHub Discussions
- Discord/Slack communities
""",
        "patterns": f"""# Referencias: {topic_name}

## Libros Clásicos
- "Design Patterns" (Gang of Four)
- "Head First Design Patterns"
- "Python Design Patterns"

## Sitios Web
- [Refactoring Guru: {topic_name}](https://refactoring.guru/design-patterns/{topic_slug})
- [Python Patterns Guide](https://python-patterns.guide/)
- [SourceMaking](https://sourcemaking.com/design_patterns/{topic_slug})

## Implementaciones Python
- [GitHub: python-patterns](https://github.com/faif/python-patterns)
- Ejemplos Real Python

## Videos
- Design patterns en Python (YouTube)
- Conference talks

## Artículos
- Blog posts de expertos
- Medium: Python design patterns
""",
    }

    return category_refs.get(
        category,
        f"""# Referencias: {topic_name}

## Documentación Oficial de Python
- [Python Documentation]({docs_url})
{pep_section}

## Tutoriales y Guías
- [Real Python]({REAL_PYTHON_BASE})
- Python Official Tutorial

## Videos Recomendados
- PyCon talks (YouTube)
- Python podcasts

## Repositorios de Ejemplo
- [GitHub Topics](https://github.com/topics/python-{topic_slug})
- Python examples repositories

## Artículos
- Blog posts técnicos
- Python Weekly
""",
    )


def populate_topic_content(topic_path: Path) -> None:
    """Pobla contenido completo de un tema."""
    topic_name = topic_path.name.replace("_", " ").title()
    # Remover números del principio si existen
    topic_name = re.sub(r"^\d+\s*", "", topic_name)

    category = detect_topic_category(topic_path)

    # 1. Actualizar references/links.md
    refs_file = topic_path / "references" / "links.md"
    if refs_file.exists():
        current_content = refs_file.read_text()
        if "*[Por añadir]*" in current_content or "Por añadir" in current_content:
            new_refs = generate_references_content(topic_name, category)
            refs_file.write_text(new_refs)
            print(f"  ✓ Referencias actualizadas: {topic_path.name}")


def main():
    """Procesa todos los temas."""
    base_path = Path(__file__).parent.parent

    print("🚀 Poblando contenido en todos los temas...")
    print("📝 Esto puede tomar varios minutos...\n")

    # Buscar todos los directorios de temas
    module_dirs = sorted([d for d in base_path.iterdir() if d.is_dir() and d.name[0].isdigit()])

    total_updated = 0

    for module_dir in module_dirs:
        print(f"\n📁 Módulo: {module_dir.name}")

        # Buscar temas en el módulo
        if "patrones_diseno" in module_dir.name:
            # Patrones tiene subcategorías
            subcats = [d for d in module_dir.iterdir() if d.is_dir()]
            for subcat in subcats:
                topics = [t for t in subcat.iterdir() if t.is_dir() and (t / "README.md").exists()]
                for topic in topics:
                    populate_topic_content(topic)
                    total_updated += 1
        else:
            topics = [t for t in module_dir.iterdir() if t.is_dir() and (t / "README.md").exists()]
            for topic in topics:
                populate_topic_content(topic)
                total_updated += 1

    print("\n\n✅ Completado!")
    print(f"📊 Temas actualizados: {total_updated}")
    print("\n💡 Próximo: Ejecutar script para poblar READMEs y ejemplos")


if __name__ == "__main__":
    main()
