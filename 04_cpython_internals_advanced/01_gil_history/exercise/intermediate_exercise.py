"""
INTERMEDIATE EXERCISE: GIL Contention Profiler

Objective:
Develop a profiling tool that analyzes GIL contention across
multiple threads, showing metrics such as waiting time, fairness,
and GIL utilization.

Tasks:
1. Create a @profile_gil decorator that tracks simulated GIL acquisition/release
2. Implement the GILProfiler class with contention metrics
3. Simulate multiple threads competing for the GIL
4. Visualize contention using a detailed report or chart
5. Compare different patterns: CPU-bound vs I/O-bound vs mixed

Metrics to calculate:
- Total execution time per thread
- Waiting time (contention) per thread
- GIL utilization (% of time with the GIL acquired)
- Fairness index (how evenly the GIL is distributed)
- Number of GIL switches

Success criteria:
✅ The decorator works correctly with multithreaded functions
✅ Metrics are accurate and consistent
✅ Correctly detects high contention in CPU-bound workloads
✅ Correctly detects low contention in I/O-bound workloads
✅ Clear visual report (table or chart)
✅ Fairness index calculation (ideal: ~1.0)

Estimated time: 90-120 minutes
"""

import functools
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class ThreadStats:
    """Statistics for an individual thread."""

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
        """% of time spent executing versus waiting."""
        total = self.total_time
        return (self.execution_time / total * 100) if total > 0 else 0.0


class GILProfiler:
    """
    TODO: Implement a GIL contention profiler.

    The profiler simulates GIL behavior by tracking when
    each thread "acquires" and "releases" the GIL.

    Required methods:
    - acquire_gil(thread_name: str): Record GIL acquisition
    - release_gil(thread_name: str): Record GIL release
    - get_stats() -> Dict[str, ThreadStats]: Return per-thread statistics
    - calculate_fairness() -> float: Calculate fairness index (Jain's fairness)
    - generate_report() -> str: Generate a formatted report
    """

    def __init__(self):
        """TODO: Initialize data structures."""
        # YOUR CODE HERE
        pass

    def acquire_gil(self, thread_name: str):
        """
        TODO: Record that a thread acquired the GIL.

        - If the GIL is already taken, the thread must wait
        - Track waiting time
        - Increment the acquisition counter
        """
        pass  # YOUR CODE HERE

    def release_gil(self, thread_name: str):
        """
        TODO: Record that a thread released the GIL.

        - Calculate execution time
        - Increment the release counter
        - Allow other threads to acquire the GIL
        """
        pass  # YOUR CODE HERE

    def get_stats(self) -> dict[str, ThreadStats]:
        """TODO: Return the collected statistics."""
        pass  # YOUR CODE HERE

    def calculate_fairness(self) -> float:
        """
        TODO: Calculate Jain's fairness index.

        Formula: (sum(x_i))^2 / (n * sum(x_i^2))
        where x_i is the execution_time of thread i

        Ideal value: 1.0 (perfectly fair)
        Worst-case value: 1/n (one thread monopolizes execution)
        """
        pass  # YOUR CODE HERE

    def generate_report(self) -> str:
        """TODO: Generate a formatted report with all metrics."""
        pass  # YOUR CODE HERE


def profile_gil(profiler: GILProfiler):
    """
    TODO: Implement a decorator that profiles functions using GILProfiler.

    The decorator must:
    1. Acquire the GIL before executing the function
    2. Execute the function
    3. Release the GIL after execution
    4. Handle exceptions appropriately

    Usage:
        @profile_gil(profiler)
        def my_function():
            # code...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # YOUR CODE HERE
            pass

        return wrapper

    return decorator


# Test helper functions for different workloads


def cpu_intensive_task(duration: float, profiler: GILProfiler):
    """
    TODO: Implement a CPU-intensive task that uses the profiler.

    It must:
    - Acquire the GIL at the start
    - Perform computations for 'duration' seconds
    - Release the GIL at the end
    - Simulate periodic GIL switches (every 0.005s)
    """
    pass  # YOUR CODE HERE


def io_intensive_task(duration: float, profiler: GILProfiler):
    """
    TODO: Implement an I/O-intensive task that uses the profiler.

    It must:
    - Acquire the GIL briefly
    - Release the GIL before time.sleep()
    - Simulate an I/O operation with sleep
    - Reacquire the GIL after sleeping
    """
    pass  # YOUR CODE HERE


def mixed_task(cpu_duration: float, io_duration: float, profiler: GILProfiler):
    """
    TODO: Implement a mixed task (CPU + I/O).

    It must alternate between CPU and I/O several times.
    """
    pass  # YOUR CODE HERE


def run_workload_test(
    workload_name: str,
    task_func: Callable,
    task_args: tuple,
    num_threads: int,
    profiler: GILProfiler,
):
    """
    TODO: Run a workload test and show the results.

    Args:
        workload_name: Descriptive test name
        task_func: Function to execute in each thread
        task_args: Arguments for task_func
        num_threads: Number of threads
        profiler: GILProfiler instance
    """
    pass  # YOUR CODE HERE


def main():
    """
    TODO: Implement the main function that runs the test suite.

    Tests to run:
    1. CPU-bound with 4 threads (high contention expected)
    2. I/O-bound with 4 threads (low contention expected)
    3. Mixed workload with 4 threads (medium contention)

    For each test:
    - Show the GILProfiler report
    - Show the fairness index
    - Analyze the results
    """
    pass  # YOUR CODE HERE


if __name__ == "__main__":
    main()


# SELF-VERIFICATION SECTION


def test_thread_stats():
    """TODO: Verify ThreadStats calculations."""
    # Example:
    # stats = ThreadStats(name="test", execution_time=80, wait_time=20)
    # assert stats.total_time == 100
    # assert stats.efficiency == 80.0
    pass


def test_fairness_calculation():
    """TODO: Verify fairness calculation."""
    # Ideal case: all threads have the same execution_time
    # Worst case: one thread monopolizes execution
    pass


# Uncomment to run tests:
# if __name__ == "__main__":
#     test_thread_stats()
#     test_fairness_calculation()
#     main()
