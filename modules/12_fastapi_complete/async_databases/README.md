# Async Databases

Estimated time: 2 hours

## 1. Definition

Synchronous SQLAlchemy blocks the event loop while waiting for database I/O. **Async SQLAlchemy** (2.x) with an async driver (`aiosqlite`, `asyncpg`) keeps the event loop free during database calls, enabling true async concurrency.

### Key Characteristics

- **`create_async_engine`**: replaces `create_engine`; uses an async-compatible driver.
- **`async_sessionmaker`**: async equivalent of `sessionmaker`.
- **`AsyncSession`**: async context manager; `await db.execute()`, `await db.commit()`.
- **`select()` construct**: replaces `.query()` for async queries; returns a `Result` object.
- **`expire_on_commit=False`**: keeps model attributes accessible after `await db.commit()`.

## 2. Practical Application

### Use Cases

- High-concurrency APIs where DB wait time dominates response time.
- PostgreSQL-backed services using `asyncpg` for maximum throughput.
- Microservices making multiple concurrent DB queries with `asyncio.gather`.

### Code Example

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select

engine = create_async_engine("sqlite+aiosqlite:///./db.sqlite")
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/notes")
async def list_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NoteModel))
    return result.scalars().all()
```

## 3. Why Is It Important?

### Problem It Solves

Synchronous `db.query()` inside an `async def` route blocks the event loop for the entire duration of the DB call, preventing FastAPI from serving other requests concurrently — eliminating the entire benefit of async.

### Solution and Benefits

With async SQLAlchemy, the event loop is released during every database wait. Multiple requests can execute their DB queries "simultaneously" (interleaved), dramatically improving throughput under load.

## 4. References

- [SQLAlchemy Asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [aiosqlite](https://aiosqlite.omnilib.dev/)
- [asyncpg](https://magicstack.github.io/asyncpg/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Set up an async SQLite engine with `aiosqlite`. Create a `NoteModel`. Implement `GET /notes` using `select(NoteModel)` and `scalars().all()`.

### Intermediate Level

Implement `POST /notes`, `PATCH /notes/{id}`, and `DELETE /notes/{id}` all with `AsyncSession`. Verify `expire_on_commit=False` is needed for the return value after commit.

### Advanced Level

Add `GET /stats` using a raw `await db.execute(select(func.count()).select_from(NoteModel))`. Run two concurrent requests in a test and verify no event loop blocking.

### Success Criteria

- All CRUD endpoints work with async SQLite.
- Removing `expire_on_commit=False` causes a `DetachedInstanceError` after commit.
- Raw SQL count query returns correct results.

## 6. Summary

Async SQLAlchemy uses the same declarative models as the synchronous version but replaces the engine, session factory, and query patterns with their async equivalents. `select()` + `scalars()` replaces `.query()`. Every database call becomes an `await`.

## 7. Reflection Prompt

When would you choose async SQLAlchemy over sync SQLAlchemy? Are there scenarios where the synchronous version is actually preferable, and what overhead does the async version add?
