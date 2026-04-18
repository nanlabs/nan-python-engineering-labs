"""Demonstrate asynchronous database access patterns using only the Python standard library."""

from __future__ import annotations

import asyncio
import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class User:
    """Represents one row in the users table."""

    user_id: int
    name: str
    email: str


class AsyncSQLiteRepo:
    """Tiny async wrapper around sqlite3 calls using asyncio.to_thread."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_sync(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
                """
            )
            conn.commit()

    async def initialize(self) -> None:
        await asyncio.to_thread(self._initialize_sync)

    def _insert_user_sync(self, name: str, email: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email),
            )
            conn.commit()
            return int(cur.lastrowid)

    async def insert_user(self, name: str, email: str) -> int:
        return await asyncio.to_thread(self._insert_user_sync, name, email)

    def _list_users_sync(self) -> list[User]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT user_id, name, email FROM users ORDER BY user_id"
            ).fetchall()
            return [User(**dict(row)) for row in rows]

    async def list_users(self) -> list[User]:
        return await asyncio.to_thread(self._list_users_sync)


async def main() -> None:
    db_path = Path(__file__).with_name("async_users.db")
    if db_path.exists():
        db_path.unlink()

    repo = AsyncSQLiteRepo(db_path)
    await repo.initialize()

    await asyncio.gather(
        repo.insert_user("Ada Lovelace", "ada@example.com"),
        repo.insert_user("Grace Hopper", "grace@example.com"),
        repo.insert_user("Linus Torvalds", "linus@example.com"),
    )

    users = await repo.list_users()
    print("Async query result:")
    for user in users:
        print(f"- #{user.user_id}: {user.name} <{user.email}>")


if __name__ == "__main__":
    asyncio.run(main())
