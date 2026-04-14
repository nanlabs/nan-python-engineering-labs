"""
EJERCICIO INTERMEDIO: GIL Contention Profiler

Objetivo:
Desarrollar una herramienta de profiling que analice la contención del GIL
entre múltiples hilos, mostrando métricas como tiempo de espera, fairness,
y utilización del GIL.

Tareas:
1. Crear decorador @profile_gil que rastree adquisición/liberación del GIL (simulado)
2. Implementar GILProfiler class con métricas de contención
3. Simular múltiples hilos compitiendo por el GIL
4. Visualizar contención mediante reporte detallado o gráfico
5. Comparar diferentes patrones: CPU-bound vs I/O-bound vs mixto

Métricas a calcular:
- Tiempo total de ejecución por hilo
- Tiempo de espera (contención) por hilo
- Utilización del GIL (% de tiempo con GIL adquirido)
- Fairness index (qué tan equitativamente se distribuye el GIL)
- Número de switches de GIL

Criterios de éxito:
✅ Decorador funciona correctamente con funciones multi-threaded
✅ Métricas son precisas y consistentes
✅ Detecta correctamente alta contención en CPU-bound
✅ Detecta baja contención en I/O-bound
✅ Reporte visual claro (tabla o gráfico)
✅ Cálculo de fairness index (ideal: ~1.0)

Tiempo estimado: 90-120 minutos
"""

import threading
import time
import functools
from typing import Callable, Dict, List
from dataclasses import dataclass, field
from collections import defaultdict
import sys

@dataclass
class ThreadStats:
    """Estadísticas de un hilo individual."""
    name: str
    execution_time: float = 0.0
    wait_time: float = 0.0
    gil_acquisitions: int = 0
    gil_releases: int = 0
    
    @property
    def total_time(self) -> float:
        return self.execution_time + self.wait_time
    
    @property
    def efficiency(self) -> float:
        """% de tiempo ejecutando vs esperando."""
        total = self.total_time
        return (self.execution_time / total * 100) if total > 0 else 0.0


class GILProfiler:
    """
    TODO: Implementar profiler de contención del GIL.
    
    El profiler simula el comportamiento del GIL rastreando cuándo
    cada hilo "adquiere" y "libera" el GIL.
    
    Métodos requeridos:
    - acquire_gil(thread_name: str): Registra adquisición del GIL
    - release_gil(thread_name: str): Registra liberación del GIL
    - get_stats() -> Dict[str, ThreadStats]: Retorna estadísticas por hilo
    - calculate_fairness() -> float: Calcula fairness index (Jain's fairness)
    - generate_report() -> str: Genera reporte formateado
    """
    
    def __init__(self):
        """TODO: Inicializar estructuras de datos."""
        # TU CÓDIGO AQUÍ
        pass
    
    def acquire_gil(self, thread_name: str):
        """
        TODO: Registrar que un hilo ha adquirido el GIL.
        
        - Si el GIL ya está tomado, el hilo debe esperar
        - Rastrear tiempo de espera
        - Incrementar contador de adquisiciones
        """
        pass  # TU CÓDIGO AQUÍ
    
    def release_gil(self, thread_name: str):
        """
        TODO: Registrar que un hilo ha liberado el GIL.
        
        - Calcular tiempo de ejecución
        - Incrementar contador de liberaciones
        - Permitir que otros hilos adquieran el GIL
        """
        pass  # TU CÓDIGO AQUÍ
    
    def get_stats(self) -> Dict[str, ThreadStats]:
        """TODO: Retornar estadísticas recopiladas."""
        pass  # TU CÓDIGO AQUÍ
    
    def calculate_fairness(self) -> float:
        """
        TODO: Calcular Jain's fairness index.
        
        Formula: (sum(x_i))^2 / (n * sum(x_i^2))
        donde x_i es el execution_time del hilo i
        
        Valor ideal: 1.0 (perfectamente fair)
        Valor peor caso: 1/n (un hilo monopoliza)
        """
        pass  # TU CÓDIGO AQUÍ
    
    def generate_report(self) -> str:
        """TODO: Generar reporte formateado con todas las métricas."""
        pass  # TU CÓDIGO AQUÍ


def profile_gil(profiler: GILProfiler):
    """
    TODO: Implementar decorador que profile funciones usando GILProfiler.
    
    El decorador debe:
    1. Adquirir el GIL antes de ejecutar la función
    2. Ejecutar la función
    3. Liberar el GIL después de la ejecución
    4. Manejar excepciones apropiadamente
    
    Uso:
        @profile_gil(profiler)
        def my_function():
            # código...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # TU CÓDIGO AQUÍ
            pass
        return wrapper
    return decorator


# Funciones de prueba para diferentes workloads

def cpu_intensive_task(duration: float, profiler: GILProfiler):
    """
    TODO: Implementar tarea CPU-intensive que usa el profiler.
    
    Debe:
    - Adquirir GIL al inicio
    - Realizar cálculos por 'duration' segundos
    - Liberar GIL al final
    - Simular gil switches periódicos (cada 0.005s)
    """
    pass  # TU CÓDIGO AQUÍ


def io_intensive_task(duration: float, profiler: GILProfiler):
    """
    TODO: Implementar tarea I/O-intensive que usa el profiler.
    
    Debe:
    - Adquirir GIL brevemente
    - Liberar GIL antes de time.sleep()
    - Simular operación I/O con sleep
    - Re-adquirir GIL después del sleep
    """
    pass  # TU CÓDIGO AQUÍ


def mixed_task(cpu_duration: float, io_duration: float, profiler: GILProfiler):
    """
    TODO: Implementar tarea mixta (CPU + I/O).
    
    Debe alternar entre CPU e I/O varias veces.
    """
    pass  # TU CÓDIGO AQUÍ


def run_workload_test(
    workload_name: str,
    task_func: Callable,
    task_args: tuple,
    num_threads: int,
    profiler: GILProfiler
):
    """
    TODO: Ejecutar test de workload y mostrar resultados.
    
    Args:
        workload_name: Nombre descriptivo del test
        task_func: Función a ejecutar en cada hilo
        task_args: Argumentos para task_func
        num_threads: Número de hilos
        profiler: Instancia de GILProfiler
    """
    pass  # TU CÓDIGO AQUÍ


def main():
    """
    TODO: Implementar función principal que ejecuta batería de tests.
    
    Tests a realizar:
    1. CPU-bound con 4 hilos (alta contención esperada)
    2. I/O-bound con 4 hilos (baja contención esperada)
    3. Mixed workload con 4 hilos (contención media)
    
    Para cada test:
    - Mostrar reporte de GILProfiler
    - Mostrar fairness index
    - Analizar resultados
    """
    pass  # TU CÓDIGO AQUÍ


if __name__ == "__main__":
    main()


# SECCIÓN DE AUTO-VERIFICACIÓN

def test_thread_stats():
    """TODO: Verificar cálculos de ThreadStats."""
    # Ejemplo:
    # stats = ThreadStats(name="test", execution_time=80, wait_time=20)
    # assert stats.total_time == 100
    # assert stats.efficiency == 80.0
    pass

def test_fairness_calculation():
    """TODO: Verificar cálculo de fairness."""
    # Caso ideal: todos los hilos tienen mismo execution_time
    # Caso peor: un hilo monopoliza
    pass

# Descomenta para ejecutar tests:
# if __name__ == "__main__":
#     test_thread_stats()
#     test_fairness_calculation()
#     main()
