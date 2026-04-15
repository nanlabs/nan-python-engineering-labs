"""
Comprehensive comparison: Threading (GIL) vs Multiprocessing.

Demuestra cuándo usar cada enfoque y los tradeoffs involucrados.
"""

import threading
import multiprocessing as mp
import time
import os
from typing import Callable, List
import sys

def fibonacci(n: int) -> int:
    """Cálculo recursivo de Fibonacci (CPU-intensive)."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def heavy_computation(numbers: List[int]) -> List[int]:
    """Simula computación pesada CPU-bound."""
    return [fibonacci(n) for n in numbers]

def benchmark_sequential(func: Callable, data_chunks: List[List[int]]) -> float:
    """Ejecuta función secuencialmente."""
    start = time.perf_counter()
    results = [func(chunk) for chunk in data_chunks]
    end = time.perf_counter()
    return end - start

def benchmark_threading(func: Callable, data_chunks: List[List[int]]) -> float:
    """Ejecuta función con threading (afectado por GIL)."""
    start = time.perf_counter()
    
    results = []
    threads = []
    
    def worker(chunk, index):
        result = func(chunk)
        results.append((index, result))
    
    for i, chunk in enumerate(data_chunks):
        t = threading.Thread(target=worker, args=(chunk, i))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end = time.perf_counter()
    return end - start

def benchmark_multiprocessing(func: Callable, data_chunks: List[List[int]]) -> float:
    """Ejecuta función con multiprocessing (sin GIL)."""
    start = time.perf_counter()
    
    with mp.Pool(processes=len(data_chunks)) as pool:
        results = pool.map(func, data_chunks)
    
    end = time.perf_counter()
    return end - start

def main():
    print("="*70)
    print("COMPARACIÓN: THREADING (GIL) VS MULTIPROCESSING")
    print("="*70)
    print(f"Python: {sys.version}")
    print(f"CPU cores: {mp.cpu_count()}")
    print(f"PID: {os.getpid()}")
    print("="*70)
    
    # Datos de prueba: calcular Fibonacci para estos números
    # Dividimos en chunks para paralelizar
    test_numbers = [30, 31, 32, 33]
    num_workers = 4
    data_chunks = [[n] for n in test_numbers]
    
    print(f"\nTarea: Calcular fibonacci({test_numbers})")
    print(f"Workers: {num_workers}")
    print("\n" + "-"*70)
    
    # Benchmark 1: Secuencial (baseline)
    print("\n1️⃣  EJECUCIÓN SECUENCIAL (Baseline)")
    print("-"*70)
    time_seq = benchmark_sequential(heavy_computation, data_chunks)
    print(f"   Tiempo: {time_seq:.4f}s")
    print(f"   Speedup: 1.00x (baseline)")
    
    # Benchmark 2: Threading
    print("\n2️⃣  THREADING (Afectado por GIL)")
    print("-"*70)
    time_threading = benchmark_threading(heavy_computation, data_chunks)
    speedup_threading = time_seq / time_threading
    print(f"   Tiempo: {time_threading:.4f}s")
    print(f"   Speedup: {speedup_threading:.2f}x")
    
    if speedup_threading < 1.2:
        print("   ❌ Sin mejora significativa - GIL serializa ejecución")
    else:
        print("   ⚠️  Mejora inesperada - puede ser variabilidad del sistema")
    
    # Benchmark 3: Multiprocessing
    print("\n3️⃣  MULTIPROCESSING (Sin GIL)")
    print("-"*70)
    time_mp = benchmark_multiprocessing(heavy_computation, data_chunks)
    speedup_mp = time_seq / time_mp
    print(f"   Tiempo: {time_mp:.4f}s")
    print(f"   Speedup: {speedup_mp:.2f}x")
    
    if speedup_mp > 2.0:
        print("   ✅ Paralelismo real efectivo")
    else:
        print("   ⚠️  Overhead de serialización/comunicación")
    
    # Análisis comparativo
    print("\n" + "="*70)
    print("ANÁLISIS COMPARATIVO")
    print("="*70)
    
    print(f"""
    Secuencial:        {time_seq:.4f}s (1.00x)
    Threading:         {time_threading:.4f}s ({speedup_threading:.2f}x)
    Multiprocessing:   {time_mp:.4f}s ({speedup_mp:.2f}x)
    
    Eficiencia de Threading:        {speedup_threading/num_workers*100:.1f}%
    Eficiencia de Multiprocessing:  {speedup_mp/num_workers*100:.1f}%
    
    🎯 RECOMENDACIÓN:
    """)
    
    if speedup_mp > speedup_threading * 1.5:
        print("""
    ✅ Para esta tarea CPU-bound, MULTIPROCESSING es claramente superior.
    
    El GIL previene que threading aproveche múltiples cores.
    Multiprocessing crea procesos separados, cada uno con su propio GIL.
    
    Tradeoffs:
    • Multiprocessing: Mayor overhead de memoria (procesos completos)
    • Multiprocessing: Serialización de datos (pickle)
    • Threading: Menor overhead, pero sin paralelismo real en CPU-bound
        """)
    else:
        print("""
    ⚠️  Los resultados son similares. Considerar:
    
    • El overhead de multiprocessing puede dominar en tareas pequeñas
    • For large CPU-bound tasks, multiprocessing should win
    • Para tareas I/O-bound, threading es suficiente y más eficiente
        """)
    
    # Cuándo usar cada uno
    print("\n" + "="*70)
    print("GUÍA DE DECISIÓN")
    print("="*70)
    print("""
    📊 USA THREADING cuando:
    • Operaciones I/O-bound (network, disk, database)
    • Necesitas compartir memoria entre workers fácilmente
    • Overhead de procesos es prohibitivo
    • Ejemplo: Web scraping, API calls, file I/O
    
    🚀 USA MULTIPROCESSING cuando:
    • Operaciones CPU-bound (cálculos, procesamiento de datos)
    • Necesitas verdadero paralelismo en múltiples cores
    • Los datos pueden serializarse eficientemente
    • Ejemplo: Image processing, data analysis, simulations
    
    ⚡ USA ASYNCIO cuando:
    • Muchas operaciones I/O concurrentes (1000s)
    • Event-driven architecture
    • Single-threaded pero altamente eficiente para I/O
    • Ejemplo: Chat servers, real-time apps, microservices
    
    🔥 USA EXTENSIONES NATIVAS cuando:
    • Necesitas máximo rendimiento
    • Bibliotecas como NumPy, TensorFlow liberan el GIL internamente
    • Ejemplo: Machine learning, scientific computing
    """)

if __name__ == "__main__":
    # Necesario para multiprocessing en Windows
    mp.freeze_support()
    main()
