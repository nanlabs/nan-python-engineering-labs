"""
GIL (Global Interpreter Lock) management in PyO3.
Demonstrates py.allow_threads() and GIL-free code.
"""

def cpu_intensive_task(count: int) -> int:
    """CPU-intensive work (simulates Rust computation without GIL)."""
    result = 0
    for i in range(count):
        result += i * i
    return result

def io_task_simulation() -> str:
    """Simulates I/O task that releases GIL."""
    import time
    # This would use py.allow_threads() in real PyO3
    time.sleep(0.1)
    return "I/O complete"

if __name__ == "__main__":
    print("CPU task:", cpu_intensive_task(1000))
    print("I/O task:", io_task_simulation())
