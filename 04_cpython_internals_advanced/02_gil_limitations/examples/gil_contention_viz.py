"""
Ejemplo: Visualización de GIL Contention en diferentes escenarios.

Demuestra convoy effect, priority inversion, y otros problemas del GIL tradicional.
"""

import threading
import time
import sys
from dataclasses import dataclass
from typing import List
from collections import defaultdict

@dataclass
class GILEvent:
    """Registro de evento de adquisición/liberación de GIL."""
    timestamp: float
    thread_name: str
    event_type: str  # 'acquire' o 'release'
    wait_time: float = 0.0

class GILTracer:
    """
    Simula y rastrea eventos del GIL para visualizar contención.
    """
    
    def __init__(self):
        self.events: List[GILEvent] = []
        self.current_holder = None
        self.wait_start_times = {}
        self.lock = threading.Lock()
    
    def acquire(self, thread_name: str):
        """Simula adquisición del GIL."""
        wait_start = time.perf_counter()
        
        with self.lock:
            # Si alguien más tiene el GIL, debemos esperar
            while self.current_holder is not None:
                self.lock.release()
                time.sleep(0.001)  # Simular espera
                self.lock.acquire()
            
            wait_time = time.perf_counter() - wait_start
            self.current_holder = thread_name
            self.events.append(GILEvent(
                timestamp=time.perf_counter(),
                thread_name=thread_name,
                event_type='acquire',
                wait_time=wait_time
            ))
    
    def release(self, thread_name: str):
        """Simula liberación del GIL."""
        with self.lock:
            if self.current_holder == thread_name:
                self.current_holder = None
                self.events.append(GILEvent(
                    timestamp=time.perf_counter(),
                    thread_name=thread_name,
                    event_type='release'
                ))
    
    def generate_timeline_report(self) -> str:
        """Genera reporte ASCII de timeline de GIL."""
        if not self.events:
            return "No hay eventos registrados"
        
        # Agrupar por thread
        thread_events = defaultdict(list)
        for event in self.events:
            thread_events[event.thread_name].append(event)
        
        report = ["\nGIL TIMELINE"]
        report.append("="*70)
        report.append("Leyenda: [A]=Acquire, [R]=Release, [W]=Waiting\n")
        
        for thread_name in sorted(thread_events.keys()):
            events = thread_events[thread_name]
            report.append(f"{thread_name:15} ", end="")
            
            for event in events:
                if event.event_type == 'acquire':
                    if event.wait_time > 0.001:
                        report.append("[W]", end="")
                    report.append("[A]", end="")
                else:
                    report.append("[R] ", end="")
            
            report.append("")
        
        # Métricas
        report.append("\n" + "="*70)
        report.append("MÉTRICAS DE CONTENCIÓN")
        report.append("="*70)
        
        for thread_name in sorted(thread_events.keys()):
            events = thread_events[thread_name]
            total_wait = sum(e.wait_time for e in events if e.event_type == 'acquire')
            acquisitions = sum(1 for e in events if e.event_type == 'acquire')
            
            report.append(f"{thread_name:15} Acquires: {acquisitions:3d}  "
                         f"Total wait: {total_wait*1000:6.2f}ms  "
                         f"Avg wait: {total_wait/acquisitions*1000:5.2f}ms")
        
        return "\n".join(report)


def demo_convoy_effect():
    """Demostración de convoy effect con múltiples hilos CPU-bound."""
    print("\n🔴 CONVOY EFFECT DEMO")
    print("="*70)
    
    tracer = GILTracer()
    
    def cpu_worker(name: str, iterations: int):
        for _ in range(iterations):
            tracer.acquire(name)
            # Simular trabajo CPU
            _ = sum(range(1000))
            tracer.release(name)
    
    threads = []
    for i in range(6):
        t = threading.Thread(
            target=cpu_worker,
            args=(f"CPU-{i}", 10),
            daemon=True
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(tracer.generate_timeline_report())
    print("\n💡 Observa: Muchos [W] (waiting) indican convoy effect severo")


def demo_priority_inversion():
    """Demostración de priority inversion: I/O bloqueado por CPU."""
    print("\n🟡 PRIORITY INVERSION DEMO")
    print("="*70)
    
    tracer = GILTracer()
    response_times = []
    
    def io_worker():
        """Worker I/O que necesita baja latencia."""
        for i in range(5):
            start = time.perf_counter()
            
            # Simular I/O (libera GIL)
            time.sleep(0.01)
            
            # Necesita GIL para procesar
            tracer.acquire("IO-Worker")
            _ = sum(range(100))
            tracer.release("IO-Worker")
            
            response_times.append(time.perf_counter() - start)
    
    def cpu_hog():
        """Worker CPU que monopoliza GIL."""
        for _ in range(20):
            tracer.acquire("CPU-Hog")
            _ = sum(range(5000))
            tracer.release("CPU-Hog")
    
    # Ejecutar simultáneamente
    io_thread = threading.Thread(target=io_worker, daemon=True)
    cpu_thread = threading.Thread(target=cpu_hog, daemon=True)
    
    io_thread.start()
    time.sleep(0.005)  # Dar ventaja a I/O
    cpu_thread.start()
    
    io_thread.join()
    cpu_thread.join()
    
    print(tracer.generate_timeline_report())
    print(f"\nResponse times de I/O worker: {[f'{t*1000:.2f}ms' for t in response_times]}")
    print("💡 Observa: I/O worker sufre delays cuando CPU-Hog retiene el GIL")


def main():
    print("GIL CONTENTION VISUALIZATION")
    print("="*70)
    print(f"Python: {sys.version.split()[0]}")
    print(f"Switch interval: {sys.getswitchinterval()}s")
    
    demo_convoy_effect()
    time.sleep(1)
    demo_priority_inversion()


if __name__ == "__main__":
    main()
