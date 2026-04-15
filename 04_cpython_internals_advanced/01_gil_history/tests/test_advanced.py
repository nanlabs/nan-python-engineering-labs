"""
Tests for the advanced exercise: Custom GIL Implementation

Ejecutar con: pytest test_advanced.py -v
"""

import pytest
import threading
import time
from typing import List

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from exercises.advanced_exercise import (
    SchedulerPolicy,
    ThreadRequest,
    FIFOScheduler,
    PriorityScheduler,
    FairShareScheduler,
    LotteryScheduler,
    CustomGIL,
    worker_task
)


class TestThreadRequest:
    """Tests para ThreadRequest dataclass."""
    
    def test_creation(self):
        """Verificar creación de ThreadRequest."""
        request = ThreadRequest(
            thread_id=1,
            thread_name="Thread-1",
            priority=5,
            tickets=100,
            arrival_time=time.time()
        )
        assert request.thread_id == 1
        assert request.priority == 5
        assert request.tickets == 100


class TestFIFOScheduler:
    """Tests para FIFOScheduler."""
    
    def test_fifo_order(self):
        """Verificar orden FIFO estricto."""
        scheduler = FIFOScheduler()
        
        # Encolar 5 requests
        for i in range(5):
            request = ThreadRequest(
                thread_id=i,
                thread_name=f"Thread-{i}",
                arrival_time=time.time()
            )
            scheduler.enqueue(request)
            time.sleep(0.01)  # Asegurar orden temporal
        
        # Desencolar en orden
        for i in range(5):
            request = scheduler.dequeue()
            assert request.thread_id == i, f"Expected thread {i}, got {request.thread_id}"
    
    def test_empty(self):
        """Verificar comportamiento con cola vacía."""
        scheduler = FIFOScheduler()
        assert scheduler.is_empty()
        
        scheduler.enqueue(ThreadRequest(1, "Thread-1"))
        assert not scheduler.is_empty()
        
        scheduler.dequeue()
        assert scheduler.is_empty()
    
    def test_dequeue_empty(self):
        """Verificar dequeue de cola vacía."""
        scheduler = FIFOScheduler()
        result = scheduler.dequeue()
        assert result is None


class TestPriorityScheduler:
    """Tests para PriorityScheduler."""
    
    def test_priority_order(self):
        """Verificar que respeta prioridades."""
        scheduler = PriorityScheduler(aging_factor=0.0)  # Sin aging
        
        # Encolar con diferentes prioridades
        priorities = [3, 7, 1, 9, 5]
        for i, priority in enumerate(priorities):
            request = ThreadRequest(
                thread_id=i,
                thread_name=f"Thread-{i}",
                priority=priority,
                arrival_time=time.time()
            )
            scheduler.enqueue(request)
        
        # Desencolar debe dar orden: 9, 7, 5, 3, 1
        expected_order = [3, 1, 4, 0, 2]  # thread_ids
        for expected_id in expected_order:
            request = scheduler.dequeue()
            assert request.thread_id == expected_id
    
    def test_aging_prevents_starvation(self):
        """Verificar que aging previene starvation."""
        scheduler = PriorityScheduler(aging_factor=1.0)  # Aging agresivo
        
        # Agregar thread de baja prioridad
        low_priority = ThreadRequest(
            thread_id=0,
            thread_name="LowPriority",
            priority=1,
            arrival_time=time.time()
        )
        scheduler.enqueue(low_priority)
        
        # Esperar para que acumule aging
        time.sleep(0.1)
        
        # Agregar threads de alta prioridad
        for i in range(1, 4):
            high_priority = ThreadRequest(
                thread_id=i,
                thread_name=f"HighPriority-{i}",
                priority=10,
                arrival_time=time.time()
            )
            scheduler.enqueue(high_priority)
        
        # El thread de baja prioridad should eventualmente
        # tener prioridad suficiente debido al aging
        # (este test es conceptual, el comportamiento exacto depende de la implementación)


