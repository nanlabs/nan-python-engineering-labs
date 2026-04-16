# GraphQL with Strawberry (Optional)

Estimated time: 2.5 hours

## 1. Definition

**GraphQL** is an API query language where clients specify exactly which fields they need. **Strawberry** is a Python-first GraphQL library using type hints. FastAPI integrates with Strawberry via `GraphQLRouter`, serving GraphQL alongside REST at `/graphql`.

### Key Characteristics

- **`@strawberry.type`**: decorates a Python class as a GraphQL type.
- **`@strawberry.input`**: input type for mutations (equivalent to a request body model).
- **Queries vs Mutations**: queries read data; mutations write data.
- **Schema**: `strawberry.Schema(query=Query, mutation=Mutation)` ties the types together.
- **GraphiQL**: browser-based IDE served at `/graphql` for interactive queries.

## 2. Practical Application

### Use Cases

- Frontend teams that need flexible field selection without coordinating with the backend.
- Mobile apps that need different data shapes for different views (list view vs detail view).
- APIs consumed by multiple clients (web, iOS, Android) with different data needs.
- Federated APIs aggregating data from multiple microservices.

### Code Example

```python
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Book:
    id: int
    title: str
    price: float

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> list[Book]:
        return [Book(id=1, title="FastAPI Guide", price=29.99)]

schema = strawberry.Schema(query=Query)
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
```

## 3. Why Is It Important?

### Problem It Solves

REST APIs suffer from over-fetching (returning more fields than needed) and under-fetching (requiring multiple requests to get related data). Each new client data need requires a new REST endpoint or a modified existing one.

### Solution and Benefits

GraphQL eliminates over-fetching: the client requests only the fields it needs. A single query can traverse relationships (author → books → reviews) in one round trip. No new endpoints needed for new client data shapes.

## 4. References

- [Strawberry Documentation](https://strawberry.rocks/)
- [FastAPI + Strawberry](https://strawberry.rocks/docs/integrations/fastapi)
- [GraphQL Specification](https://spec.graphql.org/)
- See `references/links.md` for additional resources.

## 5. Practice Task

### Basic Level

Define a `Book` type and a `Query` with a `books` field. Mount it at `/graphql`. Run a query in GraphiQL requesting only `id` and `title`.

### Intermediate Level

Add a `createBook` mutation with a `CreateBookInput` input type. Verify the mutation stores the book and it appears in subsequent `books` queries.

### Advanced Level

Add an `Author` type with a `books: list[Book]` field. Implement an async resolver that simulates a DB lookup. Add filtering to `books(inStock: true)`.

### Success Criteria

- GraphiQL is accessible at `http://localhost:8000/graphql`.
- `{ books { title } }` returns only `title` (not price or id).
- `mutation { createBook(...) { id title } }` creates and returns the new book.

## 6. Summary

Strawberry + FastAPI provides GraphQL alongside REST. `@strawberry.type` defines GraphQL types from Python classes. Queries read data; mutations modify it. The schema is the contract between server and client. GraphiQL provides an interactive development environment.

## 7. Reflection Prompt

GraphQL and REST are not mutually exclusive — many teams run both. When would you choose to add a GraphQL endpoint alongside an existing REST API, and what concerns would you have about exposing GraphQL publicly (performance, security, complexity)?
