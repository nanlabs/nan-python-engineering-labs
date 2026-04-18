"""Message queue example: producer and consumer coordinated by Queue."""
from __future__ import annotations
import queue
import threading
from dataclasses import dataclass

@dataclass
class Event:
    event_type: str
    payload: str

def consumer(event_queue: queue.Queue[Event | None]) -> None:
    while True:
        event = event_queue.get()
        try:
            if event is None:
                print("Consumer stopping")
                return
            print(f"Consumed {event.event_type}: {event.payload}")
        finally:
            event_queue.task_done()

def main() -> None:
    event_queue: queue.Queue[Event | None] = queue.Queue()
    worker = threading.Thread(target=consumer, args=(event_queue,), daemon=True)
    worker.start()
    for event in [
        Event("order.created", "ORD-200"),
        Event("payment.captured", "PAY-889"),
        Event("order.shipped", "ORD-200"),
    ]:
        event_queue.put(event)
    event_queue.put(None)
    event_queue.join()
    worker.join(timeout=1)
    print("All events processed")

if __name__ == "__main__":
    main()
