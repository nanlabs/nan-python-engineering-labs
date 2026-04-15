"""
Ejercicio Básico: Comparar pip vs uv en tu máquina

Objetivo: Instalar uv y medir el speedup en tu sistema.

TODO:
1. Instala uv:
   curl -LsSf https://astral.sh/uv/install.sh | sh

2. Crea un archivo requirements.txt con 10 paquetes:
   - requests
   - pandas
   - numpy
   - pytest
   - flask
   - (añade 5 más que uses comúnmente)

3. Implementa función measure_install_time() que:
   - Cree un venv temporal
   - Instale los paquetes
   - Mida el tiempo total
   - Limpie el venv

4. Ejecuta el benchmark con pip y con uv (sin cache)

5. Genera un reporte:
   - Tiempo pip: X segundos
   - Tiempo uv: Y segundos
   - Speedup: Z veces
   - Conclusión

Criterios de éxito:
- uv instalado correctamente (verifica con: uv --version)
- Benchmark ejecutado sin errores
- Speedup > 5x
- Reporte escrito en resultados.md
"""

def measure_install_time(tool: str, requirements_file: str) -> float:
    """
    Mide el tiempo de instalación de paquetes.
    
    Args:
        tool: "pip" o "uv"
        requirements_file: Path al archivo requirements.txt
    
    Returns:
        Tiempo en segundos
    """
    # TODO: Implementar
    pass

def generate_report(pip_time: float, uv_time: float) -> None:
    """
    Genera reporte markdown con resultados.
    
    Args:
        pip_time: Tiempo de pip en segundos
        uv_time: Tiempo de uv en segundos
    """
    # TODO: Implementar
    pass

if __name__ == "__main__":
    # TODO: Implementar lógica principal
    print("Ejercicio: Benchmark pip vs uv")
    print("Completa las funciones TODO arriba")
