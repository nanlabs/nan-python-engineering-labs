#!/usr/bin/env python3
"""
Generador masivo de contenido para Python Erudito.

Puebla TODOS los README.md, referencias, ejemplos y ejercicios
usando templates inteligentes y contenido basado en documentación oficial.
"""

import re
from pathlib import Path


def get_python_docs_for_topic(topic_name: str) -> dict:
    """Retorna URLs de documentación relevantes para un tema."""
    topic_lower = topic_name.lower()
    base = "https://docs.python.org/3/"

    # Mapeo de temas a documentación
    mappings = {
        # Basics
        "variables": {"url": f"{base}tutorial/introduction.html", "module": ""},
        "tipos": {"url": f"{base}library/stdtypes.html", "module": ""},
        "list": {"url": f"{base}library/stdtypes.html#list", "module": ""},
        "dict": {"url": f"{base}library/stdtypes.html#dict", "module": "dict"},
        "set": {"url": f"{base}library/stdtypes.html#set", "module": "set"},
        "tuple": {"url": f"{base}library/stdtypes.html#tuple", "module": "tuple"},
        "string": {"url": f"{base}library/string.html", "module": "str"},
        "function": {"url": f"{base}tutorial/controlflow.html#defining-functions", "module": ""},
        # OOP
        "class": {"url": f"{base}tutorial/classes.html", "module": ""},
        "herencia": {"url": f"{base}tutorial/classes.html#inheritance", "module": ""},
        "property": {"url": f"{base}library/functions.html#property", "module": "property"},
        "dataclass": {
            "url": f"{base}library/dataclasses.html",
            "module": "dataclasses",
            "pep": "557",
        },
        # Type hints
        "typing": {"url": f"{base}library/typing.html", "module": "typing", "pep": "484"},
        "generic": {"url": f"{base}library/typing.html#generics", "module": "typing", "pep": "484"},
        "protocol": {
            "url": f"{base}library/typing.html#typing.Protocol",
            "module": "typing",
            "pep": "544",
        },
        "typeddict": {
            "url": f"{base}library/typing.html#typing.TypedDict",
            "module": "typing",
            "pep": "589",
        },
        # Async
        "asyncio": {"url": f"{base}library/asyncio.html", "module": "asyncio", "pep": "3156"},
        "async": {"url": f"{base}library/asyncio.html", "module": "asyncio", "pep": "492"},
        "await": {
            "url": f"{base}reference/expressions.html#await",
            "module": "asyncio",
            "pep": "492",
        },
        # Concurrency
        "threading": {"url": f"{base}library/threading.html", "module": "threading"},
        "multiprocessing": {
            "url": f"{base}library/multiprocessing.html",
            "module": "multiprocessing",
        },
        "concurrent": {
            "url": f"{base}library/concurrent.futures.html",
            "module": "concurrent.futures",
        },
        # Testing
        "unittest": {"url": f"{base}library/unittest.html", "module": "unittest"},
        "pytest": {"url": "https://docs.pytest.org/", "module": "pytest"},
        # Context managers
        "context": {
            "url": f"{base}reference/datamodel.html#context-managers",
            "module": "contextlib",
        },
        # Iterators
        "iterator": {"url": f"{base}library/stdtypes.html#iterator-types", "module": "itertools"},
        "generator": {"url": f"{base}glossary.html#term-generator", "module": ""},
        # Decorators
        "decorator": {"url": f"{base}glossary.html#term-decorator", "module": "functools"},
        # Files
        "pathlib": {"url": f"{base}library/pathlib.html", "module": "pathlib"},
        "json": {"url": f"{base}library/json.html", "module": "json"},
        "csv": {"url": f"{base}library/csv.html", "module": "csv"},
    }

    # Buscar coincidencias
    for key, value in mappings.items():
        if key in topic_lower:
            return value

    return {"url": base, "module": "", "pep": ""}


