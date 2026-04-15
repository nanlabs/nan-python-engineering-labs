"""
BASIC EXERCISE: Comparison Threading vs Multiprocessing

Objective:
Implementar un programa que encuentre números primos en un rango usando:
1. Ejecución secuencial
2. Threading (múltiples hilos)
3. Multiprocessing (múltiples procesos)

Medir y comparar el rendimiento de cada enfoque.

Tareas:
1. Implementar función is_prime(n) eficiente
2. Implementar función find_primes_in_range(start, end)
3. Ejecutar con 1, 2, 4, 8 workers para threading y multiprocessing
4. Medir tiempos de ejecución
5. Calcular y mostrar speedup
6. Crear gráfico de resultados (opcional: usar matplotlib)

Datos de prueba:
- Rango: 1,000,000 - 1,100,000
- Dividir en 4 chunks iguales

Criterios de éxito:
✅ is_prime() funciona correctamente para todos los casos
✅ Encuentra mismos primos en todos los enfoques
✅ Multiprocessing muestra speedup > 2x en CPU con 4+ cores
✅ Threading muestra speedup < 1.5x (limitado por GIL)
✅ Reporte claro con conclusiones

Tiempo estimado: 45-60 minutos
"""

import threading
import multiprocessing as mp
import time
from typing import List, Tuple
import math

def is_prime(n: int) -> bool:
    """
    TODO: Implementar función eficiente para verificar si n es primo.
    
    Pistas:
    - Números menores a 2 no son primos
    - Solo necesitas verificar hasta sqrt(n)
    - Optimización: verificar solo divisores impares después de 2
    
    Args:
        n: Número a verificar
        
    Returns:
        True si n es primo, False en caso contrario
    """
    pass  # TU CÓDIGO AQUÍ


def find_primes_in_range(start: int, end: int) -> List[int]:
    """
    TODO: Encontrar todos los números primos en el rango [start, end).
    
    Args:
        start: Inicio del rango (inclusivo)
        end: Fin del rango (exclusivo)
        
    Returns:
        Lista de números primos en el rango
    """
    pass  # TU CÓDIGO AQUÍ


def sequential_execution(ranges: List[Tuple[int, int]]) -> Tuple[List[int], float]:
    """
    TODO: Ejecutar búsqueda de primos secuencialmente.
    
    Args:
        ranges: Lista de tuplas (start, end) para buscar primos
        
    Returns:
        Tupla (lista_de_primos, tiempo_de_ejecución)
    """
    pass  # TU CÓDIGO AQUÍ


def threading_execution(ranges: List[Tuple[int, int]], num_threads: int) -> Tuple[List[int], float]:
    """
    TODO: Ejecutar búsqueda de primos usando threading.
    
    Pistas:
    - Crear un Thread por cada rango
    - Usar una lista compartida para resultados (con lock si es necesario)
    - Hacer join() de todos los threads antes de retornar
    
    Args:
        ranges: Lista de tuplas (start, end) para buscar primos
        num_threads: Número de threads a usar
        
    Returns:
        Tupla (lista_de_primos, tiempo_de_ejecución)
    """
    pass  # TU CÓDIGO AQUÍ


def multiprocessing_execution(ranges: List[Tuple[int, int]], num_processes: int) -> Tuple[List[int], float]:
    """
    TODO: Ejecutar búsqueda de primos usando multiprocessing.
    
    Pistas:
    - Usar multiprocessing.Pool
    - Usar pool.starmap() para pasar múltiples argumentos
    - No olvides cerrar y join el pool
    
    Args:
        ranges: Lista de tuplas (start, end) para buscar primos
        num_processes: Número de procesos a usar
        
    Returns:
        Tupla (lista_de_primos, tiempo_de_ejecución)
    """
    pass  # TU CÓDIGO AQUÍ


def main():
    """
    TODO: Implementar función principal que:
    1. Define el rango de búsqueda (1,000,000 - 1,100,000)
    2. Divide el rango en 4 chunks
    3. Ejecuta con secuencial, threading (1,2,4,8), multiprocessing (1,2,4,8)
    4. Muestra resultados en tabla formateada
    5. Calcula y muestra speedup
    6. Dibuja conclusiones
    """
    pass  # TU CÓDIGO AQUÍ


if __name__ == "__main__":
    # Necesario para Windows
    mp.freeze_support()
    main()


# SELF-VERIFICATION SECTION
# Descomenta para verificar tu implementación:

# def test_is_prime():
#     assert is_prime(2) == True
#     assert is_prime(3) == True
#     assert is_prime(4) == False
#     assert is_prime(17) == True
#     assert is_prime(100) == False
#     assert is_prime(1009) == True
#     print("✅ test_is_prime passed")

# def test_find_primes():
#     primes = find_primes_in_range(10, 20)
#     expected = [11, 13, 17, 19]
#     assert primes == expected, f"Expected {expected}, got {primes}"
#     print("✅ test_find_primes passed")

# if __name__ == "__main__":
#     test_is_prime()
#     test_find_primes()
#     main()
