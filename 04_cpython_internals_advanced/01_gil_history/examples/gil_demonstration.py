"""
Demostración avanzada del comportamiento del GIL en CPython.

Este script demuestra:
1. Contención del GIL en operaciones CPU-bound
2. Liberación del GIL en operaciones I/O-bound
3. Switching del GIL entre hilos
4. Impacto en rendimiento real
"""

import threading
import time
import sys
from collections import defaultdict
from typing import List, Dict
import math

class GILMonitor:
    """
    Monitorea el comportamiento aproximado del GIL rastreando
    qué hilos están ejecutando código Python.
    """
    
    def __init__(self):
        self.thread_times: Dict[str, float] = defaultdict(float)
        self.start_times: Dict[str, float] = {}
        self.lock = threading.Lock()
    
    def start_execution(self, thread_name: str):
        """Registra cuando un hilo comienza a ejecutar."""
        with self.lock:
            self.start_times[thread_name] = time.perf_counter()
    
    def end_execution(self, thread_name: str):
        """Registra cuando un hilo termina de ejecutar."""
        with self.lock:
            if thread_name in self.start_times:
                elapsed = time.perf_counter() - self.start_times[thread_name]
                self.thread_times[thread_name] += elapsed
                del self.start_times[thread_name]
    
    def get_report(self) -> str:
        """Genera un reporte de tiempo de ejecución por hilo."""
        total = sum(self.thread_times.values())
        report = ["\n" + "="*60]
        report.append("GIL EXECUTION TIME REPORT")
        report.append("="*60)
        
        for thread_name, exec_time in sorted(self.thread_times.items()):
            percentage = (exec_time / total * 100) if total > 0 else 0
            report.append(f"{thread_name:20} {exec_time:8.4f}s ({percentage:5.1f}%)")
        
        report.append("="*60)
        report.append(f"{'TOTAL':20} {total:8.4f}s")
        return "\n".join(report)


def cpu_intensive_work(iterations: int, monitor: GILMonitor):
    """
    Trabajo intensivo en CPU que mantiene el GIL.
    Calcula operaciones matemáticas complejas.
    """
    thread_name = threading.current_thread().name
    monitor.start_execution(thread_name)
    
    result = 0
    for i in range(iterations):
        # Operaciones CPU-intensive que mantienen el GIL
        result += math.sqrt(i) * math.sin(i) * math.cos(i)
        
        # Python hace gil switching cada ~5ms o cada ~100 instrucciones
        # de bytecode (check_interval en Python 2, switchinterval en Python 3)
        if i % 10000 == 0:
            # Forzar un checkpoint donde Python podría hacer gil switch
            pass
    
    monitor.end_execution(thread_name)
    return result


def io_intensive_work(duration: float, monitor: GILMonitor):
    """
    Trabajo intensivo en I/O que libera el GIL.
    Simula operaciones de red/disco.
    """
    thread_name = threading.current_thread().name
    monitor.start_execution(thread_name)
    
    # time.sleep() libera el GIL, permitiendo que otros hilos ejecuten
    time.sleep(duration)
    
    monitor.end_execution(thread_name)


def mixed_workload(cpu_iterations: int, io_duration: float, monitor: GILMonitor):
    """
    Workload mixto que alterna entre CPU e I/O.
    Demuestra el comportamiento de gil switching.
    """
    thread_name = threading.current_thread().name
    
    for _ in range(3):
        monitor.start_execution(thread_name)
        # CPU work
        result = sum(math.sqrt(i) for i in range(cpu_iterations))
        monitor.end_execution(thread_name)
        
        # I/O work (libera GIL)
        time.sleep(io_duration)
    
    return result


