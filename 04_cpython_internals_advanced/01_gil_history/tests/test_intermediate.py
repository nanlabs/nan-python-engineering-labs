"""
Tests for the intermediate exercise: GIL Contention Profiler

Run with: pytest test_intermediate.py -v
"""

import os
import sys
import threading
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from exercises.intermediate_exercise import (
    GILProfiler,
    ThreadStats,
    cpu_intensive_task,
    io_intensive_task,
    mixed_task,
    profile_gil,
)


class TestThreadStats:
    """Tests for the ThreadStats dataclass."""

    def test_total_time(self):
        """Verify total_time calculation."""
        stats = ThreadStats(name="test", execution_time=80.0, wait_time=20.0)
        assert stats.total_time == 100.0

    def test_efficiency(self):
        """Verify efficiency calculation."""
        stats = ThreadStats(name="test", execution_time=80.0, wait_time=20.0)
        assert stats.efficiency == 80.0

        stats2 = ThreadStats(name="test2", execution_time=50.0, wait_time=50.0)
        assert stats2.efficiency == 50.0

    def test_efficiency_zero_division(self):
        """Verify that efficiency handles division by zero."""
        stats = ThreadStats(name="test", execution_time=0.0, wait_time=0.0)
        assert stats.efficiency == 0.0


class TestGILProfiler:
    """Tests for the GILProfiler class."""

    def test_initialization(self):
        """Verify correct initialization."""
        profiler = GILProfiler()
        assert profiler is not None
        assert profiler.get_stats() is not None

    def test_single_thread_acquisition(self):
        """Test with a single thread acquiring the GIL."""
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
        """Test with multiple threads competing for the GIL."""
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

        # Verify that all threads have statistics
        assert len(stats) == 3

        # Verify that each thread made 3 acquisitions/releases
        for thread_name in ["Thread-0", "Thread-1", "Thread-2"]:
            assert stats[thread_name].gil_acquisitions == 3
            assert stats[thread_name].gil_releases == 3

    def test_fairness_calculation(self):
        """Verify fairness index calculation."""
        profiler = GILProfiler()

        # Simulate perfectly fair execution (all threads run for the same time)
        for i in range(4):
            thread_name = f"Thread-{i}"
            profiler.acquire_gil(thread_name)
            time.sleep(0.1)
            profiler.release_gil(thread_name)

        fairness = profiler.calculate_fairness()

        # Fairness should be close to 1.0 (perfectly fair)
        assert 0.95 <= fairness <= 1.0

    def test_unfair_execution(self):
        """Verify detection of unfair execution."""
        profiler = GILProfiler()

        # Thread-0 executes much more than the others
        profiler.acquire_gil("Thread-0")
        time.sleep(0.4)
        profiler.release_gil("Thread-0")

        for i in range(1, 4):
            profiler.acquire_gil(f"Thread-{i}")
            time.sleep(0.05)
            profiler.release_gil(f"Thread-{i}")

        fairness = profiler.calculate_fairness()

        # Fairness should be low (< 0.8)
        assert fairness < 0.8

    def test_generate_report(self):
        """Verify report generation."""
        profiler = GILProfiler()

        profiler.acquire_gil("Thread-1")
        time.sleep(0.1)
        profiler.release_gil("Thread-1")

        report = profiler.generate_report()

        assert isinstance(report, str)
        assert "Thread-1" in report
        assert "Fairness" in report or "fairness" in report


class TestProfileGilDecorator:
    """Tests for the @profile_gil decorator."""

    def test_decorator_basic(self):
        """Verify basic decorator behavior."""
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
        """Verify that the decorator handles exceptions correctly."""
        profiler = GILProfiler()

        @profile_gil(profiler)
        def failing_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_func()

        # The GIL should have been released even with an exception
        # (verify that it does not remain in an inconsistent state)


class TestWorkloadTasks:
    """Tests for workload functions."""

    def test_cpu_intensive_task(self):
        """Verify the CPU-intensive task."""
        profiler = GILProfiler()

        cpu_intensive_task(0.2, profiler)

        stats = profiler.get_stats()
        thread_name = threading.current_thread().name

        assert thread_name in stats
        assert stats[thread_name].execution_time > 0

    def test_io_intensive_task(self):
        """Verify the I/O-intensive task."""
        profiler = GILProfiler()

        io_intensive_task(0.2, profiler)

        stats = profiler.get_stats()
        # The I/O task should release the GIL, so execution_time should be low
        # compared with total time

    def test_mixed_task(self):
        """Verify the mixed task."""
        profiler = GILProfiler()

        mixed_task(0.1, 0.1, profiler)

        stats = profiler.get_stats()
        assert len(stats) > 0


class TestContention:
    """Tests for GIL contention."""

    def test_high_contention_cpu_bound(self):
        """Verify high contention in a CPU-bound workload."""
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

        # In CPU-bound workloads, we expect high wait_time
        total_wait = sum(s.wait_time for s in stats.values())
        total_exec = sum(s.execution_time for s in stats.values())

        # Wait time should be significant
        assert total_wait > total_exec * 0.1  # At least 10% of execution time

    def test_low_contention_io_bound(self):
        """Verify low contention in an I/O-bound workload."""
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

        # In I/O-bound workloads, we expect low wait_time
        # (because the GIL is released during I/O)
        fairness = profiler.calculate_fairness()

        # Fairness should be high for I/O-bound work
        assert fairness > 0.7


class TestConcurrentAccess:
    """Tests for concurrent access to the profiler."""

    def test_thread_safety(self):
        """Verify that the profiler is thread-safe."""
        profiler = GILProfiler()

        def worker(thread_id: int):
            for _ in range(100):
                profiler.acquire_gil(f"Thread-{thread_id}")
                # Simulate minimal work
                profiler.release_gil(f"Thread-{thread_id}")

        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        stats = profiler.get_stats()

        # Verify that there are no race conditions in the counters
        for i in range(10):
            thread_name = f"Thread-{i}"
            assert stats[thread_name].gil_acquisitions == 100
            assert stats[thread_name].gil_releases == 100


# Fixtures


@pytest.fixture
def sample_profiler():
    """Profiler with sample data."""
    profiler = GILProfiler()

    # Simulate a few threads
    for i in range(3):
        thread_name = f"Sample-Thread-{i}"
        profiler.acquire_gil(thread_name)
        time.sleep(0.05)
        profiler.release_gil(thread_name)

    return profiler


def test_with_fixture(sample_profiler):
    """Test using a fixture."""
    stats = sample_profiler.get_stats()
    assert len(stats) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
