#!/usr/bin/env python3
"""
Completa las descripciones de los READMEs principales de módulos.
"""

from pathlib import Path

MODULO_DESCRIPTIONS = {
    "01_fundamentos_python": """Este módulo cubre los fundamentos esenciales de Python, desde variables y tipos de datos hasta estructuras de control y manejo de archivos. Es el punto de partida perfecto para construir una base sólida en el lenguaje.

**Conceptos clave**: Variables, tipos de datos, estructuras de control, funciones, listas, diccionarios, manejo de archivos, importaciones y módulos.""",
    
    "02_python_intermedio": """Este módulo profundiza en conceptos intermedios de Python, incluyendo programación funcional, manejo avanzado de excepciones, decoradores y generadores. Aprenderás técnicas que usan los desarrolladores profesionales.

**Conceptos clave**: Decoradores, generadores, context managers, closures, itertools, collections, manejo de excepciones, expresiones regulares.""",
    
    "03_poo_basica_intermedia": """Domina la Programación Orientada a Objetos en Python. Desde clases básicas hasta herencia múltiple, properties, descriptores y dataclasses. Aprende a escribir código orientado a objetos pythónico y mantenible.

**Conceptos clave**: Clases y objetos, herencia, polimorfismo, encapsulación, métodos especiales, properties, descriptores, composición.""",
    
    "05_concurrencia_moderna": """Aprende a escribir código concurrente y paralelo en Python. Cubre asyncio, threading, multiprocessing, y las nuevas características de Python 3.13+ como free-threading y subinterpreters.

**Conceptos clave**: asyncio, coroutines, threading, multiprocessing, GIL, free-threading (PEP 703), subinterpreters, TaskGroups.""",
    
    "06_tipado_metaprogramacion": """Explora el sistema de tipado estático de Python y metaprogramación avanzada. Type hints, Protocols, metaclases, descriptores y manipulación de AST. Escribe código más robusto y expresivo.

**Conceptos clave**: Type hints, generics, Protocols, TypedDict, metaclases, descriptores, AST, mypy, Pyright.""",
    
    "08_arquitectura_aplicaciones": """Diseña aplicaciones escalables y mantenibles. Aprende principios SOLID, patrones arquitectónicos, DDD, CQRS, Event-Driven Architecture y prácticas profesionales de ingeniería de software.

**Conceptos clave**: SOLID, DDD, arquitectura hexagonal, repositories, CQRS, Event-Driven, dependency injection, observabilidad.""",
    
    "09_testing_qa": """Domina el testing en Python con pytest. Testing unitario, integración, mocks, fixtures, property-based testing con hypothesis, mutation testing y CI/CD.

**Conceptos clave**: pytest, fixtures, mocking, parametrize, coverage, hypothesis, mutation testing, TDD, integration testing.""",
    
    "10_performance_optimizacion": """Optimiza el rendimiento de tus aplicaciones Python. Profiling, benchmarking, técnicas de optimización, Cython, NumPy vectorization, caching y análisis de complejidad algorítmica.

**Conceptos clave**: Profiling (cProfile, py-spy), benchmarking, optimización de memoria, Cython, Numba JIT, vectorización, caching.""",
    
    "12_fastapi_completo": """Construye APIs modernas de alto rendimiento con FastAPI. Desde lo básico hasta deployment en producción, incluyendo autenticación, bases de datos, WebSockets, testing y best practices.

**Conceptos clave**: FastAPI, Pydantic, async endpoints, dependency injection, authentication (JWT, OAuth2), SQLAlchemy, testing, deployment.""",
    
    "13_ecosistema_backend": """Explora el ecosistema completo de backend en Python. Bases de datos (PostgreSQL, Redis), message brokers (RabbitMQ, Kafka), APIs (REST, GraphQL, gRPC), observabilidad y configuración.

**Conceptos clave**: SQLAlchemy 2.0, Redis, RabbitMQ, Kafka, gRPC, OpenTelemetry, Prometheus, structured logging, Celery.""",
    
    "15_data_science_basico": """Introducción a data science con Python. NumPy, Pandas, visualización con Matplotlib/Seaborn, análisis exploratorio, limpieza de datos y Polars como alternativa moderna.

**Conceptos clave**: NumPy arrays, Pandas DataFrames, Matplotlib, Seaborn, análisis exploratorio, limpieza de datos, Polars.""",
}


def update_module_readme(module_path: Path) -> bool:
    """Actualiza el README de un módulo con su descripción."""
    readme = module_path / "README.md"
    if not readme.exists():
        return False
    
    content = readme.read_text()
    if "Por completar" not in content:
        return False
    
    module_name = module_path.name
    if module_name in MODULO_DESCRIPTIONS:
        description = MODULO_DESCRIPTIONS[module_name]
        content = content.replace(
            "*[Por completar: Descripción general del módulo]*",
            description
        )
        readme.write_text(content)
        return True
    
    return False


def main():
    base = Path(".")
    updated = 0
    
    for module_dir in sorted(base.iterdir()):
        if module_dir.is_dir() and module_dir.name[0].isdigit():
            if update_module_readme(module_dir):
                updated += 1
                print(f"✓ {module_dir.name}/README.md")
    
    print(f"\n✅ {updated} módulos actualizados")


if __name__ == "__main__":
    main()
