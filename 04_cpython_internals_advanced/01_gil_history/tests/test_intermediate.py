"""
Tests para el ejercicio intermedio: GIL Contention Profiler

Ejecutar con: pytest test_intermediate.py -v
"""

import pytest
import threading
import time
from typing import Dict

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from exercises.intermediate_exercise import (
    ThreadStats,
    GILProfiler,
    profile_gil,
    cpu_intensive_task,
    io_intensive_task,
    mixed_task
)


class TestThreadStats:
    """Tests para ThreadStats dataclass."""
    
    def test_total_time(self):
        """Verificar cálculo de total_time."""
        stats = ThreadStats(name="test", execution_time=80.0, wait_time=20.0)
        assert stats.total_time == 100.0
    
    def test_efficiency(self):
        """Verificar cálculo de efficiency."""
        stats = ThreadStats(name="test", execution_time=80.0, wait_time=20.0)
        assert stats.efficiency == 80.0
        
        stats2 = ThreadStats(name="test2", execution_time=50.0, wait_time=50.0)
        assert stats2.efficiency == 50.0
    
    def test_efficiency_zero_division(self):
        """Verificar que efficiency maneja división por cero."""
        stats = ThreadStats(name="test", execution_time=0.0, wait_time=0.0)
        assert stats.efficiency == 0.0


class TestGILProfiler:
    """Tests para GILProfiler class."""
    
    def test_initialization(self):
        """Verificar inicialización correcta."""
        profiler = GILProfiler()
        assert profiler is not None
        assert profiler.get_stats() is not None
    
    def test_single_thread_acquisition(self):
        """Test con un solo hilo adquiriendo el GIL."""
        profiler = GILProfiler()
        
        profiler.acquire_gil("Thread-1")
        time.sleep(0.1)
        profiler.release_gil("Thread-1")
        
        stats = profiler.get_stats()
        assert "Thread-1" in stats
        assert stats["Thread-1"].gil_acquisitions == 1
        assert stats["Thread-1"].gil_releases == 1
        assert stats["Thread-1"].execution_time > 0
    
    def test_multiple_threads_contention(self):
        """Test con múltiples hilos compitiendo por el GIL."""
        profiler = GILProfiler()
        
        def worker(thread_name: str):
            for _ in range(3):
                profiler.acquire_gil(thread_name)
                time.sleep(0.05)
                profiler.release_gil(thread_name)
        
        threads = []
        for i in range(3):
            t = threading.Thread(target=worker, args=(f"Thread-{i}",))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        stats = profiler.get_stats()
        
        # Verificar que todos los hilos tienen estadísticas
        assert len(stats) == 3
        
        # Verificar que cada hilo hizo 3 adquisiciones/liberaciones
        for thread_name in ["Thread-0", "Thread-1", "Thread-2"]:
            assert stats[thread_name].gil_acquisitions == 3
            assert stats[thread_name].gil_releases == 3
    
    def test_fairness_calculation(self):
        """Verificar cálculo de fairness index."""
        profiler = GILProfiler()
        
        # Simular ejecución perfectamente fair (todos ejecutan igual tiempo)
        for i in range(4):
            thread_name = f"Thread-{i}"
            profiler.acquire_gil(thread_name)
            time.sleep(0.1)
            profiler.release_gil(thread_name)
        
        fairness = profiler.calculate_fairness()
        
        # Fairness debe estar cerca de 1.0 (perfectamente fair)
        assert 0.95 <= fairness <= 1.0
    
    def test_unfair_execution(self):
        """Verificar detección de ejecución injusta."""
        profiler = GILProfiler()
        
        # Thread-0 ejecuta mucho más que los demás
        profiler.acquire_gil("Thread-0")
        time.sleep(0.4)
        profiler.release_gil("Thread-0")
        
        for i in range(1, 4):
            profiler.acquire_gil(f"Thread-{i}")
            time.sleep(0.05)
            profiler.release_gil(f"Thread-{i}")
        
        fairness = profiler.calculate_fairness()
        
        # Fairness debe ser bajo (< 0.8)
        assert fairness < 0.8
    
    def test_generate_report(self):
        """Verificar generación de reporte."""
        profiler = GILProfiler()
        
        profiler.acquire_gil("Thread-1")
        time.sleep(0.1)
        profiler.release_gil("Thread-1")
        
        report = profiler.generate_report()
        
        assert isinstance(report, str)
        assert "Thread-1" in report
        assert "Fairness" in report or "fairness" in report


