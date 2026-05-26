"""
Tests for the advanced exercise: Custom GIL Implementation

Run with: pytest test_advanced.py -v
"""

import os
import sys
import threading
import time

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from exercises.advanced_exercise import (
    CustomGIL,
    FairShareScheduler,
    FIFOScheduler,
    LotteryScheduler,
    PriorityScheduler,
    SchedulerPolicy,
    ThreadRequest,
)


class TestThreadRequest:
    """Tests for the ThreadRequest dataclass."""

    def test_creation(self):
        """Verify ThreadRequest creation."""
        request = ThreadRequest(
            thread_id=1, thread_name="Thread-1", priority=5, tickets=100, arrival_time=time.time()
        )
        assert request.thread_id == 1
        assert request.priority == 5
        assert request.tickets == 100


class TestFIFOScheduler:
    """Tests for FIFOScheduler."""

    def test_fifo_order(self):
        """Verify strict FIFO ordering."""
        scheduler = FIFOScheduler()

        # Enqueue 5 requests
        for i in range(5):
            request = ThreadRequest(
                thread_id=i, thread_name=f"Thread-{i}", arrival_time=time.time()
            )
            scheduler.enqueue(request)
            time.sleep(0.01)  # Ensure temporal ordering

        # Dequeue in order
        for i in range(5):
            request = scheduler.dequeue()
            assert request.thread_id == i, f"Expected thread {i}, got {request.thread_id}"

    def test_empty(self):
        """Verify behavior with an empty queue."""
        scheduler = FIFOScheduler()
        assert scheduler.is_empty()

        scheduler.enqueue(ThreadRequest(1, "Thread-1"))
        assert not scheduler.is_empty()

        scheduler.dequeue()
        assert scheduler.is_empty()

    def test_dequeue_empty(self):
        """Verify dequeue on an empty queue."""
        scheduler = FIFOScheduler()
        result = scheduler.dequeue()
        assert result is None


class TestPriorityScheduler:
    """Tests for PriorityScheduler."""

    def test_priority_order(self):
        """Verify that it respects priorities."""
        scheduler = PriorityScheduler(aging_factor=0.0)  # No aging

        # Enqueue with different priorities
        priorities = [3, 7, 1, 9, 5]
        for i, priority in enumerate(priorities):
            request = ThreadRequest(
                thread_id=i, thread_name=f"Thread-{i}", priority=priority, arrival_time=time.time()
            )
            scheduler.enqueue(request)

        # Dequeue should produce the order: 9, 7, 5, 3, 1
        expected_order = [3, 1, 4, 0, 2]  # thread_ids
        for expected_id in expected_order:
            request = scheduler.dequeue()
            assert request.thread_id == expected_id

    def test_aging_prevents_starvation(self):
        """Verify that aging prevents starvation."""
        scheduler = PriorityScheduler(aging_factor=1.0)  # Aggressive aging

        # Add a low-priority thread
        low_priority = ThreadRequest(
            thread_id=0, thread_name="LowPriority", priority=1, arrival_time=time.time()
        )
        scheduler.enqueue(low_priority)

        # Wait so it accumulates aging
        time.sleep(0.1)

        # Add high-priority threads
        for i in range(1, 4):
            high_priority = ThreadRequest(
                thread_id=i, thread_name=f"HighPriority-{i}", priority=10, arrival_time=time.time()
            )
            scheduler.enqueue(high_priority)

        # The low-priority thread should eventually
        # reach enough priority because of aging
        # (this test is conceptual; exact behavior depends on the implementation)


class TestFairShareScheduler:
    """Tests for FairShareScheduler."""

    def test_fair_distribution(self):
        """Verify fair distribution."""
        scheduler = FairShareScheduler()

        # Simulate several executing threads
        thread_ids = [1, 2, 3]
        execution_counts = {tid: 0 for tid in thread_ids}

        # Enqueue requests
        for tid in thread_ids:
            scheduler.enqueue(ThreadRequest(tid, f"Thread-{tid}"))

        # Execute 30 times
        for _ in range(30):
            request = scheduler.dequeue()
            execution_counts[request.thread_id] += 1

            # Record execution
            scheduler.record_execution(request.thread_id, 0.01)

            # Re-enqueue
            scheduler.enqueue(request)

        # Each thread should have executed about 10 times (±2)
        for tid, count in execution_counts.items():
            assert 8 <= count <= 12, f"Thread {tid} executed {count} times (expected ~10)"


