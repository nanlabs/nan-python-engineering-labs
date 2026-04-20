#!/usr/bin/env python3
"""
Script para generar la estructura del Módulo 07: Patrones de Diseño (88 patrones).
"""

from pathlib import Path

# Definición de los 88 patrones organizados en 8 subcategorías
PATRONES = {
    "01_gof_basicos": {
        "description": "Patrones GoF Básicos",
        "patterns": [
            "singleton",
            "factory_method",
            "builder",
            "adapter",
            "decorator_pattern",
            "facade",
            "strategy",
            "observer",
            "template_method",
            "iterator",
            "command",
        ],
    },
    "02_pythonicos": {
        "description": "Patrones Pythónicos",
        "patterns": [
            "context_manager",
            "decorator_funcion",
            "property",
            "generator",
            "coroutine",
            "dataclass",
            "descriptor",
            "mixin",
            "protocol",
            "borg_monostate",
            "registry",
            "lazy_property",
            "sentinel",
            "plugin_system",
        ],
    },
    "03_gof_avanzados": {
        "description": "Patrones GoF Avanzados",
        "patterns": [
            "abstract_factory",
            "prototype",
            "bridge",
            "composite",
            "flyweight",
            "proxy",
            "chain_of_responsibility",
            "interpreter",
            "mediator",
            "memento",
            "state",
            "visitor",
        ],
    },
    "04_arquitectonicos": {
        "description": "Patrones Arquitectónicos",
        "patterns": [
            "repository",
            "unit_of_work",
            "service_layer",
            "dependency_injection",
            "domain_model",
            "data_mapper",
            "active_record",
            "hexagonal_architecture",
            "clean_architecture",
            "mvc",
            "mvp",
            "mvvm",
            "api_gateway",
        ],
    },
    "05_sistemas_distribuidos": {
        "description": "Patrones de Sistemas Distribuidos",
        "patterns": [
            "cqrs",
            "event_sourcing",
            "saga",
            "backend_for_frontend",
            "circuit_breaker",
            "retry_pattern",
            "timeout",
            "bulkhead",
            "rate_limiter",
            "cache_aside",
            "sidecar",
            "event_driven",
        ],
    },
    "06_concurrencia": {
        "description": "Patrones de Concurrencia",
        "patterns": [
            "thread_pool",
            "producer_consumer",
            "active_object",
            "monitor_object",
            "reactor",
            "proactor",
            "future_promise",
            "barrier_pattern",
            "read_write_lock",
            "thread_specific_storage",
            "half_sync_half_async",
            "leader_followers",
            "double_checked_locking",
            "scheduler",
        ],
    },
    "07_mensajeria": {
        "description": "Patrones de Mensajería",
        "patterns": [
            "message_queue",
            "publish_subscribe",
            "request_reply",
            "event_bus",
        ],
    },
    "08_gestion_objetos": {
        "description": "Patrones de Gestión de Objetos",
        "patterns": [
            "object_pool",
            "lazy_initialization",
            "eager_initialization",
            "multiton",
            "null_object",
            "value_object",
            "entity",
            "aggregate",
        ],
    },
}


def create_pattern_structure(base_path: Path, pattern_name: str) -> None:
    """Crea estructura de carpetas para un patrón."""
    pattern_path = base_path / pattern_name
    pattern_path.mkdir(parents=True, exist_ok=True)

    # Crear subcarpetas
    (pattern_path / "examples").mkdir(exist_ok=True)
    (pattern_path / "exercise").mkdir(exist_ok=True)
    (pattern_path / "tests").mkdir(exist_ok=True)
    (pattern_path / "references").mkdir(exist_ok=True)

    # Crear README
    pattern_display = pattern_name.replace("_", " ").title()
    readme_content = f"""# Patrón: {pattern_display}

⏱️ **Tiempo estimado: 2-3 horas**

## 1. 📚 Definición

*[Por completar: 200-300 palabras explicando el patrón]*

## 2. 💡 Aplicación Práctica

### Casos de Uso

1. **Caso 1**:
2. **Caso 2**:
3. **Caso 3**:

### Diagrama UML

```
[Por añadir diagrama UML del patrón]
```

### Código Ejemplo

```python
# TODO: Implementación del patrón
```

## 3. 🤔 ¿Por Qué Es Importante?

### Problema que Resuelve
*[Por completar]*

### Ventajas
-
-
-

### Desventajas
-
-

## 4. 🔗 Referencias

- [Design Patterns (Gang of Four)](https://refactoring.guru/design-patterns/{pattern_name.replace("_", "-")})
- [Python Design Patterns](https://python-patterns.guide/)
- *[Añadir más referencias]*

## 5. ✏️ Tarea de Práctica

### Nivel Básico
Implementa una versión simple del patrón {pattern_display}.

### Nivel Intermedio
Implementa el patrón con validaciones y manejo de errores.

### Nivel Avanzado
Implementa el patrón con type hints completos, tests, y documentación.

## 6. 📝 Summary

- Punto clave 1
- Punto clave 2
- Punto clave 3
- Cuándo usar este patrón
- Cuándo NO usar este patrón

## 7. 🧠 Mi Análisis Personal

> ✍️ **Espacio para tu reflexión**
>
> - ¿En qué proyectos aplicarías este patrón?
> - ¿Qué alternativas considerarías?
> - ¿Qué aprendiste al implementarlo?
"""

    (pattern_path / "README.md").write_text(readme_content)

    # Crear references/links.md
    links_content = f"""# Referencias: {pattern_display}

## Libros Clásicos
- Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four)
- Head First Design Patterns
- Python Design Patterns and Best Practices

## Sitios Web
- [Refactoring Guru](https://refactoring.guru/design-patterns/{pattern_name.replace("_", "-")})
- [Python Patterns Guide](https://python-patterns.guide/)
- [Source Making](https://sourcemaking.com/design_patterns/{pattern_name.replace("_", "-")})

## Videos
- *[Por añadir videos específicos del patrón]*

## Implementaciones de Ejemplo
- *[Por añadir repos GitHub con implementaciones reales]*
"""

    (pattern_path / "references" / "links.md").write_text(links_content)


