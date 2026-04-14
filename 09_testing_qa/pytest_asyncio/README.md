# pytest-asyncio

Estimated time: 2-3 hours

## Definition

Test coroutine-based code with event loop support and predictable async boundaries.

## What You Practice

- Async tests
- Awaitable collaborators
- Event loop control
- Async fixtures

## Practical Applications

- API clients
- caching layers
- message consumers

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply pytest-asyncio in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement an asynchronous cache that shares in-flight work.

Success criteria:
- Implement `AsyncCache.get_or_set`.
- Store results by key.
- Avoid calling the loader twice for cached values.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

