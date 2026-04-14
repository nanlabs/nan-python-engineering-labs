# Fixtures

Estimated time: 2-3 hours

## Definition

Use fixtures to share setup logic, keep tests readable, and model dependencies explicitly.

## What You Practice

- Fixture scope
- Yield fixtures
- Dependency injection
- Test isolation

## Practical Applications

- Database seed data
- Reusable service objects
- Temporary file preparation

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply fixtures in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Build a tiny inventory service that becomes easier to test once reusable setup exists.

Success criteria:
- Implement `InventoryItem` and `InventoryService`.
- Support adding stock, reserving stock, and listing low-stock items.
- Raise `LookupError` when a SKU does not exist.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

