"""Illustrate ORM-like data access patterns with sqlite3 and repository classes."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Book:
    """Simple domain model representing a book."""

    book_id: int
    title: str
    author: str


class BookRepository:
    """Repository that mimics a tiny subset of ORM behavior."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add_book(self, title: str, author: str) -> Book:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO books (title, author) VALUES (?, ?)",
                (title, author),
            )
            conn.commit()
            return Book(book_id=int(cur.lastrowid), title=title, author=author)

    def find_all(self) -> list[Book]:
        with self._connect() as conn:
            rows = conn.execute("SELECT book_id, title, author FROM books ORDER BY book_id").fetchall()
            return [Book(**dict(row)) for row in rows]


def main() -> None:
    db_path = Path(__file__).with_name("library.db")
    if db_path.exists():
        db_path.unlink()

    repo = BookRepository(db_path)
    repo.create_schema()

    repo.add_book("Clean Architecture", "Robert C. Martin")
    repo.add_book("Designing Data-Intensive Applications", "Martin Kleppmann")

    print("Stored books:")
    for book in repo.find_all():
        print(f"- [{book.book_id}] {book.title} by {book.author}")


if __name__ == "__main__":
    main()
