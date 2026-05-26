# SQLAlchemy Integration

Estimated time: 3 hours

## 1. Definition

**SQLAlchemy** is the standard Python ORM for relational databases. FastAPI integrates with it through a `yield`-based dependency that provides a database session scoped to each HTTP request, ensuring sessions are opened, committed, and closed correctly.

### Key Characteristics

- **Declarative models**: Python classes map to database tables via `DeclarativeBase`.
- **`SessionLocal`**: configured `sessionmaker` factory; one session per request.
- **`get_db()` dependency**: yields a `Session` and closes it in the `finally` block.
- **CRUD pattern**: `db.add()`, `db.commit()`, `db.refresh()`, `db.query()`.
- **Relationships**: `relationship()` with `back_populates` for ORM-managed joins.

## 2. Practical Application

### Use Cases

- User and authentication data stored in PostgreSQL or SQLite.
- Product catalogs with one-to-many author→books relationships.
- Order management with cascaded deletes.
- Full-text search using database-native features via `text()`.

### Code Example

```python
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(UserModel).filter(UserModel.id == user_id).first()
```

## 3. Why Is It Important?

### Problem It Solves

Without a framework-managed session, database connections leak, transactions are left open, and error handling is inconsistent. Each route would need to open and close its own session.

### Solution and Benefits

The `yield`-based dependency guarantees the session is closed even if an exception occurs. One session per request prevents data leaking between concurrent requests and makes transaction boundaries predictable.

## 4. References

- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Create a `NoteModel` (id, title, content, created_at). Implement `GET /notes` and `POST /notes` with a `yield`-based session dependency.

### Intermediate Level

Add a `UserModel` with a one-to-many relationship to `NoteModel`. Implement `GET /users/{id}` that returns the user with their notes loaded.

### Advanced Level

Add cascade delete: deleting a user deletes their notes. Add `GET /notes?pinned=true` filtering. Write a test using `TestClient` with an in-memory SQLite database.

### Success Criteria

- `POST /notes` persists across requests (not reset between calls).
- `GET /users/{id}` includes the `notes` array.
- Deleting a user removes their notes.
- Tests pass with in-memory SQLite.

## 6. Summary

SQLAlchemy integrates with FastAPI via a `yield`-based `get_db()` dependency. Declarative models define the schema. `db.add() + db.commit() + db.refresh()` is the standard create pattern. Relationships are loaded automatically or explicitly via `joinedload`.

## 7. Reflection Prompt

SQLAlchemy's default lazy loading can cause the N+1 query problem. How would you detect this issue in a running application, and what SQLAlchemy feature would you use to fix it?