def run_cpu_bound_test(num_threads: int):
    """
    Test de operaciones CPU-bound con múltiples hilos.
    Demuestra que el GIL previene paralelismo real.
    """
    print(f"\n{'='*60}")
    print(f"CPU-BOUND TEST: {num_threads} thread(s)")
    print("="*60)
    
    monitor = GILMonitor()
    iterations = 500000
    
    start = time.perf_counter()
    
    threads: List[threading.Thread] = []
    for i in range(num_threads):
        t = threading.Thread(
            target=cpu_intensive_work,
            args=(iterations, monitor),
            name=f"CPU-Worker-{i+1}"
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end = time.perf_counter()
    elapsed = end - start
    
    print(f"Tiempo total: {elapsed:.4f}s")
    print(f"Tiempo esperado con paralelismo perfecto: {elapsed/num_threads:.4f}s")
    print(f"Speedup real: {1.0/(elapsed/(iterations*num_threads/500000)):.2f}x")
    print(monitor.get_report())


def run_io_bound_test(num_threads: int):
    """
    Test de operaciones I/O-bound con múltiples hilos.
    Demuestra que el GIL se libera durante I/O.
    """
    print(f"\n{'='*60}")
    print(f"I/O-BOUND TEST: {num_threads} thread(s)")
    print("="*60)
    
    monitor = GILMonitor()
    io_duration = 0.5
    
    start = time.perf_counter()
    
    threads: List[threading.Thread] = []
    for i in range(num_threads):
        t = threading.Thread(
            target=io_intensive_work,
            args=(io_duration, monitor),
            name=f"IO-Worker-{i+1}"
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end = time.perf_counter()
    elapsed = end - start
    
    print(f"Tiempo total: {elapsed:.4f}s")
    print(f"Tiempo esperado secuencial: {io_duration * num_threads:.4f}s")
    print(f"Speedup: {(io_duration * num_threads) / elapsed:.2f}x")
    print(monitor.get_report())


def run_mixed_test(num_threads: int):
    """
    Test de workload mixto (CPU + I/O).
    Muestra comportamiento real de aplicaciones.
    """
    print(f"\n{'='*60}")
    print(f"MIXED WORKLOAD TEST: {num_threads} thread(s)")
    print("="*60)
    
    monitor = GILMonitor()
    cpu_iterations = 100000
    io_duration = 0.1
    
    start = time.perf_counter()
    
    threads: List[threading.Thread] = []
    for i in range(num_threads):
        t = threading.Thread(
            target=mixed_workload,
            args=(cpu_iterations, io_duration, monitor),
            name=f"Mixed-Worker-{i+1}"
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end = time.perf_counter()
    elapsed = end - start
    
    print(f"Tiempo total: {elapsed:.4f}s")
    print(monitor.get_report())


def main():
    """
    Ejecuta batería completa de tests para demostrar el GIL.
    """
    print("="*60)
    print("DEMOSTRACIÓN DEL GLOBAL INTERPRETER LOCK (GIL)")
    print("="*60)
    print(f"Python version: {sys.version}")
    print(f"Thread switching interval: {sys.getswitchinterval()}s")
    
    # Check if free-threading is enabled (Python 3.13+)
    gil_status = "Enabled (Legacy)"
    if hasattr(sys, '_is_gil_enabled'):
        gil_status = "Disabled (Free-threaded)" if not sys._is_gil_enabled() else "Enabled"
    print(f"GIL Status: {gil_status}")
    
    # Test 1: CPU-bound with increasing threads
    print("\n" + "🔴 "*30)
    print("TEST 1: CPU-BOUND OPERATIONS")
    print("🔴 "*30)
    print("Hipótesis: Threading NO mejorará rendimiento debido al GIL")
    
    for num_threads in [1, 2, 4]:
        run_cpu_bound_test(num_threads)
    
    # Test 2: I/O-bound with increasing threads
    print("\n" + "🟢 "*30)
    print("TEST 2: I/O-BOUND OPERATIONS")
    print("🟢 "*30)
    print("Hipótesis: Threading SÍ mejorará rendimiento (GIL se libera)")
    
    for num_threads in [1, 2, 4]:
        run_io_bound_test(num_threads)
    
    # Test 3: Mixed workload
    print("\n" + "🟡 "*30)
    print("TEST 3: MIXED WORKLOAD")
    print("🟡 "*30)
    print("Hipótesis: Mejora parcial, dependiendo del ratio CPU/IO")
    
    for num_threads in [1, 2, 4]:
        run_mixed_test(num_threads)
    
    # Conclusiones
    print("\n" + "="*60)
    print("CONCLUSIONES")
    print("="*60)
    print("""
    1. CPU-bound: El GIL serializa la ejecución. No hay speedup real con threading.
       ➜ Solución: Usar multiprocessing o extensiones C que liberan el GIL.
    
    2. I/O-bound: El GIL se libera durante operaciones I/O. Threading es efectivo.
       ➜ Solución: Threading es apropiado. asyncio también es buena alternativa.
    
    3. Mixed: Comportamiento intermedio. Beneficio depende del ratio CPU/IO.
       ➜ Solución: Analizar el workload y elegir la mejor estrategia.
    
    4. Free-threading (Python 3.13+): Permite verdadero paralelismo CPU-bound.
       ➜ Requiere compilar Python con --disable-gil flag.
    """)


if __name__ == "__main__":
    main()
