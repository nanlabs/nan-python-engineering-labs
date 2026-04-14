# Test Organization

Estimated time: 2 hours

## Definition

Organize tests by behavior and seams so the suite stays navigable as the codebase grows.

## What You Practice

- Test folders
- Naming
- Conftest reuse
- Suite readability

## Practical Applications

- Service layers
- modular monoliths
- repository + API combinations

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply test organization in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Create a service with enough behavior to justify coherent test grouping.

Success criteria:
- Implement `create_user`.
- Implement `deactivate_user`.
- Implement `active_emails`.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

