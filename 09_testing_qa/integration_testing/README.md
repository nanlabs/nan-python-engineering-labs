# Integration Testing

Estimated time: 2-3 hours

## Definition

Verify components working together across boundaries such as storage, serialization, and process edges.

## What You Practice

- Real dependencies
- Test seams
- Temporary databases
- End-to-end slices

## Practical Applications

- SQLite repositories
- HTTP clients against local servers
- file-based workflows

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply integration testing in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement a tiny repository that persists users in SQLite.

Success criteria:
- Implement `create_schema(connection)`.
- Implement `insert_user(connection, email)`.
- Implement `list_users(connection)`.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