def create_subcategory(base_path: Path, subcat_name: str, subcat_info: dict) -> None:
    """Crea subcategoría de patrones."""
    subcat_path = base_path / subcat_name
    subcat_path.mkdir(parents=True, exist_ok=True)

    print(f"📁 Creando subcategoría: {subcat_name}")

    # Crear README de subcategoría
    readme_content = f"""# {subcat_info["description"]}

## 📋 Descripción

Esta subcategoría contiene {len(subcat_info["patterns"])} patrones de diseño.

## 📚 Patrones

"""

    for i, pattern in enumerate(subcat_info["patterns"], 1):
        pattern_display = pattern.replace("_", " ").title()
        readme_content += f"{i}. [{pattern_display}]({pattern}/)\n"

    readme_content += f"""
## ⏱️ Tiempo Estimado Total

**{len(subcat_info["patterns"]) * 2}-{len(subcat_info["patterns"]) * 3} horas**
"""

    (subcat_path / "README.md").write_text(readme_content)

    # Crear cada patrón
    for pattern in subcat_info["patterns"]:
        create_pattern_structure(subcat_path, pattern)
        print(f"  ✓ {pattern}")


def main():
    """Genera estructura del módulo de patrones."""
    base_path = Path(__file__).parent.parent / "07_patrones_diseno"
    base_path.mkdir(parents=True, exist_ok=True)

    print("🎨 Generando Módulo 07: Patrones de Diseño...")
    print()

    # Crear README principal del módulo
    readme_content = """# Módulo 07: Patrones de Diseño Completos 🎨

> 88 patrones de diseño organizados en 8 subcategorías

## 📋 Descripción

Este módulo cubre todos los patrones de diseño relevantes para Python, desde los clásicos Gang of Four hasta patrones modernos de sistemas distribuidos y concurrencia. Cada patrón incluye teoría, ejemplos prácticos, y ejercicios progresivos.

## 🎯 Objetivos de Aprendizaje

- Dominar los 23 patrones clásicos GoF
- Aplicar patrones pythónicos idiomáticos
- Diseñar arquitecturas con patrones arquitectónicos
- Implementar sistemas distribuidos robustos
- Manejar concurrencia con patrones seguros

## 📚 Contenido (88 Patrones en 8 Subcategorías)

### 1. [Patrones GoF Básicos](01_gof_basicos/) (11 patrones)
Los patrones más fundamentales y ampliamente usados del Gang of Four.

### 2. [Patrones Pythónicos](02_pythonicos/) (14 patrones)
Patrones específicos de Python que aprovechan las características únicas del lenguaje.

### 3. [Patrones GoF Avanzados](03_gof_avanzados/) (12 patrones)
Patrones GoF más complejos para casos de uso especializados.

### 4. [Patrones Arquitectónicos](04_arquitectonicos/) (13 patrones)
Patrones para estructurar aplicaciones completas y sistemas grandes.

### 5. [Patrones de Sistemas Distribuidos](05_sistemas_distribuidos/) (12 patrones)
Patrones para microservicios, sistemas distribuidos y cloud-native.

### 6. [Patrones de Concurrencia](06_concurrencia/) (14 patrones)
Patrones para threading, multiprocessing y programación asíncrona.

### 7. [Patrones de Mensajería](07_mensajeria/) (4 patrones)
Patrones para comunicación asíncrona y event-driven systems.

### 8. [Patrones de Gestión de Objetos](08_gestion_objetos/) (8 patrones)
Patrones para lifecycle de objetos y optimización de recursos.

## ⏱️ Tiempo Estimado Total

**100-120 horas** (aproximadamente 1.5 horas por patrón)

## 🚀 Rutas de Aprendizaje

### Ruta Rápida (Must-Learn)
```
01_gof_basicos → 02_pythonicos (primeros 5) → 04_arquitectonicos (primeros 5)
```

### Ruta Backend
```
02_pythonicos → 04_arquitectonicos → 05_sistemas_distribuidos → 06_concurrencia
```

### Ruta Completa
Estudiar todas las subcategorías en orden numérico.

## 📖 Referencias Principales

- [Design Patterns (Gang of Four Book)](https://en.wikipedia.org/wiki/Design_Patterns)
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [Python Patterns Guide](https://python-patterns.guide/)
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)

---

*Este módulo representa una biblioteca completa de patrones de diseño para Python*
"""

    (base_path / "README.md").write_text(readme_content)

    # Crear cada subcategoría
    for subcat_name, subcat_info in PATRONES.items():
        create_subcategory(base_path, subcat_name, subcat_info)
        print()

    print("✅ Módulo 07 generado exitosamente!")
    print("📊 Total: 88 patrones en 8 subcategorías")


if __name__ == "__main__":
    main()
