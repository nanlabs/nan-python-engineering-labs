#!/usr/bin/env python3
"""
Script para generar la estructura del Módulo 14: Python Avanzado 2026.
"""

from pathlib import Path

# 45 temas organizados
TEMAS_MODULO_14 = {
    "pyo3": [
        "01_pyo3_introduccion",
        "02_rust_toolchain_maturin",
        "03_primer_modulo_rust_python",
        "04_tipos_python_en_rust",
        "05_error_handling_pyresult",
        "06_conversiones_automaticas",
        "07_clases_python_en_rust",
        "08_metodos_pymethods",
        "09_properties_rust",
        "10_metodos_estaticos_clase",
        "11_operator_overloading",
        "12_python_modules",
        "13_gil_management",
        "14_shared_mutable_state",
        "15_async_rust_pyo3",
        "16_numpy_arrays_zerocopy",
        "17_callbacks_python_desde_rust",
        "18_performance_optimization",
        "19_parser_alto_rendimiento",
        "20_procesamiento_imagenes",
        "21_criptografia_hashing",
        "22_data_processing_paralelo",
    ],
    "ai_development": [
        "23_embeddings_vector_stores",
        "24_streaming_llm_responses",
        "25_structured_output_pydantic",
        "26_prompt_engineering_codigo",
        "27_function_calling_tools",
        "28_langchain_basics",
        "29_langchain_chains",
        "30_rag_retrieval_augmented",
        "31_memory_systems",
        "32_document_loaders",
        "33_text_splitters",
        "34_vector_stores_chromadb",
        "35_langgraph_intro",
        "36_graphs_vs_chains",
        "37_nodes_edges",
        "38_state_management",
        "39_conditional_routing",
        "40_human_in_loop",
        "41_react_pattern",
        "42_agent_executors",
        "43_multi_agent_systems",
        "44_testing_llm_systems",
        "45_cost_tracking",
    ],
    "devcontainers": [
        # Ya están en ai_development, solo referencia
    ],
}


def create_topic(base_path: Path, topic_name: str) -> None:
    """Crea estructura de un tema."""
    topic_path = base_path / topic_name
    topic_path.mkdir(parents=True, exist_ok=True)

    for folder in ["examples", "exercise", "tests", "references"]:
        (topic_path / folder).mkdir(exist_ok=True)

    # README básico
    display_name = (
        topic_name[3:].replace("_", " ").title()
        if topic_name[0].isdigit()
        else topic_name.replace("_", " ").title()
    )

    readme = f"""# {display_name}

⏱️ **Tiempo estimado: 2-3 horas**

## 1. 📚 Definición

*[Por completar: 200-300 palabras]*

## 2. 💡 Aplicación Práctica

### Casos de Uso
1.
2.
3.

### Código Ejemplo

```python
# TODO
```

## 3. 🤔 ¿Por Qué Es Importante?

*[Por completar]*

## 4. 🔗 Referencias

- [Documentación oficial]()
- *[Más referencias]*

## 5. ✏️ Tarea de Práctica

### Nivel Básico
*[Por completar]*

### Nivel Intermedio
*[Por completar]*

### Nivel Avanzado
*[Por completar]*

## 6. 📝 Summary

- Punto 1
- Punto 2
- Punto 3

## 7. 🧠 Mi Análisis Personal

> ✍️ Escribe aquí tu reflexión...
"""

    (topic_path / "README.md").write_text(readme)

    # references/links.md
    links = f"""# Referencias: {display_name}

## Documentación Oficial
- [PyO3 Guide](https://pyo3.rs/) (para temas PyO3)
- [LangChain Docs](https://python.langchain.com/) (para temas AI)

## Artículos
- *[Por añadir]*

## Videos
- *[Por añadir]*
"""

    (topic_path / "references" / "links.md").write_text(links)


def main():
    """Genera módulo 14."""
    base_path = Path(__file__).parent.parent / "14_python_avanzado_2026"
    base_path.mkdir(parents=True, exist_ok=True)

    print("🚀 Generando Módulo 14: Python Avanzado 2026...")
    print()

    # README del módulo
    readme_module = """# Módulo 14: Python Avanzado 2026 🚀

> PyO3, AI-Assisted Development, LangChain, Agentes Autónomos

## 📋 Descripción

Este módulo cubre las tecnologías más avanzadas y modernas de Python en 2026:
- **PyO3**: Extensiones Rust para Python (22 temas)
- **AI-Assisted Development**: LangChain, LangGraph, Agentes (23 temas)

## 🎯 Objetivos

- Crear extensiones Python en Rust con PyO3
- Integrar LLMs en aplicaciones Python
- Construir agentes autónomos con LangGraph
- Implementar RAG y memory systems

## 📚 Contenido (45 Temas)

### Grupo 1: PyO3 (22 temas)
Desde fundamentos hasta casos de uso reales de extensiones Rust.

### Grupo 2: AI-Assisted Development (23 temas)
LangChain, LangGraph, RAG, agentes autónomos.

## ⏱️ Tiempo Total

**60-75 horas**

## 🔗 Referencias

- [PyO3 Documentation](https://pyo3.rs/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
"""

    (base_path / "README.md").write_text(readme_module)

    # Crear todos los temas
    count = 0
    for category, topics in TEMAS_MODULO_14.items():
        if not topics:
            continue
        print(f"📁 Categoría: {category}")
        for topic in topics:
            create_topic(base_path, topic)
            count += 1
            if count % 10 == 0:
                print(f"  ✓ {count} temas creados...")

    print()
    print(f"✅ Módulo 14 generado: {count} temas")


if __name__ == "__main__":
    main()