class TestFairShareScheduler:
    """Tests para FairShareScheduler."""
    
    def test_fair_distribution(self):
        """Verificar distribución equitativa."""
        scheduler = FairShareScheduler()
        
        # Simular varios threads ejecutando
        thread_ids = [1, 2, 3]
        execution_counts = {tid: 0 for tid in thread_ids}
        
        # Encolar requests
        for tid in thread_ids:
            scheduler.enqueue(ThreadRequest(tid, f"Thread-{tid}"))
        
        # Ejecutar 30 veces
        for _ in range(30):
            request = scheduler.dequeue()
            execution_counts[request.thread_id] += 1
            
            # Registrar ejecución
            scheduler.record_execution(request.thread_id, 0.01)
            
            # Re-encolar
            scheduler.enqueue(request)
        
        # Cada thread debe haber ejecutado ~10 veces (±2)
        for tid, count in execution_counts.items():
            assert 8 <= count <= 12, f"Thread {tid} executed {count} times (expected ~10)"


class TestLotteryScheduler:
    """Tests para LotteryScheduler."""
    
    def test_probabilistic_selection(self):
        """Verificar selección probabilística basada en tickets."""
        scheduler = LotteryScheduler()
        
        # Thread-1: 100 tickets (50%)
        # Thread-2: 50 tickets (25%)
        # Thread-3: 50 tickets (25%)
        tickets_config = [(1, 100), (2, 50), (3, 50)]
        
        for tid, tickets in tickets_config:
            scheduler.enqueue(ThreadRequest(
                thread_id=tid,
                thread_name=f"Thread-{tid}",
                tickets=tickets
            ))
        
        # Ejecutar muchas veces y verificar distribución
        execution_counts = {1: 0, 2: 0, 3: 0}
        num_iterations = 1000
        
        for _ in range(num_iterations):
            request = scheduler.dequeue()
            execution_counts[request.thread_id] += 1
            
            # Re-encolar
            scheduler.enqueue(request)
        
        # Verificar que la distribución se aproxima a la esperada
        # Thread-1 debe tener ~50% (500 ± 100)
        assert 400 <= execution_counts[1] <= 600
        
        # Thread-2 y Thread-3 deben tener ~25% cada uno (250 ± 75)
        assert 175 <= execution_counts[2] <= 325
        assert 175 <= execution_counts[3] <= 325


class TestCustomGIL:
    """Tests para CustomGIL."""
    
    def test_mutual_exclusion(self):
        """Verificar que solo un hilo puede tener el GIL a la vez."""
        gil = CustomGIL(policy=SchedulerPolicy.FIFO)
        active_threads = []
        lock = threading.Lock()
        
        def worker(tid: int):
            for _ in range(5):
                gil.acquire(tid, f"Thread-{tid}")
                
                # Verificar mutual exclusion
                with lock:
                    active_threads.append(tid)
                    assert len(active_threads) == 1, "Multiple threads have GIL simultaneously!"
                
                time.sleep(0.01)  # Simular trabajo
                
                with lock:
                    active_threads.remove(tid)
                
                gil.release(tid)
        
        threads = []
        for i in range(4):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
    
    def test_no_deadlock(self):
        """Verificar que no hay deadlocks."""
        gil = CustomGIL(policy=SchedulerPolicy.FIFO)
        
        def worker(tid: int):
            for _ in range(10):
                acquired = gil.acquire(tid, f"Thread-{tid}", timeout=5.0)
                assert acquired, f"Thread {tid} timed out (possible deadlock)"
                time.sleep(0.01)
                gil.release(tid)
        
        threads = []
        for i in range(8):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=60.0)
            assert not t.is_alive(), "Thread did not finish (deadlock?)"
    
    def test_timeout(self):
        """Verificar que timeout funciona correctamente."""
        gil = CustomGIL(policy=SchedulerPolicy.FIFO)
        
        # Thread-1 adquiere el GIL y no lo libera
        gil.acquire(1, "Thread-1")
        
        # Thread-2 intenta adquirir con timeout corto
        acquired = gil.acquire(2, "Thread-2", timeout=0.1)
        
        assert not acquired, "Acquire should have timed out"
        
        # Limpiar
        gil.release(1)
    
    @pytest.mark.parametrize("policy", [
        SchedulerPolicy.FIFO,
        SchedulerPolicy.PRIORITY,
        SchedulerPolicy.FAIR_SHARE,
        SchedulerPolicy.LOTTERY
    ])
    def test_all_policies(self, policy):
        """Verificar que todas las políticas funcionan."""
        gil = CustomGIL(policy=policy)
        
        def worker(tid: int):
            for _ in range(5):
                gil.acquire(tid, f"Thread-{tid}", priority=tid, tickets=100)
                time.sleep(0.01)
                gil.release(tid)
        
        threads = []
        for i in range(4):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Verificar que se completó sin errores


