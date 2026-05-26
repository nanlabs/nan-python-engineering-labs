"""
Advanced demonstration of GIL behavior in CPython.

This script demonstrates:
1. GIL contention in CPU-bound operations
2. GIL release in I/O-bound operations
3. GIL switching between threads
4. Real performance impact
"""

import math
import sys
import threading
import time
from collections import defaultdict


class GILMonitor:
    """
    Monitor approximate GIL behavior by tracking
    which threads are executing Python code.
    """

    def __init__(self):
        self.thread_times: dict[str, float] = defaultdict(float)
        self.start_times: dict[str, float] = {}
        self.lock = threading.Lock()

    def start_execution(self, thread_name: str):
        """Record when a thread starts executing."""
        with self.lock:
            self.start_times[thread_name] = time.perf_counter()

    def end_execution(self, thread_name: str):
        """Record when a thread finishes executing."""
        with self.lock:
            if thread_name in self.start_times:
                elapsed = time.perf_counter() - self.start_times[thread_name]
                self.thread_times[thread_name] += elapsed
                del self.start_times[thread_name]

    def get_report(self) -> str:
        """Generate an execution time report by thread."""
        total = sum(self.thread_times.values())
        report = ["\n" + "=" * 60]
        report.append("GIL EXECUTION TIME REPORT")
        report.append("=" * 60)

        for thread_name, exec_time in sorted(self.thread_times.items()):
            percentage = (exec_time / total * 100) if total > 0 else 0
            report.append(f"{thread_name:20} {exec_time:8.4f}s ({percentage:5.1f}%)")

        report.append("=" * 60)
        report.append(f"{'TOTAL':20} {total:8.4f}s")
        return "\n".join(report)


def cpu_intensive_work(iterations: int, monitor: GILMonitor):
    """
    CPU-intensive work that keeps the GIL.
    Compute complex mathematical operations.
    """
    thread_name = threading.current_thread().name
    monitor.start_execution(thread_name)

    result = 0
    for i in range(iterations):
        # CPU-intensive operations that keep the GIL
        result += math.sqrt(i) * math.sin(i) * math.cos(i)

        # Python switches the GIL about every ~5ms or ~100 instructions
        # of bytecode (check_interval in Python 2, switch interval in Python 3)
        if i % 10000 == 0:
            # Force a checkpoint where Python could switch the GIL
            pass

    monitor.end_execution(thread_name)
    return result


def io_intensive_work(duration: float, monitor: GILMonitor):
    """
    I/O-intensive work that releases the GIL.
    Simulate network/disk operations.
    """
    thread_name = threading.current_thread().name
    monitor.start_execution(thread_name)

    # time.sleep() releases the GIL, allowing other threads to execute
    time.sleep(duration)

    monitor.end_execution(thread_name)


def mixed_workload(cpu_iterations: int, io_duration: float, monitor: GILMonitor):
    """
    Mixed workload that alternates between CPU and I/O.
    Demonstrates GIL switching behavior.
    """
    thread_name = threading.current_thread().name

    for _ in range(3):
        monitor.start_execution(thread_name)
        # CPU work
        result = sum(math.sqrt(i) for i in range(cpu_iterations))
        monitor.end_execution(thread_name)

        # I/O work (releases the GIL)
        time.sleep(io_duration)

    return result


