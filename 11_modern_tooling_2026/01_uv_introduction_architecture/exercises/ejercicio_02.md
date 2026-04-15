# Ejercicio 2: Arquitectura Profunda

## Objetivo
Investigar y comprender la arquitectura interna de uv y compararla con otras herramientas.

## Parte 1: Análisis del Binario (20 min)

### Investigación del Binario

1. Encuentra la ubicación del binario de uv:
   ```bash
   which uv
   ```

2. Verifica que es un binario compilado (no Python):
   ```bash
   file $(which uv)
   ```

3. Verifica el tamaño del binario:
   ```bash
   ls -lh $(which uv)
   ```

4. Compara con pip (que es Python):
   ```bash
   which pip
   file $(which pip)
   ```

## Parte 2: Exploración de la Caché (25 min)

### Estructura de la Caché

5. Explora la estructura de directorios de la caché:
   ```bash
   tree -L 2 $(uv cache dir)
   # O si no tienes tree:
   find $(uv cache dir) -maxdepth 2 -type d
   ```

6. Identifica los diferentes tipos de artefactos cacheados:
   - wheels-v1/
   - built-wheels-v*/
   - archive-v*/
   - flat-index-v*/

7. Inspecciona un wheel cacheado:
   ```bash
   # Encuentra un wheel
   find $(uv cache dir) -name "*.whl" | head -1
   # Descomprime y explora (los wheels son ZIPs)
   unzip -l <ruta-al-wheel>
   ```

## Parte 3: Comparación de Resolvedores (30 min)

### Crear Escenario Complejo

8. Crea un archivo `requirements.txt` con dependencias complejas:
   ```
   django>=4.0,<5.0
   celery>=5.0
   redis>=4.0
   pillow>=9.0
   psycopg2-binary>=2.9
   ```

9. Resuelve con pip (sin instalar):
   ```bash
   mkdir /tmp/pip-resolve && cd /tmp/pip-resolve
   python3 -m venv .venv
   time .venv/bin/pip download -r requirements.txt --dry-run 2>&1 | tee pip-output.txt
   ```

10. Resuelve con uv:
    ```bash
    mkdir /tmp/uv-resolve && cd /tmp/uv-resolve
    uv venv
    time uv pip compile requirements.txt -o resolved.txt 2>&1 | tee uv-output.txt
    ```

11. Compara:
    - Tiempo de resolución
    - Claridad de mensajes
    - Orden de dependencias resueltas

## Parte 4: Implementación en Rust (25 min)

### Investigación de Código

12. Clona el repositorio de uv (opcional):
    ```bash
    git clone https://github.com/astral-sh/uv /tmp/uv-repo
    cd /tmp/uv-repo
    ```

13. Explora la estructura del proyecto:
    - ¿Qué crates (librerías Rust) se utilizan?
    - ¿Cómo está organizado el código?

14. Lee sobre las optimizaciones:
    - Visita: https://astral.sh/blog/uv
    - Identifica 3 optimizaciones técnicas clave

## Tareas de Implementación

### Tarea 1: Script de Análisis de Caché

Implementa en `my_solution/cache_analyzer.py`:

```python
"""
Analizador de caché de uv
Debe mostrar:
- Tamaño total de la caché
- Número de paquetes cacheados
- Top 10 paquetes más grandes
- Antigüedad de artefactos
"""
```

### Tarea 2: Benchmark Automatizado

Implementa en `my_solution/benchmark.py`:

```python
"""
Script que compara pip vs uv en diferentes escenarios:
- Instalación desde cero
- Instalación con caché fría
- Instalación con caché caliente
- Resolución de dependencias complejas
"""
```

### Tarea 3: Visualizador de Grafo de Dependencias

Implementa en `my_solution/dep_graph.py`:

```python
"""
Visualiza el grafo de resolución de uv
Usa uv pip compile y parsea la salida
Genera un grafo con graphviz o similar
"""
```

## Preguntas Avanzadas

1. ¿Por qué Rust es mejor que Python para un gestor de paquetes?
2. ¿Qué trade-offs tiene el algoritmo PubGrub?
3. ¿Cómo maneja uv las plataformas cruzadas (wheels)?
4. ¿Qué estrategia usa uv para paralelizar descargas?
5. ¿Es posible que uv reemplace completamente a pip? ¿Por qué sí o no?

## Entregables

En `my_solution/`:
- `cache_analyzer.py` - Script funcional
- `benchmark.py` - Script funcional
- `dep_graph.py` - Script funcional
- `ANALISIS.md` - Documento con:
  - Resultados de comparaciones
  - Respuestas a preguntas avanzadas
  - Diagrama de arquitectura de uv
  - Conclusiones personales

## Criterios de Evaluación

- ✅ Scripts implementados y funcionales
- ✅ Análisis técnico profundo
- ✅ Comparaciones documentadas con evidencia
- ✅ Comprensión de trade-offs y limitaciones
- ✅ Propuestas de mejora o casos de uso
