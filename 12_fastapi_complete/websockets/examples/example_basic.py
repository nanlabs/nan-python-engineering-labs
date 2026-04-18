"""Simulate a websocket-style chat room using asyncio queues."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass
class Message:
    """Represents one chat message."""

    sender: str
    content: str


class InMemoryWebSocketHub:
    """Broadcast messages to connected clients via asyncio queues."""

    def __init__(self) -> None:
        self._clients: dict[str, asyncio.Queue[Message]] = {}

    async def connect(self, client_name: str) -> asyncio.Queue[Message]:
        queue: asyncio.Queue[Message] = asyncio.Queue()
        self._clients[client_name] = queue
        await self.broadcast(Message("system", f"{client_name} joined"))
        return queue

    async def disconnect(self, client_name: str) -> None:
        self._clients.pop(client_name, None)
        await self.broadcast(Message("system", f"{client_name} left"))

    async def broadcast(self, message: Message) -> None:
        for queue in self._clients.values():
            await queue.put(message)


async def consume(client_name: str, queue: asyncio.Queue[Message], count: int) -> None:
    for _ in range(count):
        msg = await queue.get()
        print(f"[{client_name}] {msg.sender}: {msg.content}")


async def main() -> None:
    hub = InMemoryWebSocketHub()
    alice_q = await hub.connect("alice")
    bob_q = await hub.connect("bob")

    consumer_alice = asyncio.create_task(consume("alice", alice_q, 4))
    consumer_bob = asyncio.create_task(consume("bob", bob_q, 3))

    await hub.broadcast(Message("alice", "Hello Bob!"))
    await hub.broadcast(Message("bob", "Hi Alice, good to see you."))
    await hub.disconnect("bob")

    await consumer_alice
    await consumer_bob


if __name__ == "__main__":
    asyncio.run(main())
