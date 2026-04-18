"""Ports and Adapters example: core use case independent from infrastructure."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

@dataclass
class Ticket:
    ticket_id: str
    title: str
    status: str

class TicketStorePort(Protocol):
    def add(self, ticket: Ticket) -> None: ...
    def list_open(self) -> list[Ticket]: ...

class InMemoryTicketStoreAdapter(TicketStorePort):
    def __init__(self) -> None:
        self._tickets: list[Ticket] = []
    def add(self, ticket: Ticket) -> None:
        self._tickets.append(ticket)
    def list_open(self) -> list[Ticket]:
        return [t for t in self._tickets if t.status == "open"]

class TicketService:
    def __init__(self, store: TicketStorePort) -> None:
        self.store = store
    def create(self, ticket_id: str, title: str) -> None:
        self.store.add(Ticket(ticket_id, title, "open"))
    def open_titles(self) -> list[str]:
        return [ticket.title for ticket in self.store.list_open()]

def main() -> None:
    store = InMemoryTicketStoreAdapter()
    service = TicketService(store)
    service.create("T-1", "Fix onboarding bug")
    service.create("T-2", "Add audit logs")
    store.add(Ticket("T-3", "Write release notes", "closed"))
    print("Open tickets:")
    for title in service.open_titles():
        print(f"- {title}")

if __name__ == "__main__":
    main()