class TestProfileGilDecorator:
    """Tests para el decorador @profile_gil."""
    
    def test_decorator_basic(self):
        """Verificar funcionamiento básico del decorador."""
        profiler = GILProfiler()
        
        @profile_gil(profiler)
        def test_func():
            time.sleep(0.1)
            return 42
        
        result = test_func()
        assert result == 42
        
        stats = profiler.get_stats()
        assert len(stats) > 0
    
    def test_decorator_with_exception(self):
        """Verificar que el decorador maneja excepciones correctamente."""
        profiler = GILProfiler()
        
        @profile_gil(profiler)
        def failing_func():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError):
            failing_func()
        
        # El GIL debe haberse liberado incluso con excepción
        # (verificar que no queda en estado inconsistente)


class TestWorkloadTasks:
    """Tests para las funciones de workload."""
    
    def test_cpu_intensive_task(self):
        """Verificar tarea CPU-intensive."""
        profiler = GILProfiler()
        
        cpu_intensive_task(0.2, profiler)
        
        stats = profiler.get_stats()
        thread_name = threading.current_thread().name
        
        assert thread_name in stats
        assert stats[thread_name].execution_time > 0
    
    def test_io_intensive_task(self):
        """Verificar tarea I/O-intensive."""
        profiler = GILProfiler()
        
        io_intensive_task(0.2, profiler)
        
        stats = profiler.get_stats()
        # I/O task debe liberar el GIL, así que execution_time debe ser bajo
        # comparado con el tiempo total
    
    def test_mixed_task(self):
        """Verificar tarea mixta."""
        profiler = GILProfiler()
        
        mixed_task(0.1, 0.1, profiler)
        
        stats = profiler.get_stats()
        assert len(stats) > 0


class TestContention:
    """Tests de contención del GIL."""
    
    def test_high_contention_cpu_bound(self):
        """Verificar alta contención en workload CPU-bound."""
        profiler = GILProfiler()
        
        def worker():
            cpu_intensive_task(0.2, profiler)
        
        threads = []
        for i in range(4):
            t = threading.Thread(target=worker, name=f"CPU-Worker-{i}")
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        stats = profiler.get_stats()
        
        # En CPU-bound, esperamos alto wait_time
        total_wait = sum(s.wait_time for s in stats.values())
        total_exec = sum(s.execution_time for s in stats.values())
        
        # Wait time debe ser significativo
        assert total_wait > total_exec * 0.1  # Al menos 10% del exec time
    
    def test_low_contention_io_bound(self):
        """Verificar baja contención en workload I/O-bound."""
        profiler = GILProfiler()
        
        def worker():
            io_intensive_task(0.2, profiler)
        
        threads = []
        for i in range(4):
            t = threading.Thread(target=worker, name=f"IO-Worker-{i}")
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        stats = profiler.get_stats()
        
        # En I/O-bound, esperamos bajo wait_time
        # (porque el GIL se libera durante I/O)
        fairness = profiler.calculate_fairness()
        
        # Fairness debe ser alta en I/O-bound
        assert fairness > 0.7


class TestConcurrentAccess:
    """Tests de acceso concurrente al profiler."""
    
    def test_thread_safety(self):
        """Verificar que el profiler es thread-safe."""
        profiler = GILProfiler()
        
        def worker(thread_id: int):
            for _ in range(100):
                profiler.acquire_gil(f"Thread-{thread_id}")
                # Simular trabajo mínimo
                profiler.release_gil(f"Thread-{thread_id}")
        
        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        stats = profiler.get_stats()
        
        # Verificar que no hay race conditions en los contadores
        for i in range(10):
            thread_name = f"Thread-{i}"
            assert stats[thread_name].gil_acquisitions == 100
            assert stats[thread_name].gil_releases == 100


# Fixtures

@pytest.fixture
def sample_profiler():
    """Profiler con datos de muestra."""
    profiler = GILProfiler()
    
    # Simular algunos hilos
    for i in range(3):
        thread_name = f"Sample-Thread-{i}"
        profiler.acquire_gil(thread_name)
        time.sleep(0.05)
        profiler.release_gil(thread_name)
    
    return profiler


def test_with_fixture(sample_profiler):
    """Test usando fixture."""
    stats = sample_profiler.get_stats()
    assert len(stats) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
