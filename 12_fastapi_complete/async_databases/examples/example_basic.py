"""
Basic example: Async Databases
==================================

Synchronous SQLAlchemy blocks the event loop. For truly async I/O,
use an async driver: aiosqlite (SQLite), asyncpg (PostgreSQL),
or SQLAlchemy's async extension.

This example demonstrates:
1. AsyncEngine and AsyncSession setup (SQLAlchemy 2.x async)
2. Async dependency: get_db() with async generator
3. Fully async CRUD routes (async def + await)
4. Running raw async SQL with text()
5. Connection pool behavior

Using aiosqlite for portability — no external DB required.

Dependencies:
    pip install sqlalchemy aiosqlite

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs
"""

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, select, text, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


# =============================================================================
# ASYNC DATABASE SETUP
# =============================================================================

# Note the "sqlite+aiosqlite://" prefix — the async driver
DATABASE_URL = "sqlite+aiosqlite:////tmp/fastapi_async_demo.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,           # Set True to log SQL
    pool_size=5,          # Connection pool size (ignored for SQLite)
    max_overflow=10,      # Extra connections above pool_size
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # Keep objects usable after commit
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


# =============================================================================
# ORM MODEL
# =============================================================================


class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=False)
    pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, nullable=True)


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================


class NoteCreate(BaseModel):
    title: str
    content: str
    pinned: bool = False


class NotePatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    pinned: Optional[bool] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    pinned: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


# =============================================================================
# ASYNC DEPENDENCY
# =============================================================================


async def get_db() -> AsyncSession:
    """
    Async generator dependency — yields one AsyncSession per request.

    With `async_sessionmaker`, the session is bound to the async engine.
    The `yield` ensures the session is closed even if an exception occurs.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="Async Databases Example", version="1.0.0")


@app.on_event("startup")
async def create_tables():
    """Create tables asynchronously on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {
        "message": "Async Databases Demo",
        "driver": "aiosqlite (async SQLite)",
        "docs": "/docs",
    }


# ── CRUD ─────────────────────────────────────────────────────────────────────


@app.get("/notes", response_model=List[NoteResponse])
async def list_notes(
    pinned: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """List notes, optionally filtered by pinned status."""
    stmt = select(NoteModel)
    if pinned is not None:
        stmt = stmt.where(NoteModel.pinned == pinned)
    stmt = stmt.offset(skip).limit(limit).order_by(NoteModel.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single note by ID."""
    note = await db.get(NoteModel, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    return note


@app.post("/notes", response_model=NoteResponse, status_code=201)
async def create_note(note_in: NoteCreate, db: AsyncSession = Depends(get_db)):
    """Create a new note."""
    note = NoteModel(**note_in.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


@app.patch("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    patch: NotePatch,
    db: AsyncSession = Depends(get_db),
):
    """Partially update a note."""
    note = await db.get(NoteModel, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    updates = patch.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(note, field, value)
    note.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(note)
    return note


@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a note."""
    note = await db.get(NoteModel, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.delete(note)
    await db.commit()


# ── Raw async SQL ─────────────────────────────────────────────────────────────


@app.get("/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    """
    Run raw async SQL queries.

    db.execute(text(...)) works exactly like synchronous SQLAlchemy
    but releases the event loop while waiting for the DB.
    """
    total = await db.execute(select(func.count()).select_from(NoteModel))
    pinned = await db.execute(
        select(func.count()).select_from(NoteModel).where(NoteModel.pinned == True)
    )
    return {
        "total_notes": total.scalar(),
        "pinned_notes": pinned.scalar(),
        "driver": "aiosqlite",
    }


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("ASYNC DATABASES — DEMO")
    print("=" * 65)
    print()
    print("Database:", DATABASE_URL)
    print()
    print("Key differences from sync SQLAlchemy:")
    print("  • create_async_engine()  instead of create_engine()")
    print("  • async_sessionmaker()   instead of sessionmaker()")
    print("  • AsyncSession           instead of Session")
    print("  • async def get_db()     instead of def get_db()")
    print("  • await db.execute()     instead of db.query()")
    print("  • await db.commit()      instead of db.commit()")
    print("  • select() + scalars()   instead of .query().all()")
    print()
    print("Startup hook creates tables without blocking the event loop.")
    print()
    print("Endpoints:")
    print("  GET  /notes              — list notes")
    print("  GET  /notes/{id}         — get note")
    print("  POST /notes              — create note")
    print("  PATCH /notes/{id}        — partial update")
    print("  DELETE /notes/{id}       — delete note")
    print("  GET  /stats              — raw async SQL")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
