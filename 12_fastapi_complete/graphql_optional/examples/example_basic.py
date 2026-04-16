"""
Basic example: GraphQL with Strawberry (Optional)
====================================================

Strawberry is a Python-first GraphQL library with type hints.
It integrates natively with FastAPI, serving GraphQL alongside REST.

This standalone script demonstrates the core concepts without
needing a running server.

Demonstrates:
1. Type definitions with @strawberry.type
2. Queries with arguments and nested types
3. Mutations for write operations
4. Async resolvers
5. Integration with FastAPI via GraphQLRouter

Dependencies:
    pip install strawberry-graphql[fastapi]

Run:
    python example_basic.py         ← schema demo
    uvicorn example_basic:app --reload  ← full server
    Visit http://localhost:8000/graphql  (GraphiQL playground)
"""

import strawberry
from typing import List, Optional
from datetime import datetime


# =============================================================================
# 1. STRAWBERRY TYPES
# =============================================================================


@strawberry.type
class Author:
    """Represents a book author."""

    id: int
    name: str
    email: str
    bio: Optional[str] = None


@strawberry.type
class Book:
    """Represents a book in the catalog."""

    id: int
    title: str
    isbn: str
    price: float
    in_stock: bool
    author: Author
    published_at: datetime


@strawberry.input
class CreateBookInput:
    """Input type for creating a new book."""

    title: str
    isbn: str
    price: float
    author_id: int
    in_stock: bool = True


@strawberry.input
class UpdateBookInput:
    """Input type for updating a book — all fields optional."""

    title: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None


@strawberry.type
class DeleteResult:
    """Returned after a delete mutation."""

    id: int
    success: bool


# =============================================================================
# 2. IN-MEMORY STORE
# =============================================================================

_authors: dict[int, Author] = {
    1: Author(id=1, name="Alice Smith", email="alice@example.com", bio="FastAPI expert"),
    2: Author(id=2, name="Bob Jones", email="bob@example.com"),
}

_books: dict[int, Book] = {
    1: Book(
        id=1, title="FastAPI Mastery", isbn="978-0000000001",
        price=29.99, in_stock=True, author=_authors[1],
        published_at=datetime(2023, 6, 15),
    ),
    2: Book(
        id=2, title="Python Async Deep Dive", isbn="978-0000000002",
        price=39.99, in_stock=True, author=_authors[1],
        published_at=datetime(2024, 1, 10),
    ),
    3: Book(
        id=3, title="Clean Architecture", isbn="978-0000000003",
        price=19.99, in_stock=False, author=_authors[2],
        published_at=datetime(2022, 11, 1),
    ),
}
_next_book_id = 4


# =============================================================================
# 3. QUERY TYPE
# =============================================================================


@strawberry.type
class Query:
    """Root query type — all read operations."""

    @strawberry.field
    def books(
        self,
        in_stock: Optional[bool] = None,
        author_id: Optional[int] = None,
    ) -> List[Book]:
        """
        List books with optional filters.

        GraphQL query:
            query {
              books(inStock: true) {
                id title price
                author { name }
              }
            }
        """
        results = list(_books.values())
        if in_stock is not None:
            results = [b for b in results if b.in_stock == in_stock]
        if author_id is not None:
            results = [b for b in results if b.author.id == author_id]
        return results

    @strawberry.field
    def book(self, id: int) -> Optional[Book]:
        """
        Get a single book by ID.

        GraphQL query:
            query {
              book(id: 1) {
                title price author { name email }
              }
            }
        """
        return _books.get(id)

    @strawberry.field
    def authors(self) -> List[Author]:
        """List all authors."""
        return list(_authors.values())

    @strawberry.field
    def author(self, id: int) -> Optional[Author]:
        """Get a single author by ID."""
        return _authors.get(id)

    @strawberry.field
    def catalog_stats(self) -> "CatalogStats":
        """Aggregate stats — demonstrates computed resolver."""
        return CatalogStats(
            total_books=len(_books),
            in_stock_books=sum(1 for b in _books.values() if b.in_stock),
            total_authors=len(_authors),
            avg_price=round(sum(b.price for b in _books.values()) / len(_books), 2),
        )


@strawberry.type
class CatalogStats:
    total_books: int
    in_stock_books: int
    total_authors: int
    avg_price: float


# =============================================================================
# 4. MUTATION TYPE
# =============================================================================


