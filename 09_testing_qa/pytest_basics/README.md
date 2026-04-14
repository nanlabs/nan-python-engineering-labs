# Pytest Basics

Estimated time: 2-3 hours

## Definition

Learn the core pytest workflow: test discovery, expressive assertions, and clear failure messages.

## What You Practice

- Test discovery
- Assert introspection
- Arrange-act-assert
- Exception testing

## Practical Applications

- Refactoring utility functions
- Writing fast feedback loops for data transformations
- Replacing ad-hoc manual checks with executable tests

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply pytest basics in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement a tiny calculator module with predictable behavior and robust error handling.

Success criteria:
- Implement `add`, `subtract`, and `divide`.
- Raise `ValueError` when division by zero is requested.
- Add `classify_number` returning `positive`, `negative`, or `zero`.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

