"""Demonstrate a Celery-like background task queue with the standard library."""

from __future__ import annotations

import time
from dataclasses import dataclass
from queue import Empty, Queue
from threading import Thread


@dataclass
class Task:
    """A small unit of work."""

    name: str
    value: int


class Worker(Thread):
    """Consumes tasks from a queue and stores results."""

    def __init__(self, tasks: Queue[Task], results: Queue[str]) -> None:
        super().__init__(daemon=True)
        self.tasks = tasks
        self.results = results
        self._running = True

    def stop(self) -> None:
        self._running = False

    def run(self) -> None:
        while self._running:
            try:
                task = self.tasks.get(timeout=0.2)
            except Empty:
                continue
            doubled = task.value * 2
            time.sleep(0.05)
            self.results.put(f"{task.name} -> {doubled}")
            self.tasks.task_done()


def main() -> None:
    """Entry point to demonstrate the implementation."""
    tasks: Queue[Task] = Queue()
    results: Queue[str] = Queue()
    worker = Worker(tasks, results)
    worker.start()

    for i in range(5):
        tasks.put(Task(name=f"task-{i}", value=i + 1))

    tasks.join()
    worker.stop()

    print("Background task results:")
    while not results.empty():
        print("-", results.get())


if __name__ == "__main__":
    main()