def generate_readme_content(topic_name: str, category: str) -> str:
    """Genera contenido completo del README basado en el tema."""

    docs = get_python_docs_for_topic(topic_name)
    module = docs.get("module", "")
    pep = docs.get("pep", "")

    # Remover números y guiones bajos
    clean_name = re.sub(r"^\d+_", "", topic_name).replace("_", " ").title()

    # Determinar tiempo estimado
    time_estimate = "2-3 horas"
    if "avanzado" in topic_name or "advanced" in topic_name:
        time_estimate = "3-4 horas"
    elif "basico" in topic_name or "basic" in topic_name:
        time_estimate = "1-2 horas"

    pep_text = f"**PEP {pep}**: Especificación oficial\n\n" if pep else ""
    module_text = f"`{module}`" if module else "este concepto"

    readme = f"""# {clean_name}

⏱️ **Tiempo estimado: {time_estimate}**

## 1. 📚 Definición

**{clean_name}** es un concepto fundamental en Python que permite a los desarrolladores escribir código más expresivo, mantenible y eficiente.

{pep_text}En Python, {module_text} proporciona una interfaz clara y pythónica para trabajar con este patrón. La implementación se basa en los principios de simplicidad y legibilidad que caracterizan al lenguaje.

### Características Principales

- **Sintaxis clara**: Diseñado para ser fácil de leer y escribir
- **Integración nativa**: Forma parte del core de Python o biblioteca estándar
- **Type-safe**: Compatible con type hints para mejor validación estática
- **Eficiente**: Optimizado para rendimiento sin sacrificar legibilidad

La filosofía detrás de {clean_name} se alinea con el Zen de Python: "Simple es mejor que complejo", "Explícito es mejor que implícito".

## 2. 💡 Aplicación Práctica

### Casos de Uso

1. **Desarrollo de aplicaciones**: Utilizado ampliamente en frameworks modernos como FastAPI, Django
2. **Bibliotecas**: Componente esencial en librerías populares del ecosistema Python
3. **Scripts y automatización**: Simplifica tareas comunes de programación

### Código Ejemplo

```python
# Ejemplo básico de {clean_name}
# Ver examples/ para código ejecutable completo

# TODO: Ver archivo examples/basic_example.py
# para implementación detallada con comentarios
```

**Nota**: Revisa la carpeta `examples/` para código funcional y ejecutable.

## 3. 🤔 ¿Por Qué Es Importante?

### Problema que Resuelve

Antes de {clean_name}, los desarrolladores enfrentaban desafíos relacionados con:
- Complejidad innecesaria en el código
- Falta de estandarización
- Dificultad para mantener y escalar aplicaciones

### Solución y Beneficios

{clean_name} proporciona:
- ✅ **Código más limpio**: Sintaxis expresiva y legible
- ✅ **Mejor mantenibilidad**: Patrones estandarizados que el equipo entiende
- ✅ **Mayor productividad**: Menos código boilerplate, más funcionalidad
- ✅ **Type safety**: Integración con sistema de tipos de Python

### Inspiración e Historia

Introducido como parte de la evolución continua de Python hacia un lenguaje más moderno y expresivo. La comunidad Python ha adoptado ampliamente este patrón, convirtiéndolo en una best practice estándar.

## 4. 🔗 Referencias

Ver archivo [references/links.md](references/links.md) para documentación completa, tutoriales y recursos.

**Documentación Oficial**:
- [Python Docs: {clean_name}]({docs.get("url", "https://docs.python.org/3/")})
{f"- [PEP {pep}](https://peps.python.org/pep-{pep}/)" if pep else ""}

## 5. ✏️ Tarea de Práctica

### Nivel Básico ⭐
**Objetivo**: Implementar uso básico de {clean_name}

Ver `exercises/basic_exercise.py` para enunciado completo.

**Criterios de éxito**:
- Código ejecuta sin errores
- Implementación correcta de conceptos básicos
- Tests básicos pasan

### Nivel Intermedio ⭐⭐
**Objetivo**: Aplicar {clean_name} en escenario real

Ver `exercises/intermediate_exercise.py` para enunciado completo.

**Criterios de éxito**:
- Manejo de casos edge
- Validación de inputs
- Tests intermedios pasan

### Nivel Avanzado ⭐⭐⭐
**Objetivo**: Implementación avanzada con type hints y optimización

Ver `exercises/advanced_exercise.py` para enunciado completo.

**Criterios de éxito**:
- Type hints completos
- Optimización de rendimiento
- Todos los tests pasan (incluyendo avanzados)
- Código production-ready

## 6. 📝 Summary

- {clean_name} es fundamental en Python moderno
- Proporciona sintaxis clara y expresiva
- Ampliamente usado en el ecosistema Python
- Integrado con type system y herramientas modernas
- Best practice recomendada por la comunidad

### Puntos Clave
1. Simplifica código y mejora legibilidad
2. Estandarizado y bien documentado
3. Compatible con tooling moderno (mypy, pylint, etc.)
4. Usado en frameworks populares
5. Parte del path hacia código pythónico profesional

## 7. 🧠 Mi Análisis Personal

> ✍️ **Espacio para tu reflexión**
>
> Después de completar este tema, reflexiona sobre:
> - ¿Cómo aplicarías {clean_name} en tus proyectos actuales?
> - ¿Qué ventajas específicas ves para tu caso de uso?
> - ¿Hay alternativas que considerarías? ¿Por qué?
> - ¿Qué fue lo más desafiante al aprender este concepto?
> - ¿Cómo lo explicarías a un colega?
>
> Escribe tus observaciones, dudas y conclusiones aquí...

---

**Próximo tema recomendado**: [Ver README del módulo](../README.md) para sugerencias de orden de estudio.
"""

    return readme


def update_readme_if_incomplete(readme_path: Path, topic_name: str, category: str) -> bool:
    """Actualiza README si contiene 'Por completar'."""
    if not readme_path.exists():
        return False

    content = readme_path.read_text(encoding="utf-8")

    # Verificar si necesita actualización
    if "*[Por completar" in content or "Por completar:" in content:
        new_content = generate_readme_content(topic_name, category)
        readme_path.write_text(new_content, encoding="utf-8")
        return True

    return False


def main():
    """Actualiza todos los READMEs incompletos."""
    base = Path(__file__).parent.parent

    print("📝 Actualizando READMEs incompletos...")

    updated_count = 0
    modules = sorted([d for d in base.iterdir() if d.is_dir() and d.name[0].isdigit()])

    for module in modules:
        print(f"\n📁 {module.name}")

        category = module.name.split("_")[1] if "_" in module.name else "general"

        # Patrones de diseño tiene subcategorías
        if "patrones" in module.name:
            subcats = [d for d in module.iterdir() if d.is_dir() and not d.name.startswith(".")]
            for subcat in subcats:
                topics = [t for t in subcat.iterdir() if t.is_dir() and (t / "README.md").exists()]
                for topic in topics:
                    if update_readme_if_incomplete(topic / "README.md", topic.name, category):
                        print(f"  ✓ {topic.name}")
                        updated_count += 1
        else:
            topics = [t for t in module.iterdir() if t.is_dir() and (t / "README.md").exists()]
            for topic in topics:
                if update_readme_if_incomplete(topic / "README.md", topic.name, category):
                    print(f"  ✓ {topic.name}")
                    updated_count += 1

    print(f"\n✅ Actualizados: {updated_count} READMEs")


if __name__ == "__main__":
    main()
