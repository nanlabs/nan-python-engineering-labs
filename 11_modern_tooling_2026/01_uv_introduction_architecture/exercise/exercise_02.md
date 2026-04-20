# Exercise 2: Deep Architecture

## Objective

Investigate and understand uv internal architecture and compare it with other tools.

## Parte 1: Análisis del Binario (20 min)

### Investigación del Binario

1. Encuentra la ubicación del binario de uv:

   ```bash
   which uv
   ```

1. Verify it is a compiled binary (not Python):

   ```bash
   file $(which uv)
   ```

1. Verify binary size:

   ```bash
   ls -lh $(which uv)
   ```

1. Compara con pip (que es Python):

   ```bash
   which pip
   file $(which pip)
   ```

## Part 2: Cache Exploration (25 min)

### Cache Structure

5. Explore the cache directory structure:

   ```bash
   tree -L 2 $(uv cache dir)
   # O si no tienes tree:
   find $(uv cache dir) -maxdepth 2 -type d
   ```

1. Identifica los diferentes tipos de artefactos cacheados:

   - wheels-v1/
   - built-wheels-v\*/
   - archive-v\*/
   - flat-index-v\*/

1. Inspecciona un wheel cacheado:

   ```bash
   # Encuentra un wheel
   find $(uv cache dir) -name "*.whl" | head -1
   # Descomprime y explora (los wheels son ZIPs)
   unzip -l <ruta-al-wheel>
   ```

## Part 3: Resolver Comparison (30 min)

### Create Complex Scenario

8. Create a `requirements.txt` file with complex dependencies:

   ```
   django>=4.0,<5.0
   celery>=5.0
   redis>=4.0
   pillow>=9.0
   psycopg2-binary>=2.9
   ```

1. Resolve with pip (without installing):

   ```bash
   mkdir /tmp/pip-resolve && cd /tmp/pip-resolve
   python3 -m venv .venv
   time .venv/bin/pip download -r requirements.txt --dry-run 2>&1 | tee pip-output.txt
   ```

1. Solve with uv:

   ```bash
   mkdir /tmp/uv-resolve && cd /tmp/uv-resolve
   uv venv
   time uv pip compile requirements.txt -o resolved.txt 2>&1 | tee uv-output.txt
   ```

1. Compara:

   - Resolution time
   - Claridad de mensajes
   - Order of resolved dependencies

## Parte 4: Implementción en Rust (25 min)

### Code Investigation

12. Clona el repositorio de uv (opcional):

    ```bash
    git clone https://github.com/astral-sh/uv /tmp/uv-repo
    cd /tmp/uv-repo
    ```

01. Explore the project structure:

    - ¿Qué crates (librerías Rust) se utilizan?
    - How is the code organized?

01. Lee sobre las optimizaciones:

    - Visita: https://astral.sh/blog/uv
    - Identifica 3 optimizaciones técnicas clave

## Tareas de Implementción

### Tarea 1: Script de Análisis de Caché

Implement en `my_solution/cache_analyzer.py`:

```python
"""
Analizador de caché de uv
It should show:
- Total cache size
- Number of cached packages
- Top 10 largest packages
- Antigüedad de artefactos
"""
```

### Tarea 2: Benchmark Automatizado

Implement en `my_solution/benchmark.py`:

```python
"""
Script que compara pip vs uv en diferentes escenarios:
- Installation from scratch
- Installation with cold cache
- Installation with warm cache
- Dependency resolution complejas
"""
```

### Task 3: Dependency Graph Visualizer

Implement en `my_solution/dep_graph.py`:

```python
"""
Visualize the uv resolution graph
Usa uv pip compile y parsea la salida
Genera un grafo con graphviz o similar
"""
```

## Advanced Questions

1. Why is Rust better than Python for a package manager?
1. ¿Qué trade-offs tiene el algoritmo PubGrub?
1. ¿Cómo maneja uv las plataformas cruzadas (wheels)?
1. ¿Qué estrategia usa uv para paralelizar descargas?
1. ¿Es posible que uv reemplace completamente a pip? ¿Por qué sí o no?

## Entregables

En `my_solution/`:

- `cache_analyzer.py` - Script funcional
- `benchmark.py` - Script funcional
- `dep_graph.py` - Script funcional
- `ANALISIS.md` - Documento con:
  - Resultados de comparaciones
  - Answers to advanced questions
  - uv architecture diagram
  - Conclusiones personales

## Evaluation Criteria

- ✅ Scripts implementdos y funcionales
- ✅ Análisis técnico profundo
- ✅ Comparaciones documentadas con evidencia
- ✅ Comprensión de trade-offs y limitaciones
- ✅ Propuestas de mejora o casos de uso
