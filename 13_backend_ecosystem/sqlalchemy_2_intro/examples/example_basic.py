"""Basic example: SQLAlchemy 2 style repository patterns with sqlite3."""
import sqlite3
from pathlib import Path

db = Path('/tmp/m13_sqlalchemy2.db')
if db.exists():
    db.unlink()

conn = sqlite3.connect(db)
conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, active INTEGER)')
conn.execute('INSERT INTO users (email, active) VALUES (?, ?)', ('alice@example.com', 1))
conn.execute('INSERT INTO users (email, active) VALUES (?, ?)', ('bob@example.com', 0))
conn.commit()

rows = conn.execute('SELECT id, email, active FROM users ORDER BY id').fetchall()
for row in rows:
    print(row)
