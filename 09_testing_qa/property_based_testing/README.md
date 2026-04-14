# Property-Based Testing

Estimated time: 2-3 hours

## Definition

Move from example checks to invariant thinking so tests describe what must always be true.

## What You Practice

- Invariants
- Input shrinking
- Oracles
- Metamorphic properties

## Practical Applications

- Collection helpers
- sorting transforms
- serialization round-trips

## Example Focus

The runnable example in `examples/example_basic.py` shows one concrete way to apply property-based testing in a small, self-contained scenario.

## Why It Matters

This topic helps you decide what kind of feedback you need from a test and how to keep that feedback trustworthy as the codebase grows.

## Practice Task

Goal: Implement list utilities whose properties are more valuable than a handful of examples.

Success criteria:
- Implement `rotate_list`.
- Implement `deduplicate_preserve_order`.
- Keep length and element invariants intact.

## References

See `references/links.md` for official documentation, guides, and deeper reading.

## Reflection Prompt

After finishing the exercise, write down which parts of the workflow gave you the strongest confidence and which parts still feel too implicit.

