"""
Basic example: SQLAlchemy Integration
=========================================

SQLAlchemy is the de facto ORM for Python. FastAPI integrates with it
via dependency injection to provide per-request database sessions.

This example demonstrates:
1. Engine and session setup (synchronous SQLAlchemy)
2. Declarative ORM models
3. Dependency injection for DB sessions (yield-based)
4. CRUD operations through the session
5. One-to-many relationship (Author → Books)

Using SQLite for portability — no external database required.

Run:
    uvicorn example_basic:app --reload
    Visit http://localhost:8000/docs

The database is created at: /tmp/fastapi_sqlalchemy_demo.db
"""

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey,
    create_engine, text,
)
from sqlalchemy.orm import (
    DeclarativeBase, relationship, sessionmaker, Session,
)


# =============================================================================
# DATABASE SETUP
# =============================================================================

DATABASE_URL = "sqlite:////tmp/fastapi_sqlalchemy_demo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite-only setting
    echo=False,  # Set True to log SQL queries
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# =============================================================================
# ORM MODELS
# =============================================================================


class AuthorModel(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    bio = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    books = relationship("BookModel", back_populates="author", cascade="all, delete-orphan")


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    author = relationship("AuthorModel", back_populates="books")


# Create tables on startup
Base.metadata.create_all(bind=engine)


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================


class AuthorCreate(BaseModel):
    name: str
    email: str
    bio: Optional[str] = None


class AuthorResponse(BaseModel):
    id: int
    name: str
    email: str
    bio: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class AuthorWithBooks(AuthorResponse):
    books: List["BookResponse"] = []


class BookCreate(BaseModel):
    title: str
    isbn: str
    price: float
    in_stock: bool = True
    author_id: int


class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    price: float
    in_stock: bool
    author_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# Resolve forward reference
AuthorWithBooks.model_rebuild()


# =============================================================================
# DATABASE DEPENDENCY
# =============================================================================


def get_db() -> Session:
    """
    Yield a database session for the duration of a single request.

    - Session is created at request start.
    - Committed (or rolled back on error) at request end.
    - Always closed in the finally block.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# =============================================================================
# APP
# =============================================================================

app = FastAPI(title="SQLAlchemy Integration Example", version="1.0.0")


@app.get("/")
async def root():
    return {
        "message": "SQLAlchemy Demo",
        "database": DATABASE_URL,
        "docs": "/docs",
    }


# ── Authors ──────────────────────────────────────────────────────────────────


@app.get("/authors", response_model=List[AuthorResponse])
def list_authors(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """List all authors with pagination."""
    return db.query(AuthorModel).offset(skip).limit(limit).all()


@app.get("/authors/{author_id}", response_model=AuthorWithBooks)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """Get a single author together with all their books."""
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors", response_model=AuthorResponse, status_code=201)
def create_author(author_in: AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author."""
    existing = db.query(AuthorModel).filter(AuthorModel.email == author_in.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    author = AuthorModel(**author_in.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@app.delete("/authors/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete an author and all their books (cascade)."""
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()


# ── Books ─────────────────────────────────────────────────────────────────────


@app.get("/books", response_model=List[BookResponse])
def list_books(
    in_stock: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """List books, optionally filtered by availability."""
    q = db.query(BookModel)
    if in_stock is not None:
        q = q.filter(BookModel.in_stock == in_stock)
    return q.offset(skip).limit(limit).all()


@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)):
    """Create a book for an existing author."""
    author = db.query(AuthorModel).filter(AuthorModel.id == book_in.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    existing = db.query(BookModel).filter(BookModel.isbn == book_in.isbn).first()
    if existing:
        raise HTTPException(status_code=409, detail="ISBN already exists")
    book = BookModel(**book_in.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.patch("/books/{book_id}/stock")
def toggle_stock(book_id: int, in_stock: bool, db: Session = Depends(get_db)):
    """Update a book's stock status."""
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.in_stock = in_stock
    db.commit()
    return {"id": book_id, "in_stock": in_stock}


@app.get("/stats")
def db_stats(db: Session = Depends(get_db)):
    """Return counts from the database."""
    authors = db.query(AuthorModel).count()
    books = db.query(BookModel).count()
    in_stock = db.query(BookModel).filter(BookModel.in_stock == True).count()
    return {"authors": authors, "books": books, "books_in_stock": in_stock}


# =============================================================================
# MAIN
# =============================================================================


def demo():
    print("=" * 65)
    print("SQLALCHEMY INTEGRATION — DEMO")
    print("=" * 65)
    print()
    print("Database:", DATABASE_URL)
    print()
    print("ORM Models:")
    print("  AuthorModel (id, name, email, bio, created_at)")
    print("    └─ BookModel (id, title, isbn, price, in_stock, author_id)")
    print()
    print("Key patterns:")
    print("  • yield-based get_db() dependency — session per request")
    print("  • db.query().filter().first() — read by PK or field")
    print("  • db.add() + db.commit() + db.refresh() — create")
    print("  • cascade='all, delete-orphan' — delete children on parent delete")
    print()
    print("Endpoints:")
    print("  GET  /authors               — list authors")
    print("  GET  /authors/{id}          — author + books")
    print("  POST /authors               — create author")
    print("  DELETE /authors/{id}        — delete author (+ books)")
    print("  GET  /books                 — list books (filter by in_stock)")
    print("  POST /books                 — create book")
    print("  PATCH /books/{id}/stock     — toggle stock status")
    print("  GET  /stats                 — DB row counts")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("=" * 65)


if __name__ == "__main__":
    demo()
