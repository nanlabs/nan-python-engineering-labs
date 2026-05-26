"""Request-reply example: synchronous style over asynchronous queues."""

from __future__ import annotations

import queue
import threading
import uuid
from dataclasses import dataclass


@dataclass
class Request:
    correlation_id: str
    number: int


@dataclass
class Reply:
    correlation_id: str
    result: int


def worker(requests: queue.Queue[Request | None], replies: queue.Queue[Reply]) -> None:
    while True:
        request = requests.get()
        try:
            if request is None:
                return
            replies.put(Reply(request.correlation_id, request.number * request.number))
        finally:
            requests.task_done()


def rpc_square(
    number: int, requests: queue.Queue[Request | None], replies: queue.Queue[Reply]
) -> int:
    correlation_id = str(uuid.uuid4())
    requests.put(Request(correlation_id, number))
    while True:
        reply = replies.get()
        try:
            if reply.correlation_id == correlation_id:
                return reply.result
        finally:
            replies.task_done()


def main() -> None:
    """Entry point to demonstrate the implementation."""
    requests: queue.Queue[Request | None] = queue.Queue()
    replies: queue.Queue[Reply] = queue.Queue()
    thread = threading.Thread(target=worker, args=(requests, replies), daemon=True)
    thread.start()
    for n in [4, 7, 11]:
        print(f"square({n}) = {rpc_square(n, requests, replies)}")
    requests.put(None)
    requests.join()
    thread.join(timeout=1)


if __name__ == "__main__":
    main()