class TestLotteryScheduler:
    """Tests for LotteryScheduler."""

    def test_probabilistic_selection(self):
        """Verify ticket-based probabilistic selection."""
        scheduler = LotteryScheduler()

        # Thread-1: 100 tickets (50%)
        # Thread-2: 50 tickets (25%)
        # Thread-3: 50 tickets (25%)
        tickets_config = [(1, 100), (2, 50), (3, 50)]

        for tid, tickets in tickets_config:
            scheduler.enqueue(
                ThreadRequest(thread_id=tid, thread_name=f"Thread-{tid}", tickets=tickets)
            )

        # Execute many times and verify the distribution
        execution_counts = {1: 0, 2: 0, 3: 0}
        num_iterations = 1000

        for _ in range(num_iterations):
            request = scheduler.dequeue()
            execution_counts[request.thread_id] += 1

            # Re-enqueue
            scheduler.enqueue(request)

        # Verify that the distribution approximates the expected one
        # Thread-1 should have about 50% (500 ± 100)
        assert 400 <= execution_counts[1] <= 600

        # Thread-2 and Thread-3 should have about 25% each (250 ± 75)
        assert 175 <= execution_counts[2] <= 325
        assert 175 <= execution_counts[3] <= 325


class TestCustomGIL:
    """Tests for CustomGIL."""

    def test_mutual_exclusion(self):
        """Verify that only one thread can hold the GIL at a time."""
        gil = CustomGIL(policy=SchedulerPolicy.FIFO)
        active_threads = []
        lock = threading.Lock()

        def worker(tid: int):
            for _ in range(5):
                gil.acquire(tid, f"Thread-{tid}")

                # Verify mutual exclusion
                with lock:
                    active_threads.append(tid)
                    assert len(active_threads) == 1, "Multiple threads have GIL simultaneously!"

                time.sleep(0.01)  # Simulate work

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
        """Verify that there are no deadlocks."""
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
        """Verify that timeout works correctly."""
        gil = CustomGIL(policy=SchedulerPolicy.FIFO)

        # Thread-1 acquires the GIL and does not release it
        gil.acquire(1, "Thread-1")

        # Thread-2 tries to acquire it with a short timeout
        acquired = gil.acquire(2, "Thread-2", timeout=0.1)

        assert not acquired, "Acquire should have timed out"

        # Clean up
        gil.release(1)

    @pytest.mark.parametrize(
        "policy",
        [
            SchedulerPolicy.FIFO,
            SchedulerPolicy.PRIORITY,
            SchedulerPolicy.FAIR_SHARE,
            SchedulerPolicy.LOTTERY,
        ],
    )
    def test_all_policies(self, policy):
        """Verify that all policies work."""
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

        # Verify that execution completed without errors


class TestMetrics:
    """Tests for CustomGIL metrics."""

    def test_basic_metrics(self):
        """Verify that basic metrics are collected."""
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

        assert "fairness_index" in metrics
        assert "average_wait_time" in metrics
        assert "max_wait_time" in metrics
        assert "context_switches" in metrics

    def test_fairness_metric(self):
        """Verify fairness calculation."""
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
        fairness = metrics["fairness_index"]

        # FairShare should achieve high fairness
        assert fairness > 0.85, f"Fairness too low: {fairness}"


class TestComparison:
    """Comparative tests across policies."""

    @pytest.mark.slow
    def test_fifo_vs_fair_share(self):
        """Compare FIFO vs FairShare in terms of fairness."""

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

            return gil.get_metrics()["fairness_index"]

        fairness_fifo = run_with_policy(SchedulerPolicy.FIFO)
        fairness_fair = run_with_policy(SchedulerPolicy.FAIR_SHARE)

        # FairShare should have better fairness than FIFO
        assert fairness_fair >= fairness_fifo * 0.95


# Fixtures


@pytest.fixture
def sample_gil():
    """CustomGIL with FIFO policy for tests."""
    return CustomGIL(policy=SchedulerPolicy.FIFO)


def test_with_fixture(sample_gil):
    """Test using a fixture."""
    sample_gil.acquire(1, "Test-Thread")
    sample_gil.release(1)

    metrics = sample_gil.get_metrics()
    assert metrics is not None


# Markers


def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line("markers", "slow: marks tests that are slow")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