@strawberry.type
class Mutation:
    """Root mutation type — all write operations."""

    @strawberry.mutation
    def create_book(self, input: CreateBookInput) -> Book:
        """
        Create a new book.

        GraphQL mutation:
            mutation {
              createBook(input: {
                title: "New Book"
                isbn: "978-0000000004"
                price: 24.99
                authorId: 1
              }) {
                id title author { name }
              }
            }
        """
        global _next_book_id

        author = _authors.get(input.author_id)
        if not author:
            raise ValueError(f"Author {input.author_id} not found")

        book = Book(
            id=_next_book_id,
            title=input.title,
            isbn=input.isbn,
            price=input.price,
            in_stock=input.in_stock,
            author=author,
            published_at=datetime.now(),
        )
        _books[_next_book_id] = book
        _next_book_id += 1
        return book

    @strawberry.mutation
    def update_book(self, id: int, input: UpdateBookInput) -> Optional[Book]:
        """
        Partially update a book.

        GraphQL mutation:
            mutation {
              updateBook(id: 1, input: { price: 34.99 }) {
                id title price
              }
            }
        """
        book = _books.get(id)
        if not book:
            return None

        updates = {}
        if input.title is not None:
            updates["title"] = input.title
        if input.price is not None:
            updates["price"] = input.price
        if input.in_stock is not None:
            updates["in_stock"] = input.in_stock

        for field, value in updates.items():
            object.__setattr__(book, field, value)
        return book

    @strawberry.mutation
    def delete_book(self, id: int) -> DeleteResult:
        """
        Delete a book by ID.

        GraphQL mutation:
            mutation {
              deleteBook(id: 3) {
                id success
              }
            }
        """
        if id not in _books:
            return DeleteResult(id=id, success=False)
        del _books[id]
        return DeleteResult(id=id, success=True)


# =============================================================================
# 5. SCHEMA
# =============================================================================

schema = strawberry.Schema(query=Query, mutation=Mutation)


# =============================================================================
# 6. FASTAPI INTEGRATION
# =============================================================================


def create_app():
    """Create a FastAPI app with GraphQL mounted at /graphql."""
    from fastapi import FastAPI
    from strawberry.fastapi import GraphQLRouter

    graphql_app = GraphQLRouter(schema, graphiql=True)

    app = FastAPI(title="GraphQL with Strawberry", version="1.0.0")
    app.include_router(graphql_app, prefix="/graphql")

    @app.get("/")
    async def root():
        return {
            "message": "GraphQL Demo",
            "playground": "/graphql",
            "rest_docs": "/docs",
        }

    return app


try:
    from fastapi import FastAPI
    app = create_app()
except (ImportError, TypeError):
    # Fallback for environments where strawberry FastAPI integration is unavailable
    try:
        from fastapi import FastAPI as _FastAPI

        _app = _FastAPI(title="GraphQL Demo (no router)")

        @_app.get("/")
        async def _root():
            return {"message": "GraphQL Demo", "playground": "/graphql (not mounted)"}

        app = _app
    except ImportError:
        app = None


# =============================================================================
# 7. STANDALONE DEMO
# =============================================================================


def demo():
    print("=" * 65)
    print("GRAPHQL WITH STRAWBERRY — DEMO")
    print("=" * 65)
    print()
    print("Schema introspection:")
    introspection = schema.execute_sync("{ __schema { types { name } } }")
    type_names = [t["name"] for t in introspection.data["__schema"]["types"]
                  if not t["name"].startswith("__")]
    print("  Types:", ", ".join(type_names))
    print()

    # Execute a query
    print("Query: books(inStock: true) { id title price }")
    result = schema.execute_sync("""
        {
          books(inStock: true) {
            id
            title
            price
          }
        }
    """)
    if result.data:
        for book in result.data["books"]:
            print(f"  {book}")
    print()

    # Execute a mutation
    print("Mutation: createBook(...)")
    result = schema.execute_sync("""
        mutation {
          createBook(input: {
            title: "New Demo Book"
            isbn: "978-0000000099"
            price: 15.99
            authorId: 1
          }) {
            id title price
          }
        }
    """)
    if result.data:
        print(f"  Created: {result.data['createBook']}")
    print()

    # Stats
    result = schema.execute_sync("{ catalogStats { totalBooks inStockBooks avgPrice } }")
    if result.data:
        print("Stats:", result.data["catalogStats"])
    print()

    print("GraphQL vs REST:")
    print("  REST    → GET /books, GET /books/1, GET /authors/1")
    print("  GraphQL → single endpoint, client specifies exact fields")
    print("  Benefit → no over-fetching, no under-fetching")
    print()
    print("Start: uvicorn example_basic:app --reload")
    print("  Visit: http://localhost:8000/graphql  (GraphiQL IDE)")
    print("=" * 65)


if __name__ == "__main__":
    demo()