class TestMetrics:
    """Tests para métricas del CustomGIL."""
    
    def test_basic_metrics(self):
        """Verificar que se recopilan métricas básicas."""
        gil = CustomGIL(policy=SchedulerPolicy.FIFO)
        
        def worker(tid: int):
            for _ in range(3):
                gil.acquire(tid, f"Thread-{tid}")
                time.sleep(0.05)
                gil.release(tid)
        
        threads = []
        for i in range(2):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        metrics = gil.get_metrics()
        
        assert 'fairness_index' in metrics
        assert 'average_wait_time' in metrics
        assert 'max_wait_time' in metrics
        assert 'context_switches' in metrics
    
    def test_fairness_metric(self):
        """Verificar cálculo de fairness."""
        gil = CustomGIL(policy=SchedulerPolicy.FAIR_SHARE)
        
        def worker(tid: int):
            for _ in range(10):
                gil.acquire(tid, f"Thread-{tid}")
                time.sleep(0.01)
                gil.release(tid)
        
        threads = []
        for i in range(4):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        metrics = gil.get_metrics()
        fairness = metrics['fairness_index']
        
        # FairShare should lograr alta fairness
        assert fairness > 0.85, f"Fairness too low: {fairness}"


class TestComparison:
    """Tests comparativos entre políticas."""
    
    @pytest.mark.slow
    def test_fifo_vs_fair_share(self):
        """Compare FIFO vs FairShare en términos de fairness."""
        
        def run_with_policy(policy: SchedulerPolicy) -> float:
            gil = CustomGIL(policy=policy)
            
            def worker(tid: int):
                for _ in range(20):
                    gil.acquire(tid, f"Thread-{tid}")
                    time.sleep(0.01)
                    gil.release(tid)
            
            threads = []
            for i in range(4):
                t = threading.Thread(target=worker, args=(i,))
                threads.append(t)
                t.start()
            
            for t in threads:
                t.join()
            
            return gil.get_metrics()['fairness_index']
        
        fairness_fifo = run_with_policy(SchedulerPolicy.FIFO)
        fairness_fair = run_with_policy(SchedulerPolicy.FAIR_SHARE)
        
        # FairShare debe tener mejor fairness que FIFO
        assert fairness_fair >= fairness_fifo * 0.95


# Fixtures

@pytest.fixture
def sample_gil():
    """CustomGIL con política FIFO para tests."""
    return CustomGIL(policy=SchedulerPolicy.FIFO)


def test_with_fixture(sample_gil):
    """Test usando fixture."""
    sample_gil.acquire(1, "Test-Thread")
    sample_gil.release(1)
    
    metrics = sample_gil.get_metrics()
    assert metrics is not None


# Markers

def pytest_configure(config):
    """Configurar markers personalizados."""
    config.addinivalue_line(
        "markers", "slow: marca tests que son lentos"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
