"""
Exercise: FastAPI Intro

Objective: Build a basic FastAPI application with CRUD endpoints.

Instructions:
1. Read the requirements carefully.
2. Implement the functions/classes marked with TODO.
3. Run the tests: pytest tests/
4. Put your solution in my_solution/.

DO NOT MODIFY THIS FILE. Copy it to my_solution/ and work there.
"""

# TODO: Implement your solution here.
# Create a FastAPI app with at least:
#   - GET  /              → welcome message
#   - GET  /items         → list all items (query params: skip, limit)
#   - GET  /items/{id}    → get item by ID (404 if not found)
#   - POST /items         → create item (return 201)
#   - DELETE /items/{id}  → delete item (204 on success, 404 if not found)
#
# Use a Pydantic model for Item with: name (str), price (float > 0), in_stock (bool).


def main():
    """Run a local check of your implementation."""
    # Add your manual test calls here
    pass


if __name__ == "__main__":
    main()
