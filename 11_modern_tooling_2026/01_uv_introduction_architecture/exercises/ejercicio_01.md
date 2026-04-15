# Exercise 1: Explorando uv

## Objective
Familiarizarse con los comandos básicos de uv y entender su arquitectura.

## Instructions

### Parte 1: Instalación y Verificación (10 min)

1. Verifica si uv está instalado:
   ```bash
   uv version
   ```

2. Si no está instalado, instálalo:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Verifica la ubicación de la caché:
   ```bash
   uv cache dir
   ```

4. Explora el contenido de la caché (si existe):
   ```bash
   ls -lh $(uv cache dir)
   ```

### Parte 2: Comparación de Velocidad (15 min)

5. Crea dos directorios de prueba:
   ```bash
   mkdir -p /tmp/test-pip /tmp/test-uv
   ```

6. Con pip tradicional:
   ```bash
   cd /tmp/test-pip
   time python3 -m venv .venv
   time .venv/bin/pip install requests beautifulsoup4 pandas
   ```

7. Con uv:
   ```bash
   cd /tmp/test-uv
   time uv venv
   time uv pip install requests beautifulsoup4 pandas
   ```

8. Compara los tiempos. ¿Cuánto más rápido es uv?

### Parte 3: Entendiendo la Caché (15 min)

9. Instala el mismo paquete en dos proyectos diferentes con uv:
   ```bash
   mkdir -p /tmp/project-a /tmp/project-b
   cd /tmp/project-a && uv venv && uv pip install flask==3.0.0
   cd /tmp/project-b && uv venv && uv pip install flask==3.0.0
   ```

10. Observa la salida de la segunda instalación. ¿Fue instantánea?

11. Revisa el tamaño de la caché:
    ```bash
    du -sh $(uv cache dir)
    ```

### Parte 4: Investigación (20 min)

12. Lee sobre el algoritmo PubGrub:
    - Visita: https://github.com/dart-lang/pub/blob/master/doc/solver.md
    - Resume en 3 puntos cómo difiere del backtracking

13. Experimenta con conflictos de dependencias:
    ```bash
    mkdir /tmp/conflict-test && cd /tmp/conflict-test
    uv venv
    # Intenta instalar versiones incompatibles
    uv pip install "requests==2.25.0" "urllib3==2.0.0"
    ```

14. Compara el mensaje de error de uv vs pip. ¿Cuál es más claro?

## Preguntas de Reflexión

1. ¿Por qué uv es más rápido que pip?
2. ¿Qué ventajas ofrece la caché global?
3. ¿En qué escenarios sería más beneficioso usar uv?
4. ¿Qué desventajas o riesgos podrías identificar?

## Entregables

Crea un archivo `RESPUESTAS.md` en `my_solution/` con:
- Capturas de tiempo de las comparaciones
- Respuestas a las preguntas de reflexión
- Un resumen de 3-5 líneas sobre PubGrub

## Criterios de Éxito

- ✅ uv instalado y funcionando
- ✅ Comparación de velocidad realizada y documentada
- ✅ Comprensión de la caché global
- ✅ Entendimiento básico de PubGrub