def run_cpu_bound_test(num_threads: int):
    """
    Test CPU-bound operations with multiple threads.
    Demonstrates that the GIL prevents real parallelism.
    """
    print(f"\n{'=' * 60}")
    print(f"CPU-BOUND TEST: {num_threads} thread(s)")
    print("=" * 60)

    monitor = GILMonitor()
    iterations = 500000

    start = time.perf_counter()

    threads: list[threading.Thread] = []
    for i in range(num_threads):
        t = threading.Thread(
            target=cpu_intensive_work, args=(iterations, monitor), name=f"CPU-Worker-{i + 1}"
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()
    elapsed = end - start

    print(f"Total time: {elapsed:.4f}s")
    print(f"Expected time with perfect parallelism: {elapsed / num_threads:.4f}s")
    print(f"Speedup real: {1.0 / (elapsed / (iterations * num_threads / 500000)):.2f}x")
    print(monitor.get_report())


def run_io_bound_test(num_threads: int):
    """
    Test I/O-bound operations with multiple threads.
    Demonstrates that the GIL is released during I/O.
    """
    print(f"\n{'=' * 60}")
    print(f"I/O-BOUND TEST: {num_threads} thread(s)")
    print("=" * 60)

    monitor = GILMonitor()
    io_duration = 0.5

    start = time.perf_counter()

    threads: list[threading.Thread] = []
    for i in range(num_threads):
        t = threading.Thread(
            target=io_intensive_work, args=(io_duration, monitor), name=f"IO-Worker-{i + 1}"
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()
    elapsed = end - start

    print(f"Total time: {elapsed:.4f}s")
    print(f"Expected sequential time: {io_duration * num_threads:.4f}s")
    print(f"Speedup: {(io_duration * num_threads) / elapsed:.2f}x")
    print(monitor.get_report())


def run_mixed_test(num_threads: int):
    """
    Test mixed workload (CPU + I/O).
    Shows real application behavior.
    """
    print(f"\n{'=' * 60}")
    print(f"MIXED WORKLOAD TEST: {num_threads} thread(s)")
    print("=" * 60)

    monitor = GILMonitor()
    cpu_iterations = 100000
    io_duration = 0.1

    start = time.perf_counter()

    threads: list[threading.Thread] = []
    for i in range(num_threads):
        t = threading.Thread(
            target=mixed_workload,
            args=(cpu_iterations, io_duration, monitor),
            name=f"Mixed-Worker-{i + 1}",
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.perf_counter()
    elapsed = end - start

    print(f"Total time: {elapsed:.4f}s")
    print(monitor.get_report())


def main():
    """
    Run the full set of tests to demonstrate the GIL.
    """
    print("=" * 60)
    print("DEMONSTRATION OF THE GLOBAL INTERPRETER LOCK (GIL)")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Thread switching interval: {sys.getswitchinterval()}s")

    # Check if free-threading is enabled (Python 3.13+)
    gil_status = "Enabled (Legacy)"
    if hasattr(sys, "_is_gil_enabled"):
        if not sys._is_gil_enabled():
            gil_status = "Free-threading enabled (Python 3.13+)"
        else:
            gil_status = "GIL enabled (Python 3.13+)"
    print(f"GIL Status: {gil_status}")

    # Test 1: CPU-bound with increasing threads
    print("\n" + "🔴 " * 30)
    print("TEST 1: CPU-BOUND OPERATIONS")
    print("🔴 " * 30)
    print("Hypothesis: Threading will NOT improve performance due to the GIL")

    for num_threads in [1, 2, 4]:
        run_cpu_bound_test(num_threads)

    # Test 2: I/O-bound with increasing threads
    print("\n" + "🟢 " * 30)
    print("TEST 2: I/O-BOUND OPERATIONS")
    print("🟢 " * 30)
    print("Hypothesis: Threading WILL improve performance (the GIL is released)")

    for num_threads in [1, 2, 4]:
        run_io_bound_test(num_threads)

    # Test 3: Mixed workload
    print("\n" + "🟡 " * 30)
    print("TEST 3: MIXED WORKLOAD")
    print("🟡 " * 30)
    print("Hypothesis: Partial improvement, depending on the CPU/IO ratio")

    for num_threads in [1, 2, 4]:
        run_mixed_test(num_threads)

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(
        """
    1. CPU-bound: The GIL serializes execution.
        There is no real speedup with threading.
       ➜ Solution: Use multiprocessing or C extensions that release the GIL.

    2. I/O-bound: The GIL is released during I/O operations.
        Threading is effective.
       ➜ Solution: Threading is appropriate.
       ➜ asyncio is also a good alternative.

    3. Mixed: Intermediate behavior. Benefit depends on the CPU/IO ratio.
       ➜ Solution: Analyze the workload and choose the best strategy.

    4. Free-threading (Python 3.13+): Enables true CPU-bound parallelism.
       ➜ Requires compiling Python with the --disable-gil flag.
    """
    )


if __name__ == "__main__":
    main()
