import os

# Plantilla base de README
readme_template = """# {title}

## Definición

{description}

## Aplicación Práctica

### Casos de Uso

1. **{use_case_1}**
2. **{use_case_2}**
3. **{use_case_3}**

### Código Ejemplo

```python
\"\"\"
Ejemplo: {title}

TODO: Expandir este ejemplo con implementación completa.
\"\"\"

def main():
    print("Implementación pendiente")

if __name__ == "__main__":
    main()
```

## ¿Por Qué Es Importante?

{importance}

## Referencias

### Documentación Oficial
- [Python 3.13 Documentation](https://docs.python.org/3.13/)
- [PEP 703 – Free-Threading](https://peps.python.org/pep-0703/)
- {specific_refs}

## Tarea de Práctica

### Nivel Básico
{basic_task}

### Nivel Intermedio
{intermediate_task}

### Nivel Avanzado
{advanced_task}

## Summary

- {summary_point_1}
- {summary_point_2}
- {summary_point_3}

## Estimated Time

⏱️ **{time_estimate}**

---

**Tema anterior**: [{prev_topic}](../{prev_folder}/)  
**Próximo tema**: [{next_topic}](../{next_folder}/)
"""

# Datos de cada tema (4-27)
topics_data = [
    {
        "folder": "04_free_threading_activation",
        "title": "Activación de free-threading (--disable-gil flag)",
        "description": "Guía práctica para compilar Python 3.13+ con el flag --disable-gil. Cubre proceso de compilación desde source, configuración de build options, testing de la instalación, y troubleshooting común.",
        "use_case_1": "Compilar Python free-threaded para development",
        "use_case_2": "Configurar virtual environments con free-threading",
        "use_case_3": "Testing y validation de instalación",
        "importance": "Dominar la compilación e instalación es el primer paso práctico para experimentar con free-threading. Sin una instalación correcta, no puedes aprovechar PEP 703.",
        "specific_refs": "[Building Python from Source](https://devguide.python.org/getting-started/setup-building/)",
        "basic_task": "Compile Python 3.13+ with --disable-gil. Verify with sys._is_gil_enabled(). Run the basic test suite.",
        "intermediate_task": "Crear script de instalación automatizada que compile Python free-threaded, configure venvs, e instale dependencies comunes.",
        "advanced_task": "Configurar CI/CD pipeline que teste código en ambos modos (GIL/no-GIL) automáticamente.",
        "summary_point_1": "🔧 Python 3.13+ se compila con --disable-gil flag durante ./configure",
        "summary_point_2": "✅ sys._is_gil_enabled() verifica si free-threading está activo",
        "summary_point_3": "⚠️ Requiere compilación desde source; binaries oficiales tienen GIL enabled por defecto",
        "time_estimate": "2-3 horas",
        "prev_topic": "03 - PEP 703: Free-Threading",
        "prev_folder": "03_pep_703_free_threading",
        "next_topic": "05 - Arquitectura interna sin GIL",
        "next_folder": "05_gil_free_architecture"
    },
    {
        "folder": "05_gil_free_architecture",
        "title": "Arquitectura interna sin GIL",
        "description": "Exploración profunda de los cambios arquitectónicos en CPython para soportar free-threading. Incluye: nuevas estructuras de datos thread-safe, per-object locking scheme, memory barriers, y coordinación entre threads sin GIL global.",
        "use_case_1": "Entender cómo CPython gestiona concurrencia sin GIL",
        "use_case_2": "Diseñar extensiones C compatibles con arquitectura no-GIL",
        "use_case_3": "Debugging de race conditions a nivel de intérprete",
        "importance": "Conocer la arquitectura interna es crucial para escribir código performante y thread-safe, y para contribuir al desarrollo de CPython o extensiones complejas.",
        "specific_refs": "[CPython Source: Include/internal/pycore_lock.h](https://github.com/python/cpython)",
        "basic_task": "Read Python source code in Python/ceval.c and Python/lock.c. Document differences vs the GIL-enabled version.",
        "intermediate_task": "Implement a 'mini-interpreter' that simulates per-object locking and demonstrates how multiple threads access objects safely.",
        "advanced_task": "Contribuir patch a CPython que mejore performance de algún aspecto del per-object locking scheme.",
        "summary_point_1": "🔓 Per-object locks reemplazan el GIL global",
        "summary_point_2": "🧵 Cada PyObject puede tener su propio mutex para protección granular",
        "summary_point_3": "⚡ Memory barriers y atomic operations aseguran correctness",
        "time_estimate": "4-5 horas",
        "prev_topic": "04 - Activación de free-threading",
        "prev_folder": "04_free_threading_activation",
        "next_topic": "06 - Biased reference counting",
        "next_folder": "06_biased_reference_counting"
    }
]

# Generar READMEs
for topic in topics_data:
    folder = topic["folder"]
    os.makedirs(folder, exist_ok=True)
    
    readme_content = readme_template.format(**topic)
    
    with open(f"{folder}/README.md", "w") as f:
        f.write(readme_content)
    
    print(f"✅ Created: {folder}/README.md")

print(f"\n✅ Generated {len(topics_data)} README templates")
