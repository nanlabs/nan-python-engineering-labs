"""Basic example: async DB access pattern using asyncio.to_thread."""
import asyncio
import sqlite3
from pathlib import Path

db = Path('/tmp/m13_sqlalchemy_async.db')
if db.exists():
    db.unlink()

async def run(query, params=()):
    def work():
        conn = sqlite3.connect(db)
        conn.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, name TEXT)')
        conn.execute(query, params)
        conn.commit()
        rows = conn.execute('SELECT id, name FROM jobs ORDER BY id').fetchall()
        conn.close()
        return rows
    return await asyncio.to_thread(work)

async def main():
    await run('INSERT INTO jobs (name) VALUES (?)', ('ship-order',))
    await run('INSERT INTO jobs (name) VALUES (?)', ('send-email',))
    rows = await run('SELECT id, name FROM jobs')
    print(rows)

asyncio.run(main())
