"""Scheduler example: run delayed tasks using a dedicated worker thread."""
from __future__ import annotations
import heapq
import threading
import time
from dataclasses import dataclass, field
from typing import Callable

@dataclass(order=True)
class ScheduledTask:
    run_at: float
    name: str = field(compare=False)
    action: Callable[[], None] = field(compare=False)

class TaskScheduler:
    def __init__(self) -> None:
        self._tasks: list[ScheduledTask] = []
        self._condition = threading.Condition()
        self._running = True
        self._worker = threading.Thread(target=self._loop, daemon=True)
        self._worker.start()

    def schedule(self, delay_s: float, name: str, action: Callable[[], None]) -> None:
        with self._condition:
            heapq.heappush(self._tasks, ScheduledTask(time.time() + delay_s, name, action))
            self._condition.notify()

    def _loop(self) -> None:
        while self._running:
            with self._condition:
                while self._running and not self._tasks:
                    self._condition.wait()
                if not self._running:
                    break
                next_task = self._tasks[0]
                now = time.time()
                if next_task.run_at > now:
                    self._condition.wait(timeout=next_task.run_at - now)
                    continue
                heapq.heappop(self._tasks)
            next_task.action()

    def shutdown(self) -> None:
        with self._condition:
            self._running = False
            self._condition.notify_all()
        self._worker.join(timeout=2)

def main() -> None:
    scheduler = TaskScheduler()
    start = time.time()
    def log(name: str) -> None:
        print(f"{name} executed at +{time.time() - start:.2f}s")
    scheduler.schedule(0.2, "refresh-cache", lambda: log("refresh-cache"))
    scheduler.schedule(0.05, "send-heartbeat", lambda: log("send-heartbeat"))
    scheduler.schedule(0.35, "rotate-logs", lambda: log("rotate-logs"))
    time.sleep(0.6)
    scheduler.shutdown()

if __name__ == "__main__":
    main()
