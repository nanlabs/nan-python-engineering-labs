"""Simple integration test target backed by SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path


def create_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        "CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, active INTEGER NOT NULL)"
    )
    connection.commit()


def insert_user(connection: sqlite3.Connection, email: str) -> None:
    connection.execute("INSERT INTO users (email, active) VALUES (?, 1)", (email,))
    connection.commit()


def list_users(connection: sqlite3.Connection) -> list[str]:
    rows = connection.execute("SELECT email FROM users ORDER BY email").fetchall()
    return [row[0] for row in rows]


if __name__ == "__main__":
    database_path = Path("integration_example.sqlite3")
    connection = sqlite3.connect(database_path)
    create_schema(connection)
    insert_user(connection, "alice@example.com")
    print("integration testing example")
    print(list_users(connection))
    connection.close()
    database_path.unlink(missing_ok=True)
